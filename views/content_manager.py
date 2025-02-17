import feedparser
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

import config

# Load environment variables
load_dotenv()

ACCESS_TOKEN = config.ACCESS_TOKEN


def get_rss_articles(rss_url: str, max_articles: int = 10):
    """
    Fetches and parses articles from an RSS feed, stripping any HTML content.

    :param rss_url: The URL of the RSS feed.
    :param max_articles: Number of latest articles to fetch (default: 5).
    :return: A list of dictionaries containing article details.
    """

    print("rss url:", rss_url)
    feed = feedparser.parse(rss_url)

    print("feed:",feed)

    # Check if the feed was fetched successfully
    if not feed.entries:
        print(f"Warning: No articles found or failed to fetch feed from {rss_url}")
        return []

    articles = []
    for entry in feed.entries[:max_articles]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
        })

    return articles


def post_to_linkedin(articles):
    """
    Posts multiple articles as a single LinkedIn update.
    """

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Combine articles into one post
    post_content = "📰 Latest Articles 📰\n\n"
    for article in articles:
        post_content += f"🔹 {article['title']}\nRead more: {article['link']}\n\n"

    payload = {
        "author": "urn:li:person:Fx9-1COIim",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_content[:2500]
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 201:  # LinkedIn returns 201 on success
        print(f"Error: {response.status_code} - {response.text}")

    return response.json()
