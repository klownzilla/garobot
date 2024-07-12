from html.parser import HTMLParser
from api.constants import BUSINESS_ID_CLASS_ID

class BusinessParser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if tag == 'input' and BUSINESS_ID_CLASS_ID in str(self.get_starttag_text()):
            for k, v in attrs:
                if k == 'value':
                    self.data = v

    def get_data(self) -> str:
        if self.data is not None:
            return self.data
        return ''