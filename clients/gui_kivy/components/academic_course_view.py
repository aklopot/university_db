from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory

class AcademicCourseView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_academic_course_service()
        
        # Główny układ
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Lista kursów
        self.academic_course_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.academic_course_list_container.bind(minimum_height=self.academic_course_list_container.setter('height'))
        
        scroll_view = ScrollView()
        scroll_view.add_widget(self.academic_course_list_container)
        layout.add_widget(scroll_view)
        
        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        # Przycisk dodawania nowego kursu
        add_button = Button(text='Dodaj nowy kurs', size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_academic_course)
        bottom_layout.add_widget(add_button)

        # Przycisk powrotu do menu
        back_button = Button(text='Powrót do menu', size_hint_y=None, height=50)
        back_button.bind(on_press=lambda x: self.go_back_to_menu())
        bottom_layout.add_widget(back_button)
        
        layout.add_widget(bottom_layout)

        self.add_widget(layout)
        
    def on_pre_enter(self):
        self.refresh_academic_course_list()
        
    def refresh_academic_course_list(self):
        courses = self.service.get_all_academic_courses()
        self.academic_course_list_container.clear_widgets()
        
        for course in courses:
            course_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            course_box.add_widget(Label(
                text=f"{course.academic_course_name} (ECTS: {course.ects_credits})",
                size_hint_x=0.6
            ))
            
            edit_btn = Button(text='Edytuj', size_hint_x=0.2)
            edit_btn.bind(on_press=lambda x, c=course: self.edit_academic_course(c))
            course_box.add_widget(edit_btn)
            
            delete_btn = Button(text='Usuń', size_hint_x=0.2)
            delete_btn.bind(on_press=lambda x, c=course: self.confirm_delete_course(c))
            course_box.add_widget(delete_btn)
            
            self.academic_course_list_container.add_widget(course_box)
    
    def add_academic_course(self, instance):
        self.manager.current = 'academic_course_form'
        form_screen = self.manager.get_screen('academic_course_form')
        form_screen.clear_form()
        
    def edit_academic_course(self, course):
        self.manager.current = 'academic_course_form'
        form_screen = self.manager.get_screen('academic_course_form')
        form_screen.load_course(course)
        
    def confirm_delete_course(self, course):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(
            text=f"Czy na pewno chcesz usunąć kurs:\n{course.academic_course_name}?"
        ))
        
        button_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Tak')
        no_button = Button(text='Nie')
        
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(button_layout)
        
        popup = Popup(title='Potwierdź usunięcie', content=content, size_hint=(0.6, 0.4))
        yes_button.bind(on_press=lambda *args: self.delete_course(course, popup))
        no_button.bind(on_press=popup.dismiss)
        
        popup.open()
        
    def delete_course(self, course, popup):
        self.service.delete_academic_course(course.academic_course_id)
        self.refresh_academic_course_list()
        popup.dismiss()
        
    def go_back_to_menu(self):
        self.manager.current = 'menu' 