class CytokineEnvironment:
    """
    サイトカイン環境
    複数の免疫細胞が共有する細胞外環境を表現
    """
    
    def __init__(self):
        self._levels = {}
        self._observers = []
    
    def get_level(self, cytokine_name: str) -> float:
        """特定サイトカインの現在レベルを取得"""
        return self._levels.get(cytokine_name, 0.0)
    
    def add_cytokine(self, cytokine_name: str, amount: float):
        """サイトカインを環境に追加"""
        current_level = self._levels.get(cytokine_name, 0.0)
        new_level = current_level + amount
        self._levels[cytokine_name] = new_level
        
        # 登録された細胞に通知
        for cell in self._observers:
            cell.on_cytokine_changed(cytokine_name, new_level)
    
    def register_cell(self, cell):
        """細胞を観察者として登録"""
        if cell not in self._observers:
            self._observers.append(cell)