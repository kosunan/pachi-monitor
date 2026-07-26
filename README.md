# パチスロ情報スクレイピング

スクレイピングしたデータをGitHub Pagesの簡易サイトに自動反映し、
携帯のブラウザからいつでも最新データを確認できるようにします。

## 全体の流れ

```
スクレイピング (Selenium) → データ編集 (JSON整形) → サイト更新 (GitHub Pages)
```

`python run_all.py` を実行するだけで上記3工程が自動で走ります。

## 環境構築手順

### ✅ Step 1-2: Python環境 + ChromeDriver（完了）

```bash
python setup_simple.py
```

### Step 3: 対象サイトへのログイン（毎回 or 都度）

対象サイトはセッション認証が必要です。以下でデバッグ用Chromeを起動し、
そのウィンドウで対象サイトにログインしてください。

```bash
python start_chrome_debug.py
```

- `run_all.py` 実行時、このウィンドウが開いていればそのセッションをそのまま使います
- 開いていなければ、`chrome_profile/` に保存された前回のセッションで再利用を試みます（それでも切れていれば再ログインが必要です）
- 普段使いのChromeとは別プロファイルなので、日常のブラウジングには影響しません

### Step 4: GitHub Pages セットアップ

詳細は `GITHUB_SETUP.md` を参照。

1. GitHubでリポジトリ作成
2. `git init` してリモート追加・push
3. Settings → Pages で `main` ブランチの `/docs` フォルダを公開設定

### Step 5: 動作確認

```bash
python run_all.py
```

## フォルダ構造

```
I:\work_space\パチンコ情報スクレイピング\
├── run_all.py                 (一括実行: スクレイピング→サイト生成→GitHub反映)
├── setup_simple.py            (ライブラリインストール)
├── check_chrome_version.py    (Chromeバージョン確認)
├── test_setup.py              (環境チェック)
├── chromedriver.exe
├── start_chrome_debug.py       (ログイン用Chrome起動)
├── chrome_profile/            (認証セッション保持用・自動生成)
├── GITHUB_SETUP.md            (GitHub Pages設定手順)
├── data/
│   ├── latest.json            (最新スクレイピング結果)
│   └── history/                (過去データの履歴)
├── docs/                      (GitHub Pagesで公開される静的サイト)
│   └── index.html
└── scraping/
    ├── config.py               (設定ファイル)
    ├── scraper.py              (スクレイピング本体)
    ├── site_generator.py       (サイトHTML生成)
    └── git_publish.py          (GitHubへのcommit/push)
```

## 次のステップ

- [x] Step 1-2: Python環境構築
- [x] Step 3: スクレイピング対象の構造分析（グラフ最終値の取得方法を確認済み）
- [ ] Step 4: GitHub Pages セットアップ
- [ ] Step 5: run_all.py 動作確認
- [ ] Step 6: 定期実行の自動化（タスクスケジューラー）

---

Python 3.8+ が必要です。
