import os
import tomllib
from pathlib import Path

from src.config.enums import Environment
from src.config.settings_model import Settings


def load_settings(config_path: Path, secrets_path: Path) -> Settings:
    config_data = {}
    if config_path.exists():
        with config_path.open("rb") as f:
            config_data = tomllib.load(f)
    

    secrets_data = {}
    if secrets_path.exists():
        with secrets_path.open("rb") as f:
            secrets_data = tomllib.load(f)
    else:
        # just create it for fun...
        secrets_path.touch()

    combined = config_data | secrets_data

    return Settings.model_validate(combined)


env = Environment(os.getenv("APP_ENV", Environment.development))

config_path = Path("settings.toml")

secrets_file = ".secrets.toml"
secrets_path = Path(os.getenv("SECRETS_PATH", secrets_file))

settings = load_settings(config_path, secrets_path)
