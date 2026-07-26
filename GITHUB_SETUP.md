# GitHub Pages セットアップ手順

スクレイピングしたデータを GitHub Pages で公開し、携帯からいつでも見られるようにします。

## 1️⃣ GitHub でリポジトリ作成

1. https://github.com/new にアクセス
2. リポジトリ名: `pachi-monitor`（任意）
3. **Public**（GitHub Pages を無料で使うため公開設定が必要）
4. 「Create repository」をクリック
5. 作成後に表示される **リポジトリURL** をメモ
   ```
   https://github.com/kosunan/pachi-monitor.git
   ```

---

## 2️⃣ Git のインストール確認

```powershell
git --version
```

インストールされていなければ https://git-scm.com/download/win からインストール。

---

## 3️⃣ ローカルリポジトリ初期化

```powershell
cd I:\work_space\パチンコ情報スクレイピング
git init
git add .
git commit -m "初期セットアップ"
git branch -M main
git remote add origin https://github.com/kosunan/pachi-monitor.git
git push -u origin main
```

`.gitignore` により、認証セッション（`chrome_profile/`）や `chromedriver.exe` は
自動的に除外されます（公開リポジトリに機密情報が入らないようにするためです）。

**初回 push 時、ブラウザでGitHubログインを求められます。** ログインすれば、Windows の Git Credential Manager が認証情報を保存し、以降は自動でpushできます。

---

## 4️⃣ GitHub Pages を有効化

1. GitHub のリポジトリページを開く
2. **Settings** タブをクリック
3. 左メニュー **Pages** をクリック
4. **Source** で以下を選択：
   - Branch: `main`
   - Folder: `/docs`
5. **Save** をクリック

数分後、以下のURLでサイトが公開されます：
```
https://kosunan.github.io/pachi-monitor/
```

このURLを携帯のブックマークに登録すれば、いつでも最新データを確認できます。

---

## 5️⃣ 動作確認

```powershell
python run_all.py
```

- スクレイピング → `data/latest.json` 保存
- サイト生成 → `docs/index.html` 生成
- GitHub へ自動 push

数分後、公開URLをリロードして更新を確認してください。

---

## トラブルシューティング

### git push で毎回パスワードを求められる
→ Git Credential Manager が正しく設定されていません。以下を実行：
```powershell
git config --global credential.helper manager
```

### GitHub Pages が反映されない
→ Settings → Pages で Branch/Folder の設定を再確認。反映まで数分かかることがあります

### 「Public」にしたくない
→ GitHub Pro（有料）なら Private リポジトリでも Pages が使えます。無料で完結させたい場合は Public 一択です
　※ データ自体は機種名・台番号・差玉のみなので、個人情報は含まれません

---

## 次のステップ

✅ セットアップ完了後：

→ Step: 定期実行の自動化（タスクスケジューラー）
