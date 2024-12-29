# gender_view.py: Zawiera widok do zarządzania płciami w aplikacji Kivy.
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from src.services.service_factory import ServiceFactory
import json

class GenderView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Wczytaj konfigurację
        with open("config/config.json") as config_file:
            config = json.load(config_file)

        self.service = ServiceFactory(config).get_gender_service()

        # Główny układ
        self.layout = BoxLayout(orientation='vertical')

        # Przewijalna lista płci (na górze)
        self.gender_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.gender_list_container.bind(minimum_height=self.gender_list_container.setter('height'))
        self.gender_list_scroll = ScrollView()
        self.gender_list_scroll.add_widget(self.gender_list_container)
        self.layout.add_widget(self.gender_list_scroll)

        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50)

        add_button = Button(text='Add Gender')
        add_button.bind(on_press=self.open_add_gender_form)
        bottom_layout.add_widget(add_button)

        return_button = Button(text='Return to Main Menu')
        return_button.bind(on_press=self.return_to_main_menu)
        bottom_layout.add_widget(return_button)

        self.layout.add_widget(bottom_layout)

        self.add_widget(self.layout)

        self.refresh_gender_list()

    def refresh_gender_list(self):
        genders = self.service.get_all_genders()

        # Wyczyść listę
        self.gender_list_container.clear_widgets()

        for gender in genders:
            gender_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            gender_box.add_widget(Label(text=gender.name, size_hint_x=0.6))

            edit_btn = Button(text='Edit', size_hint_x=0.2)
            edit_btn.bind(on_press=lambda instance, gender=gender: self.open_edit_gender_form(gender))
            gender_box.add_widget(edit_btn)

            delete_btn = Button(text='Delete', size_hint_x=0.2)
            delete_btn.bind(on_press=lambda instance, gender=gender: self.delete_gender(gender))
            gender_box.add_widget(delete_btn)

            self.gender_list_container.add_widget(gender_box)

    def open_add_gender_form(self, instance):
        # Przejdź do ekranu formularza dodawania płci
        self.manager.current = 'gender_form'
        form_screen = self.manager.get_screen('gender_form')
        form_screen.clear_form()

    def open_edit_gender_form(self, gender):
        # Przejdź do ekranu formularza edycji płci
        self.manager.current = 'gender_form'
        form_screen = self.manager.get_screen('gender_form')
        form_screen.load_gender(gender)

    def delete_gender(self, gender):
        # Opcjonalnie możesz dodać potwierdzenie usunięcia
        self.service.delete_gender(gender.gender_id)
        self.refresh_gender_list()

    def return_to_main_menu(self, instance):
        self.manager.current = 'menu'

    def open_add_gender_form(self, instance):
        # Przejdź do ekranu formularza dodawania płci
        self.manager.current = 'gender_form'
        form_screen = self.manager.get_screen('gender_form')
        form_screen.clear_form()
        form_screen.previous_screen = 'gender_view'  # Ustawiamy poprzedni ekran

    def open_edit_gender_form(self, gender):
        # Przejdź do ekranu formularza edycji płci
        self.manager.current = 'gender_form'
        form_screen = self.manager.get_screen('gender_form')
        form_screen.load_gender(gender)
        form_screen.previous_screen = 'gender_view'  # Ustawiamy poprzedni ekran