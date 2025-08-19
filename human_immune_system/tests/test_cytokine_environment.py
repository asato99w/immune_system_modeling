import unittest
from ..model.cytokine_environment import CytokineEnvironment


class MockCell:
    """テスト用のモック細胞"""
    def __init__(self):
        self.received_notifications = []
    
    def on_cytokine_changed(self, cytokine_name, level):
        self.received_notifications.append((cytokine_name, level))


class TestCytokineEnvironment(unittest.TestCase):
    """サイトカイン環境の最小限のテスト"""
    
    def test_initial_state(self):
        """初期状態は空の環境"""
        env = CytokineEnvironment()
        self.assertEqual(env.get_level("IL-12"), 0.0)
    
    def test_add_cytokine(self):
        """サイトカインを追加できる"""
        env = CytokineEnvironment()
        env.add_cytokine("IL-12", 10.0)
        self.assertEqual(env.get_level("IL-12"), 10.0)
    
    def test_cell_receives_notification(self):
        """登録された細胞が通知を受け取る"""
        env = CytokineEnvironment()
        cell = MockCell()
        
        env.register_cell(cell)
        env.add_cytokine("IL-12", 5.0)
        
        self.assertEqual(len(cell.received_notifications), 1)
        self.assertEqual(cell.received_notifications[0], ("IL-12", 5.0))


if __name__ == '__main__':
    unittest.main()