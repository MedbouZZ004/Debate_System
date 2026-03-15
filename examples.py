"""
Example scenarios for WSD Debate System.

Run individual examples to test different debate topics.
"""

import asyncio
from debate_manager import DebateSession
from utils import DebateExporter


async def example_ai_regulation():
    """Example 1: AI Regulation Debate."""
    print("\n" + "="*60)
    print("EXAMPLE 1: AI Regulation Debate")
    print("="*60)
    
    session = DebateSession()
    
    motion = "This house believes artificial intelligence should be regulated by governments"
    
    state = await session.start_debate(
        motion=motion,
        proposition_members=["Alice", "Bob", "Charlie"],
        opposition_members=["David", "Eve", "Frank"],
        num_arguments=3,
        num_rebuttals=3
    )
    
    summary = session.get_summary()
    print(f"Motion: {motion}")
    print(f"Execution time: {summary['execution_time']:.2f}s")
    print(f"Predicted winner: {summary['predicted_winner']}")
    
    await session.save_log("examples/example1_ai_regulation.json")
    await session.save_log("examples/example1_ai_regulation.md")


async def example_climate_action():
    """Example 2: Climate Action Debate."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Climate Action Debate")
    print("="*60)
    
    session = DebateSession()
    
    motion = "This house believes developed nations should bear the primary responsibility for combating climate change"
    
    state = await session.start_debate(
        motion=motion,
        proposition_members=["Emma", "Oliver", "Sophie"],
        opposition_members=["James", "Isabella", "Lucas"],
        num_arguments=3,
        num_rebuttals=3
    )
    
    summary = session.get_summary()
    print(f"Motion: {motion}")
    print(f"Execution time: {summary['execution_time']:.2f}s")
    print(f"Predicted winner: {summary['predicted_winner']}")
    
    await session.save_log("examples/example2_climate_action.json")
    await session.save_log("examples/example2_climate_action.md")


async def example_social_media():
    """Example 3: Social Media Regulation."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Social Media Regulation Debate")
    print("="*60)
    
    session = DebateSession()
    
    motion = "This house believes social media platforms should be made liable for user-generated content"
    
    state = await session.start_debate(
        motion=motion,
        proposition_members=["Sophia", "Liam", "Ava"],
        opposition_members=["Noah", "Olivia", "Ethan"],
        num_arguments=3,
        num_rebuttals=3
    )
    
    summary = session.get_summary()
    print(f"Motion: {motion}")
    print(f"Execution time: {summary['execution_time']:.2f}s")
    print(f"Predicted winner: {summary['predicted_winner']}")
    
    await session.save_log("examples/example3_social_media.json")
    await session.save_log("examples/example3_social_media.md")


async def example_universal_basic_income():
    """Example 4: Universal Basic Income."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Universal Basic Income Debate")
    print("="*60)
    
    session = DebateSession()
    
    motion = "This house believes universal basic income would improve societal wellbeing"
    
    state = await session.start_debate(
        motion=motion,
        proposition_members=["Mia", "Benjamin", "Charlotte"],
        opposition_members=["Logan", "Amelia", "Mason"],
        num_arguments=3,
        num_rebuttals=3
    )
    
    summary = session.get_summary()
    print(f"Motion: {motion}")
    print(f"Execution time: {summary['execution_time']:.2f}s")
    print(f"Predicted winner: {summary['predicted_winner']}")
    
    await session.save_log("examples/example4_ubi.json")
    await session.save_log("examples/example4_ubi.md")


async def example_space_exploration():
    """Example 5: Space Exploration Funding."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Space Exploration Funding Debate")
    print("="*60)
    
    session = DebateSession()
    
    motion = "This house believes governments should prioritize funding space exploration over terrestrial problems"
    
    state = await session.start_debate(
        motion=motion,
        proposition_members=["Harper", "Jack", "Ella"],
        opposition_members=["William", "Scarlett", "Alexander"],
        num_arguments=3,
        num_rebuttals=3
    )
    
    summary = session.get_summary()
    print(f"Motion: {motion}")
    print(f"Execution time: {summary['execution_time']:.2f}s")
    print(f"Predicted winner: {summary['predicted_winner']}")
    
    await session.save_log("examples/example5_space_exploration.json")
    await session.save_log("examples/example5_space_exploration.md")


async def run_all_examples():
    """Run all examples."""
    print("\n🎤 WSD Debate System - Example Scenarios")
    print("=========================================\n")
    
    try:
        # You can run individual examples or all
        await example_ai_regulation()
        
        # Uncomment to run more examples:
        # await example_climate_action()
        # await example_social_media()
        # await example_universal_basic_income()
        # await example_space_exploration()
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
    
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(run_all_examples())
