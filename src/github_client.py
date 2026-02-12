import requests
import os
import logging
from datetime import datetime, timedelta

# 設定 Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_trending_repos(limit=10):
    """
    搜尋 GitHub 熱門 AI 專案
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logger.error("未設定 GITHUB_TOKEN，無法搜尋 GitHub。")
        return []

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 設定搜尋條件：最近 7 天建立
    date_str = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # 使用關鍵字搜尋以涵蓋更多專案 (不只限制在 topic)
    # 搜尋 AI, LLM, Video Workflow 相關關鍵字
    query = f"AI LLM video workflow created:>{date_str}"
    
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }

    try:
        response = requests.get("https://api.github.com/search/repositories", headers=headers, params=params, timeout=15)
        
        # 處理 422 錯誤 (通常是查詢語法問題)
        if response.status_code == 422:
            logger.error(f"GitHub API 422 錯誤。Query: {query}")
            # 備用方案：更簡單的查詢
            query = f"AI LLM created:>{date_str}"
            params["q"] = query
            response = requests.get("https://api.github.com/search/repositories", headers=headers, params=params, timeout=15)

        response.raise_for_status()
        
        data = response.json()
        repos = data.get("items", [])
        
        # 如果還是 0 個，嘗試不限建立時間 (僅限最近更新)
        if not repos:
            logger.info("7 天內無新專案，擴大搜尋範圍至最近更新的專案...")
            query = f"AI LLM video workflow pushed:>{date_str}"
            params["q"] = query
            response = requests.get("https://api.github.com/search/repositories", headers=headers, params=params, timeout=15)
            data = response.json()
            repos = data.get("items", [])

        logger.info(f"成功搜尋到 {len(repos)} 個熱門專案。")
        return repos
        
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub API 請求失敗: {e}")
        return []
