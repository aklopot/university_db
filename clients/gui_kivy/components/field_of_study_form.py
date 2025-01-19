from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from src.services.service_factory import ServiceFactory
from src.models.universitydb import FieldOfStudy
from clients.gui_kivy.utils.colors import *

class FieldOfStudyForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_field_of_study_service()
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł
        self.title_label = Label(
            text="Dodaj kierunek studiów",
            font_size='20sp',
            size_hint_y=None,
            height=50,
            color=TEXT_WHITE
        )
        self.layout.add_widget(self.title_label)
        
        # Pole nazwy kierunku
        field_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=70,
            spacing=5
        )
        field_section.add_widget(Label(
            text="Nazwa kierunku:",
            size_hint_y=None,
            height=20,
            color=TEXT_WHITE
        ))
        self.field_name_input = TextInput(
            hint_text="Wprowadź nazwę kierunku",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        field_section.add_widget(self.field_name_input)
        self.layout.add_widget(field_section)
        
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
        
        self.current_field = None
    
    def clear_form(self):
        self.title_label.text = "Dodaj kierunek studiów"
        self.field_name_input.text = ''
        self.current_field = None
    
    def load_field_of_study(self, field):
        self.title_label.text = "Edytuj kierunek studiów"
        self.current_field = field
        self.field_name_input.text = field.field_name
    
    def save(self, instance):
        try:
            name = self.field_name_input.text.strip()
            
            if not name:
                print("Nazwa kierunku nie może być pusta")
                return
            
            if self.current_field:
                self.current_field.field_name = name
                self.service.update_field_of_study(self.current_field)
            else:
                self.service.add_field_of_study(name)
            
            self.manager.current = 'field_of_study_view'
            self.clear_form()
        except Exception as e:
            print(f"Błąd podczas zapisywania kierunku studiów: {e}")
    
    def cancel(self, instance):
        self.manager.current = 'field_of_study_view'
        self.clear_form() 