from pathlib import Path
from time import time

import click

from .parse import parse_file_content, write_json, read_file


@click.command()
@click.argument(
    "input_directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.argument("output_directory", type=click.Path(file_okay=False, dir_okay=True))
def cli(input_directory: str, output_directory: str) -> None:
    """Parse any D2R txt files in a given directory and save results as JSON to an output directory."""
    start_time = time()
    input_path = Path(input_directory)
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)
    process_file = lambda file: write_json(
        parse_file_content(read_file(file)), output_path / f"{file.stem}.json"
    )
    list(map(process_file, input_path.glob("*.txt")))
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Parsing completed in {elapsed_time:.2f} seconds")
