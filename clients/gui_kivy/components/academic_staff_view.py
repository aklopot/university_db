from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
import json

class AcademicStaffView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_academic_staff_service()
        
        # Główny układ
        self.layout = BoxLayout(orientation='vertical')
        
        # Przewijalna lista pracowników akademickich
        self.academic_staff_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.academic_staff_list_container.bind(minimum_height=self.academic_staff_list_container.setter('height'))
        self.academic_staff_list_scroll = ScrollView()
        self.academic_staff_list_scroll.add_widget(self.academic_staff_list_container)
        self.layout.add_widget(self.academic_staff_list_scroll)
        
        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        
        add_button = Button(text='Add Academic Staff')
        add_button.bind(on_press=self.add_academic_staff)
        bottom_layout.add_widget(add_button)
        
        return_button = Button(text='Return to Main Menu')
        return_button.bind(on_press=self.return_to_main_menu)
        bottom_layout.add_widget(return_button)
        
        self.layout.add_widget(bottom_layout)
        
        self.add_widget(self.layout)
        
        self.bind(on_pre_enter=lambda instance: self.refresh_academic_staff_list())
    
    def refresh_academic_staff_list(self):
        academic_staff_list = self.service.get_all_academic_staff()
        
        # Wyczyść listę
        self.academic_staff_list_container.clear_widgets()
        
        for academic_staff in academic_staff_list:
            academic_staff_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            academic_staff_box.add_widget(Label(text=f"{academic_staff.first_name} {academic_staff.last_name}", size_hint_x=0.6))
            
            edit_btn = Button(text='Edit', size_hint_x=0.2)
            edit_btn.bind(on_press=lambda instance, academic_staff=academic_staff: self.edit_academic_staff(academic_staff))
            academic_staff_box.add_widget(edit_btn)
            
            delete_btn = Button(text='Delete', size_hint_x=0.2)
            delete_btn.bind(on_press=lambda instance, academic_staff=academic_staff: self.confirm_delete_academic_staff(academic_staff))
            academic_staff_box.add_widget(delete_btn)
            
            self.academic_staff_list_container.add_widget(academic_staff_box)
    
    def add_academic_staff(self, instance):
        self.manager.current = 'academic_staff_form'
        form_screen = self.manager.get_screen('academic_staff_form')
        form_screen.clear_form()
    
    def edit_academic_staff(self, academic_staff):
        self.manager.current = 'academic_staff_form'
        form_screen = self.manager.get_screen('academic_staff_form')
        form_screen.load_academic_staff(academic_staff)
    
    def confirm_delete_academic_staff(self, academic_staff):
        # Potwierdzenie usunięcia
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"Czy na pewno chcesz usunąć tego pracownika akademickiego:\n{academic_staff.first_name} {academic_staff.last_name}"))
        
        button_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        
        content.add_widget(button_layout)
        
        popup = Popup(title='Potwierdź usunięcie', content=content, size_hint=(0.6, 0.4))
        yes_button.bind(on_press=lambda *args: self.delete_academic_staff(academic_staff, popup))
        no_button.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def delete_academic_staff(self, academic_staff, popup):
        self.service.delete_academic_staff(academic_staff.pesel)
        self.refresh_academic_staff_list()
        popup.dismiss()
    
    def return_to_main_menu(self, instance):
        self.manager.current = 'menu'
