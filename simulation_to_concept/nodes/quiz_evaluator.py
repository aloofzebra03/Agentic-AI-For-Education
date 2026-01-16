"""
Quiz Evaluator Nodes
====================
Handles quiz mode workflow: initialization, question presentation, evaluation, and routing.

Quiz Flow:
1. quiz_initializer_node - Load questions, activate quiz mode
2. quiz_teacher_node - Present current question challenge
3. [INTERRUPT] - Student adjusts simulation and clicks SUBMIT
4. quiz_evaluator_node - Evaluate parameters, generate LLM feedback
5. quiz_router - Decide next action (retry/next question/complete)

IMPORTANT: All nodes return a dictionary of STATE UPDATES, not the full state.
"""

import json
import os
from typing import Dict, Any
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from simulation_to_concept.config import GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE
from simulation_to_concept.state import TeachingState
from simulation_to_concept.simulations_config import get_quiz_questions
from simulation_to_concept.quiz_rules import (
    evaluate_quiz_submission,
    get_hint_for_attempt,
    should_allow_retry,
    calculate_quiz_progress
)


def get_llm():
    """Get configured LLM instance."""
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=TEMPERATURE
    )


def is_gemma_model() -> bool:
    """Check if using a Gemma model (doesn't support system messages)."""
    return "gemma" in GEMINI_MODEL.lower()


# ============================================================================
# NODE 1: Quiz Initializer
# ============================================================================

def quiz_initializer_node(state: TeachingState) -> Dict[str, Any]:
    """
    Initialize quiz mode after all concepts are taught.
    
    Loads quiz questions for current simulation and activates quiz mode.
    Returns a dictionary of state updates.
    """
    print("\n" + "="*60)
    print("🎯 QUIZ INITIALIZER - Starting Quiz Mode")
    print("="*60)
    
    # Get simulation ID from environment
    simulation_id = os.environ.get("SIMULATION_ID", "simple_pendulum")
    
    # Load quiz questions for this simulation
    quiz_questions = get_quiz_questions(simulation_id)
    
    if not quiz_questions:
        print(f"⚠️  No quiz questions found for simulation: {simulation_id}")
        return {
            "quiz_complete": True,
            "quiz_mode": True,
            "quiz_questions": [],
            "session_complete": True
        }
    
    print(f"📚 Loaded {len(quiz_questions)} quiz questions")
    
    # Build transition message
    transition_message = (
        "🎓 Great work! You've completed all the teaching concepts. "
        "Now let's test your understanding with some interactive challenges!\n\n"
        "I'll give you a challenge, and you'll need to adjust the simulation parameters "
        "to achieve the goal. Take your time and click SUBMIT when you're ready!"
    )
    
    # Get existing conversation history and add new message
    existing_history = state.get("conversation_history", [])
    new_history = existing_history + [{
        "role": "teacher",
        "content": transition_message,
        "timestamp": datetime.now().isoformat()
    }]
    
    print(f"✅ Quiz mode activated - {len(quiz_questions)} questions ready")
    
    # Return only the state updates
    return {
        "quiz_mode": True,
        "quiz_questions": quiz_questions,
        "current_quiz_index": 0,
        "quiz_attempts": {},
        "quiz_scores": {},
        "quiz_complete": False,
        "submitted_parameters": {},
        "quiz_evaluation": {},
        "conversation_history": new_history,
        "last_teacher_message": transition_message
    }


# ============================================================================
# NODE 2: Quiz Teacher
# ============================================================================

def quiz_teacher_node(state: TeachingState) -> Dict[str, Any]:
    """
    Present current quiz question to student.
    
    Shows the challenge and provides context if this is a retry attempt.
    Returns a dictionary of state updates.
    """
    print("\n" + "="*60)
    print("📝 QUIZ TEACHER - Presenting Question")
    print("="*60)
    
    current_index = state.get("current_quiz_index", 0)
    quiz_questions = state.get("quiz_questions", [])
    
    print(f"   DEBUG: current_quiz_index = {current_index}")
    print(f"   DEBUG: quiz_questions length = {len(quiz_questions)}")
    
    if current_index >= len(quiz_questions):
        print("✅ All questions completed!")
        return {
            "quiz_complete": True
        }
    
    current_question = quiz_questions[current_index]
    question_id = current_question["id"]
    
    # Get attempt number for this question
    quiz_attempts = state.get("quiz_attempts", {})
    attempts = quiz_attempts.get(question_id, 0)
    
    print(f"Question {current_index + 1}/{len(quiz_questions)}: {question_id}")
    print(f"Attempt: {attempts + 1}")
    
    # Build question message
    if attempts == 0:
        # First attempt - present the challenge
        message = f"**Challenge {current_index + 1}:**\n\n{current_question['challenge']}\n\n"
        message += "💡 Adjust the simulation parameters and click **SUBMIT** when you're ready!"
        
        # Update conversation history only on first attempt
        existing_history = state.get("conversation_history", [])
        new_history = existing_history + [{
            "role": "teacher",
            "content": message,
            "timestamp": datetime.now().isoformat()
        }]
        
        print(f"✅ Question presented - Waiting for student submission")
        
        return {
            "conversation_history": new_history,
            "last_teacher_message": message
        }
    else:
        # Retry attempt - don't add new message, quiz_evaluator already added feedback
        # Just update last_teacher_message for the quiz UI
        prev_eval = state.get("quiz_evaluation", {})
        message = prev_eval.get('feedback', 'Try adjusting your parameters.')
        
        print(f"✅ Retry attempt - Using previous feedback")
        
        return {
            "last_teacher_message": message
        }


# ============================================================================
# NODE 3: Quiz Evaluator
# ============================================================================

def quiz_evaluator_node(state: TeachingState) -> Dict[str, Any]:
    """
    Evaluate student's submitted parameters and generate feedback.
    
    Uses quiz_rules.py for scoring, then LLM for adaptive feedback.
    Returns a dictionary of state updates.
    """
    print("\n" + "="*60)
    print("🔍 QUIZ EVALUATOR - Evaluating Submission")
    print("="*60)
    
    from simulations_config import get_simulation
    import os
    
    current_index = state.get("current_quiz_index", 0)
    quiz_questions = state.get("quiz_questions", [])
    current_question = quiz_questions[current_index]
    question_id = current_question["id"]
    submitted_params = state.get("submitted_parameters", {})
    
    # Get parameter ranges from simulation config
    simulation_id = os.getenv('SIMULATION_ID', 'simple_pendulum')
    sim_config = get_simulation(simulation_id)
    parameter_info = sim_config.get('parameter_info', {}) if sim_config else {}
    parameter_ranges = {k: v['range'] for k, v in parameter_info.items() if 'range' in v}
    
    # Get and increment attempt count
    quiz_attempts = state.get("quiz_attempts", {}).copy()
    attempts = quiz_attempts.get(question_id, 0) + 1
    quiz_attempts[question_id] = attempts
    
    print(f"Question: {question_id}")
    print(f"Attempt: {attempts}")
    print(f"Submitted: {submitted_params}")
    print(f"Parameter ranges: {parameter_ranges}")
    
    # ========================================
    # STEP 1: Rule-based evaluation (fast)
    # ========================================
    score, status = evaluate_quiz_submission(
        submitted_params,
        current_question["success_rule"],
        parameter_ranges=parameter_ranges
    )
    
    print(f"Score: {score} | Status: {status}")
    
    # ========================================
    # STEP 2: Get hint for this attempt
    # ========================================
    hint = get_hint_for_attempt(current_question["hints"], attempts)
    
    # ========================================
    # STEP 3: Check if retry allowed
    # ========================================
    allow_retry = should_allow_retry(attempts)
    
    # ========================================
    # STEP 4: Generate LLM feedback (adaptive)
    # ========================================
    llm = get_llm()
    
    # Build context for LLM
    system_prompt = f"""You are a supportive science teacher providing feedback on a simulation-based challenge.

**Challenge:** {current_question['challenge']}

**Student's Attempt:**
They configured the simulation with these parameters:
{json.dumps(submitted_params, indent=2)}

**Evaluation:**
- Result: {status}
- Score: {score}/1.0
- Attempt: {attempts} of 3

**Learning Context:**
{current_question['concept_reminder']}

**Feedback Guidelines:**

• **If CORRECT (score=1.0):**
  - Celebrate their success enthusiastically
  - Explain WHY their configuration achieved the goal
  - Connect their choices to the underlying concept
  - Keep it concise and positive (2-3 sentences)

• **If PARTIALLY CORRECT (score between 0.3-0.9):**
  - Acknowledge what they did well
  - Identify what still needs adjustment (be specific but don't give exact values)
  - Include this hint: "{hint}"
  - Encourage experimentation

• **If INCORRECT (score < 0.3):**
  - Stay encouraging - mistakes are learning opportunities
  - Briefly explain the concept they may have overlooked
  - Provide this guidance: "{hint}"
  - Suggest a different approach without giving exact answers

**Important Rules:**
- Never reveal specific numerical values or exact parameter settings
- Use directional guidance ("increase", "decrease", "much higher", "significantly lower")
- Focus on understanding WHY, not just WHAT to change
- Keep feedback to 2-4 sentences maximum
- No markdown formatting - plain text only
- Be warm, supportive, and Socratic in tone

Generate your feedback now:"""

    user_prompt = f"Status: {status}, Attempt: {attempts}, Hint: {hint}"
    
    try:
        if is_gemma_model():
            combined = f"{system_prompt}\n\n{user_prompt}"
            messages = [HumanMessage(content=combined)]
        else:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
        
        response = llm.invoke(messages)
        feedback = response.content.strip()
        
    except Exception as e:
        print(f"❌ LLM feedback generation failed: {e}")
        # Fallback feedback
        if status == "RIGHT":
            feedback = "Excellent work! Your parameters achieve the goal perfectly."
        elif status == "PARTIALLY_RIGHT":
            feedback = f"Good progress! {hint} Try adjusting your parameters."
        else:
            feedback = f"Not quite right. {hint} Give it another try!"
    
    print(f"✅ Feedback generated ({len(feedback)} chars)")
    
    # ========================================
    # STEP 5: Build state updates
    # ========================================
    
    # Copy existing scores
    quiz_scores = state.get("quiz_scores", {}).copy()
    
    # If correct or max attempts reached, save the score and move to next
    new_index = current_index
    quiz_complete = False
    session_complete = False
    
    if status == "RIGHT" or not allow_retry:
        quiz_scores[question_id] = score
        print(f"💾 Score saved: {question_id} = {score}")
        
        if status == "RIGHT":
            print(f"✅ Question completed successfully!")
        else:
            print(f"⏭️  Max attempts reached, moving to next question")
        
        new_index = current_index + 1
        
        # Check if quiz is complete
        if new_index >= len(quiz_questions):
            quiz_complete = True
            session_complete = True
            
            # Calculate final statistics
            progress = calculate_quiz_progress(quiz_scores, len(quiz_questions))
            
            # Add completion message to feedback
            completion_message = (
                f"\n🎊 **Quiz Complete!** 🎊\n\n"
                f"**Your Results:**\n"
                f"- Questions: {progress['questions_completed']}/{progress['total_questions']}\n"
                f"- Average Score: {progress['average_score']}\n"
                f"- Perfect: {progress['perfect_count']} | "
                f"Partial: {progress['partial_count']} | "
                f"Wrong: {progress['wrong_count']}\n\n"
                f"Great work on completing the quiz! 🌟"
            )
            feedback = feedback + "\n\n" + completion_message
            
            print(f"🎊 QUIZ COMPLETE - Final Stats:")
            print(f"   Average: {progress['average_score']}")
            print(f"   Perfect: {progress['perfect_count']}/{progress['total_questions']}")
            print(f"   ✅ SESSION COMPLETE")
    
    # Store evaluation result
    evaluation = {
        "question_id": question_id,
        "score": score,
        "status": status,
        "feedback": feedback,
        "attempt": attempts,
        "allow_retry": allow_retry and status != "RIGHT",
        "submitted_parameters": submitted_params.copy()
    }
    
    # Update conversation history
    existing_history = state.get("conversation_history", [])
    new_history = existing_history + [{
        "role": "teacher",
        "content": feedback,
        "timestamp": datetime.now().isoformat()
    }]
    
    # Return state updates
    updates = {
        "quiz_attempts": quiz_attempts,
        "quiz_scores": quiz_scores,
        "quiz_evaluation": evaluation,
        "current_quiz_index": new_index,
        "quiz_complete": quiz_complete,
        "conversation_history": new_history,
        "last_teacher_message": feedback
    }
    
    if session_complete:
        updates["session_complete"] = True
    
    return updates


# ============================================================================
# ROUTING FUNCTION
# ============================================================================

def quiz_router(state: TeachingState) -> str:
    """
    Route after quiz evaluation based on result.
    
    Returns:
        - "quiz_teacher" if retry needed or next question available
        - "END" if quiz is complete
    """
    print("\n" + "="*60)
    print("🔀 QUIZ ROUTER - Determining Next Step")
    print("="*60)
    
    # Check if quiz is complete
    if state.get("quiz_complete", False):
        print("✅ Quiz complete - Ending session")
        return "END"
    
    evaluation = state.get("quiz_evaluation", {})
    
    # If retry allowed (wrong/partial answer, attempts < 3)
    if evaluation.get("allow_retry", False) and evaluation.get("status") != "RIGHT":
        print("🔄 Retry allowed - Returning to quiz_teacher")
        return "quiz_teacher"
    
    # Otherwise, present next question
    print("⏭️  Moving to next question - Returning to quiz_teacher")
    return "quiz_teacher"
