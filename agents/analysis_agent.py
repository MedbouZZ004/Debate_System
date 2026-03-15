"""
Analysis Agent for WSD Debate System.

Evaluates and analyzes complete debate cases.
"""

import time
import json
from typing import Dict, Any, List
from agents.base_agent import DebateAgent
from models import SideCase


class AnalysisAgent(DebateAgent):
    """Agent responsible for debate analysis and evaluation."""
    
    def __init__(self):
        """Initialize analysis agent."""
        super().__init__("AnalysisAgent")
    
    async def execute(
        self,
        motion: str,
        proposition: SideCase,
        opposition: SideCase
    ) -> Dict[str, Any]:
        """
        Analyze the complete debate.
        
        Args:
            motion: The debate motion
            proposition: Proposition side case
            opposition: Opposition side case
            
        Returns:
            Dictionary with analysis results
        """
        start_time = time.time()
        self._log_start("debate analysis")
        
        try:
            # Generate analysis prompt
            prompt = self._build_analysis_prompt(motion, proposition, opposition)
            
            # Call LLM
            response = await self._call_llm(prompt)
            
            # Parse response
            analysis = self._parse_analysis_response(response)
            
            duration_ms = int((time.time() - start_time) * 1000)
            self._log_end("debate analysis", duration_ms)
            
            return analysis
        
        except Exception as e:
            self._log_error("debate analysis", str(e))
            raise
    
    def _build_analysis_prompt(
        self,
        motion: str,
        proposition: SideCase,
        opposition: SideCase
    ) -> str:
        """Build analysis prompt for LLM."""
        prop_args = "\n".join([
            f"- {arg.contention}: {arg.reasoning}"
            for arg in proposition.arguments
        ])
        opp_args = "\n".join([
            f"- {arg.contention}: {arg.reasoning}"
            for arg in opposition.arguments
        ])
        
        prompt = f"""You are an expert debate judge and analyst evaluating a World Schools Debate.

Motion: {motion}

Proposition Team: {', '.join(proposition.team_members)}
Proposition Arguments:
{prop_args}

Opposition Team: {', '.join(opposition.team_members)}
Opposition Arguments:
{opp_args}

Your task is to provide a comprehensive analysis of this debate.

Analyze:
1. Key clash points between the sides
2. Strengths and weaknesses of each case
3. Which side has the better logical position
4. Likely winner and why
5. Critical points in the debate

Provide your analysis in exactly this JSON format - must be valid JSON:
{{
    "critical_clashes": [
        "Clash point 1",
        "Clash point 2",
        "Clash point 3"
    ],
    "proposition_strengths": ["Strength 1", "Strength 2"],
    "proposition_weaknesses": ["Weakness 1", "Weakness 2"],
    "opposition_strengths": ["Strength 1", "Strength 2"],
    "opposition_weaknesses": ["Weakness 1", "Weakness 2"],
    "strategic_analysis": "Overall strategic analysis of the debate",
    "predicted_winner": "Proposition or Opposition",
    "reasoning": "Why this team is predicted to win"
}}

Provide a thorough, balanced analysis that evaluates both teams fairly."""
        
        return prompt
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to extract analysis."""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                
                return {
                    "critical_clashes": data.get("critical_clashes", []),
                    "proposition_strengths": data.get("proposition_strengths", []),
                    "proposition_weaknesses": data.get("proposition_weaknesses", []),
                    "opposition_strengths": data.get("opposition_strengths", []),
                    "opposition_weaknesses": data.get("opposition_weaknesses", []),
                    "strategic_analysis": data.get("strategic_analysis", ""),
                    "predicted_winner": data.get("predicted_winner", ""),
                    "reasoning": data.get("reasoning", "")
                }
            
            return {}
        except:
            return {}
