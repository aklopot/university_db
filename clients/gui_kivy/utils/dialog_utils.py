from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
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
            background_color=BUTTON_ORANGE
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
            background_color=BUTTON_ORANGE
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