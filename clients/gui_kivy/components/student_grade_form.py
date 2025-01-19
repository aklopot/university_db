from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from src.services.service_factory import ServiceFactory
from src.models.universitydb import StudentGrade, GradeType
from clients.gui_kivy.utils.colors import *
from datetime import datetime

class StudentGradeForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_student_grade_service()
        self.academic_course_service = ServiceFactory().get_academic_course_service()
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł
        self.title_label = Label(
            text="Dodaj ocenę",
            font_size='20sp',
            size_hint_y=None,
            height=50,
            color=TEXT_WHITE
        )
        self.layout.add_widget(self.title_label)
        
        # Pole wartości oceny
        grade_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=70,
            spacing=5
        )
        grade_section.add_widget(Label(
            text="Ocena:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.grade_value_input = TextInput(
            hint_text="Wprowadź ocenę (np. 4.5)",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        grade_section.add_widget(self.grade_value_input)
        self.layout.add_widget(grade_section)
        
        # Wybór kursu
        course_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=70,
            spacing=5
        )
        course_section.add_widget(Label(
            text="Kurs:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.course_spinner = Spinner(
            text='Wybierz kurs',
            values=[],  # Pusta lista na początku
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        course_section.add_widget(self.course_spinner)
        self.layout.add_widget(course_section)
        
        # Wybór typu oceny
        grade_type_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=70,
            spacing=5
        )
        grade_type_section.add_widget(Label(
            text="Typ oceny:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.grade_type_spinner = Spinner(
            text='Wybierz typ oceny',
            values=[grade_type.value for grade_type in GradeType],
            size_hint_y=None,
            height=40,
            background_color=BUTTON_LIGHT_BLUE
        )
        grade_type_section.add_widget(self.grade_type_spinner)
        self.layout.add_widget(grade_type_section)
        
        # Przyciski
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
        save_button.bind(on_press=self.save)
        button_layout.add_widget(save_button)
        
        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)
        
        self.current_grade = None
        self.current_student = None
    
    def _get_course_names(self) -> list[str]:
        if not self.current_student or not self.current_student.field_of_study:
            return []
            
        courses = self.academic_course_service.get_all_academic_courses()
        # Filtruj kursy tylko dla kierunku studiów studenta
        field_courses = [
            course.academic_course_name 
            for course in courses 
            if course.field_of_study_id == self.current_student.field_of_study.field_of_study_id
        ]
        
        if not field_courses:
            print(f"Brak kursów dla kierunku: {self.current_student.field_of_study.field_name}")
            
        return field_courses
    
    def _get_course_by_name(self, name: str):
        return self.academic_course_service.get_academic_course_by_name(name)
    
    def _refresh_course_list(self):
        current_selection = self.course_spinner.text
        self.course_spinner.values = self._get_course_names()
        if current_selection in self.course_spinner.values:
            self.course_spinner.text = current_selection
        else:
            self.course_spinner.text = 'Wybierz kurs'
    
    def clear_form(self, student):
        self.current_student = student  # Najpierw ustaw studenta
        self.title_label.text = f"Dodaj ocenę dla studenta: {student.first_name} {student.last_name}"
        if student.field_of_study:
            self.title_label.text += f" ({student.field_of_study.field_name})"
        self.grade_value_input.text = ''
        self._refresh_course_list()  # Teraz odśwież listę kursów
        self.grade_type_spinner.text = 'Wybierz typ oceny'
        self.current_grade = None
    
    def load_grade(self, grade):
        self.current_student = grade.student  # Najpierw ustaw studenta
        self.current_grade = grade
        self.title_label.text = f"Edytuj ocenę dla studenta: {grade.student.first_name} {grade.student.last_name}"
        if grade.student.field_of_study:
            self.title_label.text += f" ({grade.student.field_of_study.field_name})"
        self.grade_value_input.text = str(grade.grade_value)
        self._refresh_course_list()  # Teraz odśwież listę kursów
        self.course_spinner.text = grade.academic_course.academic_course_name
        self.grade_type_spinner.text = grade.grade_type.value
    
    def save(self, instance):
        try:
            grade_value = float(self.grade_value_input.text.strip())
            
            if self.course_spinner.text == 'Wybierz kurs':
                print("Nie wybrano kursu")
                return
                
            if self.grade_type_spinner.text == 'Wybierz typ oceny':
                print("Nie wybrano typu oceny")
                return
            
            course = self._get_course_by_name(self.course_spinner.text)
            if not course:
                print("Nie znaleziono kursu")
                return
            
            if self.current_grade:
                self.current_grade.grade_value = grade_value
                self.current_grade.academic_course_id = course.academic_course_id
                self.current_grade.grade_type = GradeType(self.grade_type_spinner.text)
                self.service.update_student_grade(self.current_grade)
            else:
                grade = StudentGrade(
                    student_id=self.current_student.student_id,
                    academic_course_id=course.academic_course_id,
                    grade_value=grade_value,
                    grade_type=GradeType(self.grade_type_spinner.text),
                    grade_date=datetime.utcnow()
                )
                self.service.add_student_grade(grade)
            
            # Przejdź do widoku ocen i odśwież listę
            grades_screen = self.manager.get_screen('student_grades_view')
            self.manager.current = 'student_grades_view'
            grades_screen.refresh_grades_list()  # Odśwież listę ocen
            
        except ValueError as e:
            print(f"Błąd walidacji: {e}")
        except Exception as e:
            print(f"Błąd podczas zapisywania oceny: {e}")
    
    def cancel(self, instance):
        self.manager.current = 'student_grades_view' 