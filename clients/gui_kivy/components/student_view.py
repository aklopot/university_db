# student_view.py: Zawiera widok, który wyświetla listę studentów w aplikacji Kivy. Umożliwia dodawanie, edytowanie i usuwanie studentów.
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
import json

class StudentView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Wczytaj konfigurację
        with open("config/config.json") as config_file:
            config = json.load(config_file)
        
        self.service = ServiceFactory(config).get_student_service()

        # Główny układ
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Przewijalna lista studentów (na górze)
        self.student_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.student_list_container.bind(minimum_height=self.student_list_container.setter('height'))
        self.student_list_scroll = ScrollView()
        self.student_list_scroll.add_widget(self.student_list_container)
        self.layout.add_widget(self.student_list_scroll)

        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        add_button = Button(text='Add Student', size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_student)
        bottom_layout.add_widget(add_button)

        return_button = Button(text='Return to Main Menu', size_hint_y=None, height=50)
        return_button.bind(on_press=self.return_to_main_menu)
        bottom_layout.add_widget(return_button)

        self.layout.add_widget(bottom_layout)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        # Odśwież listę studentów za każdym razem, gdy wchodzimy na ekran
        self.refresh_student_list()

    def refresh_student_list(self):
        students = self.service.get_all_students()

        # Wyczyść listę
        self.student_list_container.clear_widgets()

        for student in students:
            student_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            student_info = f"{student.first_name} {student.last_name} (Index: {student.index_number})"
            student_box.add_widget(Label(text=student_info, size_hint_x=0.6))
            
            edit_btn = Button(text='Edit', size_hint_x=0.2)
            edit_btn.bind(on_press=lambda instance, student=student: self.edit_student(student))
            student_box.add_widget(edit_btn)

            delete_btn = Button(text='Delete', size_hint_x=0.2)
            delete_btn.bind(on_press=lambda instance, student=student: self.delete_student(student))
            student_box.add_widget(delete_btn)

            self.student_list_container.add_widget(student_box)

    def add_student(self, instance):
        self.manager.current = 'student_form'
        form_screen = self.manager.get_screen('student_form')
        form_screen.clear_form()

    def edit_student(self, student):
        self.manager.current = 'student_form'
        form_screen = self.manager.get_screen('student_form')
        form_screen.load_student(student)

    def delete_student(self, student):
        # Potwierdzenie usunięcia
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"Are you sure you want to delete student {student.first_name} {student.last_name}?"))

        button_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')

        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)

        content.add_widget(button_layout)

        popup = Popup(title='Confirm Delete', content=content, size_hint=(0.6, 0.4))
        yes_button.bind(on_press=lambda *args: self.confirm_delete_student(student, popup))
        no_button.bind(on_press=popup.dismiss)

        popup.open()

    def confirm_delete_student(self, student, popup):
        self.service.delete_student(student.index_number)
        self.refresh_student_list()
        popup.dismiss()

    def return_to_main_menu(self, instance):
        self.manager.current = 'menu'
