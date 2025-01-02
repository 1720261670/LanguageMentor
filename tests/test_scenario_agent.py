import unittest
from unittest.mock import patch, MagicMock
from src.agents.scenario_agent import ScenarioAgent
from langchain_core.messages import AIMessage

class TestScenarioAgent(unittest.TestCase):

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    @patch("json.load", return_value=["Intro message 1", "Intro message 2"])
    def test_initialization(self, mock_json_load, mock_file):
        # 测试 ScenarioAgent 的初始化
        scenario_name = "test_scenario"
        session_id = "test_session"
        agent = ScenarioAgent(scenario_name, session_id)

        # 检查是否正确设置了属性
        self.assertEqual(agent.name, scenario_name)
        self.assertEqual(agent.prompt_file, f"prompts/{scenario_name}_prompt.txt")
        self.assertEqual(agent.intro_file, f"content/intro/{scenario_name}.json")
        self.assertEqual(agent.session_id, session_id)

        # 检查是否调用了父类的初始化方法
        self.assertEqual(agent.prompt, "Test prompt content")
        self.assertEqual(agent.intro_messages, ["Intro message 1", "Intro message 2"])

        # 检查 open 是否被调用了两次（一次用于 prompt_file，一次用于 intro_file）
        self.assertEqual(mock_file.call_count, 2)
        mock_file.assert_any_call(f"prompts/{scenario_name}_prompt.txt", "r", encoding="utf-8")
        mock_file.assert_any_call(f"content/intro/{scenario_name}.json", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    @patch("json.load", return_value=["Intro message 1", "Intro message 2"])
    def test_start_new_session_with_empty_history(self, mock_json_load, mock_file):
        # 测试 start_new_session 方法，当会话历史为空时
        scenario_name = "test_scenario"
        session_id = "test_session"
        agent = ScenarioAgent(scenario_name, session_id)

        # 模拟 get_session_history 返回一个空的会话历史
        mock_history = MagicMock()
        mock_history.messages = []
        with patch("src.agents.scenario_agent.get_session_history", return_value=mock_history):
            initial_message = agent.start_new_session(session_id)

            # 检查是否随机选择了一条初始消息并添加到历史记录中
            self.assertIn(initial_message, ["Intro message 1", "Intro message 2"])
            mock_history.add_message.assert_called_once_with(AIMessage(content=initial_message))

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    @patch("json.load", return_value=["Intro message 1", "Intro message 2"])
    def test_start_new_session_with_existing_history(self, mock_json_load, mock_file):
        # 测试 start_new_session 方法，当会话历史不为空时
        scenario_name = "test_scenario"
        session_id = "test_session"
        agent = ScenarioAgent(scenario_name, session_id)

        # 模拟 get_session_history 返回一个非空的会话历史
        mock_history = MagicMock()
        mock_history.messages = [AIMessage(content="Existing message")]
        with patch("src.agents.scenario_agent.get_session_history", return_value=mock_history):
            initial_message = agent.start_new_session(session_id)

            # 检查是否返回了历史记录中的最后一条消息
            self.assertEqual(initial_message, "Existing message")
            mock_history.add_message.assert_not_called()

if __name__ == "__main__":
    unittest.main()