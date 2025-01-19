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

class FieldOfStudyView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_field_of_study_service()
        
        # Główny układ
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł
        title_label = Label(
            text="Lista kierunków studiów",
            font_size=FONT_SIZE_TITLE,
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(title_label)
        
        # Lista kierunków
        self.field_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.field_list_container.bind(minimum_height=self.field_list_container.setter('height'))
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.field_list_container)
        self.layout.add_widget(self.scroll_view)
        
        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        return_button = Button(
            text='Powrót do menu',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_PEARL
        )
        return_button.bind(on_press=self.return_to_main_menu)
        bottom_layout.add_widget(return_button)
        
        add_button = Button(
            text='Dodaj kierunek',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        add_button.bind(on_press=self.add_field_of_study)
        bottom_layout.add_widget(add_button)
        
        self.layout.add_widget(bottom_layout)
        self.add_widget(self.layout)
        
        self.bind(on_pre_enter=lambda instance: self.refresh_field_list())
    
    def refresh_field_list(self):
        fields = self.service.get_all_fields_of_study()
        self.field_list_container.clear_widgets()
        
        for field in fields:
            field_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=50,
                spacing=2
            )
            
            field_box.add_widget(Label(
                text=field.field_name,
                size_hint_x=0.6,
                font_size=FONT_SIZE_LIST_ITEM,
                color=TEXT_WHITE
            ))
            
            buttons_box = BoxLayout(
                size_hint_x=0.4,
                spacing=2
            )
            
            edit_btn = Button(
                text='Edytuj',
                size_hint_x=0.5,
                background_color=BUTTON_GREEN
            )
            edit_btn.bind(on_press=lambda x, f=field: self.edit_field_of_study(f))
            buttons_box.add_widget(edit_btn)
            
            delete_btn = Button(
                text='Usuń',
                size_hint_x=0.5,
                background_color=BUTTON_RED
            )
            delete_btn.bind(on_press=lambda x, f=field: self.confirm_delete_field(f))
            buttons_box.add_widget(delete_btn)
            
            field_box.add_widget(buttons_box)
            
            container = BoxLayout(orientation='vertical', size_hint_y=None, height=55)
            container.add_widget(field_box)
            
            self.field_list_container.add_widget(container)
    
    def add_field_of_study(self, instance):
        self.manager.current = 'field_of_study_form'
        form_screen = self.manager.get_screen('field_of_study_form')
        form_screen.clear_form()
    
    def edit_field_of_study(self, field):
        self.manager.current = 'field_of_study_form'
        form_screen = self.manager.get_screen('field_of_study_form')
        form_screen.load_field_of_study(field)
    
    def confirm_delete_field(self, field):
        DialogUtils.show_delete_confirmation(
            item_type="kierunek studiów",
            item_name=field.field_name,
            on_confirm=lambda: self.delete_field_of_study(field)
        )
    
    def delete_field_of_study(self, field):
        self.service.delete_field_of_study(field.field_of_study_id)
        self.refresh_field_list()
    
    def return_to_main_menu(self, instance):
        self.manager.current = 'menu' 