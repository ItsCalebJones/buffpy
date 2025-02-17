from typing import List
from urllib.parse import quote

from buffpy.models.update import Update


PATHS = {
    "GET_PENDING": "profiles/%s/updates/pending.json",
    "GET_SENT": "profiles/%s/updates/sent.json",
    "SHUFFLE": "profiles/%s/updates/shuffle.json",
    "REORDER": "profiles/%s/updates/reorder.json",
    "CREATE": "updates/create.json",
}


class Updates(list):
    """
        Implenents all the profiles and updates logic:

            * retrieve updates related to a profile.
            * create a new update.
            * reorder and shuffle updates.
    """

    def __init__(self, api, profile_id: str):
        self.api = api
        self.profile_id = profile_id

        self.__pending = []
        self.__sent = []

    @property
    def pending(self) -> List[Update]:
        """
            Returns an array of updates that are currently in buffer for an
            individual social media profile.
        """

        url = PATHS["GET_PENDING"].format(self.profile_id)
        response = self.api.get(url=url)

        self.__pending = [
            Update(api=self.api, raw_response=update)
            for update in response.get("response", [])
        ]

        return self.__pending

    @property
    def sent(self) -> List[Update]:
        """
            Returns an array of updates that have been sent from buffer for an
            individual social media profile.
        """

        url = PATHS["GET_SENT"] % self.profile_id
        response = self.api.get(url=url)

        self.__sent = [
            Update(api=self.api, raw_response=update)
            for update in response.get("response", [])
        ]

        return self.__sent

    def shuffle(self, count: str = None, utc: str = None):
        """
            Randomize the order at which statuses for a social media
            profile will be sent out.
        """

        post_data = ""
        url = PATHS["SHUFFLE"].format(self.profile_id)

        if count:
            post_data += "count={}&".format(count)

        if utc:
            post_data += "utc={}".format(utc)

        return self.api.post(url=url, data=post_data)

    def reorder(self, updates_ids: List[str],
                offset: str = None, utc: str = None):
        """
            Edit the order in which statuses for a social media profile will
            be sent out.
        """

        post_data = []
        url = PATHS["REORDER"].format(self.profile_id)

        if offset:
            post_data.append("offset={}&".format(offset))

        if utc:
            post_data.append("utc={}&".format(utc))

        order_format = "order[]={}&"
        for update in updates_ids:
            post_data.append(order_format.format(update))

        return self.api.post(url=url, data="".join(post_data))

    #TODO: Multiple profile posting
    def new(self, text: str, shorten: str = None, now: str = None,
            top: str = None, media: str = None, when: str = None,
            photo: str = None, link: str = None):
        """
            Create one or more new status updates.
        """

        url = PATHS["CREATE"]

        post_data = ["text={}&".format(quote(text.encode("utf-8")))]
        post_data.append("profile_ids[]={}&".format(self.profile_id))

        if shorten:
            post_data.append("shorten={}&".format(shorten))

        if now:
            post_data.append("now={}&".format(now))

        if top:
            post_data.append("top={}&".format(top))

        if when:
            post_data.append("scheduled_at={}&".format(str(when)))

        if media:
            media_format = "media[{}]={}&"

            for media_type, media_item in list(media.items()):
                quoted_media = quote(media_item.encode("utf-8"))
                post_data.append(media_format.format(media_type, quoted_media))

        if photo:
            photo_format = "media[photo]=%s&" % photo
            post_data.append(photo_format)

        if link:
            photo_format = "media[link]=%s&" % link
            post_data.append(photo_format)

        response = self.api.post(url=url, data="".join(post_data))
        new_update = Update(api=self.api, raw_response=response["updates"][0])

        self.append(new_update)

        return new_update
