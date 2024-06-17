from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup

from models.word_search import WordSearchDetails, WordDetails
from services.word_search.base import WordSearchService
from exceptions.word_search import (
    WordSearchWordNotFoundError,
    WordSearchUnknownError,
    WordSearchPageNotFoundError,
    WordSearchMissingTagsError, WordSearchEmptyWordError
)


SJP_URL = "https://sjp.pl"

TAG_NAME_HEADER = "h1"
TAG_NAME_PARAGRAPH = "p"

AVAILABILITY_TAG_TEXT_ACCEPTABLE = "dopuszczalne w grach (i)"
AVAILABILITY_TAG_TEXT_UNACCEPTABLE = "niedopuszczalne w grach (i)"
AVAILABILITY_TAG_TEXT_DOES_NOT_EXIST = "nie występuje w słowniku"

TAG_STYLE_BASE_WORD = "margin-bottom: 0;"
TAG_STYLE_DEFINITION = "margin: .5em 0; font: medium/1.4 sans-serif; max-width: 34em; "

STOP_ITERATION_TAG_TEXT_RELATED_WORDS = "powiązane hasła:"
STOP_ITERATION_TAG_TEXT_COMMENTS = "komentarze"


class SJPWordSearchService(WordSearchService):
    class TagName:
        H1 = TAG_NAME_HEADER
        P = TAG_NAME_PARAGRAPH

    class AvailabilityTagText:
        ACCEPTABLE = AVAILABILITY_TAG_TEXT_ACCEPTABLE
        UNACCEPTABLE = AVAILABILITY_TAG_TEXT_UNACCEPTABLE
        DOES_NOT_EXIST = AVAILABILITY_TAG_TEXT_DOES_NOT_EXIST

    class TagStyles:
        BaseWordTag = TAG_STYLE_BASE_WORD
        DefinitionTag = TAG_STYLE_DEFINITION

    class StopIterationTagText:
        RELATES_WORDS = STOP_ITERATION_TAG_TEXT_RELATED_WORDS
        COMMENTS = STOP_ITERATION_TAG_TEXT_COMMENTS

        ALL = (
            RELATES_WORDS,
            COMMENTS,
        )

    MISSING_VALUE_SIGN = "-"
    MISSING_WORD_BASE_VALUE = MISSING_VALUE_SIGN
    MISSING_WORD_DESCRIPTION_VALUE = MISSING_VALUE_SIGN
    MISSING_WORD_STATUS_VALUE = AvailabilityTagText.DOES_NOT_EXIST

    def __init__(self, base_url):
        self._base_url = base_url

    def search(self, word: str) -> WordSearchDetails:
        if not word:
            raise WordSearchEmptyWordError

        try:
            page = self._get_page(word)
        except WordSearchWordNotFoundError:
            return WordSearchDetails(
                word_details=[
                    WordDetails(
                        searched_for=word,
                        base=self.MISSING_WORD_BASE_VALUE,
                        status=self.MISSING_WORD_STATUS_VALUE,
                        description=self.MISSING_WORD_DESCRIPTION_VALUE
                    )
                ]
            )

        tags = page.body.contents

        headers, statuses, base_words, definitions = self._group_tags(tags)
        if not (len(headers) == len(statuses) == len(base_words) == len(definitions)):
            raise WordSearchMissingTagsError

        word_details = zip(headers, statuses, base_words, definitions)
        return WordSearchDetails(
            word_details=[
                WordDetails(
                    searched_for=header,
                    base=base_word,
                    status=availability,
                    description=definition
                )
                for header, availability, base_word, definition in word_details
            ]
        )

    def _get_word_url(self, word: str) -> str:
        word = quote(word)
        return urljoin(self._base_url, word)

    def _get_page(self, word: str) -> BeautifulSoup:
        url = self._get_word_url(word)

        try:
            page = urlopen(url)
        except HTTPError as err:
            if err.code == 404:
                raise WordSearchWordNotFoundError(word)
            raise WordSearchUnknownError
        except URLError as err:
            if getattr(err.reason, "errno") == -2:
                raise WordSearchPageNotFoundError(url)
            raise WordSearchUnknownError
        except Exception:
            raise WordSearchUnknownError

        html = page.read().decode("utf-8")
        return BeautifulSoup(html, "html.parser")

    def _group_tags(self, tags) -> tuple[list, list, list, list]:
        """
        :param tags:
        :return: tuple with headers, statuses, base_words, definitions
        """
        headers, statuses, base_words, definitions = [], [], [], []
        for tag in tags:
            name = tag.name
            text = tag.text.strip()

            if name == self.TagName.H1:
                # only add to header tags and go for the next tag
                # non-existing words sometimes contains " ✕"
                headers.append(text.rstrip(" ✕"))
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
                statuses.append(self.MISSING_WORD_STATUS_VALUE)
                base_words.append(self.MISSING_WORD_BASE_VALUE)
                definitions.append(self.MISSING_WORD_DESCRIPTION_VALUE)
                break

            if text.lower() in [self.AvailabilityTagText.ACCEPTABLE, self.AvailabilityTagText.UNACCEPTABLE]:
                statuses.append(text)
            elif tag.attrs.get('style') == self.TagStyles.BaseWordTag:
                base_words.append(text)
            elif tag.attrs.get('style') == self.TagStyles.DefinitionTag:
                definitions.append(text)

        return headers, statuses, base_words, definitions


sjp_word_search_service = SJPWordSearchService(
    base_url=SJP_URL,
)
