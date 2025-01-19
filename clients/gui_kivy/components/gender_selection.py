from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from src.services.service_factory import ServiceFactory
from clients.gui_kivy.utils.colors import *  # Dodajemy import kolorów
import json

class GenderSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.gender_service = ServiceFactory().get_gender_service()
        
        # Główny układ z paddingiem
        self.layout = BoxLayout(
            orientation='vertical',
            padding=10,  # Dodajemy padding 10 ze wszystkich stron
            spacing=10   # Dodajemy odstęp między elementami
        )
        
        # Przewijalna lista płci
        self.gender_list_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None
        )
        self.gender_list_container.bind(minimum_height=self.gender_list_container.setter('height'))
        self.gender_list_scroll = ScrollView()
        self.gender_list_scroll.add_widget(self.gender_list_container)
        self.layout.add_widget(self.gender_list_scroll)
        
        # Przyciski na dole
        bottom_layout = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10  # Odstęp między przyciskami
        )
        
        # Przycisk Anuluj (po lewej)
        cancel_button = Button(
            text='Anuluj',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_PEARL
        )
        cancel_button.bind(on_press=self.cancel)
        bottom_layout.add_widget(cancel_button)
        
        # Przycisk Dodaj płeć (po prawej)
        add_button = Button(
            text='Dodaj płeć',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        add_button.bind(on_press=self.open_add_gender_form)
        bottom_layout.add_widget(add_button)
        
        self.layout.add_widget(bottom_layout)
        self.add_widget(self.layout)
        
        self.previous_screen = None
        self.parent_form = None
        
    def on_pre_enter(self):
        # Odśwież listę płci za każdym razem, gdy wchodzimy na ekran
        self.refresh_gender_list()
        
    def refresh_gender_list(self):
        genders = self.gender_service.get_all_genders()
        
        # Wyczyść listę
        self.gender_list_container.clear_widgets()
        
        # Dodaj odstęp na górze listy
        self.gender_list_container.add_widget(Widget(size_hint_y=None, height=10))
        
        for gender in genders:
            # Główny box dla wiersza z płcią
            gender_box = BoxLayout(
                orientation='horizontal', 
                size_hint_y=None, 
                height=50,
                spacing=2  # Zmniejszony odstęp między elementami
            )
            
            # Label z nazwą płci
            gender_box.add_widget(Label(
                text=gender.gender_name,
                size_hint_x=0.6,
                halign='left',
                valign='middle',
                color=TEXT_WHITE,
                text_size=(None, 50)  # Ustawienie wysokości tekstu
            ))
            
            # Kontener na przyciski
            buttons_box = BoxLayout(
                size_hint_x=0.4,
                spacing=2  # Zmniejszony odstęp między przyciskami
            )
            
            # Przycisk wyboru
            select_btn = Button(
                text='Wybierz',
                size_hint_x=0.33,
                background_color=BUTTON_LIGHT_BLUE
            )
            select_btn.bind(on_press=lambda x, g=gender: self.select_gender(g))
            buttons_box.add_widget(select_btn)
            
            # Przycisk edycji
            edit_btn = Button(
                text='Edytuj',
                size_hint_x=0.33,
                background_color=BUTTON_GREEN
            )
            edit_btn.bind(on_press=lambda x, g=gender: self.open_edit_gender_form(g))
            buttons_box.add_widget(edit_btn)
            
            # Przycisk usuwania
            delete_btn = Button(
                text='Usuń',
                size_hint_x=0.33,
                background_color=BUTTON_RED
            )
            delete_btn.bind(on_press=lambda x, g=gender: self.delete_gender(g))
            buttons_box.add_widget(delete_btn)
            
            gender_box.add_widget(buttons_box)
            
            # Kontener z odstępami
            container = BoxLayout(
                orientation='vertical', 
                size_hint_y=None, 
                height=55,  # 50 na wiersz + 5 na odstęp
                padding=[0, 0, 0, 5]  # Dolny padding 5
            )
            container.add_widget(gender_box)
            
            self.gender_list_container.add_widget(container)
            
    def select_gender(self, gender):
        if hasattr(self, 'parent_form'):
            self.parent_form.selected_gender = gender
            self.parent_form.selected_gender_label.text = gender.gender_name
            self.manager.current = self.previous_screen
        
    def open_add_gender_form(self, instance):
        # Przejdź do ekranu formularza dodawania płci
        self.manager.current = 'gender_form'
        form_screen = self.manager.get_screen('gender_form')
        form_screen.clear_form()
        form_screen.previous_screen = 'gender_selection'
        
    def open_edit_gender_form(self, gender):
        # Przejdź do ekranu formularza edycji płci
        self.manager.current = 'gender_form'
        form_screen = self.manager.get_screen('gender_form')
        form_screen.load_gender(gender)
        form_screen.previous_screen = 'gender_selection'
        
    def delete_gender(self, gender):
        # Potwierdzenie usunięcia płci
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"Are you sure you want to delete gender '{gender.gender_name}'?"))
        
        button_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        
        content.add_widget(button_layout)
        
        popup = Popup(title='Confirm Delete', content=content, size_hint=(0.6, 0.4))
        yes_button.bind(on_press=lambda *args: self.confirm_delete_gender(gender, popup))
        no_button.bind(on_press=popup.dismiss)
        
        popup.open()
        
    def confirm_delete_gender(self, gender, popup):
        self.gender_service.delete_gender(gender.gender_id)
        self.refresh_gender_list()
        popup.dismiss()
        
    def cancel(self, instance):
        # Wróć do poprzedniego ekranu
        self.manager.current = self.previous_screen
