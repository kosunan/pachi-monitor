# Step 1-2: 環境構築ガイド

## クイックスタート

### 1️⃣ setup.bat を実行

ファイルエクスプローラーで以下のファイルを**ダブルクリック**：
```
I:\work_space\パチンコ情報スクレイピング\setup.bat
```

### 2️⃣ ChromeDriver をダウンロード

#### 方法A: 自動確認（推奨）
```
check_chrome_version.py
```
をダブルクリック。Chromeバージョンが自動表示されます。

#### 方法B: 手動確認
1. Google Chrome を開く
2. 右上の三点メニュー（⋮）をクリック
3. 「Google Chromeについて」をクリック
4. バージョン番号をメモ
   - 例：`126.0.6478.123`

### 3️⃣ ChromeDriver をダウンロード・配置

1. https://googlechromelabs.github.io/chrome-for-testing/ にアクセス
2. 自分のChromeバージョン（例：126）を探す
3. **Stable** 欄から `chromedriver-win64.zip` をダウンロード
4. ダウンロードしたZIPを解凍
5. `chromedriver-win64` フォルダ内の `chromedriver.exe` を以下にコピー：
   ```
   I:\work_space\パチンコ情報スクレイピング\
   ```

### 4️⃣ 確認テスト

```
test_setup.py
```
をダブルクリック。エラーがなければセットアップ完了です。

---

## トラブルシューティング

### setup.bat が実行できない
- **症状**: 黒いウィンドウが一瞬出て消える
- **対策**: 
  1. PowerShell を右クリック → 「管理者として実行」
  2. 以下を実行：
     ```powershell
     cd I:\work_space\パチンコ情報スクレイピング
     setup.bat
     ```

### Python がインストールされていない
- **症状**: `'python' は、内部コマンドまたは外部コマンドとして認識されていません`
- **対策**: https://www.python.org/downloads/ からインストール

### ChromeDriver エラー
- **症状**: `selenium.common.exceptions.WebDriverException`
- **対策**: 
  1. Chromeバージョンを確認
  2. 合ったChromeDriverをダウンロード
  3. `chromedriver.exe` がフォルダ直下にあるか確認

### ライブラリインストール エラー
- **症状**: `pip install` が失敗
- **対策**:
  ```powershell
  python -m pip install --upgrade pip
  python -m pip install selenium requests beautifulsoup4 google-auth-oauthlib google-auth-httplib2 google-api-python-client
  ```

---

## 仮想環境の有効化

セットアップ後、コマンドを実行する場合は仮想環境を有効化してください：

```powershell
cd I:\work_space\パチンコ情報スクレイピング
venv\Scripts\activate.bat
```

プロンプトが `(venv)` で始まればOK。

---

## フォルダ構成の確認

セットアップ後、以下のようなフォルダ構成になります：

```
I:\work_space\パチンコ情報スクレイピング\
├── setup.bat                      ✓ 実行済み
├── check_chrome_version.py
├── test_setup.py
├── chromedriver.exe               ← ここに配置
├── README.md
├── SETUP_GUIDE.md
├── venv\                          ✓ 自動作成
│   ├── Scripts\
│   ├── Lib\
│   └── ...
└── scraping\
    ├── __init__.py
    ├── config.py
    ├── scraper.py
    └── google_sheets.py
```

---

## 次のステップ

✅ Step 1-2 完了後：

→ **Step 3: Google Sheets API 認証設定**

詳細は `STEP3_GOOGLE_AUTH.md` を参照
