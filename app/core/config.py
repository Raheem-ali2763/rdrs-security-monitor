from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_ROOT / "config.yaml"


class ConfigurationError(Exception):
    """Raised when the RDRS configuration is invalid or cannot be loaded."""


def load_config(config_path: Path = CONFIG_FILE) -> dict[str, Any]:
    """Load and validate the RDRS YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Parsed configuration as a dictionary.

    Raises:
        ConfigurationError: If the file does not exist or contains invalid YAML.
    """
    if not config_path.is_file():
        raise ConfigurationError(
            f"Configuration file not found: {config_path}"
        )

    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            data = yaml.safe_load(config_file)
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            f"Invalid YAML configuration: {config_path}"
        ) from exc

    if not isinstance(data, dict):
        raise ConfigurationError(
            "Configuration root must be a YAML mapping."
        )

    return data


config = load_config()
