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

        # Pierwszy rząd przycisków (Studenci i Pracownicy)
        first_row = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        student_button = Button(
            text='Zarządzaj studentami',
            background_color=BUTTON_BEIGE
        )
        student_button.bind(on_press=lambda x: self.go_to_view('student_view'))
        first_row.add_widget(student_button)

        academic_staff_button = Button(
            text='Zarządzaj pracownikami',
            background_color=BUTTON_BEIGE
        )
        academic_staff_button.bind(on_press=lambda x: self.go_to_view('academic_staff_view'))
        first_row.add_widget(academic_staff_button)
        
        layout.add_widget(first_row)

        # Drugi rząd przycisków (Kursy i Kierunki)
        second_row = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        academic_course_button = Button(
            text='Zarządzaj kursami akademickimi',
            background_color=BUTTON_BEIGE
        )
        academic_course_button.bind(on_press=lambda x: self.go_to_view('academic_course_view'))
        second_row.add_widget(academic_course_button)

        field_of_study_button = Button(
            text='Zarządzaj kierunkami studiów',
            background_color=BUTTON_BEIGE
        )
        field_of_study_button.bind(on_press=lambda x: self.go_to_view('field_of_study_view'))
        second_row.add_widget(field_of_study_button)
        
        layout.add_widget(second_row)

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
