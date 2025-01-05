from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from src.services.service_factory import ServiceFactory
from src.models.universitydb import AcademicCourse

class AcademicCourseForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_academic_course_service()
        self.field_of_study_service = ServiceFactory().get_field_of_study_service()
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Pola formularza
        self.course_name_input = TextInput(
            hint_text="Nazwa kursu",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(self.course_name_input)
        
        self.ects_credits_input = TextInput(
            hint_text="Punkty ECTS",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(self.ects_credits_input)
        
        # Lista rozwijana dla kierunku studiów
        self.field_of_study_spinner = Spinner(
            text='Wybierz kierunek studiów',
            values=self._get_field_of_study_names(),
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(self.field_of_study_spinner)
        
        # Przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        save_button = Button(text='Zapisz')
        save_button.bind(on_press=self.save)
        button_layout.add_widget(save_button)
        
        cancel_button = Button(text='Anuluj')
        cancel_button.bind(on_press=self.cancel)
        button_layout.add_widget(cancel_button)
        
        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)
        
        self.current_course = None
        
    def _get_field_of_study_names(self) -> list[str]:
        fields = self.field_of_study_service.get_all_fields_of_study()
        return [field.field_name for field in fields]
        
    def clear_form(self):
        self.course_name_input.text = ''
        self.ects_credits_input.text = ''
        self.field_of_study_spinner.text = 'Wybierz kierunek studiów'
        self.current_course = None
        
    def load_course(self, course):
        self.current_course = course
        self.course_name_input.text = course.academic_course_name
        self.ects_credits_input.text = str(course.ects_credits)
        if course.field_of_study:
            self.field_of_study_spinner.text = course.field_of_study.field_name
            
    def save(self, instance):
        try:
            name = self.course_name_input.text.strip()
            ects_credits = int(self.ects_credits_input.text.strip())
            
            # Znajdź wybrany kierunek studiów
            field_name = self.field_of_study_spinner.text
            field_of_study = self.field_of_study_service.get_field_of_study_by_name(field_name)
            
            if not field_of_study:
                print("Nie wybrano kierunku studiów")
                return
                
            if self.current_course:
                # Aktualizacja istniejącego kursu
                self.current_course.academic_course_name = name
                self.current_course.ects_credits = ects_credits
                self.current_course.field_of_study_id = field_of_study.field_of_study_id
                self.service.update_academic_course(self.current_course)
            else:
                # Dodanie nowego kursu
                self.service.add_academic_course(
                    name=name,
                    ects_credits=ects_credits,
                    field_of_study_id=field_of_study.field_of_study_id
                )
            
            # Wróć do listy kursów
            self.manager.current = 'academic_course_view'
            self.clear_form()
            
        except ValueError as e:
            print(f"Błąd walidacji: {e}")
        except Exception as e:
            print(f"Błąd podczas zapisywania kursu: {e}")
            
    def cancel(self, instance):
        self.manager.current = 'academic_course_view'
        self.clear_form() 