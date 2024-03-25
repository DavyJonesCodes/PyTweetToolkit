from .api import bookmark, friendship, interaction, notification, profile, restrictions, search, tweet, upload, user


class PyTweetClient(bookmark.BookmarkActions,
                    friendship.FriendshipActions,
                    interaction.InteractionActions,
                    notification.NotificationActions,
                    profile.ProfileActions,
                    restrictions.RestrictionActions,
                    search.SearchActions,
                    tweet.TweetActions,
                    upload.UploadActions,
                    user.UserActions):
    """
    A comprehensive client for interacting with various Twitter API endpoints.

    Inherits from multiple action classes to provide a wide range of functionalities,
    including bookmarking tweets, managing friendships, handling interactions, managing notifications,
    accessing user profiles, managing restrictions, performing searches, interacting with tweets,
    uploading media, and performing user-related actions.

    Attributes:
        auth_token (str): The authentication token for API requests.
        csrf_token (str): The CSRF token for authentication.

    Methods:
        All methods inherited from action classes such as BookmarkActions, FriendshipActions, etc.

    Inheritance Classes:
        - bookmark.BookmarkActions: Provides methods for bookmarking tweets and managing bookmarks.
        - friendship.FriendshipActions: Enables actions related to managing friendships, such as following and unfollowing users.
        - interaction.InteractionActions: Handles interactions like liking, retweeting, and replying to tweets.
        - notification.NotificationActions: Manages user notifications, including fetching notifications and marking them as read.
        - profile.ProfileActions: Facilitates accessing and updating user profiles.
        - restrictions.BlockActions: Handles blocking and unblocking users.
        - search.SearchActions: Allows searching for tweets and users.
        - tweet.TweetActions: Provides methods for fetching, creating, and deleting tweets.
        - upload.UploadActions: Enables uploading media files to Twitter.
        - user.UserActions: Performs user-related actions like fetching user profiles and followers.
    """

    def __init__(self, auth_token: str, csrf_token: str) -> None:
        """
        Initializes the PyTweetClient with the provided authentication tokens.

        Args:
            auth_token (str): The authentication token for API requests.
            csrf_token (str): The CSRF token for authentication.
        """
        super().__init__(auth_token, csrf_token)
