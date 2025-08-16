# パターン認識実装計画

## 背景
自然免疫系の本質的な機能である「パターン認識受容体（PRRs）による病原体関連分子パターン（PAMPs）の認識」を、概要から詳細へと段階的に実装する。

## 設計方針
- **シンプルさを保つ**: 過度な抽象化を避ける
- **既存構造を活かす**: 現在のクラス構造を最大限活用
- **段階的な詳細化**: 概念レベルから始めて、必要に応じて詳細を追加
- **テスト駆動**: 各段階でテストを壊さない

## 実装ステップ

### Step 1: メソッド名を概念的に変更
**目的**: 自然免疫系の本質的な機能を明確に表現

```python
class InnateImmuneSystem:
    def recognize_pattern(self, antigen: Antigen) -> bool:
        # detect_threat() → recognize_pattern()
        # 実装は変えず、概念を明確化
```

**テスト更新**:
- `test_innate_system_detects_threat` → `test_innate_system_recognizes_pathogen_pattern`
- 振る舞いは同じ、命名を概念的に

### Step 2: 抗原に最小限の属性追加
**目的**: 分子パターンの概念を導入（ただし詳細は問わない）

```python
class Antigen:
    def __init__(self, antigen_type, concentration=1.0, molecular_signature=None):
        self.antigen_type = antigen_type
        self.concentration = concentration
        self.molecular_signature = molecular_signature  # 文字列やリストなどシンプルな形式
```

**デフォルト動作**:
- molecular_signatureがNoneでも既存の動作を維持
- 後方互換性を保つ

### Step 3: 認識ロジックの段階的進化

#### Phase 3.1: 現在の実装（タイプベース）
```python
def recognize_pattern(self, antigen: Antigen) -> bool:
    if not antigen:
        return False
    return antigen.antigen_type not in {AntigenType.SELF}
```

#### Phase 3.2: シグネチャの存在チェック
```python
def recognize_pattern(self, antigen: Antigen) -> bool:
    if not antigen:
        return False
    
    # molecular_signatureがあればそれで判定
    if hasattr(antigen, 'molecular_signature') and antigen.molecular_signature:
        return self._is_pathogen_signature(antigen.molecular_signature)
    
    # なければ従来通りタイプで判定（後方互換）
    return antigen.antigen_type not in {AntigenType.SELF}
```

#### Phase 3.3: 特定パターンの認識
```python
def recognize_pattern(self, antigen: Antigen) -> bool:
    # 既知のPAMPsパターン
    known_pamps = ['LPS', 'dsRNA', 'flagellin', 'peptidoglycan']
    
    if antigen.molecular_signature in known_pamps:
        return True
    # ...
```

### Step 4: 必要に応じた詳細の追加（将来）

#### 認識の閾値
```python
def recognize_pattern(self, antigen: Antigen, threshold=0.5) -> bool:
    recognition_strength = self._calculate_recognition_strength(antigen)
    return recognition_strength > threshold
```

#### 複数パターンの組み合わせ
```python
molecular_signatures = ['LPS', 'flagellin']  # 複数のPAMPs
```

#### 認識の強度を返す
```python
def recognize_pattern(self, antigen: Antigen) -> tuple[bool, float]:
    # (認識したか, 認識強度)
    return (True, 0.8)
```

## 実装の優先順位

1. **必須**: Step 1-2（概念の明確化）
2. **推奨**: Step 3.1-3.2（基本的なパターン認識）
3. **オプション**: Step 3.3以降（詳細な実装）

## 注意事項

### やらないこと
- パターンを独立したクラスにする（過度な抽象化）
- 受容体クラスを早期に導入する
- 複雑な継承階層を作る

### 守ること
- 既存のテストを壊さない
- 各ステップでコミット
- ドメイン知識に基づいた命名

## 次のアクション

1. `detect_threat` → `recognize_pattern` へのリネーム
2. 対応するテストの更新
3. READMEとCLAUDE.mdの更新

## 参考: 生物学的背景

### PAMPs（病原体関連分子パターン）
- **細菌**: LPS、ペプチドグリカン、フラジェリン
- **ウイルス**: dsRNA、ssRNA、CpG DNA  
- **真菌**: β-グルカン、マンナン

### PRRs（パターン認識受容体）
- **TLRs**: 細胞表面・エンドソーム膜上
- **NLRs**: 細胞質内
- **RLRs**: 細胞質内（ウイルスRNA認識）

これらの詳細は後の実装フェーズで必要に応じて追加する。