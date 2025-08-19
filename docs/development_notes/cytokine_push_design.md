# Push型サイトカインシステムの設計

## 概要
細胞がサイトカイン環境に「登録」し、環境変化時に自動的に通知を受ける

## 実装パターン

### 1. Observer パターン
```python
class CytokineEnvironment:
    def __init__(self):
        self.levels = {}
        self.observers = []  # 登録された細胞
    
    def register_cell(self, cell):
        """細胞を観察者として登録"""
        self.observers.append(cell)
    
    def add_cytokine(self, name, amount):
        """サイトカイン追加時に全細胞に通知"""
        old_level = self.levels.get(name, 0)
        self.levels[name] = old_level + amount
        
        # 変化を全細胞に通知
        for cell in self.observers:
            cell.on_cytokine_changed(name, old_level, self.levels[name])

class DendriticCell:
    def __init__(self, cytokine_env):
        self.cytokine_env = cytokine_env
        cytokine_env.register_cell(self)  # 自動登録
    
    def on_cytokine_changed(self, cytokine_name, old_level, new_level):
        """サイトカイン変化の通知を受信"""
        if cytokine_name == "IFN-gamma" and new_level > 10:
            self.enhance_antigen_presentation()
```

### 2. 選択的リスナー（特定サイトカインのみ監視）
```python
class CytokineEnvironment:
    def __init__(self):
        self.levels = {}
        self.listeners = {}  # {cytokine_name: [cells]}
    
    def subscribe(self, cell, cytokine_name):
        """特定サイトカインの変化を購読"""
        if cytokine_name not in self.listeners:
            self.listeners[cytokine_name] = []
        self.listeners[cytokine_name].append(cell)
    
    def add_cytokine(self, name, amount):
        self.levels[name] = self.levels.get(name, 0) + amount
        
        # 該当サイトカインを監視している細胞のみに通知
        if name in self.listeners:
            for cell in self.listeners[name]:
                cell.on_cytokine_changed(name, self.levels[name])

class TCell:
    def __init__(self, cytokine_env):
        # IL-12のみを監視
        cytokine_env.subscribe(self, "IL-12")
        cytokine_env.subscribe(self, "IL-2")
```

### 3. 閾値ベースの通知
```python
class CytokineEnvironment:
    def __init__(self):
        self.levels = {}
        self.threshold_listeners = {}  # {(cytokine, threshold): [cells]}
    
    def register_threshold(self, cell, cytokine_name, threshold):
        """閾値を超えた時のみ通知"""
        key = (cytokine_name, threshold)
        if key not in self.threshold_listeners:
            self.threshold_listeners[key] = []
        self.threshold_listeners[key].append(cell)
    
    def add_cytokine(self, name, amount):
        old_level = self.levels.get(name, 0)
        new_level = old_level + amount
        self.levels[name] = new_level
        
        # 閾値を超えた場合のみ通知
        for (cytokine, threshold), cells in self.threshold_listeners.items():
            if cytokine == name:
                if old_level <= threshold < new_level:
                    for cell in cells:
                        cell.on_threshold_exceeded(name, new_level)
```

## 生物学的な妥当性

### 利点
- 細胞表面受容体による即座の反応を表現
- シグナル伝達の連鎖反応を実装可能

### 課題
- 実際の生物では「通知」ではなく「濃度勾配の感知」
- 受容体の飽和や脱感作が表現しにくい
- 空間的な距離の概念がない

## 推奨される実装

**ハイブリッドアプローチ**：
- 基本はPush型で即座の反応を実現
- 各細胞に「感受性」パラメータを持たせる
- 不応期や受容体飽和も実装

```python
class ImmuneCell:
    def on_cytokine_changed(self, name, level):
        # 不応期チェック
        if self.is_refractory(name):
            return
        
        # 受容体飽和チェック
        effective_level = min(level, self.receptor_saturation[name])
        
        # 感受性に基づく反応
        if effective_level > self.sensitivity[name]:
            self.respond_to_cytokine(name, effective_level)
```