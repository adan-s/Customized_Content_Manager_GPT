from flask import Blueprint, jsonify, request
from views import ContentManagerView

CONTENT_MANAGER_BLUEPRINT = Blueprint("semantic", __name__, url_prefix="/content-manager")



@CONTENT_MANAGER_BLUEPRINT.route("/fetch", methods=["POST"])
def fetch():
    """
    Fetch articles from an RSS feed.
    """
    feed_url = request.json.get("feed_url")
    articles = ContentManagerView.get_rss_articles(rss_url=feed_url)

    if not articles:
        return jsonify({"message": "No articles found"}), 400

    return jsonify(articles)


@CONTENT_MANAGER_BLUEPRINT.route("/post", methods=["POST"])
def create_post():
    """
    Create a post on LinkedIn (either personal or organizational).
    """
    data = request.json
    post_as = data.get("post_as")
    article_text = data.get("articles")
    organization_id = data.get("organization_id")

    if not article_text:
        return jsonify({"error": "Article text is required"}), 400

    if post_as == "organization" and not organization_id:
        return jsonify({"error": "Organization ID is required for organization posts"}), 400

    response = ContentManagerView.post_to_linkedin(article_text, post_as, organization_id)

    return jsonify(response)


@CONTENT_MANAGER_BLUEPRINT.route("/organizations", methods=["GET"])
def get_organizations_route():
    """
    Get list of organizations for the user.
    """
    organization_names, organization_ids = ContentManagerView.get_organizations()

    return jsonify({
        "organizations": [
            {"id": org_id, "name": org_name}
            for org_id, org_name in zip(organization_ids, organization_names)
        ]
    })
