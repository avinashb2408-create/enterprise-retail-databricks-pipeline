from pathlib import Path
import yaml

DEFAULT = Path(__file__).resolve().parents[2] / "config" / "pipeline_config.yaml"

def load_config(path: str | Path | None = None) -> dict:
    with open(path or DEFAULT) as f:
        return yaml.safe_load(f)

def table_path(cfg: dict, layer: str, table: str) -> str:
    return str(Path(cfg["paths"][layer]) / table)
