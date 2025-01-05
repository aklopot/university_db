from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App

class DialogUtils:
    @staticmethod
    def show_exit_confirmation():
        # Utwórz treść okna dialogowego
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Dodaj pytanie
        question_label = Label(text="Czy na pewno chcesz zamknąć program?", font_size='18sp')
        content.add_widget(question_label)

        # Dodaj przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        yes_button = Button(text="Tak")
        yes_button.bind(on_press=lambda x: App.get_running_app().stop())
        button_layout.add_widget(yes_button)
        
        no_button = Button(text="Nie")
        
        content.add_widget(button_layout)

        # Utwórz okno dialogowe
        exit_popup = Popup(title="Potwierdzenie", content=content, size_hint=(0.6, 0.4))
        no_button.bind(on_press=exit_popup.dismiss)
        button_layout.add_widget(no_button)
        
        exit_popup.open()
        return True  # Zapobiega domyślnemu zamknięciu 