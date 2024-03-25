from . import auth, user
from ..models import user_model


class RestrictionActions(auth.Auth):
    """
    Manages user restriction actions on Twitter, such as blocking and muting users, through the platform's API.

    Inherits from `auth.Auth` for authentication handling.

    Rate Limits:
    - block_user: Subject to Twitter's standard API rate limits.
    - unblock_user: Subject to Twitter's standard API rate limits.
    - mute_user: Subject to Twitter's standard API rate limits.
    - unmute_user: Subject to Twitter's standard API rate limits.
    - get_blocked_users: Subject to Twitter's standard API rate limits.
    - get_muted_users: Subject to Twitter's standard API rate limits.

    Attributes:
        user_actions (user.UserActions): Instance for performing user-related actions.

    Methods:
        block_user(user_id: str) -> user_model.User:
            Blocks a user specified by their user ID. Returns the blocked user's details.

        unblock_user(user_id: str) -> user_model.User:
            Unblocks a user specified by their user ID. Returns the unblocked user's details.

        mute_user(user_id: str) -> user_model.User:
            Mutes a user specified by their user ID. Returns the muted user's details.

        unmute_user(user_id: str) -> user_model.User:
            Unmutes a user specified by their user ID. Returns the unmuted user's details.

        get_blocked_users(cursor: str = "") -> tuple[list[user_model.User], str, str]:
            Retrieves a list of users blocked by the authenticated user along with pagination cursors.

        get_muted_users(cursor: str = "") -> tuple[list[user_model.User], str, str]:
            Retrieves a list of users muted by the authenticated user along with pagination cursors.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes RestrictionActions with the necessary authentication tokens.

        Parameters:
            auth_token (str): Token for user session authentication.
            csrf_token (str): Token for CSRF protection.
        """

        super().__init__(auth_token, csrf_token)
        self.user_actions = user.UserActions(auth_token, csrf_token)

    def block_user(self, user_id: str) -> user_model.User:
        """
        Blocks the user with the given user ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user to block.

        Returns:
            user_model.User: The details of the blocked user.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        data = {
            'user_id': str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/blocks/create.json"
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

    def unblock_user(self, user_id: str) -> user_model.User:
        """
        Unblocks the user with the given user ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user to unblock.

        Returns:
            user_model.User: The details of the unblocked user.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        data = {
            'user_id': str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/blocks/destroy.json"
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

    def mute_user(self, user_id: str) -> user_model.User:
        """
        Mutes the user with the given user ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user to mute.

        Returns:
            user_model.User: The details of the muted user.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        data = {
            'user_id': str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/mutes/users/create.json"
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

    def unmute_user(self, user_id: str) -> user_model.User:
        """
        Unmutes the user with the given user ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user to unmute.

        Returns:
            user_model.User: The details of the unmuted user.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        data = {
            'user_id': str(user_id),
        }

        url = "https://twitter.com/i/api/1.1/mutes/users/destroy.json"
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

    def get_blocked_users(self, cursor: str = "") -> tuple[list[user_model.User], str, str]:
        """
        Retrieves a paginated list of users blocked by the authenticated user.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            cursor (str, optional): Pagination cursor for the query.

        Returns:
            tuple: A tuple containing a list of blocked users, next cursor, and previous cursor for pagination.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"count":20,"cursor":"{cursor}","includePromotedContent":false,"withSafetyModeUserFields":false}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/EDuJJnhTxj5gMtDd6iifiA/BlockedAccountsAll"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("viewer", {}).get("timeline", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
        next_cursor = entries[-2].get("content", {}).get("value", "")
        previous_cursor = entries[-1].get("content", {}).get("value", "")

        users: list[user_model.User] = []

        for user_data in entries[:-2]:
            user_result = user_data.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {})
            if user_result:
                users.append(user_model.User(user_result))

        return users, next_cursor, previous_cursor

    def get_muted_users(self, cursor: str = "") -> tuple[list[user_model.User], str, str]:
        """
        Retrieves a paginated list of users muted by the authenticated user.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            cursor (str, optional): Pagination cursor for the query.

        Returns:
            tuple: A tuple containing a list of muted users, next cursor, and previous cursor for pagination.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"count":20,"cursor":"{cursor}","includePromotedContent":false}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/7gmS7e2n-S0uFC1TqweqGA/MutedAccounts"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("viewer", {}).get("muting_timeline", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
        next_cursor = entries[-2].get("content", {}).get("value", "")
        previous_cursor = entries[-1].get("content", {}).get("value", "")

        users: list[user_model.User] = []

        for user_data in entries[:-2]:
            user_result = user_data.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {})
            if user_result:
                users.append(user_model.User(user_result))

        return users, next_cursor, previous_cursor
