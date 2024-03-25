import os
import time
import mimetypes

from . import auth


class UploadActions(auth.Auth):
    """
    Manages the upload of media files to Twitter, supporting various media types including images and videos. This class handles the entire upload process, including initialization, media upload, and finalization.

    Inherits from `auth.Auth` for authentication purposes.

    Rate Limits:
    - upload: Limited by Twitter's media upload endpoints. Generally, the rate limit is 615 media uploads per 15-minute window.

    Attributes:
        media_endpoint_url (str): The URL endpoint for media uploads on Twitter.

    Methods:
        upload(source, media_category): Uploads a media file to Twitter.
        _upload_init(): Initializes the media upload session.
        _upload_append(): Uploads the media file in chunks.
        _upload_finalize(): Finalizes the media upload and processes the uploaded media.
        _check_status(): Checks the status of media processing after upload.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes the UploadActions instance with authentication tokens.

        Parameters:
            auth_token (str): The authentication token for user session.
            csrf_token (str): The CSRF token for request protection.
        """

        super().__init__(auth_token, csrf_token)
        self.media_endpoint_url = 'https://upload.twitter.com/i/media/upload.json'

    def upload(self, source: str, media_category: str = None) -> str:
        """
        Uploads a media file to Twitter, supporting images and videos. Validates the file before upload to ensure compliance with Twitter's media requirements. The media category must be one of the following, or None for default handling:
        - "tweet_image"
        - "tweet_video"
        - "tweet_gif"
        - "dm_image"
        - "dm_video"
        - "dm_gif"

        Rate limit: 615 requests per 15-minute window.

        Parameters:
            source (str): The local file path or URL of the gif to upload.
            media_category (str, optional): The category of the media being uploaded. Accepts one of: "tweet_image", "tweet_video", "tweet_gif", "dm_image", "dm_video", "dm_gif", or None.

        Returns:
            str: The media ID of the uploaded file, which can be used in tweets or direct messages.

        Raises:
            FileNotFoundError: If the specified file path does not exist.
            ValueError: If the media category is invalid or the file does not meet Twitter's requirements.
        """

        if not os.path.exists(source):
            raise FileNotFoundError(f"The path '{source}' does not exist.")

        # List of valid media categories
        valid_categories = [
            "tweet_image",
            "tweet_video",
            "tweet_gif",
            "dm_image",
            "dm_video",
            "dm_gif"
        ]

        # Check if the media_category is valid
        if media_category and media_category not in valid_categories:
            raise ValueError(f"Invalid media category: {media_category}. Must be one of: {', '.join(valid_categories)}")

        self.is_gif = False
        self.source = source
        self.media_id = None
        self.processing_info = None
        self.media_category = media_category
        self.total_bytes = 0

        if (source.startswith('http://') or source.startswith('https://')) and source.endswith('.gif'):
            self.is_gif = True
            self.media_type = "image/gif"

        elif os.path.isfile(source):
            self.total_bytes = os.path.getsize(self.source)
            self.media_type, _ = mimetypes.guess_type(self.source)

        else:
            raise ValueError("The source does not appear to be a valid URL or file path.")

        mime_type_limits = {
            'image/jpeg': 5 * 1048576,   # JPG
            'image/png': 5 * 1048576,    # PNG
            'image/gif': 15 * 1048576,   # GIF, assuming this could be animated
            'image/webp': 5 * 1048576,   # WEBP
            'video/mp4': 512 * 1048576,  # MP4 for video
            'video/quicktime': 512 * 1048576,  # MOV for video
        }

        if self.media_type not in mime_type_limits:
            raise ValueError(f"Unsupported MIME type: {self.media_type}.")

        if self.total_bytes > mime_type_limits[self.media_type]:
            raise ValueError(f"File {self.source} exceeds the maximum allowed size for {self.media_type}.")

        self._upload_init()
        if self.is_gif:
            self.processing_info = {
                "state": "in_progress",
                "check_after_secs": 1
            }
            self._check_status()
        else:
            self._upload_append()
            self._upload_finalize()

        return self.media_id

    def _upload_init(self):
        """
        Initializes the media upload session with Twitter by specifying the media type and file size.

        This method is called internally by `upload`.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        request_data = {
            'command': 'INIT',
            'media_type': self.media_type,
        }

        if self.media_category:
            request_data['media_category'] = self.media_category

        if self.is_gif:
            request_data['source_url'] = self.source
        else:
            request_data['total_bytes'] = self.total_bytes

        response = self.request_handler.post(
            self.media_endpoint_url,
            headers=headers,
            cookies=cookies,
            data=request_data,
        )

        self.media_id = response.json().get('media_id', None)

    def _upload_append(self):
        """
        Appends media file chunks to the upload session.

        This method is called internally by `upload` for files that are uploaded in chunks.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        segment_id = 0
        bytes_sent = 0
        file = open(self.source, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4*1024*1024)

            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }

            files = {
                'media': chunk
            }

            response = self.request_handler.post(
                self.media_endpoint_url,
                headers=headers,
                cookies=cookies,
                data=request_data,
                files=files
            )

            if response.status_code < 200 or response.status_code > 299:
                raise RuntimeError(f"Error while uploading: HTTP status code {response.status_code} indicates failure.")

            segment_id = segment_id + 1
            bytes_sent = file.tell()

    def _upload_finalize(self):
        """
        Finalizes the media upload and starts processing the media on Twitter's servers.

        This method is called internally by `upload`.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        response = self.request_handler.post(
            self.media_endpoint_url,
            headers=headers,
            cookies=cookies,
            data=request_data,
        )

        self.processing_info = response.json().get('processing_info', None)
        self._check_status()

    def _check_status(self):
        """
        Checks the status of the media processing after the upload is finalized.

        This method is called internally by `upload_finalize` and recursively by itself until processing is complete.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        if self.processing_info is None:
            return

        state = self.processing_info.get('state', None)

        if state == u'succeeded':
            return

        if state == u'failed':
            raise RuntimeError("Error while uploading: State indicates failure.")

        check_after_secs = self.processing_info.get('check_after_secs', 0)

        time.sleep(check_after_secs)

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        response = self.request_handler.get(
            self.media_endpoint_url,
            headers=headers,
            cookies=cookies,
            params=request_params,
        )

        self.processing_info = response.json().get('processing_info', None)
        self._check_status()
