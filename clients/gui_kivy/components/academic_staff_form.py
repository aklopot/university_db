from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner  # Import Spinner dla listy rozwijanej
from src.services.service_factory import ServiceFactory
from src.models.universitydb import Address, Gender, AcademicStaff, AcademicPosition
from clients.gui_kivy.utils.colors import *  # Dodajemy import kolorów
from clients.gui_kivy.utils.fonts import *  # Dodajemy import stałych czcionek
import json

class AcademicStaffForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_academic_staff_service()
        self.gender_service = ServiceFactory().get_gender_service()
        self.address_service = ServiceFactory().get_address_service()
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł - używamy stałej FONT_SIZE_TITLE
        self.title_label = Label(
            text="Dodaj pracownika",
            font_size=FONT_SIZE_TITLE,  # Zmiana z '20sp' na stałą
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(self.title_label)
        
        # Sekcje formularza z polami tekstowymi
        input_sections = [
            ("Imię:", TextInput(
                hint_text="Wprowadź imię",
                multiline=False,
                size_hint_y=None,
                height=40
            )),
            ("Nazwisko:", TextInput(
                hint_text="Wprowadź nazwisko",
                multiline=False,
                size_hint_y=None,
                height=40
            )),
            ("PESEL:", TextInput(
                hint_text="Wprowadź PESEL",
                multiline=False,
                size_hint_y=None,
                height=40
            ))
        ]
        
        # Przypisanie pól do zmiennych instancji
        self.first_name_input = input_sections[0][1]
        self.last_name_input = input_sections[1][1]
        self.pesel_input = input_sections[2][1]
        
        # Dodawanie sekcji z polami tekstowymi
        for label_text, input_field in input_sections:
            section = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=70,
                spacing=5
            )
            section.add_widget(Label(
                text=label_text,
                size_hint_y=None,
                height=20,
                color=TEXT_WHITE
            ))
            section.add_widget(input_field)
            self.layout.add_widget(section)
        
        # Sekcja wyboru stanowiska
        position_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=70,
            spacing=5
        )
        position_section.add_widget(Label(
            text="Stanowisko:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.position_spinner = Spinner(
            text='Wybierz stanowisko',
            values=[position.value for position in AcademicPosition],
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        position_section.add_widget(self.position_spinner)
        self.layout.add_widget(position_section)
        
        # Sekcja wyboru płci
        gender_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=90,
            spacing=5
        )
        gender_section.add_widget(Label(
            text="Płeć:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.selected_gender_label = Label(
            text='Nie wybrano płci',
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        )
        self.select_gender_button = Button(
            text='Wybierz płeć',
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        self.select_gender_button.bind(on_press=self.open_gender_selection)
        gender_section.add_widget(self.selected_gender_label)
        gender_section.add_widget(self.select_gender_button)
        self.layout.add_widget(gender_section)
        
        # Sekcja wyboru adresu
        address_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=90,
            spacing=5
        )
        address_section.add_widget(Label(
            text="Adres:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.selected_address_label = Label(
            text='Nie wybrano adresu',
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        )
        self.select_address_button = Button(
            text='Wybierz adres',
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        self.select_address_button.bind(on_press=self.open_address_selection)
        address_section.add_widget(self.selected_address_label)
        address_section.add_widget(self.select_address_button)
        self.layout.add_widget(address_section)
        
        # Przyciski na dole
        button_layout = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )
        
        cancel_button = Button(
            text='Anuluj',
            background_color=BUTTON_PEARL
        )
        cancel_button.bind(on_press=self.cancel)
        button_layout.add_widget(cancel_button)
        
        save_button = Button(
            text='Zapisz',
            background_color=BUTTON_GREEN
        )
        save_button.bind(on_press=self.save_academic_staff)
        button_layout.add_widget(save_button)
        
        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)
        
        # Zmienne stanu
        self.current_academic_staff = None
        self.selected_address = None
        self.selected_gender = None
        
    def clear_form(self):
        """Czyści formularz do dodawania nowego pracownika"""
        # Zmień tytuł na tryb dodawania
        self.title_label.text = "Dodaj pracownika"
        
        # Czyści pola formularza
        self.first_name_input.text = ''
        self.last_name_input.text = ''
        self.pesel_input.text = ''
        self.position_spinner.text = 'Wybierz stanowisko'
        self.selected_gender_label.text = 'Nie wybrano płci'
        self.selected_address_label.text = 'Nie wybrano adresu'
        
        # Resetuj zmienne stanu
        self.current_academic_staff = None
        self.selected_address = None
        self.selected_gender = None
        
    def load_academic_staff(self, academic_staff):
        """Ładuje dane pracownika do formularza w trybie edycji"""
        # Zmień tytuł na tryb edycji
        self.title_label.text = "Edytuj pracownika"
        
        # Załaduj dane pracownika
        self.current_academic_staff = academic_staff
        self.first_name_input.text = academic_staff.first_name
        self.last_name_input.text = academic_staff.last_name
        self.pesel_input.text = academic_staff.pesel
        self.position_spinner.text = academic_staff.position.value
        
        # Załaduj płeć
        if academic_staff.gender:
            self.selected_gender = academic_staff.gender
            self.selected_gender_label.text = academic_staff.gender.gender_name
            
        # Załaduj adres
        if academic_staff.address:
            self.selected_address = academic_staff.address
            self.selected_address_label.text = f"{academic_staff.address.street}, {academic_staff.address.city}"
        
    def open_gender_selection(self, instance):
        # Przejdź do ekranu wyboru płci
        self.manager.current = 'gender_selection'
        gender_selection_screen = self.manager.get_screen('gender_selection')
        gender_selection_screen.previous_screen = 'academic_staff_form'
        gender_selection_screen.parent_form = self  # Przekazujemy referencję do tego formularza
        
    def open_address_selection(self, instance):
        # Przejdź do ekranu wyboru adresu
        self.manager.current = 'address_selection'
        address_selection_screen = self.manager.get_screen('address_selection')
        address_selection_screen.previous_screen = 'academic_staff_form'
        address_selection_screen.parent_form = self  # Przekazujemy referencję do tego formularza
        
    def save_academic_staff(self, instance):
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
            if self.current_academic_staff:
                # Aktualizacja istniejącego pracownika akademickiego
                self.current_academic_staff.first_name = first_name
                self.current_academic_staff.last_name = last_name
                self.current_academic_staff.pesel = pesel
                self.current_academic_staff.position = position
                self.current_academic_staff.gender = self.selected_gender
                self.current_academic_staff.address = self.selected_address
                
                self.service.update_academic_staff(self.current_academic_staff)
            else:
                # Dodanie nowego pracownika akademickiego
                academic_staff = AcademicStaff(
                    first_name=first_name,
                    last_name=last_name,
                    pesel=pesel,
                    position=position,
                    gender=self.selected_gender,
                    address=self.selected_address
                )
                self.service.add_academic_staff(academic_staff)
            
            # Po zapisaniu wróć do widoku listy pracowników akademickich
            self.manager.current = 'academic_staff_view'
            self.clear_form()
        except Exception as e:
            # Obsłuż ewentualne błędy
            print(f"Błąd podczas zapisywania pracownika akademickiego: {e}")
        
    def cancel(self, instance):
        # Wróć do widoku listy pracowników akademickich bez zapisywania
        self.manager.current = 'academic_staff_view'
        self.clear_form()
