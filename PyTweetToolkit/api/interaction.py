from . import auth, tweet
from ..models import tweet_model


class InteractionActions(auth.Auth):
    """
    Facilitates interactions with tweets on Twitter, such as liking, unliking, retweeting, deleting retweets, 
    and creating replies, utilizing the platform's API.

    Inherits authentication mechanisms from the base class and employs TweetActions for tweet-related operations.

    Rate Limits:
    - like_tweet: 500 actions per 15-minute window.
    - unlike_tweet: 500 actions per 15-minute window.
    - create_retweet: Subject to Twitter's standard API rate limits.
    - delete_retweet: Subject to Twitter's standard API rate limits.
    - create_reply: Subject to Twitter's standard API rate limits.

    Attributes:
        tweet_actions (tweet.TweetActions): An instance for performing actions on tweets.

    Methods:
        like_tweet(tweet_id: str) -> str:
            Likes a tweet given its ID. Returns 'Success' or 'Failed'. Rate limit: 500 actions per 15 minutes.

        unlike_tweet(tweet_id: str) -> str:
            Unlikes a tweet given its ID. Returns 'Success' or 'Failed'. Rate limit: 500 actions per 15 minutes.

        create_retweet(source_tweet_id: str) -> tweet_model.Tweet:
            Creates a retweet for a given source tweet ID. Returns the retweet details. Rate limit: Subject to Twitter's standard API rate limits.

        delete_retweet(source_tweet_id: str) -> tweet_model.Tweet:
            Deletes a retweet given the source tweet ID. Returns the original tweet details. Rate limit: Subject to Twitter's standard API rate limits.

        create_reply(reply_to_tweet_id: str, content: str = "", media_ids: list = []) -> tweet_model.Tweet:
            Creates a reply to a tweet, optionally with content and media. Returns the reply tweet details. Rate limit: Subject to Twitter's standard API rate limits.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes InteractionActions with necessary authentication tokens for making API requests.

        Parameters:
            auth_token (str): Authentication token for session management.
            csrf_token (str): CSRF token for request security.
        """

        super().__init__(auth_token, csrf_token)
        self.tweet_actions = tweet.TweetActions(auth_token, csrf_token)

    def like_tweet(self, tweet_id: str) -> str:
        """
        Likes a tweet given its ID.

        Rate limit: 500 actions per 15 minutes.

        Parameters:
            tweet_id (str): The ID of the tweet to be liked.

        Returns:
            str: 'Success' if the tweet was liked successfully, 'Failed' otherwise.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
            },
            'queryId': 'lI07N6Otwv1PhnEgXILM7A',
        }

        url = "https://twitter.com/i/api/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            json=json_data,
        )

        if response.status_code == 200:
            return "Success"

        return "Failed"

    def unlike_tweet(self, tweet_id: str) -> str:
        """
        Unlikes a tweet given its ID.

        Rate limit: 500 actions per 15 minutes.

        Parameters:
            tweet_id (str): The ID of the tweet to be unliked.

        Returns:
            str: 'Success' if the tweet was unliked successfully, 'Failed' otherwise.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
            },
            'queryId': 'ZYKSe-w7KEslx3JhSIk5LA',
        }

        url = "https://twitter.com/i/api/graphql/ZYKSe-w7KEslx3JhSIk5LA/UnfavoriteTweet"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            json=json_data,
        )

        if response.status_code == 200:
            return "Success"

        return "Failed"

    def create_retweet(self, source_tweet_id: str) -> tweet_model.Tweet:
        """
        Creates a retweet for a given source tweet ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            source_tweet_id (str): The ID of the tweet to be retweeted.

        Returns:
            tweet_model.Tweet: An instance of the retweeted tweet details.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'tweet_id': str(source_tweet_id),
                'dark_request': False,
            },
            'queryId': 'ojPdsZsimiJrUGLR1sjUtA',
        }

        url = "https://twitter.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            json=json_data,
        )

        json_response = response.json()
        tweet_id = json_response.get("data", {}).get("create_retweet", {}).get("retweet_results", {}).get("result", {}).get("rest_id")

        if tweet_id:
            tweet = self.tweet_actions.get_tweet(tweet_id)
        else:
            tweet = tweet_model.Tweet({})

        return tweet

    def delete_retweet(self, source_tweet_id: str) -> tweet_model.Tweet:
        """
        Deletes a retweet given the source tweet ID.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            source_tweet_id (str): The ID of the source tweet whose retweet is to be deleted.

        Returns:
            tweet_model.Tweet: An instance of the original tweet details.
        """

        headers = self._get_headers()
        cookies = self._get_cookies()

        json_data = {
            'variables': {
                'source_tweet_id': str(source_tweet_id),
                'dark_request': False,
            },
            'queryId': 'iQtK4dl5hBmXewYZuEOKVw',
        }

        url = "https://twitter.com/i/api/graphql/iQtK4dl5hBmXewYZuEOKVw/DeleteRetweet"
        response = self.request_handler.post(
            url,
            headers=headers,
            cookies=cookies,
            json=json_data,
        )

        json_response = response.json()
        tweet_id = json_response.get("data", {}).get("unretweet", {}).get("source_tweet_results", {}).get("result", {}).get("rest_id")

        if tweet_id:
            tweet = self.tweet_actions.get_tweet(tweet_id)
        else:
            tweet = tweet_model.Tweet({})

        return tweet

    def create_reply(self, reply_to_tweet_id: str, content: str = "", media_ids: list = []) -> tweet_model.Tweet:
        """
        Creates a reply to a tweet, optionally with content and media.

        Rate limit: Subject to Twitter's standard API rate limits.

        Parameters:
            reply_to_tweet_id (str): The ID of the tweet to reply to.
            content (str, optional): The content of the reply.
            media_ids (list, optional): A list of media IDs to attach to the reply.

        Returns:
            tweet_model.Tweet: An instance of the reply tweet details.
        """

        return self.tweet_actions.create_tweet(content=content, media_ids=media_ids, reply_to_tweet_id=reply_to_tweet_id)
