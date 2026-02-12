import os
import requests
import logging

# 設定 Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def summarize_repos(repos):
    """
    使用 OpenAI 或 Gemini 生成專案摘要
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        logger.warning("未設定 OPENAI_API_KEY，將直接輸出原始專案描述。")
        return [
            {
                "name": repo["name"],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "summary": repo["description"] or "無描述"
            }
            for repo in repos
        ]

    summaries = []
    
    for repo in repos:
        try:
            name = repo["name"]
            url = repo["html_url"]
            stars = repo["stargazers_count"]
            desc = repo.get("description", "無描述")
            
            # 組裝提示詞 (Prompt)
            prompt = f"請用繁體中文簡要總結這個 GitHub 專案：\n名稱: {name}\n描述: {desc}\n重點總結(30字內):"

            # 呼叫 OpenAI API
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",  # 或使用 gpt-3.5-turbo / gemini-pro
                "messages": [
                    {"role": "system", "content": "你是一個技術總結助手。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 100
            }
            
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                summary_text = response.json()["choices"][0]["message"]["content"].strip()
                logger.info(f"成功為 {name} 生成摘要。")
            else:
                logger.warning(f"OpenAI API 回傳錯誤: {response.status_code} - {response.text}，使用原始描述。")
                summary_text = desc

            summaries.append({
                "name": name,
                "url": url,
                "stars": stars,
                "summary": summary_text
            })
            
        except Exception as e:
            logger.error(f"生成摘要時發生錯誤 ({name}): {e}")
            summaries.append({
                "name": name,
                "url": url,
                "stars": stars,
                "summary": desc
            })

    return summaries
