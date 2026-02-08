# GlobalD

FastAPIアプリケーションを使用して、機械中心のデータを検索および管理するツール

## 機能

- 機械データに対するフリーテキスト検索
- SQLiteデータベースバックエンド
- FastAPIによるRESTful API
- セキュリティのための入力サニタイズ機能

## インストール手順

1. 依存ライブラリをインストール:
```bash
pip install -r requirements.txt
```

2. サンプルデータでデータベースを初期化:
```bash
python populate_db.py
```

3. アプリを実行:
```bash
uvicorn main:app --reload
```

APIは `http://localhost:8000` で利用可能です。

## API エンドポイント一覧

### 機械を検索
**GET** `/api/search?q=<クエリ>`

以下の機械フィールドに検索を実行します：
- 機械モデル (Machine Model)
- 機械シリアル番号 (Machine Serial)
- 製造元 (Maker)
- NCモデル (NC Model)
- 契約番号 (Contract Number)
- エンドユーザ (End User)
- 設置国 (Install Country)
- サービス拠点 (Service Base)

#### リクエスト例
製造元で検索:
```bash
curl "http://localhost:8000/api/search?q=Makino"
```

設置国で検索:
```bash
curl "http://localhost:8000/api/search?q=Japan"
```

シリアル番号で検索:
```bash
curl "http://localhost:8000/api/search?q=SN-2023-001"
```