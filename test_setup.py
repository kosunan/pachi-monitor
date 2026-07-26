"""
環境セットアップ確認用スクリプト
"""
import sys
import os
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scraping'))

print("=" * 60)
print("環境チェック")
print("=" * 60)
print()

# Python バージョン
print(f"[1] Python バージョン: {sys.version}")
print()

# 必要なライブラリ確認
required_libs = {
    'selenium': 'Selenium',
    'requests': 'Requests',
    'bs4': 'BeautifulSoup4',
}

print("[2] インストール済みライブラリ:")
all_ok = True
for import_name, display_name in required_libs.items():
    try:
        __import__(import_name)
        print(f"    ✓ {display_name}")
    except ImportError:
        print(f"    ✗ {display_name} (未インストール)")
        all_ok = False

print()

# ChromeDriver確認
chromedriver_path = "./chromedriver.exe"
print("[3] ChromeDriver:")
if os.path.exists(chromedriver_path):
    print(f"    ✓ 配置確認: {chromedriver_path}")
else:
    print(f"    ✗ 未配置: {chromedriver_path}")
    print("      check_chrome_version.py を実行してダウンロードしてください")
    all_ok = False

print()

# 認証セッション（Chromeプロファイル）確認
print("[4] 認証セッション:")
try:
    from config import CHROME_PROFILE_DIR

    if os.path.exists(CHROME_PROFILE_DIR) and os.listdir(CHROME_PROFILE_DIR):
        print(f"    ✓ プロファイル確認: {CHROME_PROFILE_DIR}")
        print("      (start_chrome_debug.py で毎回ログインすればさらに確実です)")
    else:
        print(f"    - 未作成: {CHROME_PROFILE_DIR}")
        print("      python run_all.py 実行時に自動作成されます")
        print("      毎回ログインする場合は python start_chrome_debug.py を使ってください")
except ImportError as e:
    print(f"    ✗ config.py 読み込みエラー: {e}")
    all_ok = False

print()

# Git リポジトリ確認
print("[5] Git / GitHub Pages:")
result = subprocess.run(
    ["git", "rev-parse", "--is-inside-work-tree"],
    capture_output=True, text=True
)
if result.returncode == 0:
    print(f"    ✓ git リポジトリ初期化済み")

    remote = subprocess.run(
        ["git", "remote", "-v"], capture_output=True, text=True
    )
    if remote.stdout.strip():
        print(f"    ✓ リモート設定済み")
    else:
        print(f"    ✗ リモート未設定")
        print("      GITHUB_SETUP.md の手順に従ってください")
else:
    print(f"    ✗ git リポジトリ未初期化")
    print("      GITHUB_SETUP.md の手順に従ってください")

print()
print("=" * 60)
if all_ok:
    print("✓ 基本セットアップ完了！")
    print("  次: python run_all.py で一括実行")
else:
    print("⚠ セットアップ未完了")
    print("  エラーを解決してから続行してください")
print("=" * 60)
