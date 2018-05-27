import re
from neam.python.classification.processing import NEAMProcessor


class DateProcessor(NEAMProcessor):
    def __init__(self):
        super().__init__(str, str)

    def run(self, text):
        text = self._merge_dates(text)
        return text

    def _merge_dates(self, text):
        return re.sub('</date>([,.] +)<date>', '\g<1>', text)

