# 免疫系モデリングプロジェクト

## 概要
人間の免疫系をモデリングするためのPythonプロジェクトです。ドメイン駆動設計の原則に基づいて構築されています。

## プロジェクト構造
```
immune_system_modeling/
├── human_immune_system/         # 人免疫系パッケージ
│   ├── __init__.py
│   ├── model/                   # ドメインモデル
│   │   ├── __init__.py
│   │   └── immune_system.py     # 免疫系クラス
│   └── tests/                   # テストコード
│       ├── __init__.py
│       └── test_immune_system.py
├── pytest.ini                   # pytest設定ファイル
├── requirements.txt             # 依存パッケージ
└── README.md

```

## 現在の実装

### ImmuneSystem クラス
基本的な免疫系のインターフェースを提供：
- `antigen_exposure(antigen)`: 抗原への曝露を処理
- `is_activated()`: 免疫系の活性化状態を確認

## セットアップ

### 1. 仮想環境の作成と有効化
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

## テストの実行

```bash
# すべてのテストを実行
python -m pytest

# 詳細な出力付き
python -m pytest -v

# カバレッジレポート付き
python -m pytest --cov=human_immune_system
```

## 依存パッケージ

### 科学計算
- numpy: 数値計算
- scipy: 科学技術計算
- matplotlib: グラフ描画
- pandas: データ分析
- networkx: ネットワーク分析
- sympy: 記号計算

### テスト
- pytest: テストフレームワーク
- pytest-cov: カバレッジ測定

## 今後の開発予定
- 自然免疫系（Innate Immune System）の詳細な実装
- 獲得免疫系（Adaptive Immune System）の実装
- 細胞レベルのシミュレーション機能
- 可視化機能の追加