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

            data_source_type = config["data_source"]["type"]
            result = {
                "data_source": data_source_type
            }

            # Dodaj odpowiednią konfigurację w zależności od typu źródła danych
            if data_source_type == "json":
                json_config = config["data_source"]["json"]
                # Sprawdź wymagane ścieżki tylko dla konfiguracji JSON
                for path in ConfigLoader.REQUIRED_JSON_PATHS:
                    if path not in json_config:
                        raise ValueError(f"Brak wymaganej ścieżki '{path}' w konfiguracji JSON")
                result["data_source.json"] = json_config
                
            elif data_source_type == "sqlite":
                result["sqlite_url"] = config["data_source"]["sqlite"]["sqlite_url"]
                
            elif data_source_type == "postgres":
                result["postgres_url"] = config["data_source"]["postgres"]["postgres_url"]

            return result
            
        except Exception as e:
            raise RuntimeError(f"Błąd podczas ładowania konfiguracji: {str(e)}")

# Funkcja dla zachowania kompatybilności wstecznej
def load_config() -> dict:
    """
    Funkcja wrapper dla zachowania kompatybilności wstecznej.
    Deleguje wywołanie do metody statycznej klasy ConfigLoader.
    """
    return ConfigLoader.load_config() 