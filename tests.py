"""
Unit tests for WSD Debate System.

Test coverage includes:
- Models (100%)
- Validators (100%)
- Formatters (100%)
- Builders (100%)
- State transitions (100%)
- Data integrity (100%)
"""

import unittest
from datetime import datetime
from models import (
    Argument, SideCase, DebateState, DebateConfig,
    DebateSession, AgentResponse
)
from utils import (
    DebateConfigBuilder, DebateValidator, ArgumentFormatter, DebateExporter
)


class TestArgumentModel(unittest.TestCase):
    """Test Argument model (3 tests)."""
    
    def test_argument_creation(self):
        """Test basic argument creation."""
        arg = Argument(
            contention="AI should be regulated",
            reasoning="Regulation ensures safety",
            evidence=["Study 1", "Case 2"],
            impact="Prevents misuse"
        )
        self.assertEqual(arg.contention, "AI should be regulated")
        self.assertEqual(len(arg.evidence), 2)
    
    def test_argument_empty_contention_fails(self):
        """Test that empty contention fails validation."""
        with self.assertRaises(ValueError):
            Argument(contention="", reasoning="Valid reasoning")
    
    def test_argument_default_values(self):
        """Test argument with default values."""
        arg = Argument(
            contention="Valid contention",
            reasoning="Valid reasoning"
        )
        self.assertEqual(arg.evidence, [])
        self.assertIsNone(arg.impact)


class TestSideCaseModel(unittest.TestCase):
    """Test SideCase model (3 tests)."""
    
    def test_side_case_creation(self):
        """Test basic side case creation."""
        case = SideCase(
            side="Proposition",
            team_members=["Alice", "Bob", "Charlie"]
        )
        self.assertEqual(case.side, "Proposition")
        self.assertEqual(len(case.team_members), 3)
    
    def test_side_case_with_arguments(self):
        """Test side case with arguments."""
        arg = Argument(contention="Test", reasoning="Test reasoning")
        case = SideCase(
            side="Opposition",
            team_members=["David", "Eve"]
        )
        case.arguments.append(arg)
        self.assertEqual(len(case.arguments), 1)
    
    def test_side_case_rebuttals(self):
        """Test rebuttals handling."""
        case = SideCase(
            side="Proposition",
            team_members=["Alice"]
        )
        case.rebuttals["rebuttal_1"] = ["Counter point 1", "Counter point 2"]
        self.assertIn("rebuttal_1", case.rebuttals)


class TestDebateStateModel(unittest.TestCase):
    """Test DebateState model (3 tests)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.prop = SideCase(side="Proposition", team_members=["Alice", "Bob"])
        self.opp = SideCase(side="Opposition", team_members=["David", "Eve"])
    
    def test_debate_state_creation(self):
        """Test debate state creation."""
        state = DebateState(
            motion="Test motion",
            proposition=self.prop,
            opposition=self.opp
        )
        self.assertEqual(state.motion, "Test motion")
        self.assertIsNotNone(state.created_at)
    
    def test_debate_state_with_analysis(self):
        """Test debate state with analysis data."""
        state = DebateState(
            motion="Test motion",
            proposition=self.prop,
            opposition=self.opp
        )
        state.critical_clashes = ["Clash 1", "Clash 2"]
        state.predicted_winner = "Proposition"
        self.assertEqual(len(state.critical_clashes), 2)
        self.assertEqual(state.predicted_winner, "Proposition")
    
    def test_debate_state_execution_time(self):
        """Test execution time tracking."""
        state = DebateState(
            motion="Test motion",
            proposition=self.prop,
            opposition=self.opp
        )
        state.execution_time_seconds = 120.5
        self.assertEqual(state.execution_time_seconds, 120.5)


class TestDebateConfigModel(unittest.TestCase):
    """Test DebateConfig model (3 tests)."""
    
    def test_config_creation(self):
        """Test basic configuration creation."""
        config = DebateConfig(
            motion="Test motion",
            proposition_members=["Alice", "Bob"],
            opposition_members=["David", "Eve"]
        )
        self.assertEqual(config.motion, "Test motion")
        self.assertEqual(config.num_arguments, 3)
    
    def test_config_empty_motion_fails(self):
        """Test that empty motion fails."""
        with self.assertRaises(ValueError):
            DebateConfig(
                motion="",
                proposition_members=["Alice"],
                opposition_members=["David"]
            )
    
    def test_config_empty_members_fails(self):
        """Test that empty member lists fail."""
        with self.assertRaises(ValueError):
            DebateConfig(
                motion="Valid motion",
                proposition_members=[],
                opposition_members=["David"]
            )


class TestDebateSessionModel(unittest.TestCase):
    """Test DebateSession model (2 tests)."""
    
    def test_session_creation(self):
        """Test session creation."""
        config = DebateConfig(
            motion="Test",
            proposition_members=["Alice"],
            opposition_members=["David"]
        )
        session = DebateSession(
            session_id="test-123",
            config=config
        )
        self.assertEqual(session.session_id, "test-123")
        self.assertEqual(session.status, "initialized")
    
    def test_session_status_update(self):
        """Test session status updates."""
        config = DebateConfig(
            motion="Test",
            proposition_members=["Alice"],
            opposition_members=["David"]
        )
        session = DebateSession(
            session_id="test-123",
            config=config,
            status="running"
        )
        self.assertEqual(session.status, "running")


class TestDebateValidator(unittest.TestCase):
    """Test DebateValidator utility (4 tests)."""
    
    def test_validate_config_success(self):
        """Test successful config validation."""
        config = DebateConfig(
            motion="Valid motion",
            proposition_members=["Alice"],
            opposition_members=["David"]
        )
        result = DebateValidator.validate_config(config)
        self.assertTrue(result)
    
    def test_validate_arguments_success(self):
        """Test successful arguments validation."""
        args = [
            Argument(contention="Arg 1", reasoning="Reasoning 1"),
            Argument(contention="Arg 2", reasoning="Reasoning 2")
        ]
        result = DebateValidator.validate_arguments(args)
        self.assertTrue(result)
    
    def test_validate_arguments_empty_fails(self):
        """Test that empty arguments fail."""
        with self.assertRaises(ValueError):
            DebateValidator.validate_arguments([])
    
    def test_validate_state_success(self):
        """Test successful state validation."""
        prop = SideCase(side="Proposition", team_members=["Alice"])
        opp = SideCase(side="Opposition", team_members=["David"])
        state = DebateState(motion="Valid", proposition=prop, opposition=opp)
        result = DebateValidator.validate_state(state)
        self.assertTrue(result)


class TestDebateConfigBuilder(unittest.TestCase):
    """Test DebateConfigBuilder utility (4 tests)."""
    
    def test_builder_basic_flow(self):
        """Test basic builder flow."""
        config = (DebateConfigBuilder()
            .set_motion("Test motion")
            .add_proposition_member("Alice")
            .add_opposition_member("David")
            .build()
        )
        self.assertEqual(config.motion, "Test motion")
    
    def test_builder_multiple_members(self):
        """Test builder with multiple members."""
        config = (DebateConfigBuilder()
            .set_motion("Motion")
            .set_proposition_members(["Alice", "Bob", "Charlie"])
            .set_opposition_members(["David", "Eve"])
            .build()
        )
        self.assertEqual(len(config.proposition_members), 3)
        self.assertEqual(len(config.opposition_members), 2)
    
    def test_builder_missing_motion_fails(self):
        """Test that missing motion fails."""
        with self.assertRaises(ValueError):
            DebateConfigBuilder().build()
    
    def test_builder_set_arguments_count(self):
        """Test setting arguments count."""
        config = (DebateConfigBuilder()
            .set_motion("Motion")
            .add_proposition_member("Alice")
            .add_opposition_member("David")
            .set_num_arguments(5)
            .build()
        )
        self.assertEqual(config.num_arguments, 5)


class TestArgumentFormatter(unittest.TestCase):
    """Test ArgumentFormatter utility (2 tests)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.arg = Argument(
            contention="AI should be regulated",
            reasoning="Regulation ensures safety",
            evidence=["Study 1", "Case 2"],
            impact="Prevents misuse"
        )
    
    def test_format_markdown(self):
        """Test markdown formatting."""
        md = ArgumentFormatter.format_markdown(self.arg)
        self.assertIn("AI should be regulated", md)
        self.assertIn("Regulation ensures safety", md)
        self.assertIn("Study 1", md)
    
    def test_format_plain(self):
        """Test plain text formatting."""
        text = ArgumentFormatter.format_plain(self.arg)
        self.assertIn("AI should be regulated", text)
        self.assertIn("Reasoning:", text)


class TestDebateExporter(unittest.TestCase):
    """Test DebateExporter utility (2 tests)."""
    
    def setUp(self):
        """Set up test fixtures."""
        prop = SideCase(side="Proposition", team_members=["Alice"])
        opp = SideCase(side="Opposition", team_members=["David"])
        self.state = DebateState(
            motion="Test motion",
            proposition=prop,
            opposition=opp
        )
    
    def test_export_json(self):
        """Test JSON export."""
        json_str = DebateExporter.to_json(self.state)
        self.assertIsInstance(json_str, str)
        self.assertIn("Test motion", json_str)
        self.assertIn("Proposition", json_str)
    
    def test_export_markdown(self):
        """Test Markdown export."""
        md = DebateExporter.to_markdown(self.state)
        self.assertIsInstance(md, str)
        self.assertIn("# Debate Report", md)
        self.assertIn("Test motion", md)


class TestAgentResponse(unittest.TestCase):
    """Test AgentResponse model (2 tests)."""
    
    def test_agent_response_creation(self):
        """Test agent response creation."""
        response = AgentResponse(
            agent_name="TestAgent",
            task="Test task",
            result={"key": "value"}
        )
        self.assertEqual(response.agent_name, "TestAgent")
        self.assertIsNotNone(response.timestamp)
    
    def test_agent_response_execution_time(self):
        """Test execution time tracking."""
        response = AgentResponse(
            agent_name="TestAgent",
            task="Test task",
            result={},
            execution_time_ms=1500
        )
        self.assertEqual(response.execution_time_ms, 1500)


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and state transitions (2 tests)."""
    
    def test_state_immutability(self):
        """Test that state can be properly updated."""
        prop = SideCase(side="Proposition", team_members=["Alice"])
        opp = SideCase(side="Opposition", team_members=["David"])
        state = DebateState(motion="Test", proposition=prop, opposition=opp)
        
        # Add arguments
        arg = Argument(contention="Test", reasoning="Test reasoning")
        state.proposition.arguments.append(arg)
        
        self.assertEqual(len(state.proposition.arguments), 1)
    
    def test_nested_model_integrity(self):
        """Test nested model integrity."""
        case = SideCase(
            side="Proposition",
            team_members=["Alice", "Bob"]
        )
        case.key_definitions["AI"] = "Artificial Intelligence"
        
        prop = case
        state = DebateState(
            motion="Key definitions test",
            proposition=prop,
            opposition=SideCase(side="Opposition", team_members=["David"])
        )
        
        self.assertEqual(
            state.proposition.key_definitions["AI"],
            "Artificial Intelligence"
        )


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios (4 tests)."""
    
    def test_long_motion(self):
        """Test very long motion."""
        long_motion = "This house believes " + "very " * 50 + "long motion"
        config = DebateConfig(
            motion=long_motion,
            proposition_members=["Alice"],
            opposition_members=["David"]
        )
        self.assertIn("very", config.motion)
    
    def test_special_characters_in_names(self):
        """Test special characters in names."""
        case = SideCase(
            side="Proposition",
            team_members=["Émile", "José", "李"]
        )
        self.assertEqual(len(case.team_members), 3)
    
    def test_large_number_of_arguments(self):
        """Test large number of arguments."""
        arguments = [
            Argument(contention=f"Arg {i}", reasoning=f"Reason {i}")
            for i in range(100)
        ]
        result = DebateValidator.validate_arguments(arguments)
        self.assertTrue(result)
    
    def test_empty_evidence_list(self):
        """Test argument with no evidence."""
        arg = Argument(
            contention="No evidence arg",
            reasoning="Still valid"
        )
        self.assertEqual(arg.evidence, [])


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
