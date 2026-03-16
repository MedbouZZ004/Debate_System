"""
Data models for WSD Debate System using Pydantic.

Defines all data structures with validation.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class CaseStudy(BaseModel):
    """Represents a real-world case study supporting an argument."""
    
    title: str = Field(..., description="Title of the case study")
    background: str = Field(..., description="Background and context of the case")
    methodology: Optional[str] = Field(None, description="Approach or methodology used")
    outcomes: str = Field(..., description="Results and outcomes achieved")
    impact: str = Field(..., description="Overall impact and relevance to argument")
    
    @validator('title', 'background', 'outcomes', 'impact')
    def non_empty_string(cls, v):
        """Ensure non-empty strings."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class Argument(BaseModel):
    """Represents a single argument."""
    
    contention: str = Field(..., description="Main claim or contention")
    reasoning: str = Field(..., description="Logical reasoning and explanation")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    impact: Optional[str] = Field(None, description="Impact or significance")
    case_studies: List[CaseStudy] = Field(default_factory=list, description="Real-world case studies")
    position_correlation: Optional[str] = Field(None, description="How this argument correlates with the overall position")
    
    @validator('contention', 'reasoning')
    def non_empty_string(cls, v):
        """Ensure non-empty strings."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()
    
    @validator('contention')
    def contention_length(cls, v):
        """Validate contention length."""
        if len(v) < 5:
            raise ValueError("Contention must be at least 5 characters")
        if len(v) > 500:
            raise ValueError("Contention must be less than 500 characters")
        return v
    
    @validator('evidence')
    def evidence_length(cls, v):
        """Validate evidence list length."""
        if len(v) > 20:
            raise ValueError("Evidence list cannot exceed 20 pieces")
        return v


class Rebuttal(BaseModel):
    """Represents a rebuttal to an opponent argument."""
    
    targets_argument: str = Field(..., description="The opponent's argument being rebutted")
    main_rebuttal: str = Field(..., description="The core rebuttal point")
    logical_flaw: str = Field(..., description="The logical flaw in the opponent's argument")
    counter_point: str = Field(..., description="Our counter-argument")
    impact: str = Field(..., description="Why this rebuttal matters to the debate")
    
    @validator('targets_argument', 'main_rebuttal', 'logical_flaw', 'counter_point', 'impact')
    def non_empty_string(cls, v):
        """Ensure non-empty strings."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class SideCase(BaseModel):
    """Represents one side's complete case."""
    
    side: str = Field(..., description="'Proposition' or 'Opposition'")
    team_members: List[str] = Field(..., description="Names of team members")
    
    # Research phase outputs
    motion_analysis: Optional[str] = Field(None, description="Analysis of the motion")
    key_definitions: Dict[str, str] = Field(default_factory=dict, description="Key term definitions")
    
    # Arguments
    arguments: List[Argument] = Field(default_factory=list, description="Main arguments")
    
    # Rebuttals
    rebuttals: List[Rebuttal] = Field(default_factory=list, description="Rebuttals to opponent arguments")
    
    @validator('side')
    def validate_side(cls, v):
        """Validate side is either Proposition or Opposition."""
        if v not in ["Proposition", "Opposition"]:
            raise ValueError("Side must be 'Proposition' or 'Opposition'")
        return v
    
    @validator('team_members')
    def validate_team_members(cls, v):
        """Validate team members list."""
        if not v or len(v) == 0:
            raise ValueError("Team must have at least one member")
        if len(v) > 10:
            raise ValueError("Team cannot have more than 10 members")
        for member in v:
            if not member or not member.strip():
                raise ValueError("Team member names cannot be empty")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "side": "Proposition",
                "team_members": ["Alice", "Bob", "Charlie"],
                "arguments": [
                    {
                        "contention": "AI regulation improves safety",
                        "reasoning": "Regulated systems are more transparent",
                        "evidence": ["Study X", "Case Y"]
                    }
                ]
            }
        }


class DebateState(BaseModel):
    """Complete debate state and results."""
    
    motion: str = Field(..., description="The debate motion")
    proposition: SideCase = Field(..., description="Proposition case")
    opposition: SideCase = Field(..., description="Opposition case")
    
    # Analysis
    critical_clashes: List[str] = Field(default_factory=list, description="Key points of disagreement")
    strategic_analysis: Optional[str] = Field(None, description="Strategic analysis of the debate")
    predicted_winner: Optional[str] = Field(None, description="Predicted winner ('Proposition' or 'Opposition')")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    execution_time_seconds: Optional[float] = Field(None, description="Total execution time")
    
    @validator('motion')
    def validate_motion(cls, v):
        """Validate motion string."""
        if not v or not v.strip():
            raise ValueError("Motion cannot be empty")
        if len(v) < 10:
            raise ValueError("Motion must be at least 10 characters")
        if len(v) > 2000:
            raise ValueError("Motion must be less than 2000 characters")
        return v.strip()
    
    @validator('predicted_winner')
    def validate_predicted_winner(cls, v):
        """Validate predicted winner if provided."""
        if v and v not in ["Proposition", "Opposition"]:
            raise ValueError("Predicted winner must be 'Proposition' or 'Opposition'")
        return v
    
    @validator('execution_time_seconds')
    def validate_execution_time(cls, v):
        """Validate execution time."""
        if v and v < 0:
            raise ValueError("Execution time cannot be negative")
        return v


class DebateConfig(BaseModel):
    """Configuration for a debate session."""
    
    motion: str = Field(..., description="The debate motion")
    proposition_members: List[str] = Field(..., description="Proposition team members")
    opposition_members: List[str] = Field(..., description="Opposition team members")
    
    num_arguments: int = Field(default=3, ge=1, le=10, description="Number of main arguments per side")
    num_rebuttals: int = Field(default=3, ge=1, le=10, description="Number of rebuttals per side")
    language: str = Field(default="English", description="Language for the debate output (English, Arabic, French)")
    
    @validator('motion')
    def validate_motion(cls, v):
        """Validate motion string."""
        if not v or not v.strip():
            raise ValueError("Motion cannot be empty")
        if len(v) < 10:
            raise ValueError("Motion must be at least 10 characters")
        if len(v) > 2000:
            raise ValueError("Motion must be less than 2000 characters")
        return v.strip()
    
    @validator('proposition_members', 'opposition_members')
    def validate_members(cls, v):
        """Validate member lists."""
        if not v or len(v) == 0:
            raise ValueError("Team must have at least one member")
        if len(v) > 10:
            raise ValueError("Team cannot have more than 10 members")
        for member in v:
            if not member or not member.strip():
                raise ValueError("Team member names cannot be empty")
            if len(member) > 100:
                raise ValueError(f"Team member name too long: {member}")
        return v
    
    @validator('language')
    def validate_language(cls, v):
        """Validate language specification."""
        if not v or not v.strip():
            raise ValueError("Language cannot be empty")
        if len(v) > 50:
            raise ValueError("Language specification too long")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "motion": "This house believes AI should be regulated",
                "proposition_members": ["Alice", "Bob", "Charlie"],
                "opposition_members": ["David", "Eve", "Frank"],
                "num_arguments": 3,
                "num_rebuttals": 3
            }
        }


class DebateSession(BaseModel):
    """Session information and metadata."""
    
    session_id: str = Field(..., description="Unique session identifier")
    config: DebateConfig = Field(..., description="Debate configuration")
    state: Optional[DebateState] = Field(None, description="Current debate state")
    status: str = Field(default="initialized", description="Session status")


# Response types for agents
class AgentResponse(BaseModel):
    """Base response from an agent."""
    
    agent_name: str = Field(..., description="Name of the agent")
    task: str = Field(..., description="Task performed")
    result: Dict[str, Any] = Field(..., description="Result data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Execution timestamp")
    execution_time_ms: Optional[int] = Field(None, description="Execution time in milliseconds")


class ResearchResponse(AgentResponse):
    """Response from research agent."""
    
    pass


class ArgumentResponse(AgentResponse):
    """Response from argument agent."""
    
    pass


class RebuttalResponse(AgentResponse):
    """Response from rebuttal agent."""
    
    pass


class AnalysisResponse(AgentResponse):
    """Response from analysis agent."""
    
    pass
