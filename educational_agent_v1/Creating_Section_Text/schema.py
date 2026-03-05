from pydantic import BaseModel, Field, validator

from typing import List, Literal

ALLOWED_KG_NODES = [
    'Sundial',
    'Water Clock',
    'Hourglass',
    'Candle Clock',
    'Simple Pendulum',
    'Time Period of Pendulum',
    'Speed',
    'SI Unit of Time',
    'Uniform Linear Motion',
    'Non-uniform Linear Motion',
]


class StudentParameters(BaseModel):
    # Cognitive & Academic Profile
    conceptual_clarity_level: int = Field(
        ..., ge=1, le=5,
        description="1 (very low clarity) to 5 (very high clarity)"
    )
    attention_span_category: int = Field(
        ..., ge=1, le=3,
        description="1 (short), 2 (medium), 3 (long)"
    )
    retention_strength: float = Field(
        ..., ge=0.0, le=100.0,
        description="Recall percentage (0–100%)"
    )
    problem_solving_speed_sec: int = Field(
        ..., ge=30, le=600,
        description="Time in seconds to solve a problem (30–600)"
    )
    error_pattern: Literal['calculation', 'conceptual', 'careless'] = Field(
        ..., description="Type of error the student most often makes"
    )
    growth_slope: float = Field(
        ..., ge=-1.0, le=1.0,
        description="Normalized performance change per week (–1 to +1)"
    )

    # Learning Behavior
    response_to_feedback: int = Field(
        ..., ge=1, le=5,
        description="1 (resistant) to 5 (very receptive)"
    )
    revisions_per_week: int = Field(
        ..., ge=0, le=3,
        description="Number of revision sessions per week (0–3+)"
    )
    days_between_revisions: int = Field(
        ..., ge=1, le=14,
        description="Average days between revision sessions (1–14)"
    )
    method_of_revision: List[Literal[
        'active_recall',
        'spaced_repetition',
        'flashcards',
        'practice_tests',
        'summarization',
        'group_study',
        'mnemonics'
    ]] = Field(..., min_items=1,
        description="Revision methods used by the student; choose one or more")
    question_asking_nature: int = Field(
        ..., ge=1, le=3,
        description="1 (rarely asks), 2 (asks when stuck), 3 (frequently asks)"
    )
    self_assessment_accuracy: float = Field(
        ..., ge=-100.0, le=100.0,
        description="Predicted vs. actual score difference (–100% to +100%)"
    )
    exploration_tendency: int = Field(
        ..., ge=1, le=5,
        description="1 (sticks to syllabus) to 5 (highly curious)"
    )

    # Teacher & Peer Interaction
    teacher_relationship_quality: int = Field(
        ..., ge=1, le=5,
        description="1 (poor) to 5 (excellent)"
    )
    peer_learning_behavior: int = Field(
        ..., ge=1, le=3,
        description="1 (solo), 2 (mix), 3 (groups)"
    )
    communication_clarity: int = Field(
        ..., ge=1, le=5,
        description="1 (unclear) to 5 (very clear)"
    )
    discussion_engagement: int = Field(
        ..., ge=1,le=5,
        description="Participation level in group/class discussions 1 (low) to 5 (very high)"
    )

    # Emotion & Motivation
    test_anxiety_level: int = Field(
        ..., ge=1, le=5,
        description="1 (none) to 5 (very high)"
    )
    resilience_after_failure: int = Field(
        ..., ge=1, le=5,
        description="1 (gives up) to 5 (tries again immediately)"
    )
    motivation_intrinsic_vs_extrinsic: float = Field(
        ..., ge=0.0, le=1.0,
        description="0 (fully extrinsic) to 1 (fully intrinsic)"
    )
    achievement_orientation: int = Field(
        ..., ge=1, le=3,
        description="1 (fully performance-driven) to 3 (fully mastery-driven)"
    )
    emotional_self_awareness: int = Field(
        ..., ge=1, le=5,
        description="Ability to recognize and reflect on emotional state 1 (low) to 5 (high)"
    )

    # Tech & Digital Behavior
    device_access_type: int = Field(
        ..., ge=0, le=2,
        description="0 (no device), 1 (shared), 2 (own)"
    )
    preferred_edtech_apps: List[str] = Field(
        ..., min_items=0, max_items=3,
        description="Top 3 edtech apps the student uses (single-word each)"
    )
    digital_distraction_level: int = Field(
        ..., ge=1, le=5,
        description="1 (focused) to 5 (easily distracted)"
    )
    input_method_preference: Literal['typing', 'voice', 'writing'] = Field(
        ..., description="Preferred input method"
    )

    # Contextual & Environmental
    highest_academic_level: Literal[
        'none',
        'preschool',
        'primary_school',
        'middle_school',
        'high_school',
        'bachelor',
        'master',
        'phd'
    ] = Field(...,
        description="Highest academic level attained in the household")
    study_space_quality: int = Field(
        ..., ge=1, le=5,
        description="Does student have availability of a quiet, clean space to study. 1 (very poor) to 5 (excellent)"
    )
    academic_pressure_at_home: int = Field(
        ..., ge=1, le=5,
        description="1 (low) to 5 (very high)"
    )
    family_responsibilities_hrs: int = Field(
        ..., ge=0, le=24,
        description="Hours per day (0–24)"
    )
    support_system_strength: int = Field(
        ..., ge=1, le=3,
        description="1 (none), 2 (some), 3 (strong)"
    )

    # Meta-Learning Parameters
    # learning_efficiency_index: float = Field(
    #     ..., ge=0.0,
    #     description="Units of content mastered per learning-hour (e.g. 0.5–5.0)"
    # )
    content_type_preference: List[str] = Field(
        ..., min_items=1,
        description="Preferred content types (one-word each).Eg: text, video, simulation, gamified etc."
    )
    knowledge_graph_nodes_covered: List[Literal[
    'Sundial',
    'Water Clock',
    'Hourglass',
    'Candle Clock',
    'Simple Pendulum',
    'Time Period of Pendulum',
    'Speed',
    'SI Unit of Time',
    'Uniform Linear Motion',
    'Non-uniform Linear Motion'
    ]] = Field(
        ...,
        description=(
            '''Ordered list of concept names covered so far; each entry must be one of the Literal options and preserve the defined sequence—if 'ConceptB' appears, 'ConceptA' must precede it.
            .Whenever you pick a concept ensure that all concepts precedding it in the list are also included.Eg if Concept C is picked then both A nd B should also have been picked'''
        )
    )

    @validator('knowledge_graph_nodes_covered')
    def must_be_exact_prefix(cls, v):
        if v != ALLOWED_KG_NODES[:len(v)]:
            raise ValueError(
                f"'knowledge_graph_nodes_covered' must be the prefix of {ALLOWED_KG_NODES}. "
                f"Got {v!r}"
            )
        return v

    ongoing_concept: Literal[
        'Sundial',
        'Water Clock',
        'Hourglass',
        'Candle Clock',
        'Simple Pendulum',
        'Time Period of Pendulum',
        'Speed',
        'SI Unit of Time',
        'Uniform Linear Motion',
        'Non-uniform Linear Motion'
    ] = Field(
        ...,
        description='''The concept currently being studied by the student.Ensure that this is the concept that follows the last concept in 'knowledge_graph_nodes_covered' list. Eg if 'Uniform Linear Motion' is the last concept in that list, then this would be the next concept in the list namely 'Non-uniform Linear Motion'.
        Also in case the last concept in 'knowledge_graph_nodes_covered' is 'Non-uniform Linear Motion', then this field should be set to 'Non-uniform Linear Motion' as there are no more concepts to study.'''
    )
    @validator('ongoing_concept')
    def ongoing_concept_must_follow_knowledge_graph(cls, v, values):
        covered = values.get('knowledge_graph_nodes_covered', [])
        if v != ALLOWED_KG_NODES[len(covered)] or (len(covered) == len(ALLOWED_KG_NODES) and v != ALLOWED_KG_NODES[-1]):
            raise ValueError(
                f"'ongoing_concept' must be the next concept after the last in 'knowledge_graph_nodes_covered'. "
                f"Got {v!r} with covered {covered!r}"
            )
        if(not covered and v != ALLOWED_KG_NODES[0]):
            raise ValueError(
                f"'ongoing_concept' must be the first concept in the list if 'knowledge_graph_nodes_covered' is empty. "
                f"Got {v!r}"
            )
        return v
    
    metacognitive_skill_level: int = Field(
        ..., ge=1, le=5,
        description="Awareness of one's own learning process and gaps. 1 (unaware) to 5 (very aware)"
    )

class NextSectionChoice(BaseModel):
    section_name: Literal[
        "Concept Definition",
        "Explanation (with analogies)",
        "Details (facts, sub-concepts)",
        "Intuition",
        "Logical Flow",
        "Working",
        "Critical Thinking",
        "MCQs",
        "Real-Life Application",
        "What-if Scenarios"
    ] = Field(
        ...,
        description="The next section to show, chosen as best for the student given their current parameters"
    )
    difficulty: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, the difficulty level (1–5) appropriate for the selected section"
    )
    board_exam_importance: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, how important this section is for board exams (1–5)"
    )
    olympiad_importance: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, how important this section is for Olympiad preparation (1–5)"
    )
    avg_study_time_min: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, the estimated study time (1–5 scale) for the selected section"
    )
    interest_evoking: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, how engaging this section will be (1–5)"
    )
    curiosity_evoking: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, how much this section will spark curiosity (1–5)"
    )
    critical_reasoning_needed: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, the level of critical reasoning required (1–5)"
    )
    inquiry_learning_scope: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, scope for inquiry-based learning in this section (1–5)"
    )
    example_availability: int = Field(
        ...,
        ge=1, le=5,
        description="According to current student parameters, the availability of helpful examples in this section (1–5)"
    )
