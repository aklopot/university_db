from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner  # Import Spinner dla listy rozwijanej
from src.services.service_factory import ServiceFactory
from src.models.universitydb import Address, Gender, Professor, AcademicPosition
import json

class ProfessorForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_professor_service()
        self.gender_service = ServiceFactory().get_gender_service()
        self.address_service = ServiceFactory().get_address_service()
        
        self.layout = BoxLayout(orientation='vertical')
        
        # Pola formularza
        self.first_name_input = TextInput(hint_text="First Name")
        self.last_name_input = TextInput(hint_text="Last Name")
        self.pesel_input = TextInput(hint_text="PESEL")
        
        # Spinner do wyboru stanowiska (AcademicPosition)
        self.position_spinner = Spinner(
            text='Select Position',
            values=[position.value for position in AcademicPosition],
            size_hint_y=None,
            height=50
        )
        
        # Etykieta wybranej płci
        self.selected_gender_label = Label(text='No Gender Selected', size_hint_y=None, height=50)
        # Przycisk do wyboru płci
        self.select_gender_button = Button(text='Select Gender', size_hint_y=None, height=50)
        self.select_gender_button.bind(on_press=self.open_gender_selection)
        
        # Etykieta wybranego adresu
        self.selected_address_label = Label(text='No Address Selected', size_hint_y=None, height=50)
        # Przycisk do wyboru adresu
        self.select_address_button = Button(text='Select Address', size_hint_y=None, height=50)
        self.select_address_button.bind(on_press=self.open_address_selection)
        
        self.layout.add_widget(self.first_name_input)
        self.layout.add_widget(self.last_name_input)
        self.layout.add_widget(self.pesel_input)
        self.layout.add_widget(self.position_spinner)  # Dodanie spinnera do layoutu
        self.layout.add_widget(self.selected_gender_label)
        self.layout.add_widget(self.select_gender_button)
        self.layout.add_widget(self.selected_address_label)
        self.layout.add_widget(self.select_address_button)
        
        # Przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50)
        
        save_button = Button(text="Save")
        save_button.bind(on_press=self.save_professor)
        button_layout.add_widget(save_button)
        
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.cancel)
        button_layout.add_widget(cancel_button)
        
        self.layout.add_widget(button_layout)
        
        self.add_widget(self.layout)
        
        # Aktualny profesor (do edycji)
        self.current_professor = None
        self.selected_address = None  # Przechowuje wybrany adres
        self.selected_gender = None   # Przechowuje wybraną płeć
        
    def clear_form(self):
        # Czyści pola formularza
        self.first_name_input.text = ''
        self.last_name_input.text = ''
        self.pesel_input.text = ''
        self.position_spinner.text = 'Select Position'  # Reset Spinnera
        self.selected_gender_label.text = 'No Gender Selected'
        self.selected_address_label.text = 'No Address Selected'
        
        self.current_professor = None
        self.selected_address = None
        self.selected_gender = None
        
    def load_professor(self, professor):
        # Ładuje dane profesora do formularza (edycja)
        self.current_professor = professor
        self.first_name_input.text = professor.first_name
        self.last_name_input.text = professor.last_name
        self.pesel_input.text = professor.pesel
        self.position_spinner.text = professor.position.value  # Ustawienie Spinnera
        
        # Wyświetl płeć profesora
        self.selected_gender = professor.gender
        self.selected_gender_label.text = professor.gender.name
        
        # Wyświetl adres profesora
        self.selected_address = professor.address
        self.selected_address_label.text = f"{professor.address.street}, {professor.address.city}"
        
    def open_gender_selection(self, instance):
        # Przejdź do ekranu wyboru płci
        self.manager.current = 'gender_selection'
        gender_selection_screen = self.manager.get_screen('gender_selection')
        gender_selection_screen.previous_screen = 'professor_form'
        gender_selection_screen.parent_form = self  # Przekazujemy referencję do tego formularza
        
    def open_address_selection(self, instance):
        # Przejdź do ekranu wyboru adresu
        self.manager.current = 'address_selection'
        address_selection_screen = self.manager.get_screen('address_selection')
        address_selection_screen.previous_screen = 'professor_form'
        address_selection_screen.parent_form = self  # Przekazujemy referencję do tego formularza
        
    def save_professor(self, instance):
        # Pobierz dane z pól formularza
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text
        pesel = self.pesel_input.text
        position = AcademicPosition(self.position_spinner.text)  # Wybór stanowiska
        
        if not self.selected_gender:
            print("No gender selected.")
            return
        
        if not self.selected_address:
            print("No address selected.")
            return
        
        try:
            if self.current_professor:
                # Aktualizacja istniejącego profesora
                self.current_professor.first_name = first_name
                self.current_professor.last_name = last_name
                self.current_professor.pesel = pesel
                self.current_professor.position = position
                self.current_professor.gender = self.selected_gender
                self.current_professor.address = self.selected_address
                
                self.service.update_professor(self.current_professor)
            else:
                # Dodanie nowego profesora
                professor = Professor(
                    first_name=first_name,
                    last_name=last_name,
                    pesel=pesel,
                    position=position,
                    gender=self.selected_gender,
                    address=self.selected_address
                )
                self.service.add_professor(professor)
            
            # Po zapisaniu wróć do widoku listy profesorów
            self.manager.current = 'professor_view'
            self.clear_form()
        except Exception as e:
            # Obsłuż ewentualne błędy
            print(f"Błąd podczas zapisywania profesora: {e}")
        
    def cancel(self, instance):
        # Wróć do widoku listy profesorów bez zapisywania
        self.manager.current = 'professor_view'
        self.clear_form()
