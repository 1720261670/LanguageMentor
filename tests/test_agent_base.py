import unittest
from unittest.mock import patch, mock_open
from src.agents.agent_base import AgentBase

class TestAgentBase(unittest.TestCase):

    def setUp(self):
        self.name = "TestAgent"
        self.prompt_file = "test_prompt.txt"
        self.intro_file = "test_intro.json"
        self.session_id = "test_session"

    @patch("builtins.open", new_callable=mock_open, read_data="Test prompt content")
    def test_load_prompt(self, mock_file):
        agent = AgentBase(self.name, self.prompt_file)
        self.assertEqual(agent.prompt, "Test prompt content")
        mock_file.assert_called_once_with(self.prompt_file, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"role": "system", "content": "Test intro"}]')
    def test_load_intro(self, mock_file):
        # 测试 load_intro 方法
        agent = AgentBase(self.name, self.prompt_file, self.intro_file)
        self.assertEqual(agent.intro_messages, [{"role": "system", "content": "Test intro"}])

        # 检查 open 是否被调用了两次（一次用于 prompt_file，一次用于 intro_file）
        self.assertEqual(mock_file.call_count, 2)
        mock_file.assert_any_call(self.prompt_file, "r", encoding="utf-8")
        mock_file.assert_any_call(self.intro_file, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="Test prompt content")
    @patch("langchain_openai.ChatOpenAI")
    def test_create_chatbot(self, mock_chat_openai, mock_file):
        agent = AgentBase(self.name, self.prompt_file)
        self.assertIsNotNone(agent.chatbot)
        self.assertIsNotNone(agent.chatbot_with_history)

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Test prompt content")
    @patch("langchain_openai.ChatOpenAI")
    def test_chat_with_history(self, mock_chat_openai, mock_file):
        # 测试 chat_with_history 方法
        agent = AgentBase(self.name, self.prompt_file)
        user_input = "Hello, how are you?"
        session_id = "test_session"

        # 模拟 OpenAI 返回的内容
        expected_response = "Hello! I'm just a program, so I don't have feelings, but I'm here and ready to help you. How can I assist you today?"
        mock_chat_openai.return_value.invoke.return_value.content = expected_response

        # 调用 chat_with_history 方法
        response = agent.chat_with_history(user_input, session_id)
        print(response)
        # 检查返回的内容是否与预期一致
        self.assertEqual(response, expected_response)

    @patch("builtins.open", new_callable=mock_open, read_data="Test prompt content")
    def test_file_not_found_error(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            AgentBase(self.name, self.prompt_file)

    @patch("builtins.open", new_callable=mock_open, read_data="Invalid JSON")
    def test_json_decode_error(self, mock_file):
        with self.assertRaises(ValueError):
            AgentBase(self.name, self.prompt_file, self.intro_file)

if __name__ == "__main__":
    unittest.main()