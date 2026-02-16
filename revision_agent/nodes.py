# nodes.py
"""
Revision Agent Nodes - All node implementations in a single file.

Contains 6 nodes total:
- 4 new revision-specific nodes (revision_start, question_presenter, answer_evaluator, revision_end)
- 2 adapted nodes from learning agent (ge_node, ar_node) with autosuggestions stripped
"""

import json
from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Import shared utilities
from utils.shared_utils import (
    extract_json_block,
    llm_with_history,
    build_prompt_from_template_optimized,
    add_ai_message_to_conversation,
    translate_if_kannada,
)

# Import revision-specific utilities
from revision_agent.question_bank import load_question_bank


# ─── Pydantic Response Models ────────────────────────────────────────────────

class ConceptExtractionResponse(BaseModel):
    """Response for extracting concept from a question"""
    concept: str

class AnswerEvaluationResponse(BaseModel):
    """Response for evaluating student's answer"""
    is_correct: bool
    feedback: str

class GeResponse(BaseModel):
    """Response for GE node (adapted from learning agent, autosuggestions removed)"""
    feedback: str
    next_state: Literal["AR", "GE"]

class ArResponse(BaseModel):
    """Response for AR node (adapted from learning agent, autosuggestions removed)"""
    score: float
    feedback: str
    next_state: Literal["QUESTION_PRESENTER", "GE"]  # Modified routing


# ─── Parsers ─────────────────────────────────────────────────────────────────

concept_extraction_parser = PydanticOutputParser(pydantic_object=ConceptExtractionResponse)
evaluation_parser = PydanticOutputParser(pydantic_object=AnswerEvaluationResponse)
ge_parser = PydanticOutputParser(pydantic_object=GeResponse)
ar_parser = PydanticOutputParser(pydantic_object=ArResponse)


# ══════════════════════════════════════════════════════════════════════════════
# NEW REVISION-SPECIFIC NODES
# ══════════════════════════════════════════════════════════════════════════════

def revision_start_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Initialize the revision session.
    
    - Loads question bank for the specified chapter
    - Sets up tracking variables
    - Greets the student and explains the revision flow
    """
    print("=" * 80)
    print("🎯 REVISION START NODE")
    print("=" * 80)
    
    # Get chapter from state (should be set by caller)
    chapter = state.get("chapter", "Nutrition in Plants")
    
    # Load question bank
    question_data = load_question_bank(chapter)
    
    # Initialize state - simple inline logic
    state["chapter"] = question_data.get("chapter", chapter)
    state["question_bank"] = question_data.get("questions", [])
    state["questions_total"] = len(state["question_bank"])
    state["current_question_index"] = 0
    state["questions_correct_first_try"] = 0
    state["questions_needed_explanation"] = 0
    state["concepts_for_review"] = []
    
    print(f"🎯 Initialized revision for: {state['chapter']}")
    print(f"📚 Total questions: {state['questions_total']}")
    
    # Create welcome message
    system_prompt = f"""You are a helpful revision tutor.
    
The student wants to revise the chapter '{chapter}'.
You have {state['questions_total']} questions ready for them.

Greet the student warmly and explain that:
1. You'll ask them questions about {chapter}
2. If they answer correctly, you'll move to the next question
3. If they struggle, you'll explain the concept and ask a followup question

Keep it brief (2-3 sentences) and encouraging.
"""
    
    # Add Kannada instruction if needed
    if state.get("is_kannada", False):
        system_prompt += "\nRemember the student understands only Kannada. Speak to the student in Kannada script only."
    
    # Build prompt
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,
        include_instructions=False,
        current_node="REVISION_START",
        include_autosuggestions=False  # No autosuggestions for revision agent
    )
    
    resp = llm_with_history(state, final_prompt)
    content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    # Translate and update state
    translated_content = translate_if_kannada(state, content)
    state["agent_output"] = translated_content
    state["current_state"] = "QUESTION_PRESENTER"
    state["messages"] = []  # Initialize empty message list
    add_ai_message_to_conversation(state, translated_content)
    
    # Initialize optimization fields
    state["summary"] = ""
    state["summary_last_index"] = -1
    
    print("=" * 80)
    
    return state


def question_presenter_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Present the next question from the question bank.
    
    - Gets next question from the bank
    - Displays progress (Question X/Y)
    - Routes to EVALUATOR for answer checking or END if all done
    """
    print("=" * 80)
    print("🎯 QUESTION PRESENTER NODE")
    print("=" * 80)
    
    # Get next question - simple inline logic
    question_bank = state.get("question_bank", [])
    current_idx = state.get("current_question_index", 0)
    
    if current_idx >= len(question_bank):
        # All questions completed - go to END
        print("✅ All questions completed! Moving to END.")
        state["current_state"] = "REVISION_END"
        state["agent_output"] = ""  # END node will generate summary
        return state
    
    # Store current question
    next_q = question_bank[current_idx]
    state["current_question"] = next_q
    
    print(f"📝 Presenting question {current_idx + 1}/{len(question_bank)}: ID={next_q.get('id')}")
    
    # Build presentation message
    current_idx = state["current_question_index"]
    total = state["questions_total"]
    question_text = next_q["question"]
    
    system_prompt = f"""You are a revision tutor presenting a question to the student.

Progress: Question {current_idx + 1} of {total}

Present this question to the student:
"{question_text}"

Keep it simple and clear. Just present the question naturally (you can add a brief encouraging phrase).
"""
    
    # Add Kannada instruction if needed
    if state.get("is_kannada", False):
        system_prompt += "\nRemember the student understands only Kannada. Present the question in Kannada script only."
    
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,  # Include previous context
        include_instructions=False,
        current_node="QUESTION_PRESENTER",
        include_autosuggestions=False
    )
    
    resp = llm_with_history(state, final_prompt)
    content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    translated_content = translate_if_kannada(state, content)
    state["agent_output"] = translated_content
    state["current_state"] = "EVALUATOR"
    add_ai_message_to_conversation(state, translated_content)
    
    print(f"📝 Presented question {current_idx + 1}/{total}: {question_text[:50]}...")
    print("=" * 80)
    
    return state


def answer_evaluator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate student's answer to the current question.
    
    - Checks if answer is correct
    - If INCORRECT: Uses LLM to extract the concept from the question, then routes to GE
    - If CORRECT: Moves to next question
    - Tracks progress
    """
    print("=" * 80)
    print("🎯 ANSWER EVALUATOR NODE")
    print("=" * 80)
    
    current_question = state.get("current_question", {})
    student_answer = state.get("last_user_msg", "")
    expected_answer = current_question.get("expected_answer", "")
    question_text = current_question.get("question", "")
    question_id = current_question.get("id", 0)
    
    print(f"📝 Question: {question_text}")
    print(f"💬 Student answer: {student_answer}")
    print(f"✅ Expected answer: {expected_answer}")
    
    # Evaluate answer using LLM
    evaluation_prompt = f"""Evaluate if the student's answer is correct.

Question: {question_text}
Expected answer: {expected_answer}
Student's answer: {student_answer}

Task: Determine if the student's answer is semantically correct (doesn't need to be word-for-word).
Respond with JSON in this format:
{{
    "is_correct": true/false,
    "feedback": "Brief feedback message (one sentence)"
}}
"""
    
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=evaluation_prompt,
        state=state,
        include_last_message=False,  # We already included student answer above
        include_instructions=True,
        parser=evaluation_parser,
        current_node="EVALUATOR",
        include_autosuggestions=False
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    
    try:
        parsed_obj: AnswerEvaluationResponse = evaluation_parser.parse(json_text)
        parsed = parsed_obj.model_dump()
        
        is_correct = parsed["is_correct"]
        feedback = parsed["feedback"]
        
        print(f"✅ Evaluation: {'CORRECT' if is_correct else 'INCORRECT'}")
        print(f"💬 Feedback: {feedback}")
        
        if is_correct:
            # Answer is correct - simple inline tracking
            state["questions_correct_first_try"] = state.get("questions_correct_first_try", 0) + 1
            state["current_question_index"] += 1
            print(f"✅ Question {question_id} correct on first try! Total: {state['questions_correct_first_try']}")
            
            translated_feedback = translate_if_kannada(state, feedback)
            state["agent_output"] = translated_feedback
            state["current_state"] = "QUESTION_PRESENTER"  # Go to next question
            add_ai_message_to_conversation(state, translated_feedback)
            
            print("🎉 Moving to next question!")
            
        else:
            # Answer is INCORRECT - extract concept and route to GE
            state["questions_needed_explanation"] = state.get("questions_needed_explanation", 0) + 1
            print(f"📝 Question {question_id} needed explanation. Total needing help: {state['questions_needed_explanation']}")
            
            # Extract concept using LLM
            concept_prompt = f"""What is the main concept being tested in this question?

Question: {question_text}

Task: Identify the core scientific concept (e.g., "photosynthesis", "chlorophyll", "stomata").
Respond with JSON in this format:
{{
    "concept": "concept name"
}}
"""
            
            concept_final_prompt = build_prompt_from_template_optimized(
                system_prompt=concept_prompt,
                state=state,
                include_last_message=False,
                include_instructions=True,
                parser=concept_extraction_parser,
                current_node="EVALUATOR",
                include_autosuggestions=False
            )
            
            concept_raw = llm_with_history(state, concept_final_prompt).content
            concept_json = extract_json_block(concept_raw)
            concept_parsed: ConceptExtractionResponse = concept_extraction_parser.parse(concept_json)
            
            extracted_concept = concept_parsed.concept
            state["current_concept"] = extracted_concept
            
            print(f"🔍 Extracted concept: {extracted_concept}")
            
            # Provide feedback and route to GE
            translated_feedback = translate_if_kannada(state, feedback)
            state["agent_output"] = translated_feedback
            state["current_state"] = "GE"  # Go to explanation
            state["asked_ge"] = False  # Reset GE flag
            state["asked_ar"] = False  # Reset AR flag
            add_ai_message_to_conversation(state, translated_feedback)
            
            print("📖 Routing to GE for explanation")
            
    except Exception as e:
        print(f"❌ Error evaluating answer: {e}")
        print(f"Raw response: {raw}")
        print(f"Extracted JSON: {json_text}")
        raise
    
    print("=" * 80)
    return state


def revision_end_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    End the revision session with a summary.
    
    - Shows total questions answered
    - Shows correct on first try vs needed help
    - Lists concepts that need review
    - Provides encouraging message
    """
    print("=" * 80)
    print("🎯 REVISION END NODE")
    print("=" * 80)
    
    # Generate progress summary - simple inline logic
    total = state.get("questions_total", 0)
    correct = state.get("questions_correct_first_try", 0)
    needed_help = state.get("questions_needed_explanation", 0)
    weak_concepts = state.get("concepts_for_review", [])
    
    summary = f"📊 **Revision Summary**\n\n"
    summary += f"Total Questions: {total}\n"
    summary += f"Correct on First Try: {correct}/{total}\n"
    summary += f"Needed Explanation: {needed_help}/{total}\n\n"
    
    if weak_concepts:
        summary += f"**Concepts to Review:**\n"
        for i, concept in enumerate(weak_concepts, 1):
            summary += f"{i}. {concept}\n"
    else:
        summary += f"🎉 **Great job!** You got all concepts correct!\n"
    
    print(summary)
    
    # Generate encouraging closing message
    correct_count = state.get("questions_correct_first_try", 0)
    total_count = state.get("questions_total", 0)
    
    system_prompt = f"""You are a revision tutor wrapping up the session.

Here's the student's performance:
{summary}

Task: Provide an encouraging closing message (2-3 sentences) that:
1. Acknowledges their effort
2. Highlights what they did well
3. Gently encourages them to review weak areas if any

Be warm and supportive.
"""
    
    # Add Kannada instruction if needed
    if state.get("is_kannada", False):
        system_prompt += "\nRemember the student understands only Kannada. Speak in Kannada script only."
    
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,
        include_instructions=False,
        current_node="REVISION_END",
        include_autosuggestions=False
    )
    
    resp = llm_with_history(state, final_prompt)
    closing_message = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
    
    # Combine summary and closing message
    final_output = f"{summary}\n\n{closing_message}"
    
    translated_output = translate_if_kannada(state, final_output)
    state["agent_output"] = translated_output
    state["current_state"] = "END"
    add_ai_message_to_conversation(state, translated_output)
    
    print("🎉 Revision session completed!")
    print("=" * 80)
    
    return state


# ══════════════════════════════════════════════════════════════════════════════
# ADAPTED NODES FROM LEARNING AGENT (GE & AR)
# ══════════════════════════════════════════════════════════════════════════════

def ge_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Guided Exploration node (adapted from learning agent).
    
    Explains the concept that the student struggled with.
    Modifications from learning agent:
    - Removed all autosuggestion logic
    - Uses state["current_concept"] (extracted by evaluator) instead of from CI
    - Uses state["current_question"]["question"] for context
    - Simpler routing (always → AR)
    """
    print("=" * 80)
    print("🎯 GE NODE (Guided Exploration)")
    print("=" * 80)
    
    if not state.get("asked_ge", False):
        state["asked_ge"] = True
        
        concept = state.get("current_concept", "the concept")
        question_context = state.get("current_question", {}).get("question", "")
        
        system_prompt = f"""You are explaining the concept of '{concept}' to a class 7 student who struggled with this question:

"{question_context}"

Task: Provide a clear, concise explanation of '{concept}' that:
1. Explains what it is (2-3 sentences)
2. Explains why it's important
3. Relates it back to the question they missed

Keep it simple and encouraging. Don't lecture - be conversational.
"""
        
        # Add Kannada instruction if needed
        if state.get("is_kannada", False):
            system_prompt += "\nRemember the student understands only Kannada. Explain in Kannada script only."
        
        final_prompt = build_prompt_from_template_optimized(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False,
            current_node="GE",
            include_autosuggestions=False  # KEY: No autosuggestions
        )
        
        resp = llm_with_history(state, final_prompt)
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        
        translated_content = translate_if_kannada(state, content)
        state["agent_output"] = translated_content
        add_ai_message_to_conversation(state, translated_content)
        
        print(f"📖 Explained concept: {concept}")
        print("=" * 80)
        
        return state
    
    # Student has now responded to the explanation
    # Use LLM to decide: continue explaining (GE) or test understanding (AR)
    
    concept = state.get("current_concept", "the concept")
    
    system_prompt = f"""Current node: GE (Guided Exploration)

You just explained '{concept}' to the student. They have responded.

Possible next_state values:
- "AR": Student seems to understand, move to testing their comprehension with a question
- "GE": Student is still confused, provide more clarification

Task: Evaluate their response and decide next state. Respond with JSON:
{{
    "feedback": "Your response to the student (brief, conversational)",
    "next_state": "AR" or "GE"
}}
"""
    
    # Add Kannada instruction if needed
    if state.get("is_kannada", False):
        system_prompt += "\nRemember the student understands only Kannada. Respond in Kannada script only."
    
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=system_prompt,
        state=state,
        include_last_message=True,  # Include student's response
        include_instructions=True,
        parser=ge_parser,
        current_node="GE",
        include_autosuggestions=False  # KEY: No autosuggestions
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    
    try:
        parsed_obj: GeResponse = ge_parser.parse(json_text)
        parsed = parsed_obj.model_dump()
        
        feedback = parsed["feedback"]
        next_state = parsed["next_state"]
        
        translated_feedback = translate_if_kannada(state, feedback)
        state["agent_output"] = translated_feedback
        state["current_state"] = next_state
        add_ai_message_to_conversation(state, translated_feedback)
        
        print(f"💬 Feedback: {feedback[:50]}...")
        print(f"🚀 Next state: {next_state}")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error parsing GE response: {e}")
        print(f"Raw: {raw}")
        print(f"JSON: {json_text}")
        raise
    
    return state


def ar_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adaptive Remediation node (adapted from learning agent).
    
    Asks a followup question to test understanding of the explained concept.
    Modifications from learning agent:
    - Removed all autosuggestion logic
    - Routes to QUESTION_PRESENTER (next question) instead of TC
    - If student still struggles after AR: mark concept for review and move on
    """
    print("=" * 80)
    print("🎯 AR NODE (Adaptive Remediation)")
    print("=" * 80)
    
    if not state.get("asked_ar", False):
        state["asked_ar"] = True
        
        concept = state.get("current_concept", "the concept")
        original_question = state.get("current_question", {}).get("question", "")
        
        system_prompt = f"""You just explained '{concept}' to the student.

Original question they missed: "{original_question}"

Task: Generate a SHORT followup question to test if they understood your explanation.
The question should:
1. Test the same concept but from a slightly different angle
2. Be answerable in 1-2 sentences
3. Not be the exact same question they failed before

Just ask the question naturally (no need for JSON here, just output the question).
"""
        
        # Add Kannada instruction if needed
        if state.get("is_kannada", False):
            system_prompt += "\nRemember the student understands only Kannada. Ask in Kannada script only."
        
        final_prompt = build_prompt_from_template_optimized(
            system_prompt=system_prompt,
            state=state,
            include_last_message=False,
            include_instructions=False,
            current_node="AR",
            include_autosuggestions=False  # KEY: No autosuggestions
        )
        
        resp = llm_with_history(state, final_prompt)
        content = extract_json_block(resp.content) if resp.content.strip().startswith("```") else resp.content
        
        translated_content = translate_if_kannada(state, content)
        state["agent_output"] = translated_content
        add_ai_message_to_conversation(state, translated_content)
        
        print(f"❓ Asked followup question about: {concept}")
        print("=" * 80)
        
        return state
    
    # Student answered the followup question - evaluate it
    
    concept = state.get("current_concept", "the concept")
    student_answer = state.get("last_user_msg", "")
    
    system_prompt = f"""You asked a followup question about '{concept}' to test understanding.

Student's answer: "{student_answer}"

Task: Evaluate their answer and decide next steps.
Score from 0.0 to 1.0 (0.7+ is good enough to move on).

Respond with JSON:
{{
    "score": 0.0 to 1.0,
    "feedback": "Brief feedback on their answer",
    "next_state": "QUESTION_PRESENTER" if score >= 0.7 else "GE"
}}

If score >= 0.7: They understood, move to next question
If score < 0.7: They're still struggling, explain again (GE)
"""
    
    # Add Kannada instruction if needed
    if state.get("is_kannada", False):
        system_prompt += "\nRemember the student understands only Kannada. Respond in Kannada script only."
    
    final_prompt = build_prompt_from_template_optimized(
        system_prompt=system_prompt,
        state=state,
        include_last_message=False,  # We already included answer above
        include_instructions=True,
        parser=ar_parser,
        current_node="AR",
        include_autosuggestions=False  # KEY: No autosuggestions
    )
    
    raw = llm_with_history(state, final_prompt).content
    json_text = extract_json_block(raw)
    
    try:
        parsed_obj: ArResponse = ar_parser.parse(json_text)
        parsed = parsed_obj.model_dump()
        
        score = parsed["score"]
        feedback = parsed["feedback"]
        next_state = parsed["next_state"]
        
        print(f"📊 Score: {score}")
        print(f"💬 Feedback: {feedback[:50]}...")
        print(f"🚀 Next state: {next_state}")
        
        if next_state == "QUESTION_PRESENTER":
            # Student understood - move to next question
            state["current_question_index"] += 1
            print("✅ Student understood! Moving to next question.")
        else:
            # Student still struggling - will loop back to GE
            # Add concept to review list - simple inline logic
            concepts_for_review = state.setdefault("concepts_for_review", [])
            if concept and concept not in concepts_for_review:
                concepts_for_review.append(concept)
                print(f"📌 Added '{concept}' to review list. Total: {len(concepts_for_review)}")
            
            state["asked_ge"] = False  # Reset for another explanation round
            print(f"⚠️ Student still struggling with '{concept}'. Will explain again.")
        
        translated_feedback = translate_if_kannada(state, feedback)
        state["agent_output"] = translated_feedback
        state["current_state"] = next_state
        add_ai_message_to_conversation(state, translated_feedback)
        
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error parsing AR response: {e}")
        print(f"Raw: {raw}")
        print(f"JSON: {json_text}")
        raise
    
    return state
