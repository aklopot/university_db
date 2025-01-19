from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from clients.gui_kivy.utils.dialog_utils import DialogUtils
from clients.gui_kivy.utils.colors import *

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Tytuł z większą czcionką
        title_label = Label(
            text="Akademicka baza danych studentów\ni pracowników akademickich",
            font_size='24sp',
            halign='center',
            valign='middle',
            color=TEXT_WHITE
        )
        layout.add_widget(title_label)

        # Dodanie odstępu
        layout.add_widget(Widget(size_hint_y=None, height=20))

        # Opis z informacjami
        info_label = Label(
            text="Andrzej Kłopotowski\nII Informatyka (zaoczna)\nInżynieria oprogramowania",
            font_size='18sp',
            halign='center',
            valign='middle',
            color=TEXT_GRAY
        )
        layout.add_widget(info_label)

        # Dodanie odstępu
        layout.add_widget(Widget(size_hint_y=None, height=10))

        # Przyciski do wyboru widoków
        student_button = Button(
            text='Zarządzaj studentami', 
            size_hint_y=None, 
            height=50,
            background_color=BUTTON_GREEN
        )
        student_button.bind(on_press=lambda x: self.go_to_view('student_view'))
        layout.add_widget(student_button)

        academic_staff_button = Button(
            text='Zarządzaj pracownikami', 
            size_hint_y=None, 
            height=50,
            background_color=BUTTON_GREEN
        )
        academic_staff_button.bind(on_press=lambda x: self.go_to_view('academic_staff_view'))
        layout.add_widget(academic_staff_button)
        
        academic_course_button = Button(
            text='Zarządzaj kursami akademickimi',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        academic_course_button.bind(on_press=lambda x: self.go_to_view('academic_course_view'))
        layout.add_widget(academic_course_button)

        # Dodaj przycisk zarządzania kierunkami studiów przed przyciskiem wyjścia
        field_of_study_button = Button(
            text='Zarządzaj kierunkami studiów',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        field_of_study_button.bind(on_press=lambda x: self.go_to_view('field_of_study_view'))
        layout.add_widget(field_of_study_button)

        # Przycisk wyjścia z programu
        exit_button = Button(
            text='Zamknij program', 
            size_hint_y=None, 
            height=50,
            background_color=BUTTON_RED
        )
        exit_button.bind(on_press=lambda x: DialogUtils.show_exit_confirmation())
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def go_to_view(self, view_name):
        self.manager.current = view_name
