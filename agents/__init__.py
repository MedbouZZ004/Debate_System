"""
Agents module for WSD Debate System.

Contains all specialized debate agents:
- Research Agent: Topic analysis and research
- Argument Agent: Main argument construction
- Rebuttal Agent: Counter-argument generation
- Analysis Agent: Debate evaluation
"""

from agents.base_agent import DebateAgent
from agents.research_agent import ResearchAgent
from agents.argument_agent import ArgumentConstructionAgent
from agents.rebuttal_agent import RebuttalAgent
from agents.analysis_agent import AnalysisAgent

__all__ = [
    "DebateAgent",
    "ResearchAgent",
    "ArgumentConstructionAgent",
    "RebuttalAgent",
    "AnalysisAgent",
]
