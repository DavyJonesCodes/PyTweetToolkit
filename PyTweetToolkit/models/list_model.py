from . import user_model


class List:
    """
    Represents a Twitter List, encapsulating details and metrics associated with a list on Twitter.
    This class parses and stores information from a Twitter API response related to a specific list,
    including its metadata, owner details, and social engagement metrics.

    Attributes:
        created_at (str): Timestamp for when the list was created on Twitter.
        custom_banner_media_url (str): URL for the list's custom banner image, if available.
        default_banner_media_url (str): URL for the list's default banner image, if available.
        description (str): The description of the list as provided by the list creator.
        facepile_urls (list): URLs of profile images for users featured in the list, if any.
        is_following (bool): Indicates if the authenticated user is following this list.
        id (int): The unique identifier for the list on Twitter.
        rest_id (str): The string representation of the list's unique identifier.
        is_member (bool): Indicates if the authenticated user is a member of this list.
        member_count (int): The number of users who are members of the list.
        mode (str): The visibility mode of the list (e.g., "public" or "private").
        muting (bool): Indicates if the list is muted by the authenticated user.
        name (str): The name of the list as given by the list creator.
        pinning (bool): Indicates if the list is pinned by the authenticated user.
        subscriber_count (int): The number of subscribers this list has.
        owner (user_model.User): An object representing the owner of the list.

    Methods:
        __str__(self) -> str:
            Provides a human-readable string representation of the Twitter List instance.

        to_dict(self) -> dict:
            Converts the Twitter List instance into a dictionary, primarily for serialization purposes.
            This includes converting the owner attribute to a dictionary if it has a 'to_dict' method,
            otherwise, the owner attribute is converted to a string representation.
    """

    def __init__(self, result_data: dict) -> None:
        """
        Initializes a new instance of the List class using data from a Twitter API response.

        Parameters:
            result_data (dict): A dictionary containing data from a Twitter API response for a list.
        """

        user_data = result_data.get("user_results", {}).get("result", {})

        self.created_at = result_data.get("created_at")
        self.custom_banner_media_url = result_data.get("custom_banner_media", {}).get("media_info", {}).get("original_img_url")
        self.default_banner_media_url = result_data.get("default_banner_media", {}).get("media_info", {}).get("original_img_url")
        self.description = result_data.get("description")
        self.facepile_urls = result_data.get("facepile_urls", [])
        self.is_following = result_data.get("following")
        self.id = result_data.get("id")
        self.rest_id = result_data.get("id_str")
        self.is_member = result_data.get("is_member")
        self.member_count = result_data.get("member_count")
        self.mode = result_data.get("mode")
        self.muting = result_data.get("muting")
        self.name = result_data.get("name")
        self.pinning = result_data.get("pinning")
        self.subscriber_count = result_data.get("subscriber_count")
        self.owner = user_model.User(user_data)

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the Twitter List instance.

        Returns:
            str: A string representation of the Twitter List instance.
        """

        list_str = (
            f"ID: {self.id}\n"
            f"Rest ID: {self.rest_id}\n"
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Created At: {self.created_at}\n"
            f"Custom Banner Media URL: {self.custom_banner_media_url}\n"
            f"Default Banner Media URL: {self.default_banner_media_url}\n"
            f"Owner: {str(self.owner)}\n"
            f"Is Following: {self.is_following}\n"
            f"Is Member: {self.is_member}\n"
            f"Member Count: {self.member_count}\n"
            f"Mode: {self.mode}\n"
            f"Is Muting: {self.muting}\n"
            f"Pinning: {self.pinning}\n"
            f"Subscriber Count: {self.subscriber_count}\n"
            f"Facepile URLs: {self.facepile_urls}"
        )
        return list_str.strip()

    def to_dict(self):
        """
        Returns a human-readable string representation of the Twitter List instance.

        Returns:
            str: A string representation of the Twitter List instance.
        """

        owner_dict = self.owner.to_dict() if hasattr(self.owner, 'to_dict') else str(self.owner)

        return {
            "created_at": self.created_at,
            "custom_banner_media_url": self.custom_banner_media_url,
            "default_banner_media_url": self.default_banner_media_url,
            "description": self.description,
            "facepile_urls": self.facepile_urls,
            "is_following": self.is_following,
            "id": self.id,
            "rest_id": self.rest_id,
            "is_member": self.is_member,
            "member_count": self.member_count,
            "mode": self.mode,
            "muting": self.muting,
            "name": self.name,
            "pinning": self.pinning,
            "subscriber_count": self.subscriber_count,
            "owner": owner_dict,
        }
