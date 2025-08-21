import argparse
import asyncio
import logging

from math_path.agent import run


async def main() -> None:
    args = _parse_arguments()

    _set_logging_level(args.log_level)

    run(args.start_number, args.end_number)


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CLI for the math_path application.")

    parser.add_argument(
        "--start-number",
        type=int,
        required=True,
        help="The starting number for processing.",
    )
    parser.add_argument(
        "--end-number",
        type=int,
        required=True,
        help="The ending number for processing.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level.",
    )

    return parser.parse_args()


def _set_logging_level(log_level: str) -> None:
    logging.basicConfig(level=log_level)


if __name__ == "__main__":
    asyncio.run(main())
