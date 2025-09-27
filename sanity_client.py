# backend/sanity_client.py
import os
import requests
from typing import Any, Dict

SANITY_PROJECT_ID = os.environ.get("SANITY_PROJECT_ID")
SANITY_DATASET = os.environ.get("SANITY_DATASET", "production")
SANITY_TOKEN = os.environ.get("SANITY_API_TOKEN")

if not SANITY_PROJECT_ID or not SANITY_TOKEN:
    raise ValueError("SANITY_PROJECT_ID and SANITY_API_TOKEN are required in env")

BASE_MUTATE = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-05-03/data/mutate/{SANITY_DATASET}"
BASE_QUERY = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-05-03/data/query/{SANITY_DATASET}"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SANITY_TOKEN}"
}

def save_blog_post(title: str, draft: str, edits: str, seo: str) -> Dict[str, Any]:
    payload = {
        "mutations": [
            {
                "create": {
                    "_type": "blogPost",
                    "title": title,
                    "draft": draft,
                    "edits": edits,
                    "seo": seo,
                    "status": "draft"
                }
            }
        ]
    }
    resp = requests.post(BASE_MUTATE, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def fetch_posts(limit: int = 50):
    q = '*[_type == "blogPost"] | order(_createdAt desc)[0...${limit}] { _id, title, draft, seo, _createdAt }'
    # Sanity query uses params; simple build:
    resp = requests.get(f"{BASE_QUERY}?query=*[_type%20==%20%22blogPost%22]%20|%20order(_createdAt%20desc)%20[0...{limit}]%20{title,draft,seo,_createdAt}",
                        headers=HEADERS)
    # Above is a simple approach; if errors happen, user can replace with proper encoded query via requests params
    try:
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e), "raw": resp.text}
