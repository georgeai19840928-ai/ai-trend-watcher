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

    # 設定搜尋條件：最近 7 天建立或更新的 AI 相關專案
    date_str = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    query = f"topic:ai OR topic:llm OR topic:generative-video OR topic:comfyui OR topic:stable-video-diffusion created:>{date_str}"
    
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }

    try:
        response = requests.get("https://api.github.com/search/repositories", headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        repos = data.get("items", [])
        
        logger.info(f"成功搜尋到 {len(repos)} 個熱門專案。")
        return repos
        
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub API 請求失敗: {e}")
        return []
