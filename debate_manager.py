"""
Debate Manager for WSD Debate System.

High-level orchestration and session management.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from logger import DebateLogger
from models import DebateConfig, DebateState
from models import DebateSession as DebateSessionModel
from workflow import DebateWorkflow
from utils import DebateValidator, DebateConfigBuilder


class DebateManager:
    """Main orchestration and session manager."""
    
    def __init__(self):
        """Initialize debate manager."""
        self.logger = DebateLogger
        self.workflow = DebateWorkflow()
        self.sessions: Dict[str, DebateSessionModel] = {}
    
    async def create_debate(
        self,
        motion: str,
        proposition_members: list,
        opposition_members: list,
        num_arguments: int = 3,
        num_rebuttals: int = 3,
        language: str = "English"
    ) -> DebateSessionModel:
        """
        Create and execute a debate.
        
        Args:
            motion: Debate motion
            proposition_members: Proposition team members
            opposition_members: Opposition team members
            num_arguments: Number of arguments per side
            num_rebuttals: Number of rebuttals per side
            language: Language for output (English, Arabic, French)
            
        Returns:
            Debate session with results
        """
        session_id = str(uuid.uuid4())
        self.logger.info(f"Creating debate session {session_id}")
        
        try:
            # Create config
            config = DebateConfig(
                motion=motion,
                proposition_members=proposition_members,
                opposition_members=opposition_members,
                num_arguments=num_arguments,
                num_rebuttals=num_rebuttals,
                language=language
            )
            
            # Validate
            DebateValidator.validate_config(config)
            
            # Create session
            session = DebateSessionModel(
                session_id=session_id,
                config=config,
                status="running"
            )
            
            # Execute debate
            start_time = datetime.now()
            state = await self.workflow.execute(config)
            end_time = datetime.now()
            
            # Calculate execution time
            execution_time = (end_time - start_time).total_seconds()
            state.execution_time_seconds = execution_time
            
            # Update session
            session.state = state
            session.status = "completed"
            
            # Store session
            self.sessions[session_id] = session
            
            self.logger.info(f"Debate {session_id} completed in {execution_time:.2f}s")
            return session
        
        except Exception as e:
            self.logger.error(f"Debate creation failed: {str(e)}", exc_info=True)
            raise
    
    def get_session(self, session_id: str) -> Optional[DebateSessionModel]:
        """Get debate session by ID."""
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> Dict[str, DebateSessionModel]:
        """Get all debate sessions."""
        return self.sessions.copy()
    
    def delete_session(self, session_id: str) -> bool:
        """Delete debate session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.logger.info(f"Session {session_id} deleted")
            return True
        return False


class DebateSession:
    """User-facing debate session interface."""
    
    def __init__(self, manager: Optional[DebateManager] = None):
        """
        Initialize debate session.
        
        Args:
            manager: Optional debate manager (creates new if not provided)
        """
        self.manager = manager or DebateManager()
        self.current_session: Optional[DebateSession] = None
        self.logger = DebateLogger
    
    async def start_debate(
        self,
        motion: str,
        proposition_members: list,
        opposition_members: list,
        num_arguments: int = 3,
        num_rebuttals: int = 3,
        language: str = "English"
    ) -> DebateState:
        """
        Start a new debate.
        
        Args:
            motion: Debate motion
            proposition_members: Proposition team members
            opposition_members: Opposition team members
            num_arguments: Number of arguments
            num_rebuttals: Number of rebuttals
            language: Language for output (English, Arabic, French)
            
        Returns:
            Debate state with results
        """
        session = await self.manager.create_debate(
            motion=motion,
            proposition_members=proposition_members,
            opposition_members=opposition_members,
            num_arguments=num_arguments,
            num_rebuttals=num_rebuttals,
            language=language
        )
        
        self.current_session = session
        return session.state
    
    def get_summary(self) -> Optional[Dict[str, Any]]:
        """Get summary of current debate."""
        if not self.current_session or not self.current_session.state:
            return None
        
        state = self.current_session.state
        return {
            "motion": state.motion,
            "execution_time": state.execution_time_seconds,
            "proposition_arguments": len(state.proposition.arguments),
            "opposition_arguments": len(state.opposition.arguments),
            "predicted_winner": state.predicted_winner,
            "critical_clashes": state.critical_clashes
        }
    
    def get_state(self) -> Optional[DebateState]:
        """Get current debate state."""
        return self.current_session.state if self.current_session else None
    
    async def save_log(self, filepath: str):
        """Save debate to file."""
        if not self.current_session or not self.current_session.state:
            self.logger.warning("No debate to save")
            return
        
        from utils import DebateExporter
        if filepath.endswith('.json'):
            DebateExporter.save_json(self.current_session.state, filepath)
        elif filepath.endswith('.md'):
            DebateExporter.save_markdown(self.current_session.state, filepath)
        else:
            self.logger.warning(f"Unsupported file format: {filepath}")
