from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from src.services.service_factory import ServiceFactory
from src.models.universitydb import AcademicCourse, AcademicStaff
from clients.gui_kivy.utils.colors import *
from typing import Optional

class AcademicCourseForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_academic_course_service()
        self.field_of_study_service = ServiceFactory().get_field_of_study_service()
        self.academic_staff_service = ServiceFactory().get_academic_staff_service()
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Inicjalizacja pól tekstowych
        self.course_name_input = TextInput(
            hint_text="Wprowadź nazwę kursu",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        
        self.ects_credits_input = TextInput(
            hint_text="Wprowadź liczbę punktów ECTS",
            multiline=False,
            size_hint_y=None,
            height=40
        )

        # Sekcje formularza
        input_sections = [
            ("Nazwa kursu:", self.course_name_input),
            ("Punkty ECTS:", self.ects_credits_input)
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
                color=TEXT_WHITE
            ))
            section.add_widget(input_field)
            self.layout.add_widget(section)

        # Sekcja wyboru kierunku studiów
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
            text='Wybierz kierunek studiów',
            values=self._get_field_of_study_names(),
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        field_study_section.add_widget(self.field_of_study_spinner)
        self.layout.add_widget(field_study_section)

        # Sekcja wyboru prowadzącego
        staff_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=70,
            spacing=5
        )
        staff_section.add_widget(Label(
            text="Prowadzący:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.academic_staff_spinner = Spinner(
            text='Wybierz prowadzącego',
            values=self._get_academic_staff_names(),
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        staff_section.add_widget(self.academic_staff_spinner)
        self.layout.add_widget(staff_section)
        
        # Przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        save_button = Button(
            text='Zapisz',
            background_color=BUTTON_GREEN
        )
        save_button.bind(on_press=self.save)
        button_layout.add_widget(save_button)
        
        cancel_button = Button(
            text='Anuluj',
            background_color=BUTTON_ORANGE
        )
        cancel_button.bind(on_press=self.cancel)
        button_layout.add_widget(cancel_button)
        
        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)
        
        self.current_course = None

    def _get_field_of_study_names(self) -> list[str]:
        fields = self.field_of_study_service.get_all_fields_of_study()
        return [field.field_name for field in fields]

    def _get_field_of_study_by_name(self, field_name: str):
        """
        Pobiera obiekt kierunku studiów na podstawie nazwy.
        """
        if field_name == 'Wybierz kierunek studiów':
            return None
        return self.field_of_study_service.get_field_of_study_by_name(field_name)

    def _get_academic_staff_names(self) -> list[str]:
        staff_list = self.academic_staff_service.get_all_academic_staff()
        return [f"{staff.first_name} {staff.last_name}" for staff in staff_list]

    def _get_academic_staff_by_name(self, full_name: str) -> Optional[AcademicStaff]:
        """
        Pobiera obiekt pracownika na podstawie pełnego imienia i nazwiska.
        """
        all_staff = self.academic_staff_service.get_all_academic_staff()
        for staff in all_staff:
            if f"{staff.first_name} {staff.last_name}" == full_name:
                return staff
        return None

    def clear_form(self):
        self.course_name_input.text = ''
        self.ects_credits_input.text = ''
        self.field_of_study_spinner.text = 'Wybierz kierunek studiów'
        self.academic_staff_spinner.text = 'Wybierz prowadzącego'
        self.current_course = None
        
    def load_course(self, course):
        self.current_course = course
        self.course_name_input.text = course.academic_course_name
        self.ects_credits_input.text = str(course.ects_credits)
        
        # Załaduj kierunek studiów
        if hasattr(course, 'field_of_study') and course.field_of_study:
            self.field_of_study_spinner.text = course.field_of_study.field_name
            
        # Załaduj prowadzącego
        if hasattr(course, 'academic_staff') and course.academic_staff:
            self.academic_staff_spinner.text = f"{course.academic_staff.first_name} {course.academic_staff.last_name}"
        else:
            self.academic_staff_spinner.text = 'Wybierz prowadzącego'
            
    def save(self, instance):
        try:
            name = self.course_name_input.text.strip()
            ects_credits = int(self.ects_credits_input.text.strip())
            
            # Pobierz wybrany kierunek studiów
            field_of_study = self._get_field_of_study_by_name(self.field_of_study_spinner.text)
            if not field_of_study:
                print("Nie wybrano kierunku studiów")
                return

            # Pobierz wybranego pracownika
            academic_staff = None
            if self.academic_staff_spinner.text != 'Wybierz prowadzącego':
                academic_staff = self._get_academic_staff_by_name(self.academic_staff_spinner.text)

            if self.current_course:
                # Aktualizacja istniejącego kursu
                self.current_course.academic_course_name = name
                self.current_course.ects_credits = ects_credits
                self.current_course.field_of_study_id = field_of_study.field_of_study_id
                self.current_course.academic_staff_id = academic_staff.academic_staff_id if academic_staff else None
                self.service.update_academic_course(self.current_course)
            else:
                # Dodanie nowego kursu
                self.service.add_academic_course(
                    name=name,
                    ects_credits=ects_credits,
                    field_of_study_id=field_of_study.field_of_study_id,
                    academic_staff_id=academic_staff.academic_staff_id if academic_staff else None
                )

            self.manager.current = 'academic_course_view'
            self.clear_form()

        except ValueError as e:
            print(f"Błąd walidacji: {e}")
        except Exception as e:
            print(f"Błąd podczas zapisywania kursu: {e}") 

    def cancel(self, instance):
        """
        Anuluje edycję/dodawanie kursu i wraca do widoku listy kursów.
        """
        self.manager.current = 'academic_course_view'
        self.clear_form() 