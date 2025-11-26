import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter, Namespace
from .visa import Visa

def parse_args() -> Namespace:
    parser = ArgumentParser(
        # prog="action_run.py",
        formatter_class=RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
        Extract transaction items and creates leder output.
        """
        ),
    )
    parser.add_argument(
        "file", nargs=1, help="visa bill pdf"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    visa = Visa(args)
    visa.extract()
    visa.toLedger()

if __name__ == "__main__":
    main()
