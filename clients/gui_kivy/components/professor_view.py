from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
import json

class ProfessorView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_professor_service()
        
        # Główny układ
        self.layout = BoxLayout(orientation='vertical')
        
        # Przewijalna lista profesorów
        self.professor_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.professor_list_container.bind(minimum_height=self.professor_list_container.setter('height'))
        self.professor_list_scroll = ScrollView()
        self.professor_list_scroll.add_widget(self.professor_list_container)
        self.layout.add_widget(self.professor_list_scroll)
        
        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        
        add_button = Button(text='Add Professor')
        add_button.bind(on_press=self.add_professor)
        bottom_layout.add_widget(add_button)
        
        return_button = Button(text='Return to Main Menu')
        return_button.bind(on_press=self.return_to_main_menu)
        bottom_layout.add_widget(return_button)
        
        self.layout.add_widget(bottom_layout)
        
        self.add_widget(self.layout)
        
        self.bind(on_pre_enter=lambda instance: self.refresh_professor_list())
    
    def refresh_professor_list(self):
        professors = self.service.get_all_professors()
        
        # Wyczyść listę
        self.professor_list_container.clear_widgets()
        
        for professor in professors:
            professor_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            professor_box.add_widget(Label(text=f"{professor.first_name} {professor.last_name}", size_hint_x=0.6))
            
            edit_btn = Button(text='Edit', size_hint_x=0.2)
            edit_btn.bind(on_press=lambda instance, professor=professor: self.edit_professor(professor))
            professor_box.add_widget(edit_btn)
            
            delete_btn = Button(text='Delete', size_hint_x=0.2)
            delete_btn.bind(on_press=lambda instance, professor=professor: self.confirm_delete_professor(professor))
            professor_box.add_widget(delete_btn)
            
            self.professor_list_container.add_widget(professor_box)
    
    def add_professor(self, instance):
        self.manager.current = 'professor_form'
        form_screen = self.manager.get_screen('professor_form')
        form_screen.clear_form()
    
    def edit_professor(self, professor):
        self.manager.current = 'professor_form'
        form_screen = self.manager.get_screen('professor_form')
        form_screen.load_professor(professor)
    
    def confirm_delete_professor(self, professor):
        # Potwierdzenie usunięcia
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"Czy na pewno chcesz usunąć profesora {professor.first_name} {professor.last_name}?"))
        
        button_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        
        content.add_widget(button_layout)
        
        popup = Popup(title='Potwierdź usunięcie', content=content, size_hint=(0.6, 0.4))
        yes_button.bind(on_press=lambda *args: self.delete_professor(professor, popup))
        no_button.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def delete_professor(self, professor, popup):
        self.service.delete_professor(professor.pesel)
        self.refresh_professor_list()
        popup.dismiss()
    
    def return_to_main_menu(self, instance):
        self.manager.current = 'menu'
