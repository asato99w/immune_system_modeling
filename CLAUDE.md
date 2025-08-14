# 免疫系モデリングプロジェクト - 開発ガイドライン

## プロジェクト概要
このプロジェクトは人間の免疫系をモデリングするシステムです。ドメイン駆動設計（DDD）とテスト駆動開発（TDD）の原則に基づいて開発を進めています。

## 開発原則

### 1. テスト駆動開発（TDD）
- **Red-Green-Refactor サイクル**を厳守
  1. Red: 失敗するテストを先に書く
  2. Green: テストを通す最小限の実装
  3. Refactor: コードを改善（テストは通したまま）
- テストファースト: 実装前に必ずテストケースを作成
- 1つのテストケースは1つの振る舞いのみをテスト

### 2. ドメイン駆動設計（DDD）
- **ユビキタス言語**: 生物学的に正確な用語を使用
  - `antigen_exposure()` (抗原曝露)
  - `immune_activation` (免疫活性化)
  - `is_activated()` (活性化状態の確認)
- **ドメインモデル**: `human_immune_system/model/` に配置
- **境界づけられたコンテキスト**: 免疫系の各サブシステムを独立したモジュールとして実装

## プロジェクト構造
```
human_immune_system/
├── model/          # ドメインモデル層
├── tests/          # テストコード
└── __init__.py     # パッケージ初期化
```

## 開発フロー

### 新機能追加時の手順
1. **テストケースの作成**
   ```python
   def test_新機能の振る舞い(self):
       # Arrange: 準備
       # Act: 実行
       # Assert: 検証
   ```

2. **最小限の実装**
   - テストを通すための最小限のコード
   - 過度な最適化は避ける

3. **リファクタリング**
   - 命名の改善
   - 重複の除去
   - パフォーマンスの改善

### 命名規則
- **クラス名**: PascalCase（例: `ImmuneSystem`, `Macrophage`）
- **メソッド名**: snake_case、動詞で開始（例: `antigen_exposure()`, `is_activated()`）
- **変数名**: snake_case、意味のある名前（例: `immune_activation`, `viral_antigen`）
- **テストメソッド**: `test_` + 具体的な振る舞い（例: `test_antigen_exposure_triggers_activation`）

## 生物学的ドメイン知識

### 主要な概念
- **Antigen（抗原）**: 免疫応答を引き起こす物質
- **Immune Activation（免疫活性化）**: 抗原認識後の免疫系の応答
- **Innate Immunity（自然免疫）**: 生まれつき備わる非特異的防御
- **Adaptive Immunity（獲得免疫）**: 特異的な抗原認識と記憶

### 実装予定の免疫系コンポーネント
1. **自然免疫系**
   - Macrophage（マクロファージ）
   - Neutrophil（好中球）
   - Dendritic Cell（樹状細胞）

2. **獲得免疫系**
   - T Cell（T細胞）
   - B Cell（B細胞）
   - Antibody（抗体）

## テスト実行コマンド

```bash
# 仮想環境の有効化
source venv/bin/activate

# 全テスト実行
python -m pytest

# 詳細出力
python -m pytest -v

# カバレッジ測定
python -m pytest --cov=human_immune_system

# 特定のテストファイル実行
python -m pytest human_immune_system/tests/test_immune_system.py

# テスト実行後の型チェック（将来的に追加予定）
# mypy human_immune_system/
```

## コード品質チェック

### 実行すべきチェック
1. **テスト**: `python -m pytest`
2. **カバレッジ**: `python -m pytest --cov=human_immune_system --cov-report=term-missing`
3. **今後追加予定**:
   - 型チェック: `mypy`
   - リンター: `flake8` or `ruff`
   - フォーマッター: `black`

## 実装時の注意事項

### DO
- ✅ テストを先に書く
- ✅ 生物学的に正確な命名を使用
- ✅ 1つのクラス/メソッドは1つの責任
- ✅ ドメインロジックをモデル層に集約
- ✅ 相対インポートを使用（`from ..model import`）

### DON'T
- ❌ テストなしでコードを実装
- ❌ 技術的な用語をドメインモデルに混入
- ❌ 複雑なインポート構造（sys.path操作など）
- ❌ ドメインロジックをテストコードに記述

## 次のステップ

1. **基本的な免疫応答サイクルの実装**
   - 抗原認識 → 活性化 → 応答 → 終息

2. **自然免疫系の詳細実装**
   - マクロファージの貪食作用
   - サイトカイン産生
   - 炎症反応

3. **獲得免疫系の実装**
   - T細胞の活性化
   - B細胞の抗体産生
   - 免疫記憶の形成

## 参考リソース
- Domain-Driven Design by Eric Evans
- Test-Driven Development by Kent Beck
- 免疫生物学の教科書（Janeway's Immunobiology）