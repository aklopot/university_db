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

class StudentForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_student_service()
        self.gender_service = ServiceFactory().get_gender_service()
        self.address_service = ServiceFactory().get_address_service()
        self.field_of_study_service = ServiceFactory().get_field_of_study_service()
        
        self.layout = BoxLayout(orientation='vertical')
        
        # Pola formularza
        self.first_name_input = TextInput(hint_text="First Name")
        self.last_name_input = TextInput(hint_text="Last Name")
        self.index_number_input = TextInput(hint_text="Index Number")
        self.pesel_input = TextInput(hint_text="PESEL")
        
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
        
        # Dodaj Spinner (lista rozwijana) dla kierunku studiów
        self.field_of_study_spinner = Spinner(
            text='Select Field of Study',
            values=self._get_field_of_study_names(),
            size_hint_y=None,
            height=50
        )
        
        self.layout.add_widget(self.first_name_input)
        self.layout.add_widget(self.last_name_input)
        self.layout.add_widget(self.index_number_input)
        self.layout.add_widget(self.pesel_input)
        self.layout.add_widget(self.selected_gender_label)
        self.layout.add_widget(self.select_gender_button)
        self.layout.add_widget(self.selected_address_label)
        self.layout.add_widget(self.select_address_button)
        self.layout.add_widget(self.field_of_study_spinner)
        
        # Przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50)
        
        save_button = Button(text="Save")
        save_button.bind(on_press=self.save_student)
        button_layout.add_widget(save_button)
        
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.cancel)
        button_layout.add_widget(cancel_button)
        
        self.layout.add_widget(button_layout)
        
        self.add_widget(self.layout)
        
        # Aktualny student (do edycji)
        self.current_student = None
        self.selected_address = None  # Przechowuje wybrany adres
        self.selected_gender = None   # Przechowuje wybraną płeć
        self.selected_field_of_study = None
        
    def _get_field_of_study_names(self) -> list[str]:
        fields = self.field_of_study_service.get_all_fields_of_study()
        return [field.field_name for field in fields]
        
    def clear_form(self):
        # Czyści pola formularza
        self.first_name_input.text = ''
        self.last_name_input.text = ''
        self.index_number_input.text = ''
        self.pesel_input.text = ''
        self.selected_gender_label.text = 'No Gender Selected'
        self.selected_address_label.text = 'No Address Selected'
        self.field_of_study_spinner.text = 'Select Field of Study'
        
        self.current_student = None
        self.selected_address = None
        self.selected_gender = None
        self.selected_field_of_study = None
        
    def load_student(self, student):
        # Ładuje dane studenta do formularza (edycja)
        self.current_student = student
        self.first_name_input.text = student.first_name
        self.last_name_input.text = student.last_name
        self.index_number_input.text = student.index_number
        self.pesel_input.text = student.pesel
        
        # Wyświetl płeć studenta
        self.selected_gender = student.gender
        self.selected_gender_label.text = student.gender.name
        
        # Wyświetl adres studenta
        self.selected_address = student.address
        self.selected_address_label.text = f"{student.address.street}, {student.address.city}"
        
        # Wyświetl kierunek studiów studenta
        if student.field_of_study:
            self.selected_field_of_study = student.field_of_study
            self.field_of_study_spinner.text = student.field_of_study.field_name
            
    def _get_selected_field_of_study(self) -> Optional[FieldOfStudy]:
        if self.field_of_study_spinner.text != 'Select Field of Study':
            return self.field_of_study_service.get_field_of_study_by_name(
                self.field_of_study_spinner.text
            )
        return None
        
    def open_gender_selection(self, instance):
        # Przejdź do ekranu wyboru płci
        self.manager.current = 'gender_selection'
        gender_selection_screen = self.manager.get_screen('gender_selection')
        gender_selection_screen.previous_screen = 'student_form'
        gender_selection_screen.parent_form = self  # Przekazujemy referencję do tego formularza
        
    def open_address_selection(self, instance):
        # Przejdź do ekranu wyboru adresu
        self.manager.current = 'address_selection'
        address_selection_screen = self.manager.get_screen('address_selection')
        address_selection_screen.previous_screen = 'student_form'
        address_selection_screen.parent_form = self  # Przekazujemy referencję do tego formularza
        
    def save_student(self, instance):
        try:
            first_name = self.first_name_input.text
            last_name = self.last_name_input.text
            index_number = self.index_number_input.text
            pesel = self.pesel_input.text
            
            if not self.selected_gender:
                print("No gender selected.")
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
