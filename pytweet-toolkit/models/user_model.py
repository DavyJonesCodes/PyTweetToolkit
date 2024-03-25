class User:
    """
    Represents a user profile on Twitter, detailing both personal and professional attributes, 
    as well as engagement metrics and content preferences.

    Attributes encapsulate a comprehensive set of user-related information, ranging from basic profile details
    to more nuanced social and professional indicators. This includes verification status, follower counts, 
    profile media URLs, sensitivity settings, professional credentials, and features like the ability to highlight tweets.

    Attributes:
        id (str): The unique identifier for the user.
        rest_id (str): A RESTful identifier associated with the user, used in API interactions.
        is_blue_verified (bool): Indicates if the user has a verified blue checkmark.
        profile_image_shape (str): Shape of the user's profile image.
        can_dm (bool): Indicates if the user can receive direct messages from the viewer.
        can_media_tag (bool): Indicates if the user can be tagged in media.
        created_at (str): Timestamp for when the user's account was created.
        default_profile (bool): Indicates if the user has a default profile settings.
        default_profile_image (bool): Indicates if the user is using the default profile image.
        description (str): The user's self-description.
        fast_followers_count (int): Count of followers marked as 'fast' followers.
        favourites_count (int): The number of tweets this user has liked in the account's lifetime.
        followers_count (int): The number of followers this account currently has.
        friends_count (int): The number of users this account is following.
        has_custom_timelines (bool): Indicates if the user has created custom timelines.
        is_translator (bool): Indicates if the user is marked as a translator.
        listed_count (int): The number of public lists that this user is a member of.
        location (str): The location specified in the user's profile.
        media_count (int): The number of media uploads (photos and videos) by the user.
        name (str): The name of the user, as they've defined it.
        normal_followers_count (int): Count of followers not marked as 'fast'.
        pinned_tweet_ids_str (list): List of Tweet IDs pinned by the user.
        possibly_sensitive (bool): Indicates if the user has tweeted content marked as sensitive.
        profile_banner_url (str): The URL of the user's profile banner image.
        profile_image_url_https (str): HTTPS URL pointing to the user's profile image.
        profile_interstitial_type (str): Type of interstitial profile description.
        screen_name (str): The screen name, handle, or alias that this user identifies themselves with.
        statuses_count (int): The number of tweets (including retweets) issued by the user.
        translator_type (str): Indicates the level of translation capability.
        website_urls (list): List of URLs associated with the user, typically extracted from their profile description.
        verified (bool): Flag indicating whether the user is verified.
        withheld_in_countries (list): Countries where the user's content is withheld.
        professional_rest_id (str): RESTful ID associated with the user's professional profile.
        professional_type (str): Type of professional user.
        professional_category (list): Categories associated with the user's professional profile.
        verified_phone_status (bool): Indicates if the user's phone number is verified.
        legacy_extended_profile (dict): Extended profile details maintained for legacy support.
        is_profile_translatable (bool): Indicates if the user's profile can be translated.
        has_hidden_likes_on_profile (bool): Indicates if likes are hidden on the user's profile.
        has_hidden_subscriptions_on_profile (bool): Indicates if subscriptions are hidden on the user's profile.
        is_identity_verified (bool): Indicates if the user's identity has been verified.
        can_highlight_tweets (bool): Indicates if the user can highlight tweets on their profile.
        highlighted_tweets (dict): Details of tweets highlighted by the user on their profile.

    Methods:
        __str__(self) -> str:
            Provides a human-readable string representation of the User instance, summarizing its key details.

        to_dict(self) -> dict:
            Converts the User instance into a dictionary, primarily for serialization purposes.
            This method facilitates the integration of user data with APIs or storage solutions by providing
            a structured representation of the user's profile and settings.
    """

    def __init__(self, result_data: dict) -> None:
        """
        Initializes a new instance of the User class using data typically from a Twitter API response.

        Parameters:
            result_data (dict): A dictionary containing detailed information about a Twitter user, 
            as retrieved from a Twitter API response.
        """

        legacy_data = result_data.get("legacy", {})
        entities_data = legacy_data.get("entities", {})
        professional_data = result_data.get("professional", {})
        verification_info = result_data.get("verification_info", {})
        highlights_info = result_data.get("highlights_info", {})

        self.id = result_data.get("id")
        self.rest_id = result_data.get("rest_id")
        self.is_blue_verified = result_data.get("is_blue_verified", False)
        self.profile_image_shape = result_data.get("profile_image_shape")

        self.can_dm = legacy_data.get("can_dm", False)
        self.can_media_tag = legacy_data.get("can_media_tag", False)
        self.created_at = legacy_data.get("created_at")
        self.default_profile = legacy_data.get("default_profile", False)
        self.default_profile_image = legacy_data.get("default_profile_image", False)

        self.description = legacy_data.get("description", "").encode('utf-8').decode('unicode_escape').strip()
        for url in entities_data.get("description", {}).get("urls", []):
            self.description = self.description.replace(url.get("url", ""), url.get("expanded_url", ""))

        self.fast_followers_count = legacy_data.get("fast_followers_count", 0)
        self.favourites_count = legacy_data.get("favourites_count", 0)
        self.followers_count = legacy_data.get("followers_count", 0)
        self.friends_count = legacy_data.get("friends_count", 0)
        self.has_custom_timelines = legacy_data.get("has_custom_timelines", False)
        self.is_translator = legacy_data.get("is_translator", False)
        self.listed_count = legacy_data.get("listed_count", 0)
        self.location = legacy_data.get("location")
        self.media_count = legacy_data.get("media_count", 0)
        self.name = legacy_data.get("name")
        self.normal_followers_count = legacy_data.get("normal_followers_count", 0)
        self.pinned_tweet_ids_str = legacy_data.get("pinned_tweet_ids_str", [])
        self.possibly_sensitive = legacy_data.get("possibly_sensitive", False)
        self.profile_banner_url = legacy_data.get("profile_banner_url")
        self.profile_image_url_https = legacy_data.get("profile_image_url_https")
        self.profile_interstitial_type = legacy_data.get("profile_interstitial_type")
        self.screen_name = legacy_data.get("screen_name")
        self.statuses_count = legacy_data.get("statuses_count", 0)
        self.translator_type = legacy_data.get("translator_type")
        self.website_urls = [url.get("expanded_url") for url in entities_data.get("url", {}).get("urls", [])]
        self.verified = legacy_data.get("verified", False)
        self.withheld_in_countries = legacy_data.get("withheld_in_countries", [])

        self.professional_rest_id = professional_data.get("rest_id")
        self.professional_type = professional_data.get("professional_type")
        self.professional_category = professional_data.get("category", [])

        self.verified_phone_status = result_data.get("verified_phone_status", False)
        self.legacy_extended_profile = result_data.get("legacy_extended_profile", {})
        self.is_profile_translatable = result_data.get("is_profile_translatable", False)
        self.has_hidden_likes_on_profile = result_data.get("has_hidden_likes_on_profile", False)
        self.has_hidden_subscriptions_on_profile = result_data.get("has_hidden_subscriptions_on_profile", False)
        self.is_identity_verified = verification_info.get("is_identity_verified", False)
        self.can_highlight_tweets = highlights_info.get("can_highlight_tweets", False)
        self.highlighted_tweets = highlights_info.get("highlighted_tweets")

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the User instance, summarizing its key attributes.

        This method facilitates easy logging and debugging by providing a concise summary of the user's profile,
        including identification numbers, profile details, and engagement metrics.

        Returns:
            str: A string representation of the User instance.
        """

        user_str = (
            f"User ID: {self.id}\n"
            f"REST ID: {self.rest_id}\n"
            f"Is Blue Verified: {self.is_blue_verified}\n"
            f"Profile Image Shape: {self.profile_image_shape}\n"
            f"Can DM: {self.can_dm}\n"
            f"Can Media Tag: {self.can_media_tag}\n"
            f"Created At: {self.created_at}\n"
            f"Default Profile: {self.default_profile}\n"
            f"Default Profile Image: {self.default_profile_image}\n"
            f"Description: {self.description}\n"
            f"Fast Followers Count: {self.fast_followers_count}\n"
            f"Favourites Count: {self.favourites_count}\n"
            f"Followers Count: {self.followers_count}\n"
            f"Friends Count: {self.friends_count}\n"
            f"Has Custom Timelines: {self.has_custom_timelines}\n"
            f"Is Translator: {self.is_translator}\n"
            f"Listed Count: {self.listed_count}\n"
            f"Location: {self.location}\n"
            f"Media Count: {self.media_count}\n"
            f"Name: {self.name}\n"
            f"Normal Followers Count: {self.normal_followers_count}\n"
            f"Pinned Tweet IDs: {', '.join(self.pinned_tweet_ids_str)}\n"
            f"Possibly Sensitive: {self.possibly_sensitive}\n"
            f"Profile Banner URL: {self.profile_banner_url}\n"
            f"Profile Image URL (HTTPS): {self.profile_image_url_https}\n"
            f"Profile Interstitial Type: {self.profile_interstitial_type}\n"
            f"Screen Name: {self.screen_name}\n"
            f"Statuses Count: {self.statuses_count}\n"
            f"Translator Type: {self.translator_type}\n"
            f"Website URLs: {', '.join(self.website_urls)}\n"
            f"Verified: {self.verified}\n"
            f"Withheld In Countries: {', '.join(self.withheld_in_countries)}\n"
            f"Professional REST ID: {self.professional_rest_id}\n"
            f"Professional Type: {self.professional_type}\n"
            f"Professional Category: {', '.join([category.get('name', '') for category in self.professional_category])}\n"
            f"Verified Phone Status: {self.verified_phone_status}\n"
            f"Is Identity Verified: {self.is_identity_verified}\n"
            f"Can Highlight Tweets: {self.can_highlight_tweets}\n"
            f"Highlighted Tweets: {self.highlighted_tweets}\n"
        )
        return user_str.strip()

    def to_dict(self):
        """
        Converts the User instance into a dictionary for easier serialization, including all relevant user attributes.

        This method is particularly useful for serializing the User object to store in databases, send over networks, 
        or integrate with other APIs. It ensures that all user-related data is structured and easily accessible.

        Returns:
            dict: A dictionary representation of the User instance, containing all attributes as key-value pairs.
        """

        return {
            "id": self.id,
            "rest_id": self.rest_id,
            "is_blue_verified": self.is_blue_verified,
            "profile_image_shape": self.profile_image_shape,
            "can_dm": self.can_dm,
            "can_media_tag": self.can_media_tag,
            "created_at": self.created_at,
            "default_profile": self.default_profile,
            "default_profile_image": self.default_profile_image,
            "description": self.description,
            "fast_followers_count": self.fast_followers_count,
            "favourites_count": self.favourites_count,
            "followers_count": self.followers_count,
            "friends_count": self.friends_count,
            "has_custom_timelines": self.has_custom_timelines,
            "is_translator": self.is_translator,
            "listed_count": self.listed_count,
            "location": self.location,
            "media_count": self.media_count,
            "name": self.name,
            "normal_followers_count": self.normal_followers_count,
            "pinned_tweet_ids_str": self.pinned_tweet_ids_str,
            "possibly_sensitive": self.possibly_sensitive,
            "profile_banner_url": self.profile_banner_url,
            "profile_image_url_https": self.profile_image_url_https,
            "profile_interstitial_type": self.profile_interstitial_type,
            "screen_name": self.screen_name,
            "statuses_count": self.statuses_count,
            "translator_type": self.translator_type,
            "website_urls": self.website_urls,
            "verified": self.verified,
            "withheld_in_countries": self.withheld_in_countries,
            "professional_rest_id": self.professional_rest_id,
            "professional_type": self.professional_type,
            "professional_category": self.professional_category,
            "verified_phone_status": self.verified_phone_status,
            "legacy_extended_profile": self.legacy_extended_profile,
            "is_profile_translatable": self.is_profile_translatable,
            "has_hidden_likes_on_profile": self.has_hidden_likes_on_profile,
            "has_hidden_subscriptions_on_profile": self.has_hidden_subscriptions_on_profile,
            "is_identity_verified": self.is_identity_verified,
            "can_highlight_tweets": self.can_highlight_tweets,
            "highlighted_tweets": self.highlighted_tweets,
        }
