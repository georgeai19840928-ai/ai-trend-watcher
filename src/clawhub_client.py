import requests
import logging

# 設定 Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_clawhub_trending(limit=5):
    """
    抓取 ClawHub (OpenClaw Skills) 的熱門專案。
    目前為 Mock 實作，對齊 GitHub Client 的資料格式。
    """
    logger.info("正在檢查 ClawHub 熱門趨勢...")
    
    try:
        # 這裡的 Key 必須與 src/ai_summarizer.py 預期的一致
        # 需要包含: name, html_url, stargazers_count, description
        return [
            {
                "name": "ClawHub-Standard-Skills",
                "html_url": "https://clawhub.ai/skills/standard",
                "description": "OpenClaw 官方標準技能包，提供網頁爬取與搜尋核心能力。",
                "stargazers_count": "Official"
            },
            {
                "name": "ClawHub-Notion-Sync",
                "html_url": "https://clawhub.ai/skills/notion",
                "description": "自動同步對話精華至 Notion 資料庫的技能。",
                "stargazers_count": "Hot"
            }
        ]
    except Exception as e:
        logger.error(f"ClawHub 抓取失敗: {e}")
        return []
