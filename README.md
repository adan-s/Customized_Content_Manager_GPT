# LinkedIn Content Manager

This project is a Flask-based API that fetches articles from an RSS feed and posts them to LinkedIn.

## Prerequisites

- Python 3.8+
- Flask
- Requests
- Feedparser
- BeautifulSoup4
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
    ```

## Running the Application

1. Start the Flask application:
    ```sh
    python main.py
    ```

2. The application will be running at `http://127.0.0.1:5000`.

## API Endpoints

### POST /content-manager/fetch-and-post

Fetches articles from an RSS feed and posts them to LinkedIn.

**Request Body:**
```json
{
  "feed_url": "https://example.com/rss"
}
```

**Responses:**
- `200 OK`: Successful operation
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Internal server error

## Getting the Access Token

To get the access token for LinkedIn API, follow these steps:

1. **Register your application** on the [LinkedIn Developer Portal](https://www.linkedin.com/developers/).

2. **Get the Client ID and Client Secret** from the LinkedIn Developer Portal.

3. **Generate the Authorization Code**:
    - Direct the user to LinkedIn's authorization URL:
      ```
      https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=your_client_id&redirect_uri=your_redirect_uri&state=xyz123&scope=r_liteprofile%20r_emailaddress%20w_member_social
      ```
    - After the user authorizes the application, they will be redirected to your redirect URI with a `code` parameter.

4. **Exchange the Authorization Code for an Access Token**:
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

5. **Add the Access Token** to your `.env` file:
    ```dotenv
    ACCESS_TOKEN=your_access_token
    ```
