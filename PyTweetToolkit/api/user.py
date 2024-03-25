from . import auth, tweet
from ..models import user_model, tweet_model


class UserActions(auth.Auth):
    """
    Manages actions related to Twitter users, such as retrieving user profiles, their followers, followings, media content, likes, and retweets, using authenticated API requests. This class is designed to interact with various endpoints to fetch detailed information about Twitter users and their activities.

    Inherits from `auth.Auth` to utilize authentication tokens for secured API requests.

    Rate Limits:
    - get_user_by_screen_name: 95 requests per 15-minute window.
    - get_user_following: 500 requests per 15-minute window.
    - get_user_followers: 50 requests per 15-minute window.
    - get_user_media: 500 requests per 15-minute window.
    - get_user_likes: 500 requests per 15-minute window.
    - get_user_retweets: Subject to Twitter's standard API rate limits.

    Attributes:
        tweet_actions (tweet.TweetActions): Utilized for actions on tweets, aiding in operations like fetching user retweets.

    Methods:
        get_user_by_screen_name(screen_name: str) -> user_model.User:
            Fetches a user's profile by their screen name. Rate limit: 95 actions per 15 minutes.

        get_user_following(user_id: str, cursor: str = "") -> tuple[list[user_model.User], str, str]:
            Retrieves the users followed by a specified user. Rate limit: 500 actions per 15 minutes.

        get_user_followers(user_id: str, cursor: str = "") -> tuple[list[user_model.User], str, str]:
            Fetches the followers of a specified user. Rate limit: 50 actions per 15 minutes.

        get_user_media(user_id: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
            Retrieves media content posted by a specified user. Rate limit: 500 actions per 15 minutes.

        get_user_likes(user_id: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
            Fetches tweets liked by a specified user. Rate limit: 75 actions per 15 minutes.

        get_user_retweets(user_id: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
            Retrieves tweets retweeted by a specified user. Subject to Twitter's standard API rate limits.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes UserActions with authentication tokens required for making API requests.

        Parameters:
            auth_token (str): The authentication token for session management.
            csrf_token (str): The CSRF token for securing requests against CSRF attacks.
        """

        super().__init__(auth_token, csrf_token)
        self.tweet_actions = tweet.TweetActions(auth_token, csrf_token)

    def get_user_by_screen_name(self, screen_name: str) -> user_model.User:
        """
        Fetches a Twitter user's profile by their screen name. 

        Rate limit: 95 requests per 15-minute window.

        Parameters:
            screen_name (str): The screen name of the user.

        Returns:
            user_model.User: The user's profile data encapsulated in a User model.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"screen_name":"{screen_name}","withSafetyModeUserFields":true}}',
            'features': '{"hidden_profile_likes_enabled":true,"hidden_profile_subscriptions_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
            'fieldToggles': '{"withAuxiliaryUserLabels":false}',
        }

        url = "https://twitter.com/i/api/graphql/k5XapwcSikNsEsILW5FvgA/UserByScreenName"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json().get("data", {}).get("user", {}).get("result", {})

        return user_model.User(json_response)

    def get_user_following(self, user_id: str, cursor: str = "") -> tuple[list[user_model.User], str, str]:
        """
        Retrieves the users followed by a specified user.

        Rate limit: 500 requests per 15-minute window.

        Parameters:
            user_id (str): The user ID.
            cursor (str, optional): Pagination cursor.

        Returns:
            tuple: A list of User models, next cursor, and previous cursor.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"userId":"{user_id}","count":50,"cursor":"{cursor}","includePromotedContent":false}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/PiHWpObvX9tbClrUl6rL9g/Following"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("user", {}).get("result", {}).get("timeline", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
        next_cursor = entries[-2].get("content", {}).get("value", "")
        previous_cursor = entries[-1].get("content", {}).get("value", "")

        following = []

        for user_data in entries[:-2]:
            user_result = user_data.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {})
            if user_result:
                following.append(user_model.User(user_result))

        return following, next_cursor, previous_cursor

    def get_user_followers(self, user_id: str, cursor: str = "") -> tuple[list[user_model.User], str, str]:
        """
        Fetches the followers of a specified user.

        Rate limit: 50 requests per 15-minute window.

        Parameters:
            user_id (str): The user ID.
            cursor (str, optional): Pagination cursor.

        Returns:
            tuple: A list of User models, next cursor, and previous cursor.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"userId":"{user_id}","count":50,"cursor":"{cursor}","includePromotedContent":false}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/Uc7ZOJrxsJAzMVCcaxis8Q/Followers"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("user", {}).get("result", {}).get("timeline", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
        next_cursor = entries[-2].get("content", {}).get("value", "")
        previous_cursor = entries[-1].get("content", {}).get("value", "")

        followers = []

        for user_data in entries[:-2]:
            user_result = user_data.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {})
            if user_result:
                followers.append(user_model.User(user_result))

        return followers, next_cursor, previous_cursor

    def get_user_media(self, user_id: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Retrieves media content (images, videos) posted by the specified user.

        Rate limit: 500 requests per 15-minute window.

        Parameters:
            user_id (str): The user ID for which to retrieve media content.
            cursor (str, optional): Pagination cursor for fetching specific sets of results.

        Returns:
            tuple: A list of Tweet models containing media, along with next and previous cursors for pagination.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"userId":"{user_id}","count":20,"cursor":"{cursor}","includePromotedContent":false,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":true,"withV2Timeline":true}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/TOU4gQw8wXIqpSzA4TYKgg/UserMedia"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("user", {}).get("result", {}).get("timeline_v2", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
        next_cursor = entries[-1].get("content", {}).get("value", "")
        previous_cursor = entries[-2].get("content", {}).get("value", "")

        tweets = []

        for entry in entries[:-2]:
            items = entry.get("content", {}).get("items", [])
            if items:
                for item in items:
                    tweet_result = item.get("item", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                    if tweet_result:
                        tweets.append(tweet_model.Tweet(tweet_result))

            else:
                tweet_result = entry.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                if tweet_result:
                    tweets.append(tweet_model.Tweet(tweet_result))

        return tweets, next_cursor, previous_cursor

    def get_user_likes(self, user_id: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Fetches tweets liked by the specified user, providing insight into the user's preferences.

        Rate limit: 500 requests per 15-minute window.

        Parameters:
            user_id (str): The ID of the user whose likes are being queried.
            cursor (str, optional): Pagination cursor to retrieve specific pages of results.

        Returns:
            tuple: A list of Tweet models that the user has liked, accompanied by next and previous cursors for pagination.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"userId":"{user_id}","count":100,"cursor":"{cursor}","includePromotedContent":false,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":true,"withV2Timeline":true}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/B8I_QCljDBVfin21TTWMqA/Likes"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()

        entries = json_response.get("data", {}).get("user", {}).get("result", {}).get("timeline_v2", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
        next_cursor = entries[-1].get("content", {}).get("value", "")
        previous_cursor = entries[-2].get("content", {}).get("value", "")

        tweets = []

        for entry in entries[:-2]:
            items = entry.get("content", {}).get("items", [])
            if items:
                for item in items:
                    tweet_result = item.get("item", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                    if tweet_result:
                        tweets.append(tweet_model.Tweet(tweet_result))

            else:
                tweet_result = entry.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                if tweet_result:
                    tweets.append(tweet_model.Tweet(tweet_result))

        return tweets, next_cursor, previous_cursor

    def get_user_retweets(self, user_id: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Collects tweets retweeted by the specified user, showcasing the content they have chosen to share with their followers.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            user_id (str): The ID of the user whose retweets are being queried.
            cursor (str, optional): Pagination cursor to access different pages of results.

        Returns:
            tuple: A list of Tweet models that have been retweeted by the user, with next and previous cursors for pagination.
        """

        return self.tweet_actions.get_user_tweets(user_id=user_id, cursor=cursor, is_retweet=True)
