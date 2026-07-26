#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
デバッグモードでChromeを起動する。

このChromeウィンドウで対象サイトに毎日ログインしてください。
scraper.py はこのウィンドウのセッション（Cookie）をそのまま使ってスクレイピングします。

使い方:
  1. python start_chrome_debug.py を実行（Chromeが開く）
  2. 開いたChromeで対象サイトにログイン/認証を通す
  3. そのウィンドウは開いたままにする（最小化してOK）
  4. 別のターミナルで python run_all.py を実行するとログイン状態のまま取得できる

普段使いのChromeとは別のプロファイルなので、既存のChrome作業には影響しません。
一度ログインしたセッションはプロファイルに保存されるため、
次にこのスクリプトでChromeを開いたときも基本的にログイン状態が続きます
（サイト側のセッション有効期限が切れたら再ログインしてください）。
"""
import os
import sys
import subprocess
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraping'))

from config import CHROME_PROFILE_DIR, CHROME_DEBUG_PORT, TARGET_PAGES


def find_chrome_exe():
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def main():
    print("=" * 60)
    print("デバッグモード Chrome 起動")
    print("=" * 60)

    chrome_exe = find_chrome_exe()
    if not chrome_exe:
        print("❌ Chromeの実行ファイルが見つかりませんでした")
        print("  手動でパスを指定する場合は、このファイルの")
        print("  find_chrome_exe() にパスを追加してください")
        return False

    profile_dir = os.path.abspath(CHROME_PROFILE_DIR)
    os.makedirs(profile_dir, exist_ok=True)

    args = [
        chrome_exe,
        f"--remote-debugging-port={CHROME_DEBUG_PORT}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
    ]

    if TARGET_PAGES:
        args.append(TARGET_PAGES[0]["url"])

    print(f"起動中: {chrome_exe}")
    print(f"プロファイル: {profile_dir}")
    print(f"デバッグポート: {CHROME_DEBUG_PORT}")

    subprocess.Popen(args)

    print("\n✓ Chrome を起動しました")
    print("\nこのウィンドウで対象サイトにログイン/認証を通してください。")
    print("ログインできたら、このウィンドウは閉じずに開いたままにしておき、")
    print("別のターミナルで python run_all.py を実行してください。")

    return True


if __name__ == "__main__":
    try:
        success = main()
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        success = False
    finally:
        input("\nEnter キーを押して終了...")
    sys.exit(0 if success else 1)
