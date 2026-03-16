"""
Main entry point for WSD Debate System.

Run this to start a debate.
"""

import asyncio
import sys
import traceback
from debate_manager import DebateSession
from utils import DebateExporter
from logger import DebateLogger
from pydantic import ValidationError


async def main():
    """Main function with enhanced error handling."""
    logger = DebateLogger
    
    try:
        logger.info("Starting WSD Debate System")
        
        # Create session
        session = DebateSession()
        
        # Define debate parameters
        motion = "This house believes artificial intelligence should be regulated by governments"
        proposition_members = ["Alice", "Bob", "Charlie"]
        opposition_members = ["David", "Eve", "Frank"]
        
        logger.info(f"Motion: {motion}")
        logger.info(f"Proposition: {', '.join(proposition_members)}")
        logger.info(f"Opposition: {', '.join(opposition_members)}")
        
        # Validate parameters before starting
        if len(motion.strip()) < 10:
            raise ValueError("Motion must be at least 10 characters long")
        
        if not proposition_members or len(proposition_members) == 0:
            raise ValueError("Proposition team must have at least one member")
        
        if not opposition_members or len(opposition_members) == 0:
            raise ValueError("Opposition team must have at least one member")
        
        # Start debate
        print("\n🎤 Starting debate...")
        state = await session.start_debate(
            motion=motion,
            proposition_members=proposition_members,
            opposition_members=opposition_members,
            num_arguments=3,
            num_rebuttals=3
        )
        
        # Get summary
        summary = session.get_summary()
        
        print("\n✅ Debate Completed!")
        print(f"Execution time: {summary['execution_time']:.2f} seconds")
        print(f"Proposition arguments: {summary['proposition_arguments']}")
        print(f"Opposition arguments: {summary['opposition_arguments']}")
        print(f"Predicted winner: {summary['predicted_winner']}")
        
        # Save results
        try:
            await session.save_log("debate_result.json")
            await session.save_log("debate_result.md")
            
            print("\n📄 Results saved to:")
            print("  - debate_result.json")
            print("  - debate_result.md")
        except Exception as e:
            logger.warning(f"Could not save all result files: {str(e)}")
            print(f"⚠️ Warning: Could not save all results: {str(e)}")
        
        logger.info("Debate system execution completed successfully")
    
    except ValidationError as e:
        print(f"\n❌ Validation Error: Invalid input parameters")
        print(f"Details: {e}")
        logger.error(f"Validation error: {str(e)}", exc_info=True)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Debate interrupted by user")
        logger.info("Debate interrupted by user")
        sys.exit(0)
    except ValueError as e:
        print(f"\n❌ Value Error: {str(e)}")
        logger.error(f"Value error: {str(e)}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
