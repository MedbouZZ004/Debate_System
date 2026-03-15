"""
Argument Construction Agent for WSD Debate System.

Builds main arguments for debate cases.
"""

import time
import json
from typing import Dict, Any, List
from agents.base_agent import DebateAgent
from models import SideCase, Argument


class ArgumentConstructionAgent(DebateAgent):
    """Agent responsible for constructing main arguments."""
    
    def __init__(self):
        """Initialize argument construction agent."""
        super().__init__("ArgumentConstructionAgent")
    
    async def execute(
        self,
        motion: str,
        side: SideCase,
        num_arguments: int = 3,
        research_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Construct main arguments for a debate case.
        
        Args:
            motion: The debate motion
            side: The side (proposition/opposition)
            num_arguments: Number of arguments to construct
            research_data: Optional research data to inform arguments
            
        Returns:
            Dictionary with constructed arguments
        """
        start_time = time.time()
        self._log_start(f"argument construction for {side.side}")
        
        try:
            # Generate arguments prompt
            prompt = self._build_arguments_prompt(
                motion, side, num_arguments, research_data
            )
            
            # Call LLM
            response = await self._call_llm(prompt)
            
            # Parse response
            arguments = self._parse_arguments_response(response, num_arguments)
            
            duration_ms = int((time.time() - start_time) * 1000)
            self._log_end(f"argument construction for {side.side}", duration_ms)
            
            return {
                "side": side.side,
                "arguments": arguments,
                "count": len(arguments)
            }
        
        except Exception as e:
            self._log_error(f"argument construction for {side.side}", str(e))
            raise
    
    def _build_arguments_prompt(
        self,
        motion: str,
        side: SideCase,
        num_arguments: int,
        research_data: Dict[str, Any] = None
    ) -> str:
        """Build arguments construction prompt for LLM."""
        side_stance = "supporting" if side.side == "Proposition" else "opposing"
        
        research_context = ""
        if research_data:
            research_context = f"""
Research Background:
- Motion Analysis: {research_data.get('motion_analysis', '')}
- Key Definitions: {json.dumps(research_data.get('key_definitions', {}))}
- Strategic Points: {json.dumps(research_data.get('strategic_points', []))}
"""
        
        prompt = f"""You are a debate expert constructing main arguments for a {side.side} team in World Schools Debate.

Motion: {motion}
Team Members: {', '.join(side.team_members)}
{research_context}

Your task is to construct {num_arguments} distinct, compelling arguments {side_stance} this motion.

Each argument should:
1. Be clear and decisive
2. Have strong logical structure
3. Include evidence or examples
4. Have clear impact on the debate

Provide the arguments in exactly this JSON format - must be valid JSON:
{{
    "arguments": [
        {{
            "contention": "Clear main claim",
            "reasoning": "Logical explanation of why this is true",
            "evidence": ["Evidence 1", "Evidence 2", "Evidence 3"],
            "impact": "Why this matters in the debate"
        }}
    ]
}}

Construct {num_arguments} strong arguments that support the {side.side} position. Each should be distinct and address different aspects of the motion."""
        
        return prompt
    
    def _parse_arguments_response(self, response: str, num_arguments: int) -> List[Argument]:
        """Parse LLM response to extract arguments."""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                
                arguments = []
                for arg_data in data.get("arguments", [])[:num_arguments]:
                    try:
                        arg = Argument(
                            contention=arg_data.get("contention", ""),
                            reasoning=arg_data.get("reasoning", ""),
                            evidence=arg_data.get("evidence", []),
                            impact=arg_data.get("impact")
                        )
                        arguments.append(arg)
                    except:
                        continue
                
                return arguments
            
            return []
        except:
            return []
