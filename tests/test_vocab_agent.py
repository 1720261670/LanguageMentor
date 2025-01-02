import unittest
from unittest.mock import patch, MagicMock
from src.agents.vocab_agent import VocabAgent

class TestVocabAgent(unittest.TestCase):

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    def test_initialization(self, mock_file):
        # 测试 VocabAgent 的初始化
        session_id = "test_session"
        agent = VocabAgent(session_id)

        # 检查是否正确设置了属性
        self.assertEqual(agent.name, "vocab_study")
        self.assertEqual(agent.prompt_file, "prompts/vocab_study_prompt.txt")
        self.assertEqual(agent.session_id, session_id)

        # 检查是否调用了父类的初始化方法
        self.assertEqual(agent.prompt, "Test prompt content")
        mock_file.assert_called_once_with("prompts/vocab_study_prompt.txt", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    def test_restart_session(self, mock_file):
        # 测试 restart_session 方法
        session_id = "test_session"
        agent = VocabAgent(session_id)

        # 模拟 get_session_history 返回一个会话历史对象
        mock_history = MagicMock()
        with patch("src.agents.vocab_agent.get_session_history", return_value=mock_history):
            result = agent.restart_session(session_id)

            # 检查是否调用了 clear 方法
            mock_history.clear.assert_called_once()
            # 检查返回的结果是否正确
            self.assertEqual(result, mock_history)

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    def test_restart_session_default_session_id(self, mock_file):
        # 测试 restart_session 方法，当 session_id 为 None 时
        agent = VocabAgent()

        # 模拟 get_session_history 返回一个会话历史对象
        mock_history = MagicMock()
        with patch("src.agents.vocab_agent.get_session_history", return_value=mock_history):
            result = agent.restart_session()

            # 检查是否使用了默认的 session_id
            mock_history.clear.assert_called_once()
            # 检查返回的结果是否正确
            self.assertEqual(result, mock_history)

if __name__ == "__main__":
    unittest.main()