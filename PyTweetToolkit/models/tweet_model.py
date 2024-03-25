from . import user_model


class Tweet:
    """
    Represents a single tweet, encapsulating a wide range of data associated with a tweet on Twitter.
    This class is designed to process and store detailed information from a Twitter API response,
    including user data, tweet content, media attachments, and interaction metrics.

    Attributes:
        rest_id (str): The unique identifier for the tweet, as defined by Twitter.
        user (user_model.User): An instance of the User class representing the tweet's author.
        edit_tweet_ids (list): A list of tweet IDs related to this tweet's edit history, if any.
        editable_until_msecs (str): The timestamp until which the tweet is eligible for editing.
        is_edit_eligible (bool): Indicates whether the tweet is eligible for editing.
        edits_remaining (int): The number of edits remaining for the tweet.
        is_translatable (bool): Indicates whether the tweet can be translated.
        views (int): The view count of the tweet.
        quoted_tweet (Tweet): An instance of the Tweet class representing the tweet being quoted, if any.
        bookmark_count (int): The number of bookmarks for the tweet.
        bookmarked (bool): Indicates whether the tweet has been bookmarked by the current user.
        created_at (str): The creation time of the tweet.
        hashtags (list): A list of hashtags mentioned in the tweet.
        symbols (list): A list of symbols (e.g., stock tickers) mentioned in the tweet.
        timestamps (list): A list of timestamps mentioned in the tweet.
        urls (list): A list of URLs included in the tweet.
        user_mentions (list): A list of user mentions in the tweet.
        media (list): A list of media items (photos, videos, GIFs) attached to the tweet.
        favorite_count (int): The number of likes for the tweet.
        favorited (bool): Indicates whether the tweet has been liked by the current user.
        full_text (str): The full text of the tweet.
        in_reply_to_screen_name (str): The screen name of the user to whom the tweet is a reply.
        in_reply_to_tweet_id_str (str): The tweet ID to which this tweet is a reply.
        in_reply_to_user_id_str (str): The user ID to whom the tweet is a reply.
        is_reply (bool): Indicates whether the tweet is a reply to another tweet.
        is_quote_tweet (bool): Indicates whether the tweet quotes another tweet.
        quoted_tweet_id_str (str): The ID of the quoted tweet.
        quoted_tweet_permalink (str): The permalink of the quoted tweet.
        lang (str): The language code for the tweet.
        possibly_sensitive (bool): Indicates whether the tweet may contain sensitive content.
        possibly_sensitive_editable (bool): Indicates whether the tweet's sensitivity label can be edited.
        quote_count (int): The number of times the tweet has been quoted.
        reply_count (int): The number of replies to the tweet.
        retweet_count (int): The number of retweets of the tweet.
        retweeted (bool): Indicates whether the tweet has been retweeted by the current user.
        retweeted_tweet (Tweet): An instance of the Tweet class representing the original tweet if this is a retweet.

    Methods:
        __str__(self) -> str:
            Provides a human-readable string representation of the Tweet instance, summarizing its key details.

        to_dict(self) -> dict:
            Converts the Tweet instance into a dictionary, primarily for serialization purposes.
            This includes converting all user and tweet objects into their dictionary representations if applicable,
            facilitating the integration with APIs or storage solutions.
    """

    def __init__(self, result_data: dict) -> None:
        """
        Initializes a new instance of the Tweet class using data from a Twitter API response.

        Parameters:
            result_data (dict): A dictionary containing data from a Twitter API response for a tweet.
        """

        user_data = result_data.get("core", {}).get("user_results", {}).get("result", {})
        edit_data = result_data.get("edit_control", {})
        quoted_tweet_data = result_data.get("quoted_status_result", {}).get("result", {})
        legacy_data = result_data.get("legacy", {})
        entities_data = legacy_data.get("entities", {})
        extended_entities_data = legacy_data.get("extended_entities", {})
        retweeted_tweet_data = legacy_data.get("retweeted_status_result", {}).get("result", {})

        self.rest_id = result_data.get("rest_id")
        self.user = user_model.User(user_data)

        self.edit_tweet_ids = edit_data.get("edit_tweet_ids", [])
        self.editable_until_msecs = edit_data.get("editable_until_msecs")
        self.is_edit_eligible = edit_data.get("is_edit_eligible", False)
        self.edits_remaining = edit_data.get("edits_remaining", 0)

        self.is_translatable = result_data.get("is_translatable", False)
        self.views = result_data.get("views", {}).get("count", 0)

        self.quoted_tweet = Tweet(quoted_tweet_data) if quoted_tweet_data else {}

        self.bookmark_count = legacy_data.get("bookmark_count", 0)
        self.bookmarked = legacy_data.get("bookmarked", False)
        self.created_at = legacy_data.get("created_at")

        self.hashtags = entities_data.get("hashtags", [])
        self.symbols = entities_data.get("symbols", [])
        self.timestamps = entities_data.get("timestamps", [])
        self.urls = entities_data.get("urls", [])
        self.user_mentions = entities_data.get("user_mentions", [])

        self.media = [
            {
                "type": media.get("type"),
                "monetizable": media.get("monetizable", False),
                "allow_download": media.get("allow_download_status", {}).get("allow_download", False),
                "url": media.get("video_info", {}).get("variants", [{}])[-1].get("url")
                if media.get("type") in ["video", "animated_gif"] else media.get("media_url_https"),
            }
            for media in extended_entities_data.get("media", [])
        ]

        self.favorite_count = legacy_data.get("favorite_count", 0)
        self.favorited = legacy_data.get("favorited", False)

        self.full_text = legacy_data.get("full_text", "").encode('utf-8').decode('unicode_escape').strip()
        for url in self.urls:
            self.full_text = self.full_text.replace(url.get("url", ""), url.get("expanded_url", ""))
        for media in entities_data.get("media", []):
            self.full_text = self.full_text.replace(media.get("url", ""), "")

        self.in_reply_to_screen_name = legacy_data.get("in_reply_to_screen_name")
        self.in_reply_to_tweet_id_str = legacy_data.get("in_reply_to_status_id_str")
        self.in_reply_to_user_id_str = legacy_data.get("in_reply_to_user_id_str")
        self.is_reply = True if self.in_reply_to_screen_name else False

        self.is_quote_tweet = legacy_data.get("is_quote_status", False)
        self.quoted_tweet_id_str = legacy_data.get("quoted_status_id_str")
        self.quoted_tweet_permalink = legacy_data.get("quoted_status_permalink", {}).get("expanded")

        self.lang = legacy_data.get("lang")
        self.possibly_sensitive = legacy_data.get("possibly_sensitive", False)
        self.possibly_sensitive_editable = legacy_data.get("possibly_sensitive_editable", False)
        self.quote_count = legacy_data.get("quote_count", 0)
        self.reply_count = legacy_data.get("reply_count", 0)
        self.retweet_count = legacy_data.get("retweet_count", 0)
        self.retweeted = legacy_data.get("retweeted", False)

        self.retweeted_tweet = Tweet(retweeted_tweet_data) if retweeted_tweet_data else {}

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the Tweet instance, summarizing its key details.

        Returns:
            str: A string representation of the Tweet instance.
        """

        tweet_str = (
            f"Tweet ID: {self.rest_id}\n"
            f"User: {str(self.user)}\n"
            f"Edit Tweet IDs: {self.edit_tweet_ids}\n"
            f"Editable Until: {self.editable_until_msecs}\n"
            f"Is Edit Eligible: {self.is_edit_eligible}\n"
            f"Edits Remaining: {self.edits_remaining}\n"
            f"Is Translatable: {self.is_translatable}\n"
            f"Views: {self.views}\n"
            f"Quoted Tweet: {str(self.quoted_tweet)}\n"
            f"Bookmark Count: {self.bookmark_count}\n"
            f"Bookmarked: {self.bookmarked}\n"
            f"Created At: {self.created_at}\n"
            f"Hashtags: {self.hashtags}\n"
            f"Symbols: {self.symbols}\n"
            f"Timestamps: {self.timestamps}\n"
            f"URLs: {self.urls}\n"
            f"User Mentions: {self.user_mentions}\n"
            f"Media: {self.media}\n"
            f"Favorite Count: {self.favorite_count}\n"
            f"Favorited: {self.favorited}\n"
            f"Full Text: {self.full_text}\n"
            f"In Reply To Screen Name: {self.in_reply_to_screen_name}\n"
            f"In Reply To Tweet ID: {self.in_reply_to_tweet_id_str}\n"
            f"In Reply To User ID: {self.in_reply_to_user_id_str}\n"
            f"Is Reply: {self.is_reply}\n"
            f"Is Quote Tweet: {self.is_quote_tweet}\n"
            f"Quoted Tweet ID: {self.quoted_tweet_id_str}\n"
            f"Quoted Tweet Permalink: {self.quoted_tweet_permalink}\n"
            f"Language: {self.lang}\n"
            f"Possibly Sensitive: {self.possibly_sensitive}\n"
            f"Possibly Sensitive Editable: {self.possibly_sensitive_editable}\n"
            f"Quote Count: {self.quote_count}\n"
            f"Reply Count: {self.reply_count}\n"
            f"Retweet Count: {self.retweet_count}\n"
            f"Retweeted: {self.retweeted}\n"
            f"Retweeted Tweet: {str(self.retweeted_tweet)}\n"
        )
        return tweet_str.strip()

    def to_dict(self):
        """
        Converts the Tweet instance into a dictionary for easier serialization, including all nested user and tweet objects.

        Returns:
            dict: A dictionary representation of the Tweet instance, suitable for serialization.
        """

        user_dict = self.user.to_dict() if hasattr(self.user, 'to_dict') else str(self.user)
        quoted_tweet_dict = self.quoted_tweet.to_dict() if hasattr(self.quoted_tweet, 'to_dict') else self.quoted_tweet
        retweeted_tweet_dict = self.retweeted_tweet.to_dict() if hasattr(self.retweeted_tweet, 'to_dict') else self.retweeted_tweet

        return {
            "rest_id": self.rest_id,
            "user": user_dict,
            "edit_tweet_ids": self.edit_tweet_ids,
            "editable_until_msecs": self.editable_until_msecs,
            "is_edit_eligible": self.is_edit_eligible,
            "edits_remaining": self.edits_remaining,
            "is_translatable": self.is_translatable,
            "views": self.views,
            "quoted_tweet": quoted_tweet_dict,
            "bookmark_count": self.bookmark_count,
            "bookmarked": self.bookmarked,
            "created_at": self.created_at,
            "hashtags": self.hashtags,
            "symbols": self.symbols,
            "timestamps": self.timestamps,
            "urls": self.urls,
            "user_mentions": self.user_mentions,
            "media": self.media,
            "favorite_count": self.favorite_count,
            "favorited": self.favorited,
            "full_text": self.full_text,
            "in_reply_to_screen_name": self.in_reply_to_screen_name,
            "in_reply_to_tweet_id_str": self.in_reply_to_tweet_id_str,
            "in_reply_to_user_id_str": self.in_reply_to_user_id_str,
            "is_reply": self.is_reply,
            "is_quote_tweet": self.is_quote_tweet,
            "quoted_tweet_id_str": self.quoted_tweet_id_str,
            "quoted_tweet_permalink": self.quoted_tweet_permalink,
            "lang": self.lang,
            "possibly_sensitive": self.possibly_sensitive,
            "possibly_sensitive_editable": self.possibly_sensitive_editable,
            "quote_count": self.quote_count,
            "reply_count": self.reply_count,
            "retweet_count": self.retweet_count,
            "retweeted": self.retweeted,
            "retweeted_tweet": retweeted_tweet_dict,
        }
