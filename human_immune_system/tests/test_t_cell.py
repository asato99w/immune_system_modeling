import unittest
from ..model.t_cell import TCell


class TestTCellMinimal(unittest.TestCase):
    """T細胞の最小限機能テスト"""
    
    def test_initial_state(self):
        """初期状態は未活性"""
        t_cell = TCell()
        self.assertFalse(t_cell.is_activated())
    
    def test_activation(self):
        """活性化可能"""
        t_cell = TCell()
        t_cell.activate()
        self.assertTrue(t_cell.is_activated())
    
    def test_cannot_reactivate(self):
        """すでに活性化されたT細胞は再活性化しない"""
        t_cell = TCell()
        t_cell.activate()
        self.assertTrue(t_cell.is_activated())
        
        # 2回目の活性化は無視される
        t_cell.activate()
        self.assertTrue(t_cell.is_activated())


if __name__ == '__main__':
    unittest.main()