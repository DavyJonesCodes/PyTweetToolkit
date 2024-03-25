from datetime import datetime

from . import auth, upload, user, tweet
from ..models import notification_model, tweet_model


class NotificationActions(auth.Auth):
    """
    Manages user notifications on Twitter, including fetching all notifications, verified notifications, 
    and mention notifications, utilizing the platform's API.

    Inherits from an authentication base class for API authentication.

    Rate Limits:
    - All notification retrieval methods: 180 actions per 15-minute window.

    Attributes:
        user_actions (user.UserActions): Instance for performing actions related to user accounts.
        upload_actions (upload.UploadActions): Instance for handling media uploads.
        tweet_actions (tweet.TweetActions): Instance for actions related to tweets.

    Methods:
        get_all_notifications(cursor: str = "") -> tuple[list[notification_model.Notification], str, str]:
            Retrieves all notifications for the authenticated user. Returns a list of notifications and pagination cursors.
            Rate limit: 180 actions per 15 minutes.

        get_verified_notifications(cursor: str = "") -> tuple[list[notification_model.Notification], str, str]:
            Retrieves notifications from verified accounts for the authenticated user. Returns a list of notifications and pagination cursors.
            Rate limit: 180 actions per 15 minutes.

        get_mention_notifications(cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
            Retrieves mention notifications for the authenticated user. Returns a list of tweets mentioning the user and pagination cursors.
            Rate limit: 180 actions per 15 minutes.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes NotificationActions with necessary authentication tokens for making API requests.

        Parameters:
            auth_token (str): Authentication token for session management.
            csrf_token (str): CSRF token for securing requests.
        """

        super().__init__(auth_token, csrf_token)
        self.user_actions = user.UserActions(auth_token, csrf_token)
        self.upload_actions = upload.UploadActions(auth_token, csrf_token)
        self.tweet_actions = tweet.TweetActions(auth_token, csrf_token)
        self.params = {
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
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': 'true',
            'include_ext_limited_action_results': 'true',
            'include_quote_count': 'true',
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': 'true',
            'include_entities': 'true',
            'include_user_entities': 'true',
            'include_ext_media_color': 'true',
            'include_ext_media_availability': 'true',
            'include_ext_sensitive_media_warning': 'true',
            'include_ext_trusted_friends_metadata': 'true',
            'send_error_codes': 'true',
            'simple_quoted_tweet': 'true',
            'count': '20',
            'ext': 'mediaStats,highlightedLabel,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }

    def get_all_notifications(self, cursor: str = "") -> tuple[list[notification_model.Notification], str, str]:
        """
        Fetches all notifications for the authenticated user, including likes, retweets, follows, and mentions.

        Rate limit: 180 actions per 15 minutes.

        Parameters:
            cursor (str, optional): Pagination cursor for fetching specific page of notifications.

        Returns:
            tuple: A tuple containing a list of Notification objects, the next cursor, and the previous cursor for pagination.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        self.params['cursor'] = f'{cursor}'

        url = "https://twitter.com/i/api/2/notifications/all.json"

        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=self.params,
        )

        json_response = response.json()
        notifications_data = json_response.get("globalObjects", {}).get("notifications", {})
        timeline = json_response.get("timeline", {}).get("instructions", [])
        entries = {}

        for event in timeline:
            if "addEntries" in event:
                entries = event
                break

        entries = entries.get("addEntries", {}).get("entries", [])

        next_cursor = entries[0].get("content", {}).get("value", "")
        previous_cursor = entries[-1].get("content", {}).get("value", "")

        notifications: list[notification_model.Notification] = []

        for _, data in notifications_data.items():
            tweet_ids = data.get("template", {}).get("aggregateUserActionsV1", {}).get("targetObjects", {})
            tweet_details = [self.tweet_actions.get_tweet(tweet_id) for tweet_id in tweet_ids]
            notifications.append(notification_model.Notification(data, tweet_details))

        notifications = sorted(notifications, key=lambda x: x.timestamp_ms, reverse=True)

        return notifications, next_cursor, previous_cursor

    def get_verified_notifications(self, cursor: str = "") -> tuple[list[notification_model.Notification], str, str]:
        """
        Fetches notifications from verified accounts for the authenticated user.

        Rate limit: 180 actions per 15 minutes.

        Parameters:
            cursor (str, optional): Pagination cursor for fetching specific page of notifications.

        Returns:
            tuple: A tuple containing a list of Notification objects from verified accounts, the next cursor, and the previous cursor.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        self.params['cursor'] = f'{cursor}'

        url = "https://twitter.com/i/api/2/notifications/verified.json"

        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=self.params,
        )

        json_response = response.json()
        notifications_data = json_response.get("globalObjects", {}).get("notifications", {})
        timeline = json_response.get("timeline", {}).get("instructions", [])
        entries = {}

        for event in timeline:
            if "addEntries" in event:
                entries = event
                break

        entries = entries.get("addEntries", {}).get("entries", [])

        next_cursor = entries[0].get("content", {}).get("value", "")
        previous_cursor = entries[-1].get("content", {}).get("value", "")

        notifications: list[notification_model.Notification] = []

        for _, data in notifications_data.items():
            tweet_ids = data.get("template", {}).get("aggregateUserActionsV1", {}).get("targetObjects", {})
            tweet_details = [self.tweet_actions.get_tweet(tweet_id) for tweet_id in tweet_ids]
            notifications.append(notification_model.Notification(data, tweet_details))

        notifications = sorted(notifications, key=lambda x: x.timestamp_ms, reverse=True)

        return notifications, next_cursor, previous_cursor

    def get_mention_notifications(self, cursor: str = "") -> tuple[list[tweet_model.Tweet], str, str]:
        """
        Fetches mention notifications for the authenticated user, showing tweets that mention the user.

        Rate limit: 180 actions per 15 minutes.

        Parameters:
            cursor (str, optional): Pagination cursor for fetching a specific page of mention notifications.

        Returns:
            tuple: A tuple containing a list of tweets mentioning the user, the next cursor, and the previous cursor for pagination.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        self.params['cursor'] = f'{cursor}'

        url = "https://twitter.com/i/api/2/notifications/mentions.json"

        response = self.request_handler.get(
            url,
            headers=headers,
            cookies=cookies,
            params=self.params,
        )

        json_response = response.json()
        tweets_data = json_response.get("globalObjects", {}).get("tweets", {})
        timeline = json_response.get("timeline", {}).get("instructions", [])
        entries = {}

        for event in timeline:
            if "addEntries" in event:
                entries = event
                break

        entries = entries.get("addEntries", {}).get("entries", [])

        next_cursor = entries[0].get("content", {}).get("value", "")
        previous_cursor = entries[-1].get("content", {}).get("value", "")

        tweets: list[tweet_model.Tweet] = []

        for tweet_id, _ in tweets_data.items():
            tweet_detail = self.tweet_actions.get_tweet(tweet_id)
            tweets.append(tweet_detail)

        date_format = "%a %b %d %H:%M:%S %z %Y"

        tweets = sorted(tweets, key=lambda x: datetime.strptime(x.created_at, date_format), reverse=True)

        return tweets, next_cursor, previous_cursor
