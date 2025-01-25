from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.services.service_factory import ServiceFactory
from clients.gui_kivy.utils.colors import *
from clients.gui_kivy.utils.dialog_utils import DialogUtils
from clients.gui_kivy.utils.fonts import *
from kivy.uix.widget import Widget
import json

class AcademicStaffView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.service = ServiceFactory().get_academic_staff_service()
        
        # Główny układ
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł
        title_label = Label(
            text="Lista pracowników akademickich",
            font_size=FONT_SIZE_TITLE,
            size_hint_y=None,
            height=50,
            halign='center',
            color=TEXT_WHITE
        )
        self.layout.add_widget(title_label)
        
        # Przewijalna lista pracowników akademickich
        self.academic_staff_list_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.academic_staff_list_container.bind(minimum_height=self.academic_staff_list_container.setter('height'))
        self.academic_staff_list_scroll = ScrollView()
        self.academic_staff_list_scroll.add_widget(self.academic_staff_list_container)
        self.layout.add_widget(self.academic_staff_list_scroll)
        
        # Przyciski sortowania
        sort_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        sort_by_name_button = Button(
            text='Sortuj po nazwisku',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_HEATHER
        )
        sort_by_name_button.bind(on_press=self.sort_by_name)
        sort_layout.add_widget(sort_by_name_button)

        sort_by_pesel_button = Button(
            text='Sortuj po PESEL',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_HEATHER
        )
        sort_by_pesel_button.bind(on_press=self.sort_by_pesel)
        sort_layout.add_widget(sort_by_pesel_button)
        
        self.layout.add_widget(sort_layout)

        # Przyciski wyszukiwania
        search_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        search_by_name_button = Button(
            text='Wyszukaj po nazwisku',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_YELLOW
        )
        search_by_name_button.bind(on_press=self.search_by_name)
        search_layout.add_widget(search_by_name_button)

        search_by_pesel_button = Button(
            text='Wyszukaj po PESEL',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_YELLOW
        )
        search_by_pesel_button.bind(on_press=self.search_by_pesel)
        search_layout.add_widget(search_by_pesel_button)
        
        self.layout.add_widget(search_layout)

        # Nowy przycisk "Pokaż wszystkich pracowników"
        show_all_button = Button(
            text='Pokaż wszystkich pracowników',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_YELLOW
        )
        show_all_button.bind(on_press=self.refresh_academic_staff_list)
        self.layout.add_widget(show_all_button)

        # Przyciski na dole
        bottom_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        return_button = Button(
            text='Powrót do menu',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_PEARL
        )
        return_button.bind(on_press=self.return_to_main_menu)
        bottom_layout.add_widget(return_button)
        
        add_button = Button(
            text='Dodaj pracownika',
            size_hint_y=None,
            height=50,
            background_color=BUTTON_GREEN
        )
        add_button.bind(on_press=self.add_academic_staff)
        bottom_layout.add_widget(add_button)
        
        self.layout.add_widget(bottom_layout)
        self.add_widget(self.layout)
        
        self.bind(on_pre_enter=lambda instance: self.refresh_academic_staff_list())
    
    def refresh_academic_staff_list(self, *args):
        try:
            academic_staff_list = self.service.get_all_academic_staff()
            self.academic_staff_list_container.clear_widgets()
            print(f"Odświeżam listę pracowników, znaleziono: {len(academic_staff_list)}")  # Debug log
            
            # Dodaj odstęp na górze listy
            self.academic_staff_list_container.add_widget(Widget(size_hint_y=None, height=10))
            
            for academic_staff in academic_staff_list:
                # Główny box dla wiersza z pracownikiem
                academic_staff_box = BoxLayout(
                    orientation='horizontal', 
                    size_hint_y=None, 
                    height=50,
                    spacing=2
                )
                
                # Label z danymi pracownika
                academic_staff_box.add_widget(Label(
                    text=f"{academic_staff.first_name} {academic_staff.last_name} ({academic_staff.position.value}) PESEL: {academic_staff.pesel}",
                    size_hint_x=0.6,
                    font_size=FONT_SIZE_LIST_ITEM,
                    color=TEXT_WHITE
                ))
                
                # Przyciski w osobnym boxlayout
                buttons_box = BoxLayout(
                    size_hint_x=0.4, 
                    spacing=2
                )
                
                # Ważne: tworzymy osobną funkcję dla każdego przycisku, aby uniknąć problemu z domknięciami
                def create_edit_callback(staff):
                    return lambda instance: self.edit_academic_staff(staff)
                    
                def create_delete_callback(staff):
                    return lambda instance: self.confirm_delete_academic_staff(staff)
                
                edit_btn = Button(
                    text='Edytuj',
                    size_hint_x=0.5,
                    background_color=BUTTON_GREEN
                )
                edit_btn.bind(on_press=create_edit_callback(academic_staff))
                buttons_box.add_widget(edit_btn)
                
                delete_btn = Button(
                    text='Usuń',
                    size_hint_x=0.5,
                    background_color=BUTTON_RED
                )
                delete_btn.bind(on_press=create_delete_callback(academic_staff))
                buttons_box.add_widget(delete_btn)
                
                academic_staff_box.add_widget(buttons_box)
                
                container = BoxLayout(orientation='vertical', size_hint_y=None, height=55)
                container.add_widget(academic_staff_box)
                self.academic_staff_list_container.add_widget(container)
        except Exception as e:
            print(f"Błąd podczas odświeżania listy pracowników: {e}")
    
    def add_academic_staff(self, instance):
        self.manager.current = 'academic_staff_form'
        form_screen = self.manager.get_screen('academic_staff_form')
        form_screen.clear_form()
    
    def edit_academic_staff(self, academic_staff):
        self.manager.current = 'academic_staff_form'
        form_screen = self.manager.get_screen('academic_staff_form')
        form_screen.load_academic_staff(academic_staff)
    
    def confirm_delete_academic_staff(self, academic_staff):
        def delete_callback():
            try:
                print(f"Rozpoczynam usuwanie pracownika o ID: {academic_staff.academic_staff_id}")  # Debug log
                self.service.delete_academic_staff(academic_staff.academic_staff_id)
                print("Pracownik został usunięty, odświeżam listę")  # Debug log
                self.refresh_academic_staff_list()
            except Exception as e:
                print(f"Błąd podczas usuwania pracownika: {e}")

        DialogUtils.show_delete_confirmation(
            item_type="pracownika",
            item_name=f"{academic_staff.first_name} {academic_staff.last_name}",
            on_confirm=delete_callback
        )
    
    def return_to_main_menu(self, instance):
        self.manager.current = 'menu'

    def sort_by_name(self, instance):
        try:
            staff_list = self.service.get_all_academic_staff_sorted_by_name()
            self.academic_staff_list_container.clear_widgets()
            self.academic_staff_list_container.add_widget(Widget(size_hint_y=None, height=10))
            
            for staff in staff_list:
                staff_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=50,
                    spacing=2
                )
                
                staff_box.add_widget(Label(
                    text=f"{staff.first_name} {staff.last_name} ({staff.position.value}) PESEL: {staff.pesel}",
                    size_hint_x=0.6,
                    font_size=FONT_SIZE_LIST_ITEM,
                    color=TEXT_WHITE
                ))
                
                buttons_box = BoxLayout(
                    size_hint_x=0.4,
                    spacing=2
                )
                
                edit_btn = Button(
                    text='Edytuj',
                    size_hint_x=0.5,
                    background_color=BUTTON_GREEN
                )
                edit_btn.bind(on_press=lambda x, s=staff: self.edit_academic_staff(s))
                buttons_box.add_widget(edit_btn)
                
                delete_btn = Button(
                    text='Usuń',
                    size_hint_x=0.5,
                    background_color=BUTTON_RED
                )
                delete_btn.bind(on_press=lambda x, s=staff: self.confirm_delete_academic_staff(s))
                buttons_box.add_widget(delete_btn)
                
                staff_box.add_widget(buttons_box)
                
                container = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=55
                )
                container.add_widget(staff_box)
                
                self.academic_staff_list_container.add_widget(container)
                
        except Exception as e:
            print(f"Błąd podczas sortowania pracowników: {e}")

    def sort_by_pesel(self, instance):
        pass

    def search_by_name(self, instance):
        def handle_search(last_name):
            try:
                filtered_staff = self.service.get_by_last_name(last_name)
                self.academic_staff_list_container.clear_widgets()
                self.academic_staff_list_container.add_widget(Widget(size_hint_y=None, height=10))
                
                for staff in filtered_staff:
                    staff_box = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=50,
                        spacing=2
                    )
                    
                    # Używamy tego samego formatu co w głównej liście
                    staff_box.add_widget(Label(
                        text=f"{staff.first_name} {staff.last_name} ({staff.position.value}) PESEL: {staff.pesel}",
                        size_hint_x=0.6,
                        font_size=FONT_SIZE_LIST_ITEM,
                        color=TEXT_WHITE
                    ))
                    
                    buttons_box = BoxLayout(
                        size_hint_x=0.4,
                        spacing=2
                    )
                    
                    edit_btn = Button(
                        text='Edytuj',
                        size_hint_x=0.5,
                        background_color=BUTTON_GREEN
                    )
                    edit_btn.bind(on_press=lambda x, s=staff: self.edit_academic_staff(s))
                    buttons_box.add_widget(edit_btn)
                    
                    delete_btn = Button(
                        text='Usuń',
                        size_hint_x=0.5,
                        background_color=BUTTON_RED
                    )
                    delete_btn.bind(on_press=lambda x, s=staff: self.confirm_delete_academic_staff(s))
                    buttons_box.add_widget(delete_btn)
                    
                    staff_box.add_widget(buttons_box)
                    
                    container = BoxLayout(
                        orientation='vertical',
                        size_hint_y=None,
                        height=55
                    )
                    container.add_widget(staff_box)
                    
                    self.academic_staff_list_container.add_widget(container)
                    
            except Exception as e:
                print(f"Błąd podczas wyszukiwania pracowników: {e}")

        DialogUtils.show_search_by_name_dialog(on_search=handle_search)

    def search_by_pesel(self, instance):
        def handle_search(pesel):
            try:
                filtered_staff = self.service.get_by_pesel(pesel)
                self.academic_staff_list_container.clear_widgets()
                self.academic_staff_list_container.add_widget(Widget(size_hint_y=None, height=10))
                
                for staff in filtered_staff:
                    staff_box = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=50,
                        spacing=2
                    )
                    
                    staff_box.add_widget(Label(
                        text=f"{staff.first_name} {staff.last_name} ({staff.position.value}) PESEL: {staff.pesel}",
                        size_hint_x=0.6,
                        font_size=FONT_SIZE_LIST_ITEM,
                        color=TEXT_WHITE
                    ))
                    
                    buttons_box = BoxLayout(
                        size_hint_x=0.4,
                        spacing=2
                    )
                    
                    edit_btn = Button(
                        text='Edytuj',
                        size_hint_x=0.5,
                        background_color=BUTTON_GREEN
                    )
                    edit_btn.bind(on_press=lambda x, s=staff: self.edit_academic_staff(s))
                    buttons_box.add_widget(edit_btn)
                    
                    delete_btn = Button(
                        text='Usuń',
                        size_hint_x=0.5,
                        background_color=BUTTON_RED
                    )
                    delete_btn.bind(on_press=lambda x, s=staff: self.confirm_delete_academic_staff(s))
                    buttons_box.add_widget(delete_btn)
                    
                    staff_box.add_widget(buttons_box)
                    
                    container = BoxLayout(
                        orientation='vertical',
                        size_hint_y=None,
                        height=55
                    )
                    container.add_widget(staff_box)
                    
                    self.academic_staff_list_container.add_widget(container)
                    
            except Exception as e:
                print(f"Błąd podczas wyszukiwania pracowników: {e}")

        DialogUtils.show_search_by_pesel_dialog(on_search=handle_search)
