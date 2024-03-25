from . import auth
from ..models import tweet_model, user_model, list_model


class SearchActions(auth.Auth):
    """
    Facilitates various search operations within Twitter, including searching for top content, latest tweets, people, media, and lists based on a query.

    Inherits from `auth.Auth` for handling authenticated requests.

    Rate Limits:
    - All search methods: 50 requests per 15-minute window.

    Attributes:
        None specified beyond those inherited from `auth.Auth`.

    Methods:
        search_top(query, cursor): Searches for top content related to the query.
        search_latest(query, cursor): Searches for the latest tweets related to the query.
        search_people(query, cursor): Searches for user profiles related to the query.
        search_media(query, cursor): Searches for media tweets related to the query.
        search_lists(query, cursor): Searches for lists related to the query.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes SearchActions with authentication tokens.

        Parameters:
            auth_token (str): Session authentication token.
            csrf_token (str): Token for CSRF protection.
        """

        super().__init__(auth_token, csrf_token)

    def search_top(self, query: str, cursor: str = "") -> tuple[list[user_model.User], list[tweet_model.Tweet], str, str]:
        """
        Searches for top content including users and tweets related to the provided query.

        Rate limit: 50 requests per 15-minute window.

        Parameters:
            query (str): The search query.
            cursor (str, optional): Pagination cursor for fetching a specific page of results.

        Returns:
            A tuple containing lists of user and tweet models, next cursor, and previous cursor.
        """

        users, lists, tweets, next_cursor, previous_cursor = self._search(query, "Top", cursor)
        return users, tweets, next_cursor, previous_cursor

    def search_latest(self, query: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Searches for the latest tweets related to the provided query.

        Rate limit: 50 requests per 15-minute window.

        Parameters:
            query (str): The search query.
            cursor (str, optional): Pagination cursor for fetching a specific page of results.

        Returns:
            A tuple containing a list of tweet models, next cursor, and previous cursor.
        """

        users, lists, tweets, next_cursor, previous_cursor = self._search(query, "Latest", cursor)
        return tweets, next_cursor, previous_cursor

    def search_people(self, query: str, cursor: str = "") -> tuple[list[user_model.User], str, str]:
        """
        Searches for user profiles related to the provided query.

        Rate limit: 50 requests per 15-minute window.

        Parameters:
            query (str): The search query.
            cursor (str, optional): Pagination cursor for fetching a specific page of results.

        Returns:
            A tuple containing a list of user models, next cursor, and previous cursor.
        """

        users, lists, tweets, next_cursor, previous_cursor = self._search(query, "People", cursor)
        return users, next_cursor, previous_cursor

    def search_media(self, query: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Searches for media tweets related to the provided query.

        Rate limit: 50 requests per 15-minute window.

        Parameters:
            query (str): The search query.
            cursor (str, optional): Pagination cursor for fetching a specific page of results.

        Returns:
            A tuple containing a list of tweet models with media, next cursor, and previous cursor.
        """

        users, lists, tweets, next_cursor, previous_cursor = self._search(query, "Media", cursor)
        return tweets, next_cursor, previous_cursor

    def search_lists(self, query: str, cursor: str = "") -> tuple[list[list_model.List], str, str]:
        """
        Searches for lists related to the provided query.

        Rate limit: 50 requests per 15-minute window.

        Parameters:
            query (str): The search query.
            cursor (str, optional): Pagination cursor for fetching a specific page of results.

        Returns:
            A tuple containing a list of list models, next cursor, and previous cursor.
        """

        users, lists, tweets, next_cursor, previous_cursor = self._search(query, "Lists", cursor)
        return lists, next_cursor, previous_cursor

    def _search(self, query: str, type: str, cursor: str = "") -> tuple[list[user_model.User], list[list_model.List], list[tweet_model.Tweet], str, str]:
        """
        Private method to perform the actual search operation.

        Parameters:
            query (str): The search query.
            type (str): The type of search (e.g., "Top", "Latest").
            cursor (str, optional): Pagination cursor for fetching a specific page of results.

        Returns:
            A tuple containing lists of user models, list models, tweet models, next cursor, and previous cursor.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"rawQuery":"{query}","count":40,"cursor":"{cursor}","querySource":"typed_query","product":"{type}"}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/flaR-PUMshxFWZWPNpq4zA/SearchTimeline"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("search_by_raw_query", {}).get("search_timeline", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
        next_cursor = entries[-1].get("content", {}).get("value", "")
        previous_cursor = entries[-2].get("content", {}).get("value", "")

        users: list[user_model.User] = []
        lists: list[list_model.List] = []
        tweets: list[tweet_model.Tweet] = []

        for entry in entries[:-2]:
            items = entry.get("content", {}).get("items", [])
            if items:
                if "user" in entry.get("entryID", "").lower():
                    for item in items:
                        user_result = item.get("item", {}).get("itemContent", {}).get("user_results", {}).get("result", {})
                        if user_result:
                            users.append(user_model.User(user_result))
                elif "list" in entry.get("entryID", "").lower():
                    for item in items:
                        list_result = item.get("item", {}).get("itemContent", {}).get("list", {})
                        if list_result:
                            lists.append(list_model.List(list_result))
                else:
                    for item in items:
                        tweet_result = item.get("item", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                        if tweet_result:
                            tweets.append(tweet_model.Tweet(tweet_result))

            else:
                if "user" in entry.get("entryID", "").lower():
                    user_result = item.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {})
                    if user_result:
                        users.append(user_model.User(user_result))
                elif "list" in entry.get("entryID", "").lower():
                    list_result = item.get("item", {}).get("itemContent", {}).get("list", {})
                    if list_result:
                        lists.append(list_model.List(list_result))
                else:
                    tweet_result = entry.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                    if tweet_result:
                        tweets.append(tweet_model.Tweet(tweet_result))

        return users, lists, tweets, next_cursor, previous_cursor
