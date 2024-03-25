from . import auth, tweet
from ..models import tweet_model


class BookmarkActions(auth.Auth):
    """
    Handles bookmark actions for tweets on Twitter, leveraging the platform's GraphQL API for managing bookmarks.

    Inherits from an authentication base class and uses TweetActions for tweet interactions. Offers methods for
    bookmarking a tweet, removing a bookmark, and retrieving bookmarked tweets, with explicit mention of API rate limits.

    Rate Limits:
    - bookmark_tweet: 500 actions per 15-minute window.
    - unbookmark_tweet: 500 actions per 15-minute window.
    - get_bookmarks: 500 actions per 15-minute window.

    Attributes:
        tweet_actions (tweet.TweetActions): Instance for fetching tweet details.

    Methods:
        bookmark_tweet(tweet_id: str) -> tweet_model.Tweet:
            Bookmarks a tweet by ID. Rate limit: 500 actions per 15 minutes.

        unbookmark_tweet(tweet_id: str) -> tweet_model.Tweet:
            Removes a bookmark from a tweet by ID. Rate limit: 500 actions per 15 minutes.

        get_bookmarks(cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
            Retrieves a list of bookmarked tweets with pagination cursors. Rate limit: 500 actions per 15 minutes.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes the BookmarkActions instance with authentication tokens necessary for making API requests.

        Parameters:
            auth_token (str): The authentication token for session management.
            csrf_token (str): The CSRF token for securing requests against CSRF attacks.
        """

        super().__init__(auth_token, csrf_token)
        self.tweet_actions = tweet.TweetActions(auth_token, csrf_token)

    def bookmark_tweet(self, tweet_id: str) -> tweet_model.Tweet:
        """
        Adds a bookmark to a specified tweet.

        Rate limit: 500 actions per 15 minutes.

        Parameters:
            tweet_id (str): ID of the tweet to bookmark.

        Returns:
            tweet_model.Tweet: Instance representing the bookmarked tweet.

        Raises:
            HTTP errors or specific exceptions based on API response.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
            },
            'queryId': 'aoDbu3RHznuiSkQ9aNM67Q',
        }

        url = "https://twitter.com/i/api/graphql/aoDbu3RHznuiSkQ9aNM67Q/CreateBookmark"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            json=json_data,
        )

        return self.tweet_actions.get_tweet(tweet_id)

    def unbookmark_tweet(self, tweet_id: str) -> tweet_model.Tweet:
        """
        Removes a bookmark from a specified tweet. 

        Rate limit: 500 actions per 15 minutes.

        Parameters:
            tweet_id (str): ID of the tweet to unbookmark.

        Returns:
            tweet_model.Tweet: Instance representing the tweet post-unbookmark.

        Raises:
            HTTP errors or specific exceptions based on API response.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
            },
            'queryId': 'Wlmlj2-xzyS1GN3a6cj-mQ',
        }

        url = "https://twitter.com/i/api/graphql/Wlmlj2-xzyS1GN3a6cj-mQ/DeleteBookmark"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            json=json_data,
        )

        return self.tweet_actions.get_tweet(tweet_id)

    def get_bookmarks(self, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Fetches bookmarked tweets with pagination. 

        Rate limit: 500 actions per 15 minutes.

        Parameters:
            cursor (str, optional): Pagination cursor for bookmark retrieval.

        Returns:
            tuple[list[tweet_model.Tweet], str, str]: Bookmarked tweets, next and previous cursors.

        Raises:
            HTTP errors or specific exceptions based on API response.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"count":20,"cursor":"{cursor}","includePromotedContent":true}}',
            'features': '{"graphql_timeline_v2_bookmark_timeline":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/uNowfj04D8HFVFMbjm6xrQ/Bookmarks"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("bookmark_timeline_v2", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
        next_cursor = entries[-1].get("content", {}).get("value", "")
        previous_cursor = entries[-2].get("content", {}).get("value", "")

        tweets: list[tweet_model.Tweet] = []

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
