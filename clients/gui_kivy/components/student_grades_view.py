from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
from clients.gui_kivy.utils.colors import *
from clients.gui_kivy.utils.dialog_utils import DialogUtils
from clients.gui_kivy.utils.fonts import *

class StudentGradesView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_student_grade_service()
        
        # Główny układ
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł
        self.title_label = Label(
            text="Oceny studenta",
            font_size=FONT_SIZE_TITLE,
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(self.title_label)
        
        # Lista ocen
        self.grades_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.grades_list_container.bind(minimum_height=self.grades_list_container.setter('height'))
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.grades_list_container)
        self.layout.add_widget(self.scroll_view)
        
        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        return_button = Button(
            text='Powrót',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_PEARL
        )
        return_button.bind(on_press=self.return_to_students)
        bottom_layout.add_widget(return_button)
        
        add_button = Button(
            text='Dodaj ocenę',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        add_button.bind(on_press=self.add_grade)
        bottom_layout.add_widget(add_button)
        
        self.layout.add_widget(bottom_layout)
        self.add_widget(self.layout)
        
        self.current_student = None
        
    def load_student_grades(self, student):
        self.current_student = student
        self.title_label.text = f"Oceny studenta: {student.first_name} {student.last_name}"
        self.refresh_grades_list()
        
    def refresh_grades_list(self):
        if not self.current_student:
            return
            
        grades = self.service.get_student_grades(self.current_student.student_id)
        self.grades_list_container.clear_widgets()
        
        for grade in grades:
            grade_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=50,
                spacing=2
            )
            
            grade_box.add_widget(Label(
                text=f"{grade.academic_course.academic_course_name}: {grade.grade_value} ({grade.grade_type.value})",
                size_hint_x=0.6,
                font_size=FONT_SIZE_LIST_ITEM,
                color=TEXT_WHITE
            ))
            
            buttons_box = BoxLayout(
                size_hint_x=0.3,
                spacing=2
            )
            
            edit_btn = Button(
                text='Edytuj',
                size_hint_x=0.5,
                background_color=BUTTON_GREEN
            )
            edit_btn.bind(on_press=lambda x, g=grade: self.edit_grade(g))
            buttons_box.add_widget(edit_btn)
            
            delete_btn = Button(
                text='Usuń',
                size_hint_x=0.5,
                background_color=BUTTON_RED
            )
            delete_btn.bind(on_press=lambda x, g=grade: self.confirm_delete_grade(g))
            buttons_box.add_widget(delete_btn)
            
            grade_box.add_widget(buttons_box)
            
            container = BoxLayout(orientation='vertical', size_hint_y=None, height=55)
            container.add_widget(grade_box)
            
            self.grades_list_container.add_widget(container)
            
    def add_grade(self, instance):
        self.manager.current = 'student_grade_form'
        form_screen = self.manager.get_screen('student_grade_form')
        form_screen.clear_form(self.current_student)
        
    def edit_grade(self, grade):
        self.manager.current = 'student_grade_form'
        form_screen = self.manager.get_screen('student_grade_form')
        form_screen.load_grade(grade)
        
    def confirm_delete_grade(self, grade):
        DialogUtils.show_delete_confirmation(
            item_type="ocenę",
            item_name=f"{grade.grade_value} z {grade.academic_course.academic_course_name}",
            on_confirm=lambda: self.delete_grade(grade)
        )
        
    def delete_grade(self, grade):
        self.service.delete_student_grade(grade.student_grade_id)
        self.refresh_grades_list()
        
    def return_to_students(self, instance):
        self.manager.current = 'student_view' 