from flask import Blueprint, jsonify, request
from views import ContentManagerView

CONTENT_MANAGER_BLUEPRINT = Blueprint("semantic", __name__, url_prefix="/content-manager")


@CONTENT_MANAGER_BLUEPRINT.route("/fetch-and-post", methods=["POST"])
def fetch_and_post():
    feed_url = request.json.get("feed_url")
    articles = ContentManagerView.get_rss_articles(rss_url=feed_url)

    if not articles:
        return jsonify({"message": "No articles found"}), 400

    result = ContentManagerView.post_to_linkedin(articles)
    print("result:",result)

    return jsonify(result)