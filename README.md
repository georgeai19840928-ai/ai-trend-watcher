# AI Trend Watcher 🦐

> **Project Manager**: 喬治蝦 (George Shrimp) (@G928_Sigma_bot)
> **Developer**: 程式蝦 (Programmer Shrimp) (@G928_theta_bot)
> **Owner**: George Ghien (@goergechien)

## 📌 專案簡介 (Project Overview)
本專案旨在每日自動掃描 GitHub 上關於 **AI**、**LLM**、**Generative Video Workflow** 等主題的熱門開源專案，並利用 AI 進行摘要總結，最後透過 Telegram Bot 發送日報通知。

## 🎯 核心目標 (Goals)
1.  **自動化趨勢追蹤**：無需手動搜尋，自動捕捉 GitHub 最新動態。
2.  **AI 摘要**：過濾大量專案資訊，只提供精簡扼要的亮點。
3.  **每日推送**：固定於每日早上 05:00 (UTC+8) 發送報告。
4.  **Zeabur 部署**：支援 Zeabur 平台的一鍵部署與定時任務。

## 🛠 技術規格 (Technical Specs)

### 1. 核心組件
*   **語言**: Python 3.10+
*   **資料來源**: GitHub API (REST API v3)
    *   Search Endpoint: `GET /search/repositories`
    *   Authentication: `Authorization: token <GITHUB_TOKEN>`
*   **AI 摘要**: OpenAI GPT-4o-mini / Google Gemini Flash (需配置 API Key)
*   **通知管道**: Telegram Bot API (`sendMessage`)
*   **排程**: Python `schedule` 庫 或 Zeabur Cron Job

### 2. 搜尋策略 (Search Strategy)
*   **關鍵字 (Keywords)**:
    *   `topic:ai`
    *   `topic:llm`
    *   `topic:generative-video`
    *   `topic:comfyui`
    *   `topic:stable-video-diffusion`
    *   `topic:autogpt`
    *   `topic:workflow` AND `AI`
*   **篩選條件 (Filters)**:
    *   `created:>now-7d` (最近 7 天建立) OR `pushed:>now-24h` (最近 24 小時更新)
    *   `stars:>50` (星數大於 50，過濾雜訊)
    *   `sort:stars` (按星數排序)

### 3. 資料處理流程 (Workflow)
1.  **Fetch**: 呼叫 GitHub API 獲取符合條件的 Repo 列表 (取前 10 名)。
2.  **Summarize**: 對每個 Repo 的 `description` 和 `README` (前 500 字) 進行 AI 摘要。
    *   Prompt: "請用繁體中文簡要總結這個專案的核心功能與亮點，50字以內。"
3.  **Format**: 整理成 Markdown 格式的日報。
4.  **Notify**: 透過 Telegram Bot 發送至指定 Chat ID。

## 🚀 部署指南 (Deployment)

### 1. 環境變數 (Environment Variables)
在 Zeabur Dashboard 中設定以下變數：
*   `GITHUB_TOKEN`: 用於 GitHub API 認證 (避免 Rate Limit)。
*   `OPENAI_API_KEY` (或 `GEMINI_API_KEY`): 用於生成摘要。
*   `TELEGRAM_BOT_TOKEN`: Telegram Bot 的 Access Token。
*   `TELEGRAM_CHAT_ID`: 接收通知的 Chat ID (個人或群組)。

### 2. 本地開發 (Local Development)
```bash
# 1. Clone 專案
git clone https://github.com/your-username/ai-trend-watcher.git
cd ai-trend-watcher

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定 .env 檔案
cp .env.example .env
# 填入上述變數

# 4. 執行測試
python main.py --test
```

### 3. Zeabur 部署
本專案包含 `zeabur.toml` (可選) 與 `Dockerfile`，推送到 GitHub 後，在 Zeabur 選擇該 Repo 即可自動部署。
建議設定 Service Type 為 **Cron Job** (若 Zeabur 支援) 或 **Long-running Service** (內部使用 `schedule` loop)。

## 📂 檔案結構 (File Structure)
```
ai-trend-watcher/
├── main.py             # 主程式入口
├── config.py           # 設定檔讀取
├── requirements.txt    # Python 依賴
├── README.md           # 本規格書
├── .gitignore          # Git 忽略檔
├── src/
│   ├── github_client.py # GitHub API 封裝
│   ├── ai_summarizer.py # AI 摘要邏輯
│   └── notifier.py      # Telegram 通知邏輯
└── Dockerfile          # 容器化部署設定
```

---
**Status**: 🚧 Planning / In Progress
**Last Updated**: 2026-02-12
