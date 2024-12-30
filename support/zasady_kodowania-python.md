# Zasady kodowania w Pythonie

## Konwencje nazewnicze

| Kategoria          | Konwencja        | Przykład               | Opis                                                     |
|--------------------|------------------|------------------------|----------------------------------------------------------|
| Plik               | snake_case       | `message_service.py`   | Małe litery z podkreśleniem pomiędzy                     |
| Klasa              | PascalCase       | `MessageService`       | Pierwsza i następne wielkie litery                       |
| Metoda publiczna   | snake_case       | `get_message_format()` | Małe litery z podkreśleniem pomiędzy                     |
| Metoda prywatna    | _snake_case      | `_process_data()`      | Małe litery z podkreśleniem pomiędzy i na początku       |
| Metoda chroniona   | __snake_case     | `__internal_calc()`    | Małe litery z podkreśleniem pomiędzy i dwoma na początku |
| Zmienna publiczna  | snake_case       | `transfer_id`          | Małe litery z podkreśleniem pomiędzy                     |
| Zmienna prywatna   | _snake_case      | `_counter`             | Małe litery z podkreśleniem pomiędzy i na początku       |
| Zmienna chroniona  | __snake_case     | `__state`              | Małe litery z podkreśleniem pomiędzy i dwoma na początku |
| Stała globalna     | UPPER_SNAKE_CASE | `MAX_CONNECTIONS`      | Wielkie litery z podkreśleniem pomiędzy                  |

---

## Przykłady użycia
### Plik: `user_service.py`
```python
class UserService:
    MAX_USERS = 100  # Stała
    user_type = "standard"   # Zmienna publiczna
    
    def __init__(self):
        self._user_count = 0  # Zmienna prywatna
        self.__state = {}     # Zmienna bardzo prywatna
    
    def add_user(self):       # Metoda publiczna
        pass
        
    def _validate(self):      # Metoda prywatna
        pass
        
    def __update_state(self): # Metoda bardzo prywatna
        pass
```

## Oficjalna dokumentacja konwencji

Powyższe zasady są zgodne z oficjalną konwencją nazewnictwa Python - PEP 8.
Pełna dokumentacja dostępna jest pod adresem: [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)