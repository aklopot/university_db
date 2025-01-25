from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
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
from clients.gui_kivy.components.field_of_study_view import FieldOfStudyView
from clients.gui_kivy.components.field_of_study_form import FieldOfStudyForm
from clients.gui_kivy.components.student_grades_view import StudentGradesView
from clients.gui_kivy.components.student_grade_form import StudentGradeForm

class UniversityDBApp(App):
    def build(self):
        Window.size = (950, 750)
        
        # Ustawienie tytułu okna
        self.title = 'Akademicka baza danych'
        
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
        self.sm.add_widget(FieldOfStudyView(name='field_of_study_view'))
        self.sm.add_widget(FieldOfStudyForm(name='field_of_study_form'))
        
        # Dodanie nowych ekranów dla ocen
        self.sm.add_widget(StudentGradesView(name='student_grades_view'))
        self.sm.add_widget(StudentGradeForm(name='student_grade_form'))

        return self.sm

if __name__ == '__main__':
    UniversityDBApp().run()
