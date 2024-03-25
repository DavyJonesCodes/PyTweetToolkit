from . import auth, user
from ..models import user_model


class FriendshipActions(auth.Auth):
    """
    Manages friendship actions on Twitter, leveraging the platform's API to follow and unfollow users, handle follow requests,
    and more. Inherits from an authentication base class to use Twitter's authentication mechanism for API requests.

    Rate Limits: While specific rate limits for these actions are not mentioned, they are subject to Twitter's standard API rate limits.
    It is important for users to check Twitter's API documentation for the most current rate limits.

    Attributes:
        user_actions (user.UserActions): Instance for fetching user details.

    Methods:
        follow_user(user_id: str) -> user_model.User:
            Follows a user by ID. Returns the followed user's details.
            Rate limit: Subject to Twitter's standard API rate limits.

        unfollow_user(user_id: str) -> user_model.User:
            Unfollows a user by ID. Returns the unfollowed user's details.
            Rate limit: Subject to Twitter's standard API rate limits.

        follow_requests(user_id: str) -> list[user_model.User]:
            Retrieves a list of users who have requested to follow the authenticated user.
            Rate limit: Subject to Twitter's standard API rate limits.

        accept_follow_request(user_id: str) -> user_model.User:
            Accepts a follow request from a user by ID. Returns the user's details post-acceptance.
            Rate limit: Subject to Twitter's standard API rate limits.

        reject_follow_request(user_id: str) -> user_model.User:
            Rejects a follow request from a user by ID. Returns the user's details post-rejection.
            Rate limit: Subject to Twitter's standard API rate limits.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes the FriendshipActions instance with necessary authentication tokens for making API requests.

        Parameters:
            auth_token (str): The authentication token for session management.
            csrf_token (str): The CSRF token for securing requests against CSRF attacks.
        """

        super().__init__(auth_token, csrf_token)
        self.user_actions = user.UserActions(auth_token, csrf_token)

    def follow_user(self, user_id: str) -> user_model.User:
        """
        Follows a user specified by their user ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user to follow.

        Returns:
            user_model.User: An instance representing the followed user's details.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

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
            'user_id': str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/friendships/create.json"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=data,
        )

        json_response = response.json()
        screen_name = json_response.get("screen_name")

        if screen_name:
            return self.user_actions.get_user_by_screen_name(screen_name)

        return user_model.User({})

    def unfollow_user(self, user_id: str) -> user_model.User:
        """
        Unfollows a user specified by their user ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user to unfollow.

        Returns:
            user_model.User: An instance representing the unfollowed user's details.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

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
            'user_id': str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/friendships/destroy.json"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=data,
        )

        json_response = response.json()
        screen_name = json_response.get("screen_name")

        if screen_name:
            return self.user_actions.get_user_by_screen_name(screen_name)

        return user_model.User({})

    def follow_requests(self, user_id: str) -> list[user_model.User]:
        """
        Retrieves follow requests for the authenticated user.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The user ID of the authenticated user.

        Returns:
            list[user_model.User]: A list of users who have requested to follow the authenticated user.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
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
            'user_id': str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/users/lookup.json"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        users: list[user_model.User] = []

        json_response = response.json()
        for user in json_response:
            screen_name = user.get("screen_name")

            if screen_name:
                users.append(self.user_actions.get_user_by_screen_name(screen_name))

        return users

    def accept_follow_request(self, user_id: str) -> user_model.User:
        """
        Accepts a follow request from a user specified by their user ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user whose follow request is being accepted.

        Returns:
            user_model.User: An instance representing the user's details post-acceptance.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

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
            'cursor': '-1',
            'user_id':  str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/friendships/accept.json"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=data,
        )

        json_response = response.json()
        screen_name = json_response.get("screen_name")

        if screen_name:
            return self.user_actions.get_user_by_screen_name(screen_name)

        return user_model.User({})

    def reject_follow_request(self, user_id: str) -> user_model.User:
        """
        Rejects a follow request from a user specified by their user ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user whose follow request is being rejected.

        Returns:
            user_model.User: An instance representing the user's details post-rejection.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

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
            'cursor': '-1',
            'user_id':  str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/friendships/deny.json"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=data,
        )

        json_response = response.json()
        screen_name = json_response.get("screen_name")

        if screen_name:
            return self.user_actions.get_user_by_screen_name(screen_name)

        return user_model.User({})
