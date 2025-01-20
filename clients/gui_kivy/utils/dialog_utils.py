from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.textinput import TextInput
from clients.gui_kivy.utils.colors import *

class DialogUtils:
    @staticmethod
    def show_exit_confirmation():
        # Utwórz treść okna dialogowego
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Utwórz okno dialogowe
        exit_popup = Popup(
            title="Potwierdzenie",
            content=content,
            size_hint=(0.6, 0.4),
            title_size='16sp',
            title_color=TEXT_WHITE
        )

        # Dodaj pytanie
        question_label = Label(
            text="Czy na pewno chcesz zamknąć program?",
            font_size='18sp',
            color=TEXT_WHITE
        )
        content.add_widget(question_label)

        # Dodaj przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        content.add_widget(button_layout)
        
        no_button = Button(
            text="Nie",
            background_color=BUTTON_PEARL
        )
        no_button.bind(on_press=exit_popup.dismiss)
        button_layout.add_widget(no_button)

        yes_button = Button(
            text="Tak",
            background_color=BUTTON_RED
        )
        yes_button.bind(on_press=lambda x: App.get_running_app().stop())
        button_layout.add_widget(yes_button)

        exit_popup.open()
        return True

    @staticmethod
    def show_delete_confirmation(item_type: str, item_name: str, on_confirm):
        """
        Wyświetla okno dialogowe potwierdzające usunięcie elementu.
        
        Args:
            item_type (str): Typ elementu (np. "studenta", "pracownika", "kurs")
            item_name (str): Nazwa/identyfikator elementu do wyświetlenia
            on_confirm (callable): Funkcja do wywołania po potwierdzeniu
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Utwórz okno dialogowe
        popup = Popup(
            title="Potwierdzenie usunięcia",
            content=content,
            size_hint=(0.6, 0.4),
            title_size='16sp',
            title_color=TEXT_WHITE
        )

        # Dodaj pytanie
        question_label = Label(
            text=f"Czy na pewno chcesz usunąć {item_type}:\n{item_name}",
            font_size='18sp',
            color=TEXT_WHITE,
            halign='center'
        )
        content.add_widget(question_label)

        # Dodaj przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        content.add_widget(button_layout)
        
        no_button = Button(
            text="Nie",
            background_color=BUTTON_PEARL
        )
        no_button.bind(on_press=popup.dismiss)
        button_layout.add_widget(no_button)

        yes_button = Button(
            text="Tak",
            background_color=BUTTON_RED
        )
        yes_button.bind(on_press=lambda x: [on_confirm(), popup.dismiss()])
        button_layout.add_widget(yes_button)

        popup.open()

    @staticmethod
    def show_search_by_name_dialog(on_search):
        """
        Wyświetla okno dialogowe do wyszukiwania po nazwisku.
        
        Args:
            on_search: Callback wywoływany po kliknięciu przycisku Szukaj, 
                      przyjmuje jako argument wprowadzone nazwisko
        """
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Pole tekstowe na nazwisko z wycentrowanym tekstem
        name_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=40,
            hint_text='Wprowadź nazwisko',
            halign='center',  # Centrowanie tekstu w poziomie
            padding=[10, (40-20)/2],
            font_size='16sp'  # Dodanie odpowiedniej wielkości czcionki
        )
        content.add_widget(Label(
            text='Podaj nazwisko:',
            font_size='18sp',
            halign='center',  # Centrowanie tekstu etykiety
            valign='middle'   # Wycentrowanie w pionie
        ))
        content.add_widget(name_input)
        
        # Przyciski
        button_layout = BoxLayout(
            size_hint_y=None, 
            height=40, 
            spacing=10
        )
        
        cancel_button = Button(
            text='Anuluj',
            background_color=BUTTON_PEARL
        )
        
        search_button = Button(
            text='Szukaj',
            background_color=BUTTON_YELLOW
        )
        
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(search_button)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='Wyszukiwanie',
            content=content,
            size_hint=(0.4, 0.3),
            title_size='16sp',
            title_color=TEXT_WHITE,
            auto_dismiss=False
        )
        
        def on_search_button(instance):
            popup.dismiss()
            on_search(name_input.text.strip())
            
        search_button.bind(on_press=on_search_button)
        cancel_button.bind(on_press=popup.dismiss)
        
        popup.open() 