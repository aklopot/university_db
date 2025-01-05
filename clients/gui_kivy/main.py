from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
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

class UniversityDBApp(App):
    def build(self):
        sm = ScreenManager()

        # Ekrany aplikacji
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(StudentView(name='student_view'))
        sm.add_widget(StudentForm(name='student_form'))
        sm.add_widget(AddressSelectionScreen(name='address_selection'))
        sm.add_widget(AddressForm(name='address_form'))
        sm.add_widget(AcademicStaffView(name='academic_staff_view'))
        sm.add_widget(AcademicStaffForm(name='academic_staff_form'))
        sm.add_widget(AcademicCourseView(name='academic_course_view'))
        sm.add_widget(AcademicCourseForm(name='academic_course_form')) 
        sm.add_widget(GenderForm(name='gender_form'))
        sm.add_widget(GenderSelectionScreen(name='gender_selection'))

        return sm

if __name__ == '__main__':
    UniversityDBApp().run()
