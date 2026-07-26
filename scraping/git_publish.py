"""
生成したサイト（docs/）を GitHub にコミット & プッシュする
GitHub Pages が docs/ フォルダを公開するよう設定されている前提
"""
import subprocess
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import GIT_REPO_DIR, GIT_AUTO_PUSH


def run(cmd, cwd):
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, shell=False
    )
    return result.returncode, result.stdout, result.stderr


def publish():
    if not GIT_AUTO_PUSH:
        print("[スキップ] GIT_AUTO_PUSH が無効です")
        return True

    repo_dir = os.path.abspath(GIT_REPO_DIR)

    # git リポジトリか確認
    code, out, err = run(["git", "rev-parse", "--is-inside-work-tree"], repo_dir)
    if code != 0:
        print("❌ このフォルダは git リポジトリではありません")
        print("  GITHUB_SETUP.md の手順に従って初期化してください")
        return False

    # 変更があるか確認
    code, out, err = run(["git", "status", "--porcelain"], repo_dir)
    if not out.strip():
        print("[スキップ] 変更なし（コミット不要）")
        return True

    print("[1/3] git add...")
    code, out, err = run(["git", "add", "docs", "data"], repo_dir)
    if code != 0:
        print(f"❌ git add エラー: {err}")
        return False

    print("[2/3] git commit...")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code, out, err = run(
        ["git", "commit", "-m", f"データ更新: {ts}"], repo_dir
    )
    if code != 0:
        print(f"❌ git commit エラー: {err}")
        return False
    print(out.strip())

    print("[3/3] git push...")
    code, out, err = run(["git", "push"], repo_dir)
    if code != 0:
        print(f"❌ git push エラー: {err}")
        print("  認証が必要な場合は GITHUB_SETUP.md を参照してください")
        return False

    print("✓ GitHub に反映しました")
    return True


if __name__ == "__main__":
    success = publish()
    sys.exit(0 if success else 1)
