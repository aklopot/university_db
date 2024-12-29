from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from src.services.service_factory import ServiceFactory
from src.models.universitydb import Address
import json

class AddressForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Wczytaj konfigurację
        with open("config/config.json") as config_file:
            config = json.load(config_file)
        
        self.address_service = ServiceFactory(config).get_address_service()
        
        self.layout = BoxLayout(orientation='vertical')
        
        # Pola formularza
        self.street_input = TextInput(hint_text="Street")
        self.building_number_input = TextInput(hint_text="Building Number")
        self.city_input = TextInput(hint_text="City")
        self.zip_code_input = TextInput(hint_text="Zip Code")
        self.region_input = TextInput(hint_text="Region")
        self.country_input = TextInput(hint_text="Country")
        
        self.layout.add_widget(self.street_input)
        self.layout.add_widget(self.building_number_input)
        self.layout.add_widget(self.city_input)
        self.layout.add_widget(self.zip_code_input)
        self.layout.add_widget(self.region_input)
        self.layout.add_widget(self.country_input)
        
        # Przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50)
        
        save_button = Button(text="Save")
        save_button.bind(on_press=self.save_address)
        button_layout.add_widget(save_button)
        
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.cancel)
        button_layout.add_widget(cancel_button)
        
        self.layout.add_widget(button_layout)
        
        self.add_widget(self.layout)
        
        self.current_address = None
        self.previous_screen = None  # Nazwa poprzedniego ekranu (np. 'address_selection')
    
    def clear_form(self):
        self.street_input.text = ''
        self.building_number_input.text = ''
        self.city_input.text = ''
        self.zip_code_input.text = ''
        self.region_input.text = ''
        self.country_input.text = ''
        
        self.current_address = None
    
    def load_address(self, address):
        self.current_address = address
        self.street_input.text = address.street
        self.building_number_input.text = address.building_number
        self.city_input.text = address.city
        self.zip_code_input.text = address.zip_code
        self.region_input.text = address.region
        self.country_input.text = address.country
    
    def save_address(self, instance):
        street = self.street_input.text
        building_number = self.building_number_input.text
        city = self.city_input.text
        zip_code = self.zip_code_input.text
        region = self.region_input.text
        country = self.country_input.text
        
        try:
            if self.current_address:
                # Aktualizacja istniejącego adresu
                self.current_address.street = street
                self.current_address.building_number = building_number
                self.current_address.city = city
                self.current_address.zip_code = zip_code
                self.current_address.region = region
                self.current_address.country = country
                
                self.address_service.update_address(self.current_address)
            else:
                # Dodanie nowego adresu
                address = Address(
                    street=street,
                    building_number=building_number,
                    city=city,
                    zip_code=zip_code,
                    region=region,
                    country=country
                )
                self.address_service.add_address(address)
            
            # Wróć do poprzedniego ekranu
            self.manager.current = self.previous_screen
        except Exception as e:
            # Obsłuż ewentualne błędy
            print(f"Błąd podczas zapisywania adresu: {e}")
    
    def cancel(self, instance):
        # Wróć do poprzedniego ekranu bez zapisywania
        self.manager.current = self.previous_screen
        self.clear_form()
