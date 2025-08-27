import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langfuse import Langfuse


# Pydantic model for LLM-analyzed metrics
class LLMAnalyzedMetrics(BaseModel):
    """Metrics that require LLM analysis from conversation history"""
    
    concepts_covered: List[str] = Field(description="List of educational concepts taught during the session (e.g., 'simple pendulum', 'oscillation', 'period')")
    clarity_conciseness_score: float = Field(description="Score 1-5 for how clear and concise the agent's explanations were", ge=1, le=5)
    user_type: Literal["Dull", "Medium", "High"] = Field(description="Learner classification based on comprehension speed and curiosity")
    user_interest_rating: float = Field(description="Score 1-5 based on enthusiasm, questions asked, and voluntary engagement", ge=1, le=5)
    user_engagement_rating: float = Field(description="Score 1-5 based on response quality, participation, and willingness to explore", ge=1, le=5)
    enjoyment_probability: float = Field(description="Probability 0-1 that the user enjoyed and benefited from the session", ge=0, le=1)


class SessionMetrics(BaseModel):
    """Complete session-level metrics for educational agent interactions"""
    
    # LLM-analyzed metrics
    concepts_covered: List[str] = Field(description="List of concepts taught during the session")
    num_concepts_covered: int = Field(description="Total number of concepts touched")
    clarity_conciseness_score: float = Field(description="Based on LLM evaluation (1-5)", ge=1, le=5)
    user_type: str = Field(description="Categorized as Dull, Medium, or High learner")
    user_interest_rating: float = Field(description="Score (1-5) based on engagement indicators", ge=1, le=5)
    user_engagement_rating: float = Field(description="Score (1-5) using response patterns", ge=1, le=5)
    enjoyment_probability: float = Field(description="Likelihood (0-1) that user enjoyed and benefited", ge=0, le=1)
    
    # Computed metrics
    quiz_score: float = Field(description="Score from formative assessments (0-100)", ge=0, le=100)
    error_handling_count: int = Field(description="Count of corrections/re-prompts", ge=0)
    adaptability: bool = Field(description="Whether flow was adjusted dynamically to user performance")
    average_response_time: float = Field(description="Average seconds taken per interaction", ge=0)
    
    # Session metadata
    session_id: str = Field(description="Unique session identifier")
    total_interactions: int = Field(description="Total number of user-agent exchanges", ge=0)
    session_duration: float = Field(description="Total session duration in minutes", ge=0)
    persona_name: Optional[str] = Field(description="User persona if known")


class MetricsComputer:
    """Computes session metrics from conversation history and state"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2,
        )
        self.langfuse = Langfuse()
        self.llm_parser = PydanticOutputParser(pydantic_object=LLMAnalyzedMetrics)
    
    def compute_metrics(self, 
                       session_id: str,
                       history: List[Dict[str, Any]], 
                       session_state: Dict[str, Any],
                       persona_name: Optional[str] = None) -> SessionMetrics:
        """
        Compute all session metrics from conversation history and agent state
        """
        
        # Extract basic session info
        user_interactions = [h for h in history if h.get("role") == "user"]
        agent_interactions = [h for h in history if h.get("role") == "assistant"]
        total_interactions = len(user_interactions)
        
        # Calculate session duration (estimate based on interaction count)
        session_duration = total_interactions * 2.5  # Rough estimate: 2.5 min per interaction
        
        # Get LLM-analyzed metrics in one call
        llm_metrics = self._analyze_conversation_with_llm(history, persona_name)
        
        # Compute simple metrics that don't need LLM
        quiz_score = self._extract_quiz_score(history, session_state)
        error_handling_count = self._count_error_handling(history)
        adaptability = self._check_adaptability(session_state)
        avg_response_time = self._estimate_avg_response_time(history)
        
        return SessionMetrics(
            # LLM-analyzed metrics
            concepts_covered=llm_metrics.concepts_covered,
            num_concepts_covered=len(llm_metrics.concepts_covered),
            clarity_conciseness_score=llm_metrics.clarity_conciseness_score,
            user_type=llm_metrics.user_type,
            user_interest_rating=llm_metrics.user_interest_rating,
            user_engagement_rating=llm_metrics.user_engagement_rating,
            enjoyment_probability=llm_metrics.enjoyment_probability,
            
            # Computed metrics
            quiz_score=quiz_score,
            error_handling_count=error_handling_count,
            adaptability=adaptability,
            average_response_time=avg_response_time,
            
            # Session metadata
            session_id=session_id,
            total_interactions=total_interactions,
            session_duration=session_duration,
            persona_name=persona_name
        )
    
    def _analyze_conversation_with_llm(self, history: List[Dict[str, Any]], persona_name: Optional[str] = None) -> LLMAnalyzedMetrics:
        """Use LLM to analyze conversation and extract all subjective metrics in one call"""
        
        # Format conversation for LLM analysis
        conversation_text = self._format_conversation_for_analysis(history)
        
        persona_context = f"\nThe user was acting with the persona: {persona_name}\n" if persona_name else ""
        
        prompt = f"""
You are an expert educational analyst. Analyze this educational conversation and provide structured metrics.

{persona_context}
**Conversation History:**
{conversation_text}

**Analysis Instructions:**
1. **Concepts Covered**: List the main educational concepts that were taught (e.g., "simple pendulum", "oscillation", "period", "frequency")
2. **Clarity & Conciseness**: Rate 1-5 how clear and concise the agent's explanations were
3. **User Type**: Classify as "Dull", "Medium", or "High" based on:
   - Speed of understanding
   - Quality of questions asked
   - Curiosity level
   - Response complexity
4. **Interest Rating**: Rate 1-5 the user's interest level based on:
   - Enthusiasm in responses
   - Questions asked voluntarily
   - Engagement indicators
5. **Engagement Rating**: Rate 1-5 the user's engagement based on:
   - Response length and quality
   - Willingness to participate
   - Active involvement
6. **Enjoyment Probability**: Estimate 0-1 likelihood that user enjoyed and benefited from the session

{self.llm_parser.get_format_instructions()}
"""
        
        try:
            response = self.llm.invoke(prompt)
            return self.llm_parser.parse(response.content)
        except Exception as e:
            print(f"❌ Error: LLM analysis failed: {e}")
            raise RuntimeError(f"Failed to analyze conversation with LLM: {e}") from e
    
    def _format_conversation_for_analysis(self, history: List[Dict[str, Any]]) -> str:
        """Format conversation history for LLM analysis"""
        formatted_lines = []
        for interaction in history:
            role = interaction.get("role", "unknown")
            content = interaction.get("content", "")
            
            # Handle string content in history
            if isinstance(content, str):
                formatted_lines.append(f"{role.title()}: {content}")
            else:
                formatted_lines.append(f"{role.title()}: [Non-text content]")
        
        return "\n".join(formatted_lines)
    
    def _extract_quiz_score(self, history: List[Dict], state: Dict) -> float:
        """Extract quiz score from conversation or session state"""
        
        # First check if quiz results are stored in session state
        if state.get("quiz_results"):
            quiz_data = state["quiz_results"]
            if isinstance(quiz_data, dict):
                correct = quiz_data.get("correct", 0)
                total = quiz_data.get("total", 0)
                if total > 0:
                    return (correct / total) * 100
        
        # Look for quiz-related interactions in conversation
        correct_answers = 0
        total_questions = 0
        
        for interaction in history:
            if interaction.get("role") == "assistant":
                content = str(interaction.get("content", "")).lower()
                if any(word in content for word in ["correct", "right", "well done", "excellent", "good job"]):
                    correct_answers += 1
                    total_questions += 1
                elif any(word in content for word in ["incorrect", "wrong", "not quite", "try again", "not right"]):
                    total_questions += 1
        
        if total_questions > 0:
            return (correct_answers / total_questions) * 100
        
        # Default score if no quiz interactions found
        return 75.0
    
    def _count_error_handling(self, history: List[Dict]) -> int:
        """Count corrections and re-prompts in the conversation"""
        error_count = 0
        
        for interaction in history:
            if interaction.get("role") == "assistant":
                content = str(interaction.get("content", "")).lower()
                error_indicators = [
                    "let me clarify", "correction", "actually", "i mean", "sorry", 
                    "let me rephrase", "to be more precise", "what i meant was",
                    "let me explain that better", "clarification"
                ]
                if any(indicator in content for indicator in error_indicators):
                    error_count += 1
        
        return error_count
    
    def _check_adaptability(self, state: Dict) -> bool:
        """Check if the agent adapted its flow based on user performance"""
        # Look for adaptation indicators in the state
        adaptation_indicators = [
            "_asked_mh",  # Moved to more help
            "misconception_detected",
            "last_correction",
            "retrieval_score",
            "transfer_success"
        ]
        
        for indicator in adaptation_indicators:
            if state.get(indicator):
                return True
        
        return False
    
    def _estimate_avg_response_time(self, history: List[Dict]) -> float:
        """Estimate average response time based on response complexity"""
        user_responses = [h for h in history if h.get("role") == "user"]
        
        if len(user_responses) == 0:
            return 30.0
        
        total_estimated_time = 0
        for response in user_responses:
            content = str(response.get("content", ""))
            # Estimate time based on response length and complexity
            base_time = 15  # Base 15 seconds
            length_factor = len(content) * 0.1  # 0.1 second per character
            word_count = len(content.split())
            complexity_factor = word_count * 0.5  # 0.5 second per word
            
            estimated_time = base_time + length_factor + complexity_factor
            total_estimated_time += min(estimated_time, 120)  # Cap at 2 minutes
        
        return total_estimated_time / len(user_responses)
    def upload_to_langfuse(self, metrics: SessionMetrics) -> bool:
        """Upload computed metrics to Langfuse as session-level metrics"""
        try:
            # Convert metrics to dictionary for Langfuse
            metrics_dict = metrics.model_dump()
            
            # Upload as session metadata
            self.langfuse.trace(
                id=metrics.session_id,
                metadata={
                    "session_metrics": metrics_dict,
                    "computed_at": datetime.now().isoformat()
                }
            )
            
            # Also log as individual scores for easier querying
            for metric_name, metric_value in metrics_dict.items():
                if metric_name not in ["session_id", "concepts_covered", "persona_name"]:  # Skip non-numeric or complex fields
                    try:
                        if isinstance(metric_value, (int, float, bool)):
                            self.langfuse.score(
                                name=metric_name,
                                value=float(metric_value),
                                trace_id=metrics.session_id,
                                comment=f"Session-level metric: {metric_name}"
                            )
                    except (ValueError, TypeError):
                        # Skip problematic metrics
                        pass
            
            print(f"✅ Successfully uploaded metrics to Langfuse for session: {metrics.session_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error: Failed to upload metrics to Langfuse: {e}")
            raise RuntimeError(f"Failed to upload metrics to Langfuse: {e}") from e


def compute_and_upload_session_metrics(session_id: str, 
                                     history: List[Dict[str, Any]], 
                                     session_state: Dict[str, Any],
                                     persona_name: Optional[str] = None) -> SessionMetrics:
    """
    Convenience function to compute and upload session metrics
    
    Args:
        session_id: Unique session identifier
        history: Conversation history
        session_state: Agent's final state
        persona_name: Optional persona name for the user
    
    Returns:
        SessionMetrics object with all computed metrics
        
    Raises:
        RuntimeError: If metrics computation or upload fails
    """
    try:
        computer = MetricsComputer()
        metrics = computer.compute_metrics(session_id, history, session_state, persona_name)
        
        # Upload to Langfuse
        computer.upload_to_langfuse(metrics)
        
        print(f"📊 Session metrics computed and uploaded successfully!")
        print(f"   - Concepts covered: {metrics.num_concepts_covered}")
        print(f"   - User type: {metrics.user_type}")
        print(f"   - Quiz score: {metrics.quiz_score:.1f}%")
        print(f"   - Engagement rating: {metrics.user_engagement_rating:.1f}/5")
        print(f"   - Enjoyment probability: {metrics.enjoyment_probability:.2f}")
        
        return metrics
    
    except Exception as e:
        print(f"❌ Error: Session metrics computation failed: {e}")
        raise RuntimeError(f"Session metrics computation failed: {e}") from e
