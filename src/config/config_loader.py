import tomllib
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Ładuje konfigurację z pliku TOML."""
    try:
        with open("config/config.toml", "rb") as f:
            config = tomllib.load(f)
            
        # Spłaszczamy konfigurację dla zachowania kompatybilności
        flattened_config = {
            "data_source": config["general"]["data_source"],
            "json_student_path": config["data_source"]["json"]["json_student_path"],
            "json_professor_path": config["data_source"]["json"]["json_professor_path"],
            "sqlite_url": config["data_source"]["sqlite"]["sqlite_url"],
            "postgres_url": config["data_source"]["postgres"]["postgres_url"]
        }
        return flattened_config
    except Exception as e:
        raise RuntimeError(f"Błąd podczas ładowania konfiguracji: {str(e)}") 