import unittest
from unittest.mock import patch
from src.agents.conversation_agent import ConversationAgent

class TestConversationAgent(unittest.TestCase):

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    def test_initialization(self, mock_file):
        # 测试 ConversationAgent 的初始化
        session_id = "test_session"
        agent = ConversationAgent(session_id=session_id)

        # 检查是否正确设置了属性
        self.assertEqual(agent.name, "conversation")
        self.assertEqual(agent.prompt_file, "prompts/conversation_prompt.txt")
        self.assertEqual(agent.session_id, session_id)

        # 检查是否调用了父类的初始化方法
        self.assertEqual(agent.prompt, "Test prompt content")
        mock_file.assert_called_once_with("prompts/conversation_prompt.txt", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    def test_default_session_id(self, mock_file):
        # 测试当 session_id 为 None 时，是否使用默认的 session_id
        agent = ConversationAgent()

        # 检查 session_id 是否设置为默认值（即 name）
        self.assertEqual(agent.session_id, "conversation")

if __name__ == "__main__":
    unittest.main()