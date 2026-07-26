# 設定ファイル

# スクレイピング対象（複数機種を追加可能）
TARGET_PAGES = [
    {
        "name": "P大海物語5スペシャルALTA",
        "url": "https://www.pscube.jp/h/a751210/cgi-bin/nc-v05-011.php?cd_ps=1&bai=4&nmk_kisyu=P%25E5%25A4%25A7%25E6%25B5%25B7%25E7%2589%25A9%25E8%25AA%259E5%25EF%25BD%25BD%25EF%25BE%258D%25EF%25BE%259F%25EF%25BD%25BC%25EF%25BD%25AC%25EF%25BE%2599ALTA",
    },
]

# Chrome設定
CHROME_DRIVER_PATH = "./chromedriver.exe"
HEADLESS = True  # ヘッドレスモード（ブラウザ表示なし）
CHROME_PROFILE_DIR = "./chrome_profile"  # 認証セッションを保持する専用プロファイル
CHROME_DEBUG_PORT = 9222  # start_chrome_debug.bat で起動したChromeのデバッグポート
TIMEOUT = 30  # ページロードのタイムアウト（秒）

# データ保存
DATA_DIR = "./data"
LATEST_JSON = "./data/latest.json"
HISTORY_DIR = "./data/history"

# サイト出力
SITE_DIR = "./docs"  # GitHub Pages公開用フォルダ
SITE_INDEX = "./docs/index.html"

# Git / GitHub Pages 設定
GIT_REPO_DIR = "."  # git リポジトリのルート（このフォルダ自体をリポジトリにする）
GIT_AUTO_PUSH = True  # スクレイピング後に自動で commit & push するか

# その他設定
DEBUG = False  # デバッグモード
