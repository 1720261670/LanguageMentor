import unittest

# 导入所有测试模块
from test_agent_base import TestAgentBase
from test_conversation_agent import TestConversationAgent
from test_scenario_agent import TestScenarioAgent
from test_vocab_agent import TestVocabAgent

def create_test_suite():
    """
    创建测试套件并添加所有测试用例。
    """
    # 创建一个测试加载器
    loader = unittest.TestLoader()

    # 添加所有测试类到测试套件
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestAgentBase))
    suite.addTests(loader.loadTestsFromTestCase(TestConversationAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestScenarioAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestVocabAgent))

    return suite

if __name__ == "__main__":
    # 创建测试套件
    test_suite = create_test_suite()

    # 运行测试套件
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # 输出测试结果
    if result.wasSuccessful():
        print("所有测试通过！")
    else:
        print("部分测试失败。")