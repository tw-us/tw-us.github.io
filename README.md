# 台美緊急連線 TW-US Crisis Connect

🌐 **[tw-us.cc](https://tw-us.cc)**

身在美國的台灣人緊急應變指南 - 開源的安全準備與危機應變資源

## 關於本專案

**台美緊急連線** 是專為身在美國的台灣人打造的緊急應變指南網站。在這個充滿不確定性的時代，我們相信準備工作能夠拯救生命，而每個台美人都可以成為台灣的堅實後盾。

### 核心目標

- 💪 **賦能台美人**：提供實用的工具和知識，讓身在美國的台灣人能夠有效支援台灣
- 🔗 **建立連結**：強化台美社群之間的合作與相互支援
- 📋 **實用導向**：提供可執行的檢查清單和行動指南，而非純理論內容
- 🌍 **開源協作**：透過開放原始碼的方式，讓所有人都能貢獻與改善內容

### 網站內容

**現在怎麼做**：
- 為家人與朋友準備（通訊、物資、避難計畫）
- 為社會與其他人準備（政治倡議、組織參與、資訊戰）

**緊急時怎麼做**：
- 協助急難的家人與朋友（聯絡、資金支援、撤離協助）
- 支援更多急難的人（社區動員、募款、政治行動）

**其他資源**：
- 官方準備指引連結
- 台美組織資訊
- 豐富的封存內容（準備清單、組織資料、政策資訊）

## 技術架構

### 技術棧
- **靜態網站生成器**：[MkDocs](https://www.mkdocs.org/)
- **主題**：[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- **部署平台**：GitHub Pages
- **域名**：tw-us.cc
- **語言**：繁體中文

### 特色功能
- **中文搜尋優化**：使用 jieba 分詞提供準確的中文搜尋功能
- **響應式設計**：支援電腦、平板、手機各種裝置
- **深色模式**：自動切換或手動選擇明暗主題
- **導航整合**：目錄整合到側邊欄，方便瀏覽
- **無障礙設計**：符合網頁無障礙標準

### 內容管理
- **自動導航**：使用 `awesome-nav` 插件自動生成導航結構
- **Markdown 支援**：支援豐富的 Markdown 擴充功能
- **多媒體支援**：支援圖片、影片等多媒體內容
- **表情符號**：支援 Material Design 表情符號

## 如何貢獻

我們歡迎所有形式的貢獻！

### 貢獻方式

**內容貢獻**：
- 🔧 修正錯誤資訊或過時連結
- 📝 新增或改善現有內容
- 🌐 翻譯成其他語言
- 📊 提供更多統計數據或資源

**技術貢獻**：
- 🐛 回報或修復技術問題
- 💡 建議新功能或改善
- 🎨 設計改善或視覺優化
- ⚡ 效能優化

**社群貢獻**：
- 📢 分享網站給需要的人
- 💬 提供使用回饋
- 🤝 協助推廣與外展

### 開發環境設定

1. **Clone 專案**：
   ```bash
   git clone https://github.com/tw-us/tw-us.github.io.git
   cd tw-us.github.io
   ```

2. **安裝依賴**：
   ```bash
   poetry install --no-root
   ```

3. **本地開發**：
   ```bash
   poetry run mkdocs serve
   ```
   網站會在 `http://127.0.0.1:8000` 運行

4. **部署到 GitHub Pages**：

   Do not run `mkdocs gh-deploy`. GitHub Actions builds and deploys `main` to GitHub Pages after validation.

### 內容編輯指南

- **語言**：主要使用繁體中文
- **語氣**：實用、直接、可執行
- **格式**：多使用檢查清單 (`- [ ]`) 和行動導向的內容
- **連結**：優先連結到官方資源和可信來源
- **更新**：定期檢查並更新連結和資訊

### 提交 Pull Request

建立 PR 前必須執行：

```bash
poetry run mkdocs build --strict
poetry run python scripts/check-built-site.py
```

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 專案結構

```
.
├── docs/                    # 網站內容
│   ├── index.md            # 首頁
│   ├── 現在怎麼做/          # 平時準備指南
│   ├── 緊急時怎麼做/        # 緊急應變指南
│   ├── 其他資源/            # 資源與封存內容
│   ├── assets/             # 圖片與靜態資源
│   └── stylesheets/        # 自定義樣式
├── jieba_dict/             # 中文分詞詞典
├── mkdocs.yml              # MkDocs 設定檔
├── pyproject.toml          # Python 專案設定
├── poetry.lock             # 依賴版本鎖定
└── README.md               # 本檔案
```

## 授權

本專案採用 **MIT 授權條款**。詳細內容請參閱 [LICENSE](LICENSE) 檔案。

### 開源精神

我們相信重要的安全資訊應該是開放、可取得的。透過開源的方式：

- 🔍 **透明度**：所有人都可以檢視和驗證內容
- 🤝 **協作**：集合眾人智慧提供更好的資源
- 📚 **可持續性**：確保資訊能夠持續更新和維護
- 🌍 **無障礙**：任何人都可以使用和改善這些資源

## 聯絡資訊

- **網站**：[tw-us.cc](https://tw-us.cc)
- **GitHub**：[tw-us/tw-us.github.io](https://github.com/tw-us/tw-us.github.io)
- **Issues**：[回報問題或建議](https://github.com/tw-us/tw-us.github.io/issues)

---

**記住：準備工作做得越充分，危機來臨時就越能保護所愛的人。每個貢獻都很重要，每個聲音都值得被聽見。**

讓我們一起建立一個更強韌、更團結的台美社群。🇹🇼🇺🇸
