from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
from clients.gui_kivy.utils.colors import *
from clients.gui_kivy.utils.dialog_utils import DialogUtils

class AcademicCourseView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_academic_course_service()
        
        # Główny układ
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Tytuł
        title_label = Label(
            text="Lista kursów akademickich",
            font_size='20sp',
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(title_label)

        # Lista kursów
        self.academic_course_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.academic_course_list_container.bind(minimum_height=self.academic_course_list_container.setter('height'))
        
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.academic_course_list_container)
        self.layout.add_widget(self.scroll_view)
        
        # Przyciski na dole
        self.bottom_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        # Przycisk powrotu do menu
        back_button = Button(
            text='Powrót do menu',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_ORANGE
        )
        back_button.bind(on_press=lambda x: self.go_back_to_menu())
        self.bottom_layout.add_widget(back_button)

        # Przycisk dodawania nowego kursu
        add_button = Button(
            text='Dodaj nowy kurs',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        add_button.bind(on_press=self.add_academic_course)
        self.bottom_layout.add_widget(add_button)
        
        self.layout.add_widget(self.bottom_layout)
        self.add_widget(self.layout)
        
    def on_pre_enter(self):
        self.refresh_academic_course_list()
        
    def refresh_academic_course_list(self):
        courses = self.service.get_all_academic_courses()
        self.academic_course_list_container.clear_widgets()
        
        for course in courses:
            # Główny box dla wiersza z kursem
            course_box = BoxLayout(
                orientation='horizontal', 
                size_hint_y=None, 
                height=50,
                spacing=2  # Odstęp poziomy między elementami
            )
            
            # Label z danymi kursu
            course_box.add_widget(Label(
                text=f"{course.academic_course_name} ({course.field_of_study.field_name if course.field_of_study else 'Brak kierunku'})",
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
            edit_btn.bind(on_press=lambda x, c=course: self.edit_academic_course(c))
            buttons_box.add_widget(edit_btn)
            
            delete_btn = Button(
                text='Usuń',
                size_hint_x=0.5,
                background_color=BUTTON_RED
            )
            delete_btn.bind(on_press=lambda x, c=course: self.confirm_delete_course(c))
            buttons_box.add_widget(delete_btn)
            
            course_box.add_widget(buttons_box)
            
            # Dodaj odstęp pionowy między wierszami
            container = BoxLayout(orientation='vertical', size_hint_y=None, height=55)  # 50 + 5 na margines
            container.add_widget(course_box)
            
            self.academic_course_list_container.add_widget(container)
    
    def add_academic_course(self, instance):
        self.manager.current = 'academic_course_form'
        form_screen = self.manager.get_screen('academic_course_form')
        form_screen.clear_form()
        
    def edit_academic_course(self, course):
        self.manager.current = 'academic_course_form'
        form_screen = self.manager.get_screen('academic_course_form')
        form_screen.load_course(course)
        
    def confirm_delete_course(self, course):
        DialogUtils.show_delete_confirmation(
            item_type="kurs",
            item_name=course.academic_course_name,
            on_confirm=lambda: self.delete_course(course)
        )
        
    def delete_course(self, course):
        self.service.delete_academic_course(course.academic_course_id)
        self.refresh_academic_course_list()
        
    def go_back_to_menu(self):
        self.manager.current = 'menu' 