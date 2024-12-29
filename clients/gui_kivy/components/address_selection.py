from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
import json

class AddressSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Wczytaj konfigurację
        with open("config/config.json") as config_file:
            config = json.load(config_file)
        
        self.address_service = ServiceFactory(config).get_address_service()
        
        # Główny układ
        self.layout = BoxLayout(orientation='vertical')
        
        # Przewijalna lista adresów
        self.address_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.address_list_container.bind(minimum_height=self.address_list_container.setter('height'))
        self.address_list_scroll = ScrollView()
        self.address_list_scroll.add_widget(self.address_list_container)
        self.layout.add_widget(self.address_list_scroll)
        
        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        
        add_button = Button(text='Add Address')
        add_button.bind(on_press=self.open_add_address_form)
        bottom_layout.add_widget(add_button)
        
        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_press=self.cancel)
        bottom_layout.add_widget(cancel_button)
        
        self.layout.add_widget(bottom_layout)
        
        self.add_widget(self.layout)
        
        self.previous_screen = None  # Nazwa poprzedniego ekranu
        self.parent_form = None  # Referencja do formularza, który otworzył ten ekran
    
    def on_pre_enter(self):
        # Odśwież listę adresów za każdym razem, gdy wchodzimy na ekran
        self.refresh_address_list()
    
    def refresh_address_list(self):
        addresses = self.address_service.get_all_addresses()
        
        # Wyczyść listę
        self.address_list_container.clear_widgets()
        
        for address in addresses:
            address_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            address_info = f"{address.street}, {address.city}, {address.country}"
            address_box.add_widget(Label(text=address_info, size_hint_x=0.6))
            
            select_btn = Button(text='Select', size_hint_x=0.2)
            select_btn.bind(on_press=lambda instance, address=address: self.select_address(address))
            address_box.add_widget(select_btn)
            
            edit_btn = Button(text='Edit', size_hint_x=0.2)
            edit_btn.bind(on_press=lambda instance, address=address: self.edit_address(address))
            address_box.add_widget(edit_btn)
            
            delete_btn = Button(text='Delete', size_hint_x=0.2)
            delete_btn.bind(on_press=lambda instance, address=address: self.delete_address(address))
            address_box.add_widget(delete_btn)
            
            self.address_list_container.add_widget(address_box)
    
    def select_address(self, address):
        # Ustaw wybrany adres w formularzu rodzica
        self.parent_form.selected_address = address
        self.parent_form.selected_address_label.text = f"{address.street}, {address.city}"
        # Wróć do formularza studenta
        self.manager.current = self.previous_screen
    
    def open_add_address_form(self, instance):
        # Przejdź do ekranu formularza adresu
        self.manager.current = 'address_form'
        form_screen = self.manager.get_screen('address_form')
        form_screen.clear_form()
        form_screen.previous_screen = 'address_selection'
    
    def edit_address(self, address):
        # Przejdź do ekranu edycji adresu
        self.manager.current = 'address_form'
        form_screen = self.manager.get_screen('address_form')
        form_screen.load_address(address)
        form_screen.previous_screen = 'address_selection'
    
    def delete_address(self, address):
        # Potwierdzenie usunięcia adresu
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"Are you sure you want to delete this address?\n{address.street}, {address.city}, {address.country}"))
        
        button_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        
        content.add_widget(button_layout)
        
        popup = Popup(title='Confirm Delete', content=content, size_hint=(0.6, 0.4))
        yes_button.bind(on_press=lambda *args: self.confirm_delete_address(address, popup))
        no_button.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def confirm_delete_address(self, address, popup):
        self.address_service.delete_address(address.address_id)
        self.refresh_address_list()
        popup.dismiss()
    
    def cancel(self, instance):
        # Wróć do poprzedniego ekranu
        self.manager.current = self.previous_screen
