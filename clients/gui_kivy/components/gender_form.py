from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from src.services.service_factory import ServiceFactory
import json

class GenderForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Wczytaj konfigurację
        with open("config/config.json") as config_file:
            config = json.load(config_file)

        self.service = ServiceFactory(config).get_gender_service()
        self.gender = None  # Przechowuje aktualnie edytowaną płeć

        # Główny układ
        self.layout = BoxLayout(orientation='vertical')

        # Pole do wprowadzania nazwy płci
        self.name_input = TextInput(hint_text="Enter gender name", size_hint_y=None, height=50)
        self.layout.add_widget(self.name_input)

        # Przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50)

        save_button = Button(text='Save')
        save_button.bind(on_press=self.save_gender)
        button_layout.add_widget(save_button)

        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_press=self.cancel)
        button_layout.add_widget(cancel_button)

        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

        self.previous_screen = None  # Nazwa poprzedniego ekranu

    def load_gender(self, gender):
        # Ładuje dane płci do formularza (edycja)
        self.gender = gender
        self.name_input.text = gender.name

    def clear_form(self):
        # Czyści formularz (dodawanie nowej płci)
        self.gender = None
        self.name_input.text = ''

    def save_gender(self, instance):
        gender_name = self.name_input.text.strip().upper()
        if gender_name:
            if self.gender:
                # Aktualizacja istniejącej płci
                self.gender.name = gender_name
                self.service.update_gender(self.gender)
            else:
                # Dodanie nowej płci
                self.service.add_gender(gender_name)
            # Powrót do poprzedniego ekranu
            self.manager.current = self.previous_screen
            # Odśwież listę płci na poprzednim ekranie
            if self.previous_screen == 'gender_selection':
                gender_selection = self.manager.get_screen('gender_selection')
                gender_selection.refresh_gender_list()
            elif self.previous_screen == 'gender_view':
                gender_view = self.manager.get_screen('gender_view')
                gender_view.refresh_gender_list()
        else:
            # Możesz dodać komunikat o błędzie
            pass

    def cancel(self, instance):
        # Powrót do poprzedniego ekranu bez zapisywania
        self.manager.current = self.previous_screen
