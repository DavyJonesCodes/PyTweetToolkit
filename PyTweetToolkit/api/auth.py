import re

from ..utils.request_handler import RequestHandler


class Auth:
    """
    Manages authentication, CSRF protection, and session management for API requests, with a focus on Twitter. Utilizes a custom RequestHandler for HTTP requests, facilitating the integration of authentication and session tokens into requests made to Twitter's API.

    Attributes:
        request_handler (RequestHandler): Handles HTTP requests.
        _auth_token (str): Used for user session authentication.
        _csrf_token (str): Mitigates CSRF attacks.
        _bearer_token (str): Authorizes API requests.

    Methods:
        __init__(auth_token: str, csrf_token: str): Initializes the Auth instance with session management and CSRF protection tokens, and dynamically fetches the Bearer token.
        _get_headers() -> dict: Returns headers for authenticated API requests, including authorization and CSRF tokens.
        _get_cookies() -> dict: Returns cookies for session management, using authentication and CSRF tokens.
        _get_bearer_token() -> str: Fetches and extracts the Bearer token from a specific JavaScript file hosted by Twitter.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes the Auth instance, sets up tokens for user session authentication and CSRF protection, and fetches the Bearer token for API authorization.

        Parameters:
            auth_token (str): Token for authenticating user sessions.
            csrf_token (str): Token for CSRF protection.
        """

        self.request_handler = RequestHandler()
        self._auth_token = auth_token
        self._csrf_token = csrf_token
        self._bearer_token = self._get_bearer_token()

    def _get_headers(self) -> dict:
        """
        Constructs headers necessary for making authenticated API requests. Includes the Bearer token for authorization and the CSRF token for request integrity.

        Returns:
            dict: Headers including authorization, CSRF protection, and standard request metadata.
        """

        return {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self._bearer_token,
            "DNT": "1",
            "referer": "https://twitter.com/",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            "x-csrf-token": self._csrf_token,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en",
        }

    def _get_cookies(self) -> dict:
        """
        Prepares cookies required for session management. Includes tokens for authentication and CSRF protection.

        Returns:
            dict: Cookies incorporating the authentication token and the CSRF token.
        """

        return {
            "auth_token": self._auth_token,
            "ct0": self._csrf_token
        }

    def _get_bearer_token(self) -> str:
        """
        Dynamically retrieves the Bearer token from Twitter's JavaScript resources. This token is essential for making authorized API requests.

        Returns:
            str: The Bearer token necessary for API authorization.
        """

        url = "https://abs.twimg.com/responsive-web/client-web/main.18d8447a.js"
        response = self.request_handler.get(url)

        if response.status_code == 200:
            match = re.search(r"Bearer ([A-Za-z0-9%-_]+)", response.text)
            if match:
                return match.group(0)
            else:
                raise ValueError("Bearer Token not found.")
        else:
            raise ConnectionError(f"Failed to fetch Bearer Token: HTTP {response.status_code}")
