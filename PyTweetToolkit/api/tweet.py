from . import auth
from ..models import tweet_model


class TweetActions(auth.Auth):
    """
    Manages tweet-related actions on Twitter, including retrieving user tweets, individual tweets, conversations, tweets from a list, and timelines, as well as creating and deleting tweets. This class leverages authenticated API requests for various tweet operations.

    Inherits from `auth.Auth` for using authentication tokens to secure API requests.

    Rate Limits:
    - get_user_tweets: 50 requests per 15-minute window.
    - get_tweet: 150 requests per 15-minute window.
    - get_tweet_conversation: 150 requests per 15-minute window.
    - get_tweets_from_list: 500 requests per 15-minute window.
    - get_for_you_timeline: 500 requests per 15-minute window.
    - get_following_timeline: 500 requests per 15-minute window.
    - create_tweet: Subject to Twitter's standard API rate limits.
    - delete_tweet: Subject to Twitter's standard API rate limits.

    Methods:
        get_user_tweets(user_id: str, cursor: str = "", is_reply=False, is_retweet=False) -> tuple[list[tweet_model.Tweet], str, str]:
            Fetches tweets posted by a specified user. Rate limit: 50 actions per 15 minutes.

        get_tweet(tweet_id: str) -> tweet_model.Tweet:
            Retrieves a single tweet by its ID. Rate limit: 150 actions per 15 minutes.

        get_tweet_conversation(tweet_id: str) -> list[tweet_model.Tweet]:
            Fetches the conversation thread for a given tweet. Rate limit: 150 actions per 15 minutes.

        get_tweets_from_list(list_id: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
            Retrieves tweets from a specified list. Rate limit: 500 actions per 15 minutes.

        get_for_you_timeline(cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
            Fetches tweets from the 'For You' timeline. Rate limit: 500 actions per 15 minutes.

        get_following_timeline(cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
            Retrieves tweets from the timeline of accounts a user follows. Rate limit: 500 actions per 15 minutes.

        create_tweet(content: str = "", media_ids: list = [], reply_to_tweet_id: str = None, quote_tweet_id: str = None) -> tweet_model.Tweet:
            Creates a new tweet. Subject to Twitter's standard API rate limits.

        delete_tweet(tweet_id: str) -> None:
            Deletes a specified tweet. Subject to Twitter's standard API rate limits.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes TweetActions with authentication tokens.

        Parameters:
            auth_token (str): Token for session authentication.
            csrf_token (str): Token for CSRF protection.
        """

        super().__init__(auth_token, csrf_token)

    def get_user_tweets(self, user_id: str, cursor: str = "", is_reply=False, is_retweet=False) -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Fetches tweets posted by a specified user. Includes options to filter for replies or retweets only.

        Rate limit: 50 requests per 15-minute window.

        Parameters:
            user_id (str): The user ID of the account whose tweets are being fetched.
            cursor (str, optional): Pagination cursor for the request.
            is_reply (bool, optional): Flag to filter for replies only.
            is_retweet (bool, optional): Flag to filter for retweets only.

        Returns:
            tuple: A list of Tweet models, next cursor, and previous cursor.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"userId":"{user_id}","count":20,"cursor":"{cursor}","includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/eS7LO5Jy3xgmd3dbL044EA/UserTweets"
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

        if is_reply:
            tweets = [tweet for tweet in tweets if tweet.is_reply]

        if is_retweet:
            tweets = [tweet for tweet in tweets if tweet.retweeted]

        return tweets, next_cursor, previous_cursor

    def get_tweet(self, tweet_id: str) -> tweet_model.Tweet:
        """
        Retrieves a single tweet by its ID. 

        Rate limit: 150 requests per 15-minute window.

        Parameters:
            tweet_id (str): The ID of the tweet to retrieve.

        Returns:
            tweet_model.Tweet: The retrieved tweet.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"focalTweetId":"{tweet_id}","with_rux_injections":false,"includePromotedContent":true,"withCommunity":true,"withQuickPromoteEligibilityTweetFields":true,"withBirdwatchNotes":true,"withVoice":true,"withV2Timeline":true}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
            'fieldToggles': '{"withArticleRichContentState":true}',
        }

        url = "https://twitter.com/i/api/graphql/ZkD-1KkxjcrLKp60DPY_dQ/TweetDetail"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("threaded_conversation_with_injections_v2", {}).get("instructions", [{}])[0].get("entries", [])

        tweet_result = {}

        for entry in entries:
            if tweet_id in entry.get("entryId", ""):
                tweet_result = entry.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                break

        tweet = tweet_model.Tweet(tweet_result)

        return tweet

    def get_tweet_conversation(self, tweet_id: str) -> list[tweet_model.Tweet]:
        """
        Fetches the conversation thread for a given tweet.

        Rate limit: 150 requests per 15-minute window.

        Parameters:
            tweet_id (str): The ID of the tweet to retrieve the conversation for.

        Returns:
            list[tweet_model.Tweet]: A list of tweets representing the conversation thread.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"focalTweetId":"{tweet_id}","with_rux_injections":false,"includePromotedContent":true,"withCommunity":true,"withQuickPromoteEligibilityTweetFields":true,"withBirdwatchNotes":true,"withVoice":true,"withV2Timeline":true}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
            'fieldToggles': '{"withArticleRichContentState":true}',
        }

        url = "https://twitter.com/i/api/graphql/ZkD-1KkxjcrLKp60DPY_dQ/TweetDetail"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("threaded_conversation_with_injections_v2", {}).get("instructions", [{}])[0].get("entries", [])

        tweets = []

        for entry in entries:
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

        return tweets

    def get_tweets_from_list(self, list_id: str, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Retrieves tweets from a specified list.

        Rate limit: 500 requests per 15-minute window.

        Parameters:
            list_id (str): The ID of the list from which to fetch tweets.
            cursor (str, optional): Pagination cursor for fetching tweets.

        Returns:
            tuple: A list of Tweet models, next cursor, and previous cursor.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        params = {
            'variables': f'{{"listId":"{list_id}","count":40,"cursor":"{cursor}"}}',
            'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }

        url = "https://twitter.com/i/api/graphql/TOTgqavWmxywKv5IbMMK1w/ListLatestTweetsTimeline"
        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("list", {}).get("tweets_timeline", {}).get("timeline", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
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

    def get_for_you_timeline(self, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Fetches tweets from the 'For You' timeline.

        Rate limit: 500 requests per 15-minute window.

        Parameters:
            cursor (str, optional): Pagination cursor for fetching tweets.

        Returns:
            tuple: A list of Tweet models, next cursor, and previous cursor.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'count': 50,
                'cursor': cursor,
                'includePromotedContent': True,
                'latestControlAvailable': True,
                'withCommunity': True,
                'seenTweetIds': [],
            },
            'features': {
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': True,
                'creator_subscriptions_tweet_preview_api_enabled': True,
                'responsive_web_graphql_timeline_navigation_enabled': True,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'c9s_tweet_anatomy_moderator_badge_enabled': True,
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                'view_counts_everywhere_api_enabled': True,
                'longform_notetweets_consumption_enabled': True,
                'responsive_web_twitter_article_tweet_consumption_enabled': True,
                'tweet_awards_web_tipping_enabled': False,
                'freedom_of_speech_not_reach_fetch_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                'rweb_video_timestamps_enabled': True,
                'longform_notetweets_rich_text_read_enabled': True,
                'longform_notetweets_inline_media_enabled': True,
                'responsive_web_enhance_cards_enabled': False,
            },
            'queryId': 'k3YiLNE_MAy5J-NANLERdg',
        }

        url = "https://twitter.com/i/api/graphql/k3YiLNE_MAy5J-NANLERdg/HomeTimeline"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=json_data,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("home", {}).get("home_timeline_urt", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
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

    def get_following_timeline(self, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Retrieves tweets from the timeline of accounts a user follows.

        Rate limit: 500 requests per 15-minute window.

        Parameters:
            cursor (str, optional): Pagination cursor for fetching tweets.

        Returns:
            tuple: A list of Tweet models, next cursor, and previous cursor.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'count': 100,
                'cursor': cursor,
                'includePromotedContent': True,
                'latestControlAvailable': True,
                'seenTweetIds': [],
            },
            'features': {
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': True,
                'creator_subscriptions_tweet_preview_api_enabled': True,
                'responsive_web_graphql_timeline_navigation_enabled': True,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'c9s_tweet_anatomy_moderator_badge_enabled': True,
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                'view_counts_everywhere_api_enabled': True,
                'longform_notetweets_consumption_enabled': True,
                'responsive_web_twitter_article_tweet_consumption_enabled': True,
                'tweet_awards_web_tipping_enabled': False,
                'freedom_of_speech_not_reach_fetch_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                'rweb_video_timestamps_enabled': True,
                'longform_notetweets_rich_text_read_enabled': True,
                'longform_notetweets_inline_media_enabled': True,
                'responsive_web_enhance_cards_enabled': False,
            },
            'queryId': 'U0cdisy7QFIoTfu3-Okw0A',
        }

        url = "https://twitter.com/i/api/graphql/U0cdisy7QFIoTfu3-Okw0A/HomeLatestTimeline"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            data=json_data,
        )

        json_response = response.json()
        entries = json_response.get("data", {}).get("home", {}).get("home_timeline_urt", {}).get("instructions", [{}])[-1].get("entries", [{}, {}])
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

    def create_tweet(self, content: str = "", media_ids: list = [], reply_to_tweet_id: str = None, quote_tweet_id: str = None) -> tweet_model.Tweet:
        """
        Creates a new tweet. Allows for specifying content, attaching media, replying to an existing tweet, or quoting a tweet.

        Subject to Twitter's standard API rate limits.

        Parameters:
            content (str, optional): The text content of the tweet.
            media_ids (list, optional): List of media IDs to attach to the tweet.
            reply_to_tweet_id (str, optional): The ID of the tweet to reply to.
            quote_tweet_id (str, optional): The ID of the tweet to quote.

        Returns:
            tweet_model.Tweet: The newly created tweet.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        if len(media_ids) > 4:
            raise ValueError("Only up to 4 media items can be uploaded at a time.")

        if not content and (media_ids is None or not media_ids):
            raise ValueError("You must provide at least one of 'content' or 'media_ids'.")

        json_data = {
            'variables': {
                'tweet_text': content,
                'dark_request': False,
                'media': {
                    'media_entities': [{'media_id': f'{media_id}', 'tagged_users': [], } for media_id in media_ids],
                    'possibly_sensitive': False,
                },
                'semantic_annotation_ids': [],
            },
            'features': {
                'c9s_tweet_anatomy_moderator_badge_enabled': True,
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                'view_counts_everywhere_api_enabled': True,
                'longform_notetweets_consumption_enabled': True,
                'responsive_web_twitter_article_tweet_consumption_enabled': True,
                'tweet_awards_web_tipping_enabled': False,
                'longform_notetweets_rich_text_read_enabled': True,
                'longform_notetweets_inline_media_enabled': True,
                'rweb_video_timestamps_enabled': True,
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': True,
                'freedom_of_speech_not_reach_fetch_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': True,
                'responsive_web_enhance_cards_enabled': False,
            },
            'queryId': 'sgqau0P5BUJPMU_lgjpd_w',
        }

        if reply_to_tweet_id:
            json_data["variables"]["reply"] = {
                'in_reply_to_tweet_id': reply_to_tweet_id,
                'exclude_reply_user_ids': [],
            }
            json_data["variables"]["batch_compose"] = "BatchSubsequent"

        elif quote_tweet_id:
            json_data["variables"]["attachment_url"] = f'https://twitter.com/elonmusk/status/{quote_tweet_id}'

        url = "https://twitter.com/i/api/graphql/sgqau0P5BUJPMU_lgjpd_w/CreateTweet"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            json=json_data,
        )

        json_response = response.json()

        tweet_result = json_response.get("data", {}).get("create_tweet", {}).get("tweet_results", {}).get("result", {})

        tweet = tweet_model.Tweet(tweet_result)

        return tweet

    def delete_tweet(self, tweet_id: str) -> None:
        """
        Deletes a specified tweet.

        Subject to Twitter's standard API rate limits.

        Parameters:
            tweet_id (str): The ID of the tweet to delete.

        Returns:
            None
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
                'dark_request': False,
            },
            'queryId': 'VaenaVgh5q5ih7kvyVjgtg',
        }
        url = "https://twitter.com/i/api/graphql/VaenaVgh5q5ih7kvyVjgtg/DeleteTweet"

        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            json=json_data,
        )
