from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from clients.gui_kivy.components.menu_screen import MenuScreen
from clients.gui_kivy.components.student_view import StudentView
from clients.gui_kivy.components.student_form import StudentForm
from clients.gui_kivy.components.academic_staff_view import AcademicStaffView
from clients.gui_kivy.components.academic_staff_form import AcademicStaffForm
from clients.gui_kivy.components.gender_form import GenderForm
from clients.gui_kivy.components.address_selection import AddressSelectionScreen
from clients.gui_kivy.components.address_form import AddressForm
from clients.gui_kivy.components.gender_selection import GenderSelectionScreen
from clients.gui_kivy.components.academic_course_view import AcademicCourseView
from clients.gui_kivy.components.academic_course_form import AcademicCourseForm
from clients.gui_kivy.utils.dialog_utils import DialogUtils

class UniversityDBApp(App):
    def build(self):
        # Podłącz handler zamknięcia okna
        Window.bind(on_request_close=lambda *args: DialogUtils.show_exit_confirmation())
        
        self.sm = ScreenManager()

        # Ekrany aplikacji
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(StudentView(name='student_view'))
        self.sm.add_widget(StudentForm(name='student_form'))
        self.sm.add_widget(AddressSelectionScreen(name='address_selection'))
        self.sm.add_widget(AddressForm(name='address_form'))
        self.sm.add_widget(AcademicStaffView(name='academic_staff_view'))
        self.sm.add_widget(AcademicStaffForm(name='academic_staff_form'))
        self.sm.add_widget(AcademicCourseView(name='academic_course_view'))
        self.sm.add_widget(AcademicCourseForm(name='academic_course_form')) 
        self.sm.add_widget(GenderForm(name='gender_form'))
        self.sm.add_widget(GenderSelectionScreen(name='gender_selection'))

        return self.sm

if __name__ == '__main__':
    UniversityDBApp().run()
