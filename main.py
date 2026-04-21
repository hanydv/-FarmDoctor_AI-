import arabic_reshaper
from kivy.clock import Clock
import arabic_reshaper
import webbrowser 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.utils import platform

def ask_permissions(self):
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.CAMERA,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.INTERNET
        ])

def get_display(self, text):
    # دي دالة يدوية بتعكس النص عشان يظهر صح في أندرويد
    return text[::-1]
# محرك التنسيق العربي لضمان ظهور النصوص بشكل صحيح
def get_tr(self,text):
    if not text: return ""
    import arabic_reshaper
    reshaped_text = arabic_reshaper.reshape(text)
    return reshaped_text[::-1]

KV = '''
<ArabicLabel@Label>:
    font_name: "arial.ttf"
    halign: "center"
    markup: True

<GreenButton@Button>:
    font_name: "arial.ttf"
    background_normal: ''
    background_color: (0.1, 0.5, 0.2, 1)
    size_hint_y: None
    height: '50dp'

ScreenManager:
    LoginScreen:
    MainDashboard:

<LoginScreen>:
    name:'login'
    BoxLayout:
        orientation: 'vertical'
        padding: '25dp'
        spacing: '15dp'
        canvas.before:
            Color:
                rgba: (0.96, 1, 0.96, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            text: "🛡️"
            font_size: '80sp'
            size_hint_y: None
            height: '100dp'
            color: (0.1, 0.5, 0.2, 1)

        ArabicLabel:
            text: app.get_tr("طبيب المزرعة الذكي / Farm Doctor AI")
            font_size: '24sp'
            color: (0.1, 0.5, 0.2, 1)
            
        ArabicLabel:
            text: app.get_tr("حقوق الملكية الرقمية © د. هاني خلف / nDigital Rights © Dr. Hani Khalaf")
            font_size: '14sp'
            color: (0.5, 0.5, 0.5, 1)

        TextInput:
            id: user_phone
            hint_text: "رقم الموبايل / Phone Number"
            size_hint_y: None
            height: '50dp'
            multiline: False
            
        GreenButton:
            text: app.get_tr("دخول لخدمة الجيش الأخضر / Enter")
            on_release: root.manager.current = 'dashboard'

<MainDashboard>:
    name: 'dashboard'
    BoxLayout:
        orientation: 'vertical'
        
        # Header (Top Bar)
        BoxLayout:
            size_hint_y: None
            height: '60dp'
            canvas.before:
                Color:
                    rgba: (0.1, 0.5, 0.2, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            ArabicLabel:
                text: "Dr. Hani Khalaf - Farm Doctor"
                bold: True
                color: (1, 1, 1, 1)

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: '15dp'
                spacing: '15dp'

                # التشخيص الذكي
                GreenButton:
                    text: app.get_tr("التشخيص الذكي الشامل / Smart Diagnosis")
                    height: '100dp'
                    on_release: app.diagnose_action()
                GreenButton:
                    text: app.get_tr("رجوع / Back")
                    size_hint_y: None
                    height: '50dp'
                    on_release: root.manager.current = 'login'
                # أزرار التواصل
                BoxLayout:
                    size_hint_y: None
                    height: '60dp'
                    spacing: '10dp'
                    Button:
                        text: "WhatsApp"
                        background_normal: ''
                        background_color: (0.2, 0.7, 0.3, 1)
                        on_release: app.open_whatsapp()
                    Button:
                        text: "Email Support"
                        background_normal: ''
                        background_color: (0.1, 0.4, 0.8, 1)
                        on_release: app.open_email()

                # سجل المزرعة
                GreenButton:
                    text: app.get_tr("سجل المزرعة والتربة / History & Soil")
                    on_release: app.show_history()

                # الأسواق والطقس
                GridLayout:
                    cols: 2
                    spacing: '12dp'
                    size_hint_y: None
                    height: '100dp'
                    GreenButton:
                        text: app.get_tr("الأسواق / Market")
                        on_release: app.show_market()
                    GreenButton:
                        text: app.get_tr("الطقس / Weather")
                        on_release: app.show_weather()

        ArabicLabel:
            id: status_label
            text: app.get_tr("جميع الحقوق محفوظة © د. هاني خلف")
            size_hint_y: None
            height: '40dp'
            font_size: '12sp'
            color: (0.3, 0.3, 0.3, 1)
'''

class LoginScreen(Screen):
    pass

class MainDashboard(Screen):
    pass

class FarmDoctorApp(App):
    def build(self):
        return Builder.load_string(KV)

    def get_tr(self, text):
        return self.get_tr(text)
    
    def open_whatsapp(self):
        webbrowser.open("https://wa.me/201063732596") 

    def open_email(self):
        webbrowser.open("mailto:hanyk201@gmail.com")

    def update_status(self, msg):
        self.root.get_screen('dashboard').ids.status_label.text = self.get_tr(msg)

    def diagnose_action(self):
        self.update_status(self.get_tr("بدء التشخيص الذكي / AI Diagnosis Started"))

    def show_history(self):
        self.update_status(self.get_tr("استرجاع سجل المزرعة / Fetching History"))

    def show_market(self):
        self.update_status(self.get_tr("تحديث الأسعار / Updating Market Prices"))

    def show_weather(self):
        self.update_status(self.get_tr("جلب نشرة الطقس / Getting Weather Data"))
    def on_start(self):
        # بنقول للتطبيق: افتح واستقر الأول، وبعد ثانية اطلب الكاميرا
        Clock.schedule_once(lambda dt: self.ask_permissions(), 2)
if __name__ == '__main__':
    FarmDoctorApp().run()