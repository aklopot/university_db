from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from src.services.service_factory import ServiceFactory
from src.models.universitydb import Address, Gender, Student, FieldOfStudy
import json
from typing import Optional
from clients.gui_kivy.utils.colors import *

class StudentForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_student_service()
        self.gender_service = ServiceFactory().get_gender_service()
        self.address_service = ServiceFactory().get_address_service()
        self.field_of_study_service = ServiceFactory().get_field_of_study_service()
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł
        self.title_label = Label(
            text="Dodaj studenta",
            font_size='20sp',
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(self.title_label)
        
        # Inicjalizacja pól formularza
        self.first_name_input = TextInput(
            hint_text="Wprowadź imię",
            size_hint_y=None,
            height=40
        )
        self.last_name_input = TextInput(
            hint_text="Wprowadź nazwisko",
            size_hint_y=None,
            height=40
        )
        self.index_number_input = TextInput(
            hint_text="Wprowadź numer indeksu",
            size_hint_y=None,
            height=40
        )
        self.pesel_input = TextInput(
            hint_text="Wprowadź PESEL",
            size_hint_y=None,
            height=40
        )

        # Definicja sekcji z etykietami i polami
        input_sections = [
            ("Imię:", self.first_name_input),
            ("Nazwisko:", self.last_name_input),
            ("Numer indeksu:", self.index_number_input),
            ("PESEL:", self.pesel_input)
        ]

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
                color=TEXT_WHITE,
                halign='left'
            ))
            section.add_widget(input_field)
            self.layout.add_widget(section)

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
            text='Nie wybrano',
            size_hint_y=None,
            height=25,
            color=TEXT_WHITE
        )
        gender_section.add_widget(self.selected_gender_label)
        
        self.select_gender_button = Button(
            text='Wybierz płeć',
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        self.select_gender_button.bind(on_press=self.open_gender_selection)
        gender_section.add_widget(self.select_gender_button)
        self.layout.add_widget(gender_section)
        
        # Sekcja wyboru adresu (podobna wysokość jak płeć)
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
            text='Nie wybrano',
            size_hint_y=None,
            height=25,
            color=TEXT_WHITE
        )
        address_section.add_widget(self.selected_address_label)
        
        self.select_address_button = Button(
            text='Wybierz adres',
            size_hint_y=None,
            height=40,
            background_color=BUTTON_GREEN
        )
        self.select_address_button.bind(on_press=self.open_address_selection)
        address_section.add_widget(self.select_address_button)
        
        # Sekcja wyboru kierunku studiów (mniejsza wysokość - tylko spinner)
        field_study_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=70,
            spacing=5
        )
        field_study_section.add_widget(Label(
            text="Kierunek studiów:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.field_of_study_spinner = Spinner(
            text='Wybierz kierunek',
            values=self._get_field_of_study_names(),
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        field_study_section.add_widget(self.field_of_study_spinner)
        
        # Dodawanie wszystkich elementów do głównego layoutu
        self.layout.add_widget(address_section)
        self.layout.add_widget(field_study_section)
        
        # Przyciski akcji
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
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
        save_button.bind(on_press=self.save)
        button_layout.add_widget(save_button)
        
        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)
        
        # Aktualny student (do edycji)
        self.current_student = None
        self.selected_address = None  # Przechowuje wybrany adres
        self.selected_gender = None   # Przechowuje wybraną płeć
        self.selected_field_of_study = None
        
        # Aktualizacja kolorów dla etykiet
        self.selected_address_label.color = TEXT_WHITE

        # Aktualizacja kolorów dla przycisków wyboru
        self.select_address_button.background_color = BUTTON_LIGHT_BLUE
        
        # Aktualizacja koloru dla spinnera
        self.field_of_study_spinner.background_color = BUTTON_LIGHT_BLUE
        
    def _get_field_of_study_names(self) -> list[str]:
        fields = self.field_of_study_service.get_all_fields_of_study()
        return [field.field_name for field in fields]
        
    def _get_gender_names(self) -> list[str]:
        genders = self.gender_service.get_all_genders()
        return [gender.gender_name for gender in genders]

    def _get_gender_by_name(self, name: str):
        genders = self.gender_service.get_all_genders()
        for gender in genders:
            if gender.gender_name == name:
                return gender
        return None
        
    def clear_form(self):
        # Ustaw tytuł dla nowego studenta
        self.title_label.text = "Dodaj studenta"
        
        # Czyści pola formularza
        self.first_name_input.text = ''
        self.last_name_input.text = ''
        self.index_number_input.text = ''
        self.pesel_input.text = ''
        self.selected_address_label.text = 'Nie wybrano'
        self.field_of_study_spinner.text = 'Wybierz kierunek'
        self.selected_gender_label.text = 'Nie wybrano'
        
        self.current_student = None
        self.selected_address = None
        self.selected_gender = None
        self.selected_field_of_study = None
        
    def load_student(self, student):
        # Zmień tytuł na tryb edycji
        self.title_label.text = "Edytuj studenta"
        
        # Ładuje dane studenta do formularza (edycja)
        self.current_student = student
        self.first_name_input.text = student.first_name
        self.last_name_input.text = student.last_name
        self.index_number_input.text = student.index_number
        self.pesel_input.text = student.pesel
        
        # Wyświetl płeć studenta
        if student.gender:
            self.selected_gender = student.gender
            self.selected_gender_label.text = student.gender.gender_name
        
        # Wyświetl adres studenta
        self.selected_address = student.address
        self.selected_address_label.text = f"{student.address.street}, {student.address.city}"
        
        # Wyświetl kierunek studiów studenta
        if student.field_of_study:
            self.selected_field_of_study = student.field_of_study
            self.field_of_study_spinner.text = student.field_of_study.field_name
            
    def _get_selected_field_of_study(self) -> Optional[FieldOfStudy]:
        if self.field_of_study_spinner.text != 'Wybierz kierunek':
            return self.field_of_study_service.get_field_of_study_by_name(
                self.field_of_study_spinner.text
            )
        return None
        
    def open_address_selection(self, instance):
        # Przejdź do ekranu wyboru adresu
        self.manager.current = 'address_selection'
        address_selection_screen = self.manager.get_screen('address_selection')
        address_selection_screen.previous_screen = 'student_form'
        address_selection_screen.parent_form = self  # Przekazujemy referencję do tego formularza
        
    def open_gender_selection(self, instance):
        # Przejdź do ekranu wyboru płci
        self.manager.current = 'gender_selection'
        gender_selection_screen = self.manager.get_screen('gender_selection')
        gender_selection_screen.previous_screen = 'student_form'
        gender_selection_screen.parent_form = self
        
    def save(self, instance):
        try:
            first_name = self.first_name_input.text.strip()
            last_name = self.last_name_input.text.strip()
            index_number = self.index_number_input.text.strip()
            pesel = self.pesel_input.text.strip()
            
            if not all([first_name, last_name, index_number, pesel]):
                print("Wszystkie pola muszą być wypełnione")
                return

            if not self.selected_gender:
                print("Nie wybrano płci")
                return

            if not self.selected_address:
                print("No address selected.")
                return
            
            field_of_study = self._get_selected_field_of_study()
            
            if self.current_student:
                # Aktualizacja istniejącego studenta
                self.current_student.first_name = first_name
                self.current_student.last_name = last_name
                self.current_student.index_number = index_number
                self.current_student.pesel = pesel
                self.current_student.gender = self.selected_gender
                self.current_student.gender_id = self.selected_gender.gender_id
                self.current_student.address = self.selected_address
                self.current_student.field_of_study = field_of_study
                self.current_student.field_of_study_id = field_of_study.field_of_study_id if field_of_study else None
                
                self.service.update_student(self.current_student)
            else:
                # Dodanie nowego studenta
                student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    index_number=index_number,
                    pesel=pesel,
                    gender=self.selected_gender,
                    gender_id=self.selected_gender.gender_id,
                    address=self.selected_address,
                    field_of_study=field_of_study,
                    field_of_study_id=field_of_study.field_of_study_id if field_of_study else None
                )
                self.service.add_student(student)
            
            # Po zapisaniu wróć do widoku listy studentów
            self.manager.current = 'student_view'
            self.clear_form()
        except Exception as e:
            # Obsłuż ewentualne błędy (np. wyświetl komunikat)
            print(f"Błąd podczas zapisywania studenta: {e}")
        
    def cancel(self, instance):
        # Wróć do widoku listy studentów bez zapisywania
        self.manager.current = 'student_view'
        self.clear_form()
