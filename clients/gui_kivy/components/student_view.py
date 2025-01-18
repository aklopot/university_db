# student_view.py: Zawiera widok, który wyświetla listę studentów w aplikacji Kivy. Umożliwia dodawanie, edytowanie i usuwanie studentów.
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
import json
from clients.gui_kivy.utils.colors import *
from clients.gui_kivy.utils.dialog_utils import DialogUtils

class StudentView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_student_service()

        # Główny układ
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Tytuł
        title_label = Label(
            text="Lista studentów",
            font_size='20sp',
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(title_label)

        # Przewijalna lista studentów (na górze)
        self.student_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.student_list_container.bind(minimum_height=self.student_list_container.setter('height'))
        self.student_list_scroll = ScrollView()
        self.student_list_scroll.add_widget(self.student_list_container)
        self.layout.add_widget(self.student_list_scroll)

        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        return_button = Button(
            text='Powrót do menu',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_ORANGE
        )
        return_button.bind(on_press=self.return_to_main_menu)
        bottom_layout.add_widget(return_button)

        add_button = Button(
            text='Dodaj studenta', 
            size_hint_y=None, 
            height=50,
            background_color=BUTTON_GREEN
        )
        add_button.bind(on_press=self.add_student)
        bottom_layout.add_widget(add_button)

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
            # Główny box dla wiersza ze studentem
            student_box = BoxLayout(
                orientation='horizontal', 
                size_hint_y=None, 
                height=50,
                spacing=2  # Odstęp poziomy między elementami
            )
            
            # Label z danymi studenta
            student_info = f"{student.first_name} {student.last_name} (Index: {student.index_number})"
            student_box.add_widget(Label(
                text=student_info, 
                size_hint_x=0.6,
                font_size='18sp',
                color=TEXT_WHITE
            ))
            
            # Przyciski w osobnym boxlayout dla lepszego rozmieszczenia
            buttons_box = BoxLayout(
                size_hint_x=0.4, 
                spacing=2  # Odstęp poziomy między przyciskami
            )
            
            edit_btn = Button(
                text='Edytuj',
                size_hint_x=0.5,
                background_color=BUTTON_GREEN
            )
            edit_btn.bind(on_press=lambda instance, student=student: self.edit_student(student))
            buttons_box.add_widget(edit_btn)

            delete_btn = Button(
                text='Usuń',
                size_hint_x=0.5,
                background_color=BUTTON_RED
            )
            delete_btn.bind(on_press=lambda instance, student=student: self.delete_student(student))
            buttons_box.add_widget(delete_btn)
            
            student_box.add_widget(buttons_box)
            
            # Dodaj odstęp pionowy między wierszami
            container = BoxLayout(orientation='vertical', size_hint_y=None, height=55)  # 50 + 5 na margines
            container.add_widget(student_box)
            
            self.student_list_container.add_widget(container)

    def add_student(self, instance):
        self.manager.current = 'student_form'
        form_screen = self.manager.get_screen('student_form')
        form_screen.clear_form()

    def edit_student(self, student):
        self.manager.current = 'student_form'
        form_screen = self.manager.get_screen('student_form')
        form_screen.load_student(student)

    def delete_student(self, student):
        DialogUtils.show_delete_confirmation(
            item_type="studenta",
            item_name=f"{student.first_name} {student.last_name}",
            on_confirm=lambda: self.confirm_delete_student(student)
        )
    
    def confirm_delete_student(self, student):
        self.service.delete_student(student.index_number)
        self.refresh_student_list()

    def return_to_main_menu(self, instance):
        self.manager.current = 'menu'
