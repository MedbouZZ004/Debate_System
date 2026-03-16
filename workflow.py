"""
LangGraph workflow orchestration for WSD Debate System.

Implements the debate workflow as a state machine.
"""

import asyncio
from typing import Dict, Any, List
from logger import DebateLogger
from models import DebateState, DebateConfig, SideCase
from agents import (
    ResearchAgent,
    ArgumentConstructionAgent,
    RebuttalAgent,
    AnalysisAgent
)


class DebateWorkflow:
    """LangGraph-based debate workflow orchestrator."""
    
    def __init__(self):
        """Initialize workflow with agents."""
        self.research_agent = ResearchAgent()
        self.argument_agent = ArgumentConstructionAgent()
        self.rebuttal_agent = RebuttalAgent()
        self.analysis_agent = AnalysisAgent()
        self.logger = DebateLogger
    
    async def execute(self, config: DebateConfig) -> DebateState:
        """
        Execute the complete debate workflow.
        
        Args:
            config: Debate configuration
            
        Returns:
            Complete debate state
        """
        self.logger.info(f"Starting debate workflow for motion: {config.motion}")
        
        try:
            # Initialize state
            proposition = SideCase(
                side="Proposition",
                team_members=config.proposition_members
            )
            opposition = SideCase(
                side="Opposition",
                team_members=config.opposition_members
            )
            
            state = DebateState(
                motion=config.motion,
                proposition=proposition,
                opposition=opposition
            )
            
            # Phase 1: Research (Parallel)
            self.logger.info("Phase 1: Research for both sides")
            prop_research, opp_research = await asyncio.gather(
                self.research_agent.execute(config.motion, state.proposition, language=config.language),
                self.research_agent.execute(config.motion, state.opposition, language=config.language)
            )
            
            # Update state with research
            state.proposition.motion_analysis = prop_research.get("motion_analysis")
            state.proposition.key_definitions = prop_research.get("key_definitions", {})
            state.opposition.motion_analysis = opp_research.get("motion_analysis")
            state.opposition.key_definitions = opp_research.get("key_definitions", {})
            
            # Phase 2: Argument Construction (Parallel)
            self.logger.info("Phase 2: Argument construction for both sides")
            prop_args, opp_args = await asyncio.gather(
                self.argument_agent.execute(
                    config.motion,
                    state.proposition,
                    num_arguments=config.num_arguments,
                    research_data=prop_research,
                    language=config.language
                ),
                self.argument_agent.execute(
                    config.motion,
                    state.opposition,
                    num_arguments=config.num_arguments,
                    research_data=opp_research,
                    language=config.language
                )
            )
            
            # Update state with arguments
            from models import Argument
            for arg_data in prop_args.get("arguments", []):
                if isinstance(arg_data, Argument):
                    state.proposition.arguments.append(arg_data)
                else:
                    state.proposition.arguments.append(Argument(**arg_data))
            
            for arg_data in opp_args.get("arguments", []):
                if isinstance(arg_data, Argument):
                    state.opposition.arguments.append(arg_data)
                else:
                    state.opposition.arguments.append(Argument(**arg_data))
            
            # Phase 3: Rebuttal Generation (Parallel)
            self.logger.info("Phase 3: Rebuttal generation for both sides")
            prop_rebuttals, opp_rebuttals = await asyncio.gather(
                self.rebuttal_agent.execute(
                    config.motion,
                    state.proposition,
                    state.opposition,
                    state.opposition.arguments,
                    num_rebuttals=config.num_rebuttals,
                    language=config.language
                ),
                self.rebuttal_agent.execute(
                    config.motion,
                    state.opposition,
                    state.proposition,
                    state.proposition.arguments,
                    num_rebuttals=config.num_rebuttals,
                    language=config.language
                )
            )
            
            # Update state with rebuttals
            state.proposition.rebuttals = prop_rebuttals.get("rebuttals", {})
            state.opposition.rebuttals = opp_rebuttals.get("rebuttals", {})
            
            # Phase 4: Debate Analysis
            self.logger.info("Phase 4: Debate analysis")
            analysis = await self.analysis_agent.execute(
                config.motion,
                state.proposition,
                state.opposition,
                language=config.language
            )
            
            # Update state with analysis
            state.critical_clashes = analysis.get("critical_clashes", [])
            state.strategic_analysis = analysis.get("strategic_analysis")
            state.predicted_winner = analysis.get("predicted_winner")
            
            self.logger.info("Debate workflow completed successfully")
            return state
        
        except Exception as e:
            self.logger.error(f"Debate workflow failed: {str(e)}", exc_info=True)
            raise
