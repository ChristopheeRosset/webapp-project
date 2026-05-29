import yaml
from pathlib import Path

def load_config(env="dci"):
    config_file = Path(f"server/config/config.{env}.yaml")
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    return yaml.safe_load(config_file.read_text())