from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
from clients.gui_kivy.utils.colors import *
from clients.gui_kivy.utils.dialog_utils import DialogUtils
import json

class AcademicStaffView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_academic_staff_service()
        
        # Główny układ
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł
        title_label = Label(
            text="Lista pracowników akademickich",
            font_size='20sp',
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(title_label)
        
        # Przewijalna lista pracowników akademickich
        self.academic_staff_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.academic_staff_list_container.bind(minimum_height=self.academic_staff_list_container.setter('height'))
        self.academic_staff_list_scroll = ScrollView()
        self.academic_staff_list_scroll.add_widget(self.academic_staff_list_container)
        self.layout.add_widget(self.academic_staff_list_scroll)
        
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
            text='Dodaj pracownika',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        add_button.bind(on_press=self.add_academic_staff)
        bottom_layout.add_widget(add_button)
        
        self.layout.add_widget(bottom_layout)
        self.add_widget(self.layout)
        
        self.bind(on_pre_enter=lambda instance: self.refresh_academic_staff_list())
    
    def refresh_academic_staff_list(self):
        academic_staff_list = self.service.get_all_academic_staff()
        
        # Wyczyść listę
        self.academic_staff_list_container.clear_widgets()
        
        for academic_staff in academic_staff_list:
            # Główny box dla wiersza z pracownikiem
            academic_staff_box = BoxLayout(
                orientation='horizontal', 
                size_hint_y=None, 
                height=50,
                spacing=2  # Odstęp poziomy między elementami
            )
            
            # Label z danymi pracownika
            academic_staff_box.add_widget(Label(
                text=f"{academic_staff.first_name} {academic_staff.last_name}",
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
                size_hint_x=0.5,  # Zmienione z 0.2 na 0.5 bo teraz jest w osobnym boxlayout
                background_color=BUTTON_GREEN
            )
            edit_btn.bind(on_press=lambda instance, staff=academic_staff: self.edit_academic_staff(staff))
            buttons_box.add_widget(edit_btn)
            
            delete_btn = Button(
                text='Usuń',
                size_hint_x=0.5,  # Zmienione z 0.2 na 0.5 bo teraz jest w osobnym boxlayout
                background_color=BUTTON_RED
            )
            delete_btn.bind(on_press=lambda instance, staff=academic_staff: self.confirm_delete_academic_staff(staff))
            buttons_box.add_widget(delete_btn)
            
            academic_staff_box.add_widget(buttons_box)
            
            # Dodaj odstęp pionowy między wierszami
            container = BoxLayout(orientation='vertical', size_hint_y=None, height=55)  # 50 + 5 na margines
            container.add_widget(academic_staff_box)
            
            self.academic_staff_list_container.add_widget(container)
    
    def add_academic_staff(self, instance):
        self.manager.current = 'academic_staff_form'
        form_screen = self.manager.get_screen('academic_staff_form')
        form_screen.clear_form()
    
    def edit_academic_staff(self, academic_staff):
        self.manager.current = 'academic_staff_form'
        form_screen = self.manager.get_screen('academic_staff_form')
        form_screen.load_academic_staff(academic_staff)
    
    def confirm_delete_academic_staff(self, academic_staff):
        DialogUtils.show_delete_confirmation(
            item_type="pracownika",
            item_name=f"{academic_staff.first_name} {academic_staff.last_name}",
            on_confirm=lambda: self.delete_academic_staff(academic_staff)
        )
    
    def delete_academic_staff(self, academic_staff):
        self.service.delete_academic_staff(academic_staff.pesel)
        self.refresh_academic_staff_list()
    
    def return_to_main_menu(self, instance):
        self.manager.current = 'menu'
