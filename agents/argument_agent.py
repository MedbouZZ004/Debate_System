"""
Argument Construction Agent for WSD Debate System.

Builds main arguments for debate cases with sophisticated case studies and position correlation.
"""

import time
import json
from typing import Dict, Any, List
from agents.base_agent import DebateAgent
from models import SideCase, Argument, CaseStudy


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
        research_data: Dict[str, Any] = None,
        language: str = "English"
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
                motion, side, num_arguments, research_data, language
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
        research_data: Dict[str, Any] = None,
        language: str = "English"
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
        
        language_instruction = f"\n\nIMPORTANT: You MUST write your entire response — all contentions, reasoning, evidence, case studies, and position correlation — in {language}. Do not use any other language."
        
        prompt = f"""You are a highly sophisticated debate expert constructing compelling, well-developed main arguments for a {side.side} team in World Schools Debate.

Motion: {motion}
Team Members: {', '.join(side.team_members)}
{research_context}

Your task is to construct {num_arguments} distinct, exceptionally compelling arguments {side_stance} this motion.

CRITICAL REQUIREMENTS FOR EACH ARGUMENT:

1. **Contention**: A clear, decisive main claim
2. **Reasoning**: Comprehensive logical explanation backed with scholarly reasoning
3. **Evidence**: 3-5 credible pieces of evidence from real-world scenarios
4. **Impact**: Explain why this argument fundamentally matters to the debate
5. **Case Studies**: Include 2-3 real-world case studies that validate the argument with specific outcomes
6. **Position Correlation**: Show how this argument interconnects with the overall {side.side} position and strengthens the team's case

CASE STUDY REQUIREMENTS:
- Each case study must have: title, background context, methodology/approach, concrete outcomes, and impact on the argument
- Use real historical examples, policy implementations, scientific studies, or documented organizational cases
- Focus on verifiable, specific results and measurable outcomes
- Connect outcomes directly to why the argument matters in this debate

POSITION CORRELATION REQUIREMENTS:
- Explain explicitly how this argument supports the {side.side}'s overall strategic position
- Show logical progression: how this argument connects to and strengthens other arguments on your side
- Demonstrate how accepting this argument makes the {side.side} position harder to defeat

Provide the arguments in exactly this JSON format - MUST be valid JSON:
{{
    "arguments": [
        {{
            "contention": "Clear main claim",
            "reasoning": "Comprehensive logical explanation with scholarly depth",
            "evidence": ["Evidence 1", "Evidence 2", "Evidence 3", "Evidence 4"],
            "impact": "Why this matters critically in the debate",
            "case_studies": [
                {{
                    "title": "Real-world case title",
                    "background": "Context and circumstances of the case",
                    "methodology": "How it was implemented or approached",
                    "outcomes": "Specific, measurable results achieved",
                    "impact": "How this validates the argument"
                }},
                {{
                    "title": "Second case study",
                    "background": "Context",
                    "methodology": "Implementation approach",
                    "outcomes": "Results",
                    "impact": "Relevance to argument"
                }}
            ],
            "position_correlation": "How this argument strengthens the {side.side} position and connects to the wider case"
        }}
    ]
}}

Construct {num_arguments} extraordinarily strong arguments supporting the {side.side} position. 
Each argument must be development-grade, backed by real case studies, and show clear correlation with the team's strategic position.
Focus on arguments that are hardest to rebut and most impactful in adjudication.{language_instruction}"""
        
        return prompt
    
    def _parse_arguments_response(self, response: str, num_arguments: int) -> List[Argument]:
        """Parse LLM response to extract arguments with case studies and position correlation."""
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
                        # Parse case studies
                        case_studies = []
                        for cs_data in arg_data.get("case_studies", []):
                            try:
                                case_study = CaseStudy(
                                    title=cs_data.get("title", ""),
                                    background=cs_data.get("background", ""),
                                    methodology=cs_data.get("methodology", ""),
                                    outcomes=cs_data.get("outcomes", ""),
                                    impact=cs_data.get("impact", "")
                                )
                                case_studies.append(case_study)
                            except:
                                continue
                        
                        # Create argument with new fields
                        arg = Argument(
                            contention=arg_data.get("contention", ""),
                            reasoning=arg_data.get("reasoning", ""),
                            evidence=arg_data.get("evidence", []),
                            impact=arg_data.get("impact", ""),
                            case_studies=case_studies,
                            position_correlation=arg_data.get("position_correlation", "")
                        )
                        arguments.append(arg)
                    except Exception as e:
                        continue
                
                return arguments
            
            return []
        except Exception as e:
            return []
