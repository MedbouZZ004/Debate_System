"""
Main entry point for WSD Debate System.

Run this to start a debate.
"""

import asyncio
from debate_manager import DebateSession
from utils import DebateExporter
from logger import DebateLogger


async def main():
    """Main function."""
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
        await session.save_log("debate_result.json")
        await session.save_log("debate_result.md")
        
        print("\n📄 Results saved to:")
        print("  - debate_result.json")
        print("  - debate_result.md")
        
        logger.info("Debate system execution completed successfully")
    
    except KeyboardInterrupt:
        print("\n⚠️ Debate interrupted by user")
        logger.info("Debate interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
