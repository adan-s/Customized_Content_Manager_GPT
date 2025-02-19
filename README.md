# LinkedIn Content Manager

This project is a Flask-based API that fetches articles from an RSS feed and posts them to LinkedIn. The user provides a topic to search, and the GPT model fetches related RSS feeds for that topic and sends them to the API endpoint. The API returns the articles, which are then shown to the user. The user can decide to post the articles as they are on LinkedIn or modify them. Before posting, the GPT model asks the user whether to post on their personal account or an organization account and which organization account. Once confirmed, it posts on LinkedIn and provides the link to the post to the user.

## Prerequisites

- Python 3.8+
- Flask
- Requests
- Feedparser
- python-dotenv

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/LinkedInContentManager.git
    cd LinkedInContentManager
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add the following environment variables:
    ```dotenv
    DEBUG_MODE=True
    APPLICATION_HOST=127.0.0.1
    APPLICATION_PORT=5000
    CLIENT_ID=your_client_id
    PRIMARY_CLIENT_SECRET=your_client_secret
    ACCESS_TOKEN=your_access_token
    AUTHORIZATION_CODE=your_authorization_code
    PERSON_URN=your_person_urn
    ```

## Getting the Access Token

To get the access token for LinkedIn API, follow these steps:

1. **Register your application** on the [LinkedIn Developer Portal](https://www.linkedin.com/developers/).

2. **Get the Client ID and Client Secret** from the LinkedIn Developer Portal.

3. **Ensure your application has access to the following products**:
    - Sign In with LinkedIn using OpenID Connect
    - Share on LinkedIn
    - Advertising API

4. **Generate the Authorization Code**:
    - Direct the user to LinkedIn's authorization URL:
      ```
      https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=your_client_id&redirect_uri=your_redirect_uri&state=xyz123&scope=r_liteprofile%20r_emailaddress%20w_member_social%20r_organization_social%20w_organization_social
      ```
    - After the user authorizes the application, they will be redirected to your redirect URI with a `code` parameter.

5. **Exchange the Authorization Code for an Access Token**:
    - Make a POST request to LinkedIn's token endpoint:
      ```sh
      curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
      -d grant_type=authorization_code \
      -d code=your_authorization_code \
      -d redirect_uri=your_redirect_uri \
      -d client_id=your_client_id \
      -d client_secret=your_client_secret
      ```
    - The response will contain the access token.

6. **Add the Access Token** to your `.env` file:
    ```dotenv
    ACCESS_TOKEN=your_access_token
    ```

7. **Get your URN**:
    - Make a GET request to LinkedIn's user info endpoint:
      ```sh
      curl -X GET https://api.linkedin.com/v2/userinfo \
      -H "Authorization: Bearer <access_token>"
      ```
    - The value of the `sub` key in the response is your URN.

8. **Add the URN** to your `.env` file:
    ```dotenv
    PERSON_URN=your_person_urn
    ```

## Running the Application

1. Start the Flask application:
    ```sh
    python main.py
    ```

2. The application will be running at `http://127.0.0.1:5000`.

## API Endpoints

### POST /content-manager/fetch

Fetches articles from an RSS feed.

**Request Body:**
```json
{
  "feed_url": "https://example.com/rss"
}
```

**Responses:**
- `200 OK`: Successful operation
- `400 Bad Request`: No articles found
- `500 Internal Server Error`: Internal server error

### POST /content-manager/post

Posts articles to LinkedIn.

**Request Body:**
- To post on personal feed
```json
{
  "articles": "Article title\n\nArticle summary\nRead more: Article link",
  "post_as": "personal"
}
```

- To post on organization feed
```json
{
  "articles": "Article title\n\nArticle summary\nRead more: Article link",
  "post_as": "organization",
  "organization_id": "123456"
}
```

**Responses:**
- `200 OK`: Successful operation
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Internal server error

### GET /content-manager/organizations

Fetches the names of organizations associated with the user where they have the ADMINISTRATOR role.

**Responses:**
- `200 OK`: Successful operation
- `400 Bad Request`: No organizations found
- `500 Internal Server Error`: Internal server error

## OpenAI Schema

The `open_ai_schema` file contains the schema to give to your customized GPT actions. In the `url` field, you can provide the URL on which your backend is hosted for runtime testing. You can deploy your backend on [ngrok](https://ngrok.com/) and refer to its documentation for further detailed assistance.


## OpenAI Prompt
The user will provide a topic to search, 
and this GPT will fetch related RSS feeds for that topic and send to the API endpoint.
The API will return the articles, and it will be shown to the user. 
The user will then decide to post them as they are on LinkedIn or modify them. 
Before posting, this GPT will ask the user whether to post on their personal account or an organization account and which organization account. 
Once confirmed, it will post on LinkedIn and provide the link of the post to the user.



## Credits

This project uses the LinkedIn API. For more information, refer to the [LinkedIn API documentation](https://learn.microsoft.com/en-us/linkedin/).
