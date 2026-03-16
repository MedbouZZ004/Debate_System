"""
Rebuttal Agent for WSD Debate System.

Generates rebuttals and counter-arguments.
"""

import time
import json
from typing import Dict, Any, List
from agents.base_agent import DebateAgent
from models import SideCase, Argument, Rebuttal


class RebuttalAgent(DebateAgent):
    """Agent responsible for generating rebuttals and counter-arguments."""
    
    def __init__(self):
        """Initialize rebuttal agent."""
        super().__init__("RebuttalAgent")
    
    async def execute(
        self,
        motion: str,
        defending_side: SideCase,
        attacking_side: SideCase,
        opponent_arguments: List[Argument],
        num_rebuttals: int = 3,
        language: str = "English"
    ) -> Dict[str, Any]:
        """
        Generate rebuttals to opponent arguments.
        
        Args:
            motion: The debate motion
            defending_side: The side generating rebuttals
            attacking_side: The side being rebutted
            opponent_arguments: Arguments to rebut
            num_rebuttals: Number of rebuttals to generate
            language: Language for output (default: "English")
            
        Returns:
            Dictionary with generated rebuttals
            
        Raises:
            ValueError: If inputs are invalid
            Exception: If rebuttal generation fails
        """
        start_time = time.time()
        self._log_start(f"rebuttal generation for {defending_side.side}")
        
        try:
            # Validate inputs
            self._validate_prompt_input(motion, defending_side.side)
            self._validate_team_members(defending_side.team_members)
            
            if not opponent_arguments or len(opponent_arguments) == 0:
                raise ValueError("Must provide at least one opponent argument to rebut")
            
            if num_rebuttals < 1 or num_rebuttals > 10:
                raise ValueError("Number of rebuttals must be between 1 and 10")
            
            if language and len(language) > 50:
                raise ValueError("Language specification too long")
            
            # Generate rebuttals prompt
            prompt = self._build_rebuttals_prompt(
                motion,
                defending_side,
                attacking_side,
                opponent_arguments,
                num_rebuttals,
                language
            )
            
            # Call LLM
            response = await self._call_llm(prompt)
            
            # Parse response
            rebuttals = self._parse_rebuttals_response(response)
            
            duration_ms = int((time.time() - start_time) * 1000)
            self._log_end(f"rebuttal generation for {defending_side.side}", duration_ms)
            
            return {
                "side": defending_side.side,
                "rebuttals": rebuttals,
                "count": len(rebuttals)
            }
        
        except Exception as e:
            self._log_error(f"rebuttal generation for {defending_side.side}", str(e))
            raise
    
    def _build_rebuttals_prompt(
        self,
        motion: str,
        defending_side: SideCase,
        attacking_side: SideCase,
        opponent_arguments: List[Argument],
        num_rebuttals: int,
        language: str = "English"
    ) -> str:
        """Build rebuttals prompt for LLM."""
        defending_stance = "supporting" if defending_side.side == "Proposition" else "opposing"
        
        # Format opponent arguments
        opponent_args_text = ""
        for i, arg in enumerate(opponent_arguments[:num_rebuttals], 1):
            opponent_args_text += f"\nArgument {i}: {arg.contention}\n"
            opponent_args_text += f"Reasoning: {arg.reasoning}\n"
            if arg.evidence:
                opponent_args_text += f"Evidence: {', '.join(arg.evidence)}\n"
        
        prompt = f"""You are a debate expert preparing rebuttals for a {defending_side.side} team in World Schools Debate.

Motion: {motion}

Our Team ({defending_side.side}): {', '.join(defending_side.team_members)}
Opposing Team ({attacking_side.side}): {', '.join(attacking_side.team_members)}

The {attacking_side.side} team has made the following arguments:
{opponent_args_text}

Your task is to generate pointed, logical rebuttals to these {len(opponent_arguments)} arguments.

Each rebuttal should:
1. Directly address the opponent's contention
2. Identify logical flaws or weaknesses
3. Provide a counter-argument
4. Explain impact

Provide the rebuttals in exactly this JSON format - must be valid JSON:
{{
    "rebuttals": [
        {{
            "targets_argument": "The opponent's contention being rebutted",
            "main_rebuttal": "The core rebuttal point",
            "logical_flaw": "What's wrong with their logic",
            "counter_point": "Our counter-argument",
            "impact": "Why this rebuttal matters"
        }}
    ]
}}

Generate {min(num_rebuttals, len(opponent_arguments))} strong rebuttals that effectively counter the {attacking_side.side} arguments and support our {defending_side.side} position."""
        
        language_instruction = (f"\n\nIMPORTANT: You MUST write your entire response "
                                 f"\u2014 all rebuttals, logical flaws, counter-points, and impact explanations "
                                 f"\u2014 in {language}. Do not use any other language.")
        
        return prompt + language_instruction
    
    def _parse_rebuttals_response(self, response: str) -> List[Rebuttal]:
        """Parse LLM response to extract rebuttals."""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                
                rebuttals = []
                for rebuttal_data in data.get("rebuttals", []):
                    rebuttal = Rebuttal(
                        targets_argument=rebuttal_data.get("targets_argument", ""),
                        main_rebuttal=rebuttal_data.get("main_rebuttal", ""),
                        logical_flaw=rebuttal_data.get("logical_flaw", ""),
                        counter_point=rebuttal_data.get("counter_point", ""),
                        impact=rebuttal_data.get("impact", "")
                    )
                    rebuttals.append(rebuttal)
                
                return rebuttals
            
            return []
        except Exception as e:
            self.logger.warning(f"Failed to parse rebuttals response: {str(e)}")
            return []
