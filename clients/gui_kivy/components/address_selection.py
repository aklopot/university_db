from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
from clients.gui_kivy.utils.colors import *
from clients.gui_kivy.utils.dialog_utils import DialogUtils
from clients.gui_kivy.utils.fonts import *

class AddressSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.address_service = ServiceFactory().get_address_service()
        
        # Główny układ z paddingiem
        self.layout = BoxLayout(
            orientation='vertical',
            padding=10,  # Dodajemy padding 10 ze wszystkich stron
            spacing=10   # Dodajemy odstęp między elementami
        )
        
        # Tytuł - używamy stałej FONT_SIZE_TITLE
        title_label = Label(
            text="Wybierz adres",
            font_size=FONT_SIZE_TITLE,
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(title_label)
        
        # Lista adresów
        self.address_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.address_list_container.bind(minimum_height=self.address_list_container.setter('height'))
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.address_list_container)
        self.layout.add_widget(self.scroll_view)
        
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
        
        # Przycisk Dodaj adres (po prawej)
        add_button = Button(
            text='Dodaj adres',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        add_button.bind(on_press=self.open_add_address_form)
        bottom_layout.add_widget(add_button)
        
        self.layout.add_widget(bottom_layout)
        self.add_widget(self.layout)
        
        # Dodajemy te pola, które są potrzebne do działania ekranu
        self.previous_screen = None  # Nazwa poprzedniego ekranu
        self.parent_form = None      # Referencja do formularza, który otworzył ten ekran
        
    def on_pre_enter(self):
        """
        Metoda wywoływana przed wejściem na ekran.
        Odświeża listę adresów.
        """
        self.refresh_address_list()
        
    def refresh_address_list(self):
        addresses = self.address_service.get_all_addresses()
        self.address_list_container.clear_widgets()
        
        # Dodaj odstęp na górze listy
        self.address_list_container.add_widget(Widget(size_hint_y=None, height=10))
        
        for address in addresses:
            # Główny box dla wiersza z adresem
            address_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=50,
                spacing=2  # Zmniejszony odstęp między elementami
            )
            
            # Label z danymi adresu - używamy stałej FONT_SIZE_LIST_ITEM
            address_box.add_widget(Label(
                text=f"{address.street}, {address.city}",
                size_hint_x=0.6,
                font_size=FONT_SIZE_LIST_ITEM,
                halign='left',
                valign='middle',
                color=TEXT_WHITE
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
            select_btn.bind(on_press=lambda x, addr=address: self.select_address(addr))
            buttons_box.add_widget(select_btn)
            
            # Przycisk edycji
            edit_btn = Button(
                text='Edytuj',
                size_hint_x=0.33,
                background_color=BUTTON_GREEN
            )
            edit_btn.bind(on_press=lambda x, addr=address: self.open_edit_address_form(addr))
            buttons_box.add_widget(edit_btn)
            
            # Przycisk usuwania
            delete_btn = Button(
                text='Usuń',
                size_hint_x=0.33,
                background_color=BUTTON_RED
            )
            delete_btn.bind(on_press=lambda x, addr=address: self.delete_address(addr))
            buttons_box.add_widget(delete_btn)
            
            address_box.add_widget(buttons_box)
            
            # Kontener z odstępami
            container = BoxLayout(
                orientation='vertical', 
                size_hint_y=None, 
                height=55,  # 50 na wiersz + 5 na odstęp
                padding=[0, 0, 0, 5]  # Dolny padding 5
            )
            container.add_widget(address_box)
            
            self.address_list_container.add_widget(container)
    
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
    
    def open_edit_address_form(self, address):
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
