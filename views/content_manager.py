import feedparser
import requests
from dotenv import load_dotenv
import os
from flask import Blueprint, jsonify, request

# Load environment variables
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PERSON_URN = os.getenv("PERSON_URN")
ORG_URN = str

CONTENT_MANAGER_BLUEPRINT = Blueprint("content_manager", __name__, url_prefix="/content-manager")


def get_rss_articles(rss_url: str, max_articles: int = 10):
    """
    Fetches and parses articles from an RSS feed.

    :param rss_url: The URL of the RSS feed.
    :param max_articles: Number of latest articles to fetch (default: 10).
    :return: A list of dictionaries containing article details.
    """
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        print(f"Warning: No articles found or failed to fetch feed from {rss_url}")
        return []

    articles = [{"title": entry.title, "link": entry.link} for entry in feed.entries[:max_articles]]

    return articles


def post_to_linkedin(articles, post_as="personal", organization_id=None):
    """
    Posts multiple articles as a LinkedIn update.

    :param articles: List of articles to post.
    :param post_as: "personal" for personal profile, "organization" for company page.
    :param organization_id: ID of the selected organization (if posting as an organization).
    :return: JSON response from the LinkedIn API.
    """
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Determine author
    print("organization_id",organization_id)
    if post_as == "organization":
        if not organization_id:
            return {"error": "Organization ID is required when posting as an organization"}
        author_urn = f"organization:{organization_id}"
    else:
        author_urn = f"person:{PERSON_URN}"

    payload = {
        "author": f"urn:li:{author_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": articles[:2500]},
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
        return {"error": response.json()}

    return response.json()


def fetch_user_organizations():
    """
    Fetch organizations associated with the authenticated user where the role is 'ADMINISTRATOR'.
    """
    url = "https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee&role=ADMINISTRATOR"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return {"error": response.json()}

    organizations_data = response.json()

    organization_ids = []
    if "elements" in organizations_data:
        # Extract the organization IDs from the response
        organization_ids = [org["organizationalTarget"].split(":")[3] for org in organizations_data["elements"]]

    return organization_ids


def fetch_organization_details(organization_id):
    """
    Fetch organization details by organization ID.
    """
    url = f"https://api.linkedin.com/v2/organizations/{organization_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return {"error": response.json()}

    return response.json()


def get_organizations():
    """
    Fetch the names of organizations associated with the user where they have the ADMINISTRATOR role.
    """
    # Step 1: Fetch the organization IDs associated with the user
    organization_ids = fetch_user_organizations()

    if not organization_ids:
        return jsonify({"message": "No organizations found"}), 400

    # Step 2: Fetch details for each organization and extract names
    organization_names = []
    for org_id in organization_ids:
        org_details = fetch_organization_details(org_id)
        if "localizedName" in org_details:
            organization_names.append(org_details["localizedName"])

    return organization_names,organization_ids