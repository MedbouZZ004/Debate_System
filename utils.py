"""
Utility functions and classes for WSD Debate System.

Includes builders, validators, and export utilities.
"""

import json
from typing import List, Optional
from datetime import datetime
from models import DebateConfig, DebateState, Argument, SideCase
from logger import DebateLogger


class DebateConfigBuilder:
    """Builder pattern for constructing DebateConfig."""
    
    def __init__(self):
        """Initialize builder."""
        self._motion: Optional[str] = None
        self._proposition_members: List[str] = []
        self._opposition_members: List[str] = []
        self._num_arguments: int = 3
        self._num_rebuttals: int = 3
    
    def set_motion(self, motion: str) -> "DebateConfigBuilder":
        """Set the debate motion."""
        self._motion = motion
        return self
    
    def add_proposition_member(self, name: str) -> "DebateConfigBuilder":
        """Add a proposition team member."""
        self._proposition_members.append(name)
        return self
    
    def add_opposition_member(self, name: str) -> "DebateConfigBuilder":
        """Add an opposition team member."""
        self._opposition_members.append(name)
        return self
    
    def set_proposition_members(self, members: List[str]) -> "DebateConfigBuilder":
        """Set all proposition members."""
        self._proposition_members = members
        return self
    
    def set_opposition_members(self, members: List[str]) -> "DebateConfigBuilder":
        """Set all opposition members."""
        self._opposition_members = members
        return self
    
    def set_num_arguments(self, num: int) -> "DebateConfigBuilder":
        """Set number of arguments."""
        self._num_arguments = num
        return self
    
    def set_num_rebuttals(self, num: int) -> "DebateConfigBuilder":
        """Set number of rebuttals."""
        self._num_rebuttals = num
        return self
    
    def build(self) -> DebateConfig:
        """Build the configuration."""
        if not self._motion:
            raise ValueError("Motion must be set")
        if not self._proposition_members:
            raise ValueError("Proposition team must have at least one member")
        if not self._opposition_members:
            raise ValueError("Opposition team must have at least one member")
        
        return DebateConfig(
            motion=self._motion,
            proposition_members=self._proposition_members,
            opposition_members=self._opposition_members,
            num_arguments=self._num_arguments,
            num_rebuttals=self._num_rebuttals
        )


class DebateValidator:
    """Validation utilities for debate data."""
    
    @staticmethod
    def validate_config(config: DebateConfig) -> bool:
        """Validate a debate configuration."""
        try:
            config.model_validate(config.model_dump())
            DebateLogger.info(f"Config validated: {config.motion}")
            return True
        except Exception as e:
            DebateLogger.error(f"Config validation failed: {str(e)}")
            raise
    
    @staticmethod
    def validate_arguments(arguments: List[Argument]) -> bool:
        """Validate list of arguments."""
        if not arguments:
            raise ValueError("Arguments list cannot be empty")
        
        for i, arg in enumerate(arguments):
            if not arg.contention or not arg.reasoning:
                raise ValueError(f"Argument {i} missing contention or reasoning")
        
        return True
    
    @staticmethod
    def validate_state(state: DebateState) -> bool:
        """Validate debate state."""
        if not state.motion:
            raise ValueError("Motion cannot be empty")
        if not state.proposition or not state.opposition:
            raise ValueError("Both sides must be present")
        return True


class ArgumentFormatter:
    """Format arguments for display and export."""
    
    @staticmethod
    def format_markdown(arg: Argument) -> str:
        """Format argument as markdown."""
        md = f"### {arg.contention}\n\n"
        md += f"**Reasoning:** {arg.reasoning}\n\n"
        
        if arg.evidence:
            md += "**Evidence:**\n"
            for evidence in arg.evidence:
                md += f"- {evidence}\n"
            md += "\n"
        
        if arg.impact:
            md += f"**Impact:** {arg.impact}\n"
        
        return md
    
    @staticmethod
    def format_plain(arg: Argument) -> str:
        """Format argument as plain text."""
        text = f"{arg.contention}\n"
        text += f"Reasoning: {arg.reasoning}\n"
        
        if arg.evidence:
            text += "Evidence:\n"
            for evidence in arg.evidence:
                text += f"  - {evidence}\n"
        
        if arg.impact:
            text += f"Impact: {arg.impact}\n"
        
        return text


class DebateExporter:
    """Export debate results in various formats."""
    
    @staticmethod
    def to_json(state: DebateState, indent: int = 2) -> str:
        """Export debate state to JSON."""
        return json.dumps(state.model_dump(), indent=indent, default=str)
    
    @staticmethod
    def to_markdown(state: DebateState) -> str:
        """Export debate state to Markdown."""
        md = f"# Debate Report\n\n"
        md += f"**Motion:** {state.motion}\n\n"
        
        # Proposition
        md += f"## Proposition\n"
        md += f"**Team:** {', '.join(state.proposition.team_members)}\n\n"
        
        if state.proposition.motion_analysis:
            md += f"**Analysis:** {state.proposition.motion_analysis}\n\n"
        
        md += "### Main Arguments\n"
        for i, arg in enumerate(state.proposition.arguments, 1):
            md += f"{i}. {ArgumentFormatter.format_markdown(arg)}\n"
        
        # Opposition
        md += f"## Opposition\n"
        md += f"**Team:** {', '.join(state.opposition.team_members)}\n\n"
        
        if state.opposition.motion_analysis:
            md += f"**Analysis:** {state.opposition.motion_analysis}\n\n"
        
        md += "### Main Arguments\n"
        for i, arg in enumerate(state.opposition.arguments, 1):
            md += f"{i}. {ArgumentFormatter.format_markdown(arg)}\n"
        
        # Analysis
        if state.critical_clashes:
            md += f"## Critical Clashes\n"
            for clash in state.critical_clashes:
                md += f"- {clash}\n"
            md += "\n"
        
        if state.strategic_analysis:
            md += f"## Strategic Analysis\n{state.strategic_analysis}\n\n"
        
        if state.predicted_winner:
            md += f"## Predicted Winner\n{state.predicted_winner}\n"
        
        return md
    
    @staticmethod
    def save_json(state: DebateState, filepath: str):
        """Save debate state to JSON file."""
        with open(filepath, 'w') as f:
            f.write(DebateExporter.to_json(state))
        DebateLogger.info(f"Debate saved to {filepath}")
    
    @staticmethod
    def save_markdown(state: DebateState, filepath: str):
        """Save debate state to Markdown file."""
        with open(filepath, 'w') as f:
            f.write(DebateExporter.to_markdown(state))
        DebateLogger.info(f"Debate saved to {filepath}")


class DebateExportHelper:
    """Convenience helper for debate exports."""
    
    @staticmethod
    def save_debate_json(state: DebateState, filepath: str):
        """Save debate to JSON."""
        DebateExporter.save_json(state, filepath)
    
    @staticmethod
    def save_debate_markdown(state: DebateState, filepath: str):
        """Save debate to Markdown."""
        DebateExporter.save_markdown(state, filepath)
