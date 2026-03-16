"""
Research Agent for WSD Debate System.

Analyzes debate topics and prepares research for both sides.
"""

import time
from typing import Dict, Any, List
from agents.base_agent import DebateAgent
from models import SideCase


class ResearchAgent(DebateAgent):
    """Agent responsible for topic research and analysis."""
    
    def __init__(self):
        """Initialize research agent."""
        super().__init__("ResearchAgent")
    
    async def execute(self, motion: str, side: SideCase, language: str = "English") -> Dict[str, Any]:
        """
        Conduct research on the debate motion.
        
        Args:
            motion: The debate motion
            side: The side (proposition/opposition) to research
            language: Language for output (default: "English")
            
        Returns:
            Dictionary with research results
            
        Raises:
            ValueError: If inputs are invalid
            Exception: If research fails
        """
        start_time = time.time()
        self._log_start(f"research for {side.side}")
        
        try:
            # Validate inputs
            self._validate_prompt_input(motion, side.side)
            self._validate_team_members(side.team_members)
            
            if language and len(language) > 50:
                raise ValueError("Language specification too long")
            
            # Generate research prompt
            prompt = self._build_research_prompt(motion, side, language)
            
            # Call LLM
            response = await self._call_llm(prompt)
            
            # Parse response
            analysis = self._parse_research_response(response, motion, side)
            
            duration_ms = int((time.time() - start_time) * 1000)
            self._log_end(f"research for {side.side}", duration_ms)
            
            return {
                "side": side.side,
                "motion_analysis": analysis["motion_analysis"],
                "key_definitions": analysis["key_definitions"],
                "strategic_points": analysis["strategic_points"]
            }
        
        except Exception as e:
            self._log_error(f"research for {side.side}", str(e))
            raise
    
    def _build_research_prompt(self, motion: str, side: SideCase, language: str = "English") -> str:
        """Build research prompt for LLM."""
        side_stance = "supporting" if side.side == "Proposition" else "opposing"
        
        language_instruction = f"\n\nIMPORTANT: You MUST write your entire response in {language}. All text, analysis, definitions, and strategic points must be in {language}."
        
        prompt = f"""You are a debate expert preparing a {side.side} team for World Schools Debate.

Motion: {motion}

Team Members: {', '.join(side.team_members)}

Your task is to provide research and strategic analysis for the {side_stance} position.

Provide your analysis in the following JSON format:
{{
    "motion_analysis": "A detailed analysis of the motion and its implications",
    "key_definitions": {{
        "term1": "definition1",
        "term2": "definition2"
    }},
    "strategic_points": [
        "Strategic point 1",
        "Strategic point 2",
        "Strategic point 3"
    ]
}}

Focus on:
1. Analyzing the key terms in the motion
2. Identifying assumptions in the motion
3. Determining framework and key clash points
4. Strategic advantages for the {side.side} position
5. Potential weaknesses to address

Provide thorough, strategic research that will help the {side.side} team prepare strong arguments.{language_instruction}"""
        
        return prompt
    
    def _parse_research_response(self, response: str, motion: str, side: SideCase) -> Dict[str, Any]:
        """Parse LLM response to extract research data."""
        fallback = {
            "motion_analysis": response,
            "key_definitions": {},
            "strategic_points": []
        }

        try:
            import json

            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)

                # Validate required keys; fill in safe defaults for any that are missing
                return {
                    "motion_analysis": data.get("motion_analysis") or response,
                    "key_definitions": data.get("key_definitions") or {},
                    "strategic_points": data.get("strategic_points") or [],
                }

            # Fallback if JSON block not found
            return fallback

        except Exception:
            return fallback
