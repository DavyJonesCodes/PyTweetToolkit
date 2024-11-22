import requests
import datetime
import time


class RequestHandler:
    """
    A wrapper class for the requests library to simplify making HTTP GET and POST requests and handling responses.

    This class uses a session for connection pooling and reuses the TCP connection for requests to the same endpoint, 
    which can improve performance. It also provides a unified method to handle HTTP responses, automatically raising 
    exceptions for HTTP error statuses while decoding JSON error messages if available.

    Methods:
        get(url, **kwargs) -> requests.Response:
            Performs a GET request to the specified URL with optional arguments and returns the response object.

        post(url, **kwargs) -> requests.Response:
            Performs a POST request to the specified URL with optional arguments and returns the response object.

        _handle_response(response) -> requests.Response:
            Handles the response from GET or POST requests, checks the status code, and raises appropriate exceptions
            for error codes while returning the original response for HTTP 200 OK statuses.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the RequestHandler class, creating a new session for making requests.
        """

        self.session = requests.Session()

    def get(self, url: str, **kwargs) -> requests.Response:
        """
        Sends a GET request to a specified URL and returns the response after handling.

        Parameters:
            url (str): The URL to send the GET request to.
            **kwargs: Optional arguments that request takes.

        Returns:
            requests.Response: The response object to the GET request.

        Raises:
            Various exceptions based on the response status code, indicating the type of error encountered.
        """

        response = self.session.get(url, **kwargs)
        return self._handle_response(response)

    def post(self, url: str, **kwargs) -> requests.Response:
        """
        Sends a POST request to a specified URL and returns the response after handling.

        Parameters:
            url (str): The URL to send the POST request to.
            **kwargs: Optional arguments that request takes.

        Returns:
            requests.Response: The response object to the POST request.

        Raises:
            Various exceptions based on the response status code, indicating the type of error encountered.
        """

        response = self.session.post(url, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> requests.Response:
        """
        Handles the HTTP response, raising exceptions for error status codes and returning the response for HTTP 200 OK.

        Parameters:
            response (requests.Response): The response object from a GET or POST request.

        Returns:
            requests.Response: The original response if the status code is 200 OK.

        Raises:
            ValueError, PermissionError, RuntimeError: Customized exceptions based on the HTTP status code of the response.
        """

        if response.status_code == 200:
            return response
        else:
            try:
                error_msg = response.json().get('errors', [{}])[0].get('message', '')
            except Exception:
                error_msg = ''

            if response.status_code == 400:
                raise ValueError(f"400 Bad Request | Message: {error_msg}".strip())
            elif response.status_code == 401:
                raise PermissionError(f"401 Unauthorized | Message: {error_msg}".strip())
            elif response.status_code == 403:
                raise PermissionError(f"403 Forbidden | Message: {error_msg}".strip())
            elif response.status_code == 404:
                raise ValueError(f"404 Not Found | Message: {error_msg}".strip())
            elif response.status_code == 429:
                # Handle rate limiting
                reset_time = response.headers.get('x-rate-limit-reset')
                if reset_time:
                    reset_time = datetime.datetime.fromtimestamp(int(reset_time), datetime.UTC) 
                    current_time = datetime.datetime.fromtimestamp(time.time(), datetime.UTC)
                    wait_seconds = (reset_time - current_time).total_seconds() + 1
                    raise RuntimeError(f"429 Too Many Requests | Rate limit exceeded. Retry after {wait_seconds} seconds | Message: {error_msg}".strip())
                else:
                    raise RuntimeError(f"429 Too Many Requests | Rate limit exceeded | Message: {error_msg}".strip())
            elif response.status_code == 500:
                raise RuntimeError(f"500 Internal Server Error | Message: {error_msg}".strip())
            elif response.status_code == 503:
                raise RuntimeError(f"503 Service Unavailable | Message: {error_msg}".strip())

            return response
