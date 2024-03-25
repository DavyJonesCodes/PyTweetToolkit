import os
from PIL import Image

from . import auth, upload, user
from ..models import user_model


class ProfileActions(auth.Auth):
    """
    Manages user profile actions on Twitter, enabling the updating of profile details,
    profile images, and profile banners through the platform's API.

    Inherits from an authentication base class for API authentication.

    Rate Limits:
    - update_profile: Subject to Twitter's standard API rate limits.
    - update_profile_image: Subject to Twitter's standard API rate limits.
    - update_profile_banner: Subject to Twitter's standard API rate limits.

    Attributes:
        user_actions (user.UserActions): Instance for actions related to user accounts.
        upload_actions (upload.UploadActions): Instance for handling media uploads.

    Methods:
        update_profile(name: str = None, description: str = None, location: str = None, website_url: str = None) -> user_model.User:
            Updates the authenticated user's profile details. Optionally updates name, description, location, and website URL.
            Returns the updated user details.

        update_profile_image(source: str) -> user_model.User:
            Updates the authenticated user's profile image. Requires the local path to the image. Returns the updated user details.

        update_profile_banner(source: str) -> user_model.User:
            Updates the authenticated user's profile banner. Requires the local path to the image. Returns the updated user details.

        _check_image_requirements(file_path: str, max_size_bytes: int, required_dimensions: tuple, required_aspect_ratio: float) -> bool:
            Validates the provided image against Twitter's image requirements. Checks for file existence, size, format, dimensions, and aspect ratio.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes ProfileActions with authentication tokens.

        Parameters:
            auth_token (str): Token for session authentication.
            csrf_token (str): Token for CSRF protection.
        """

        super().__init__(auth_token, csrf_token)
        self.user_actions = user.UserActions(auth_token, csrf_token)
        self.upload_actions = upload.UploadActions(auth_token, csrf_token)

    def update_profile(self, name: str = None, description: str = None, location: str = None, website_url: str = None) -> user_model.User:
        """
        Updates the authenticated user's profile details.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            name (str, optional): New name of the user.
            description (str, optional): New description for the user's profile.
            location (str, optional): New location of the user.
            website_url (str, optional): New website URL for the user's profile.

        Returns:
            user_model.User: The updated user model.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        data = {}

        MAX_LENGTHS = {
            "name": 50,
            "description": 160,
            "location": 30,
            "url": 100,
        }

        def set_data_attribute(key, value):
            """
            Sets the key-value pair in data dictionary if value is provided and does not exceed max_length.

            Args:
                key (str): The key under which to store the value.
                value (str): The value to store.

            Raises:
                ValueError: If the value exceeds max_length.
            """
            if value is not None:
                if len(value) > MAX_LENGTHS[key]:
                    raise ValueError(f"{key} exceeds the maximum length of {MAX_LENGTHS['key']}.")
                data[key] = value

        set_data_attribute('name', name)
        set_data_attribute('description', description)
        set_data_attribute('location', location)
        set_data_attribute('url', website_url)

        url = "https://api.twitter.com/1.1/account/update_profile.json"

        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=data,
        )

        if response.status_code == 200:
            screen_name = response.json().get("screen_name", "")
            return self.user_actions.get_user_by_screen_name(screen_name)

        return user_model.User({})

    def update_profile_image(self, source: str) -> user_model.User:
        """
        Updates the authenticated user's profile image.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            source (str): File path to the new profile image.

        Returns:
            user_model.User: The updated user model with the new profile image.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        max_size_bytes = 2 * 1024 * 1024
        required_dimensions = (100, 100)
        required_aspect_ratio = 1

        self._check_image_requirements(source, max_size_bytes, required_dimensions, required_aspect_ratio)

        media_id = self.upload_actions.upload(source)

        data = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'return_user': 'true',
            'media_id': str(media_id),
        }

        url = "https://api.twitter.com/1.1/account/update_profile_image.json"

        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=data,
        )

        if response.status_code == 200:
            screen_name = response.json().get("screen_name", "")
            return self.user_actions.get_user_by_screen_name(screen_name)

        return user_model.User({})

    def update_profile_banner(self, source: str) -> user_model.User:
        """
        Updates the authenticated user's profile banner.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            source (str): File path to the new profile banner image.

        Returns:
            user_model.User: The updated user model with the new profile banner.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        max_size_bytes = 5 * 1024 * 1024
        required_dimensions = (300, 100)
        required_aspect_ratio = 3

        self._check_image_requirements(source, max_size_bytes, required_dimensions, required_aspect_ratio)

        media_id = self.upload_actions.upload(source)

        data = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'return_user': 'true',
            'media_id': str(media_id),
        }

        url = "https://api.twitter.com/1.1/account/update_profile_banner.json"

        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=data,
        )

        if response.status_code == 200:
            screen_name = response.json().get("screen_name", "")
            return self.user_actions.get_user_by_screen_name(screen_name)

        return user_model.User({})

    def _check_image_requirements(self, file_path: str, max_size_bytes: int, required_dimensions: tuple, required_aspect_ratio: float) -> None:
        """
        Checks if the image meets Twitter's requirements for profile images and banners.

        This method does not interact with Twitter's API and thus is not subject to API rate limits.

        Parameters:
            file_path (str): Path to the image file.
            max_size_bytes (int): Maximum allowed image file size in bytes.
            required_dimensions (tuple): Required minimum dimensions (width, height) of the image.
            required_aspect_ratio (float): Required aspect ratio (width/height) of the image.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the image does not meet the specified requirements.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The path '{file_path}' does not exist.")

        if os.path.getsize(file_path) > max_size_bytes:
            raise ValueError(f"Image exceeds maximum file size of {max_size_bytes // (1024 * 1024)} MB.")

        with Image.open(file_path) as img:
            allowed_formats = ["JPEG", "PNG", "GIF", "WEBP"]
            if img.format not in allowed_formats:
                raise ValueError(f"Image format {img.format} is not among the allowed formats: {', '.join(allowed_formats)}.")

            width, height = img.size
            actual_aspect_ratio = width / height

            if width < required_dimensions[0] or height < required_dimensions[1]:
                raise ValueError(f"Image dimensions ({width}x{height}) are smaller than the required {required_dimensions[0]}x{required_dimensions[1]}.")

            if round(actual_aspect_ratio, 2) != round(required_aspect_ratio, 2):
                raise ValueError(f"Image aspect ratio {actual_aspect_ratio:.2f} is different from the required {required_aspect_ratio:.2f}.")
