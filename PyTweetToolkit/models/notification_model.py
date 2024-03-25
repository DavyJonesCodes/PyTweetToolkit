from . import tweet_model


class Notification:
    """
    Represents a Twitter Notification, encapsulating the details and context of a notification event on Twitter.
    This class processes notification data, including related tweets and user information, to provide a structured
    representation of a notification event.

    Attributes:
        id (str): The unique identifier for the notification.
        timestamp_ms (str): The timestamp of the notification in milliseconds.
        icon (str): An identifier for the icon associated with the notification.
        message (str): The notification message text.
        tweet_ids (dict): A dictionary containing IDs of tweets related to the notification.
        user_ids (dict): A dictionary containing IDs of users related to the notification.
        additional_info (dict): A dictionary containing additional context or information related to the notification.
        tweet_details (list[tweet_model.Tweet]): A list of `Tweet` objects representing the tweets associated with the notification.

    Methods:
        __str__(self) -> str:
            Provides a human-readable string representation of the Notification instance.

        to_dict(self) -> dict:
            Converts the Notification instance into a dictionary, primarily for serialization purposes. 
            This includes converting tweet details into dictionaries if they implement the 'to_dict' method, 
            providing a structured representation of the notification suitable for serialization.
    """

    def __init__(self, result_data: dict, tweet_detials: list[tweet_model.Tweet]) -> None:
        """
        Initializes a new instance of the Notification class using data from a Twitter API response
        and a list of tweet details.

        Parameters:
            result_data (dict): A dictionary containing data from a Twitter API response for a notification.
            tweet_details (list[tweet_model.Tweet]): A list of `Tweet` objects representing the tweets associated with the notification.
        """

        self.id = result_data.get("id")
        self.timestamp_ms = result_data.get("timestampMs")
        self.icon = result_data.get("icon", {}).get("id")
        self.message = result_data.get("message", {}).get("text")
        self.tweet_ids = result_data.get("template", {}).get("aggregateUserActionsV1", {}).get("targetObjects", {})
        self.user_ids = result_data.get("template", {}).get("aggregateUserActionsV1", {}).get("fromUsers", {})
        self.additional_info = result_data.get("template", {}).get("aggregateUserActionsV1", {}).get("additionalContext", {}).get("contextText", {}).get("text", {})
        self.tweet_details = tweet_detials

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the Notification instance.

        Returns:
            str: A string representation of the Notification instance.
        """

        notification_str = (
            f"ID: {self.id}\n"
            f"Time Stamp Ms: {self.timestamp_ms}\n"
            f"Icon: {self.icon}\n"
            f"Message: {self.message}\n"
            f"Tweet IDs: {self.tweet_ids}\n"
            f"User IDs: {self.user_ids}\n"
            f"Additional Info: {self.additional_info}\n"
            f"Tweet Details: {str(self.tweet_details)}"
        )
        return notification_str.strip()

    def to_dict(self):
        """
        Converts the Notification instance into a dictionary for easier serialization.

        Returns:
            dict: A dictionary representation of the Notification instance, suitable for serialization. 
            This includes a list of tweets associated with the notification, converted into dictionaries if applicable.
        """

        return {
            "id": self.id,
            "timestamp": self.timestamp_ms,
            "icon": self.icon,
            "message": self.message,
            "tweet_ids": self.tweet_ids,
            "user_ids": self.user_ids,
            "additional_info": self.additional_info,
            "tweet_details": [tweet.to_dict() for tweet in self.tweet_details] if self.tweet_details and all(hasattr(tweet, 'to_dict') for tweet in self.tweet_details) else self.tweet_details
        }
