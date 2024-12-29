from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.popup import Popup

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Tytuł z większą czcionką
        title_label = Label(
            text="Akademicka baza danych studentów\ni profesorów",
            font_size='24sp',
            halign='center',
            valign='middle'
        )
        layout.add_widget(title_label)

        # Dodanie odstępu
        layout.add_widget(Widget(size_hint_y=None, height=20))

        # Opis z informacjami
        info_label = Label(
            text="Andrzej Kłopotowski\nII Informatyka (zaoczna)\nInżynieria oprogramowania",
            font_size='18sp',
            halign='center',
            valign='middle'
        )
        layout.add_widget(info_label)

        # Dodanie odstępu
        layout.add_widget(Widget(size_hint_y=None, height=10))

        # Przyciski do wyboru widoków
        student_button = Button(text='Zarządzaj studentami', size_hint_y=None, height=50)
        student_button.bind(on_press=lambda x: self.go_to_view('student_view'))
        layout.add_widget(student_button)

        professor_button = Button(text='Zarządzaj profesorami', size_hint_y=None, height=50)
        professor_button.bind(on_press=lambda x: self.go_to_view('professor_view'))
        layout.add_widget(professor_button)

        # Dodanie przycisku wyjścia z programu
        exit_button = Button(text='Zamknij program', size_hint_y=None, height=50)
        exit_button.bind(on_press=lambda x: self.show_exit_confirmation())
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def go_to_view(self, view_name):
        self.manager.current = view_name

    def show_exit_confirmation(self):
        # Utwórz treść okna dialogowego
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Dodaj pytanie
        question_label = Label(text="Czy na pewno chcesz zamknąć program?", font_size='18sp')
        content.add_widget(question_label)

        # Dodaj przyciski
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        yes_button = Button(text="Tak")
        yes_button.bind(on_press=lambda x: self.exit_program())
        button_layout.add_widget(yes_button)
        
        no_button = Button(text="Nie")
        no_button.bind(on_press=lambda x: exit_popup.dismiss())
        button_layout.add_widget(no_button)
        
        content.add_widget(button_layout)

        # Utwórz okno dialogowe
        exit_popup = Popup(title="Potwierdzenie", content=content, size_hint=(0.6, 0.4))
        exit_popup.open()

    def exit_program(self):
        # Wyjście z programu
        App.get_running_app().stop()
