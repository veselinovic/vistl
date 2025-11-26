import re
from argparse import Namespace

import pdfplumber


class Visa:
    def __init__(self, args: Namespace):
        """Creates Visa object"""
        self._pdf = pdfplumber.open(args.file[0])

    def extract(self) -> str:
        self._text = "".join(page.extract_text() for page in self._pdf.pages)
        return self._text

    def toLedger(self) -> None:
        results = []
        for line in self._text.splitlines():
            # First date
            date_match = re.match(r"^(\d{2})\.(\d{2})\.(\d{2})", line)
            if not date_match:
                continue
            year = f"20{date_match.group(3)}"
            month = date_match.group(2)
            day = date_match.group(1)
            date = f"{year}/{month}/{day}"

            # Text after second date, up to first comma
            info_match = re.match(
                r"^\d{2}\.\d{2}\.\d{2} \d{2}\.\d{2}\.\d{2} ([^,]+),", line
            )
            if not info_match:
                continue
            info = info_match.group(1).strip()

            # Find all numbers with optional thousands separator & decimals
            numbers = re.findall(r"\d{1,3}(?:'\d{3})*\.\d{2}", line)
            if not numbers:
                continue
            amount_str = numbers[-1].replace("'", "")  # Remove thousands sep
            amount = float(amount_str)  # Now as 1200.80

            results.append((date, info, amount))

        for date, info, amount in results:
            print(f"{date} * {info}\n       CHF {amount:.2f}\n    Liabilities:Visa\n")
