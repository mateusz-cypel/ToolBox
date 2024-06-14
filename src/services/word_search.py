from urllib.error import HTTPError
from urllib.parse import quote, urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup

SJP_URL = "https://sjp.pl"


class SJPWordSearch:
    class TagName:
        H1 = "h1"
        P = "p"

    class AvailabilityTagText:
        ACCEPTABLE = "dopuszczalne w grach (i)"
        UNACCEPTABLE = "niedopuszczalne w grach (i)"
        DOES_NOT_EXIST = "nie występuje w słowniku"

        ALL = (
            ACCEPTABLE,
            UNACCEPTABLE,
            DOES_NOT_EXIST,
        )

    class TagStyles:
        BaseWordTag = "margin-bottom: 0;"
        DefinitionTag = "margin: .5em 0; font: medium/1.4 sans-serif; max-width: 34em; "

    class StopIterationTagText:
        RELATES_WORDS = "powiązane hasła:"
        COMMENTS = "komentarze"

        ALL = (
            RELATES_WORDS,
            COMMENTS,
        )

    def __init__(self, base_url):
        self._base_url = base_url

    def search(self, word):
        url = self._get_word_url(word)

        try:
            page = urlopen(url)
        except HTTPError as e:
            if e.code == 404:
                return word, self.AvailabilityTagText.DOES_NOT_EXIST, "-", "-"
            raise Exception
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        tags = soup.body.contents

        header_tags, availability_tags, base_word_tags, definition_tags = [], [], [], []

        for tag in tags:
            name = tag.name
            text = tag.text.strip()

            if name == self.TagName.H1:
                # only add to header tags and go for the next tag
                header_tags.append(tag.text.strip().rstrip(" ✕"))
                continue

            if name != self.TagName.P:
                # if its not p or h1 tag just skip it
                continue

            if text.lower() in self.StopIterationTagText.ALL:
                # only tags before these stop tags are interested
                # after reaching one of the stop tags iteration can be stopped
                break

            if text.lower() in [self.AvailabilityTagText.DOES_NOT_EXIST]:
                # if searched word does not exist it contains only tag name and text
                # there is no base word or definition for searched word
                availability_tags.append(tag.text.strip())
                base_word_tags.append("-")
                definition_tags.append("-")
                break

            if text.lower() in [self.AvailabilityTagText.ACCEPTABLE, self.AvailabilityTagText.UNACCEPTABLE]:
                availability_tags.append(tag.text.strip())
            elif tag.attrs['style'] == self.TagStyles.BaseWordTag:
                base_word_tags.append(tag.text.strip())
            elif tag.attrs['style'] == self.TagStyles.DefinitionTag:
                definition_tags.append(tag.text.strip())

        return [x for x in zip(header_tags, availability_tags, base_word_tags, definition_tags)]

    def _get_word_url(self, word):
        word = quote(word)
        return urljoin(self._base_url, word)


sjp_word_search = SJPWordSearch(
    base_url=SJP_URL,
)
