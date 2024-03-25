from utils.request_handler import RequestHandler


class Auth:
    """
    Handles authentication for making API requests, particularly to Twitter. Manages authentication, CSRF protection, and session tokens, providing utility methods for preparing headers and cookies for authenticated API calls.

    Attributes:
        request_handler (RequestHandler): Utilized for executing HTTP requests.
        _auth_token (str): Token for authenticating user sessions.
        _csrf_token (str): Token used to mitigate CSRF attacks.
        _bearer_token (str): Bearer token for API authorization.

    Methods:
        __init__(auth_token: str, csrf_token: str, bearer_token: str):
            Initializes Auth with necessary tokens for authentication and session management.
            Parameters:
                auth_token (str): Authentication token for user sessions.
                csrf_token (str): CSRF protection token.
                bearer_token (str): Authorization bearer token.

        _get_headers() -> dict:
            Constructs and returns standard headers for authenticated requests, including the bearer token and CSRF token.
            Returns:
                A dictionary of headers for authenticated requests.

        _get_cookies() -> dict:
            Generates and returns cookies required for session management, incorporating the auth and CSRF tokens.
            Returns:
                A dictionary of session management cookies.
    """

    def __init__(self, auth_token: str, csrf_token: str, bearer_token: str) -> None:
        """
        Initializes the Auth instance with authentication and session management tokens.

        Parameters:
            auth_token (str): A token for user session authentication.
            csrf_token (str): A token for CSRF protection.
            bearer_token (str): A token for API authorization.
        """

        self.request_handler = RequestHandler()
        self._auth_token = auth_token
        self._csrf_token = csrf_token
        self._bearer_token = bearer_token

    def _get_headers(self) -> dict:
        """
        Generates the standard headers required for authenticated API requests.

        Returns:
            A dictionary containing necessary headers for authenticated requests, such as authorization and CSRF tokens.
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
        Creates cookies necessary for maintaining an authenticated session state with the API.

        Returns:
            A dictionary containing session management cookies, including the authentication and CSRF tokens.
        """

        return {
            "auth_token": self._auth_token,
            "ct0": self._csrf_token
        }
