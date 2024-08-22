import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Union, Optional


def to_snake_case(name: str) -> str:
    """Convert PascalCase or camelCase to snake_case."""
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return re.sub(r"\W+", "", name)  # Remove any non-word characters


def transform_fields(fields: List[str]) -> List[str]:
    """Transform fields to snake_case and remove unwanted symbols."""
    return [to_snake_case(field) for field in fields]


def convert_value(value: str) -> Optional[Union[int, float, str]]:
    """Convert string value to appropriate type."""
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return None if value == "" else value


@dataclass(frozen=True)
class DynamicParser:
    fields: List[str]
    values: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            key: value for key, value in zip(self.fields, self.values) if key != "eol"
        }

    @classmethod
    def from_line(cls, header: str, data: str) -> "DynamicParser":
        fields = transform_fields(header.strip().split("\t"))
        values = [convert_value(value.strip()) for value in data.strip().split("\t")]
        return cls(fields, values)


def parse_file_content(content: str) -> List[Dict[str, Any]]:
    lines = content.splitlines()
    header, *data_lines = lines
    parsed_data = [
        parsed_dict
        for parsed_dict in [
            DynamicParser.from_line(header, line).to_dict()
            for line in data_lines
            if line.strip()
        ]
        if parsed_dict.get("name") != "expansion"
    ]
    return parsed_data


def read_file(file_path: Path) -> str:
    return file_path.read_text()


def write_json(data: List[Dict[str, str]], output_file: Path) -> None:
    output_file.write_text(json.dumps(data, indent=2))
