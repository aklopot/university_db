import tomllib
from pathlib import Path
from typing import Dict

class ConfigLoader:
    """Klasa odpowiedzialna za ładowanie konfiguracji zgodnie z zasadą Single Responsibility."""
    
    REQUIRED_JSON_PATHS = [
        'json_student_path',
        'json_academic_staff_path',
        'json_field_of_study_path',
        'json_gender_path',
        'json_address_path',
        'json_academic_course_path'
    ]

    @staticmethod
    def load_config() -> dict:
        """Ładuje konfigurację z pliku TOML."""
        try:
            config_path = Path("config/config.toml")
            with open(config_path, "rb") as f:
                config = tomllib.load(f)

            # Sprawdź czy wszystkie wymagane ścieżki są obecne
            json_config = config["data_source"]["json"]
            for path in ConfigLoader.REQUIRED_JSON_PATHS:
                if path not in json_config:
                    raise ValueError(f"Brak wymaganej ścieżki '{path}' w konfiguracji JSON")
                
            return {
                "data_source": config["general"]["data_source"],
                "data_source.json": json_config,
                "database": config.get("database", {})
            }
        except Exception as e:
            raise RuntimeError(f"Błąd podczas ładowania konfiguracji: {str(e)}")

# Funkcja dla zachowania kompatybilności wstecznej
def load_config() -> dict:
    """
    Funkcja wrapper dla zachowania kompatybilności wstecznej.
    Deleguje wywołanie do metody statycznej klasy ConfigLoader.
    """
    return ConfigLoader.load_config() 