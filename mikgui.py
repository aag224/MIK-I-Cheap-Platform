from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Ellipse, Color
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from interface.actuars import pumpsWork, pumpsWorkTC, stirring, cleanUp
import RPi.GPIO as GPIO
import threading
import time
from time import sleep



Window.size = (1135, 665)
Window.resizable = False
Window.title = "MIK-I"

class MikiScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_pumps()
        self.selection_mood = ""
        self.stir_stage = None
        self.used_pines = {}


    def create_pumps(self):
        # (Pump 1 to Pump 4)
        for i in range(4):
            with self.canvas:
                Color(0,0,0,1)
                Ellipse(pos= (259 + 220 * i,430),size = (150,152))
                Color(0,194,0,0.6)
                Ellipse(pos=(260 + 220 * i, 432), size=(148, 148))
                Color(3,0.55,8,0.63)
                Ellipse(pos=(326 + 221 * i, 499), size=(13, 13))
            label = Label(text=f"Pump {i + 1}",
                          size_hint=(None, None),
                          size=(100, 30),
                          pos=(285 + 220 * i, 585),
                          color=(0, 0, 0, 1),
                          font_size=20)
            self.add_widget(label)
            label = Label(text=f"Vol (ml): ",
                          size_hint=(None, None),
                          size=(100, 30),
                          pos=(238 + 225 * i, 385),
                          color=(0, 0, 0, 1),
                          font_size=18)
            self.add_widget(label)
            
        # (Pump 5 to Pump 9)
        for j in range(5):
            x = 110 + 203*j
            y = 170
            
            with self.canvas:
                Color(0,0,0,1) # black color
                Ellipse(pos = (x + 24, y+5),size = (150,152))
                Color(0,194,0,0.6) # green color
                Ellipse(pos=(x + 25, y + 7), size = (148,148))
                Color(3,0.55,8,0.63) # grey color
                Ellipse(pos=(x + 92, y + 73), size=(13, 13))
            label = Label(text=f"Pump {j + 5}",
                          size_hint = (None, None),
                          size = (90,30),
                          pos=(152 + 206 * j, 332),
                          color = (0,0,0,1),
                          font_size=20)
            self.add_widget(label)
            label = Label(text=f"Vol (ml): ",
                          size_hint=(None, None),
                          size = (30, 30),
                          pos = (155 + 204 * j, 133),
                          color = (0, 0, 0, 1),
                          font_size = 18)
            self.add_widget(label)

        # (Service Pump)  
        with self.canvas:
            Color(0,0,0,1) # black color
            Ellipse(pos = (49, 428),size = (150,152))
            Color(1,1,5,0.95) # white color
            Ellipse(pos = (50, 430), size=(148, 148))
            Color(12,0.35,0.2,0.15) # color
            Ellipse(pos=(119, 499), size=(13, 13))
        label = Label(text="Service Pump",
                      size_hint=(None, None),
                      size=(150, 300),
                      pos=(45, 445),
                      color=(0, 0, 0, 1),
                      font_size=20)
        self.add_widget(label)
        label = Label(text="Vol (ml): ",
                      size_hint=(None, None),
                      size=(150,3),
                      pos=(4.5,400),
                      color=(0,0,0,1),
                      font_size=18)
        self.add_widget(label)
        label = Label(text="Addition",
                      size_hint=(None, None),
                      size=(150,3),
                      pos=(235,85),
                      color=(0,0,0,1),
                      font_size=20)
        self.add_widget(label)
        #Label stirring
        label = Label(text="Stirring",
                      size_hint=(None, None),
                      size=(150,3),
                      pos=(595,85),
                      color=(0,0,0,1),
                      font_size=20)
        self.add_widget(label)
        # Label time
        label = Label(text="time (min)",
                      size_hint=(None, None),
                      size=(150,3),
                      pos=(735,65),
                      color=(0,0,0,1),
                      font_size=16)
        self.add_widget(label)
    
    # Set the stirring stage from togglebuttons
    def set_stirringStage(self, value, active):
        if active:
            self.stir_stage = value
    
    # Set the addition form from buttons
    def set_moodWork(self, togglebutton):
        if togglebutton.state == "down":
            self.selection_mood = togglebutton.text

    # Clear all the inputs
    def clr_text(self):
        for n in [self.ids.checkno, self.ids.check1, self.ids.check2, self.ids.check3, self.ids.parallel, self.ids.inorder]:
            n.state = "normal"
        self.selection_mood = ""
        for v in [self.ids.vol0,self.ids.vol1,self.ids.vol2,self.ids.vol3,self.ids.vol4,self.ids.vol5,self.ids.vol6,self.ids.vol7,self.ids.vol8,self.ids.vol9]:
            v.text = "0"
        self.stir_stage = None

    # Ended reaction prompt
    def reaction_finished(self):
        popup = Popup(
            title="Info",
            content=Label(text="Reaction finished",font_size=18),
            size_hint=(None, None),
            size=(300, 150)
        )
        popup.open()

        # Life time of view the prompt
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.ask_clean_tubes(), 5)

    def ask_clean_tubes(self):
        # Prompt asking to clean or not the used tubes
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Do you want to clean the tubes?", font_size=18))

        btn_layout = BoxLayout(spacing=10, size_hint_y=None, height=40)

        btn_yes = Button(text="Yes")
        btn_no = Button(text="No")

        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)

        layout.add_widget(btn_layout)

        popup = Popup(
            title="Clean Tubes",
            content=layout,
            size_hint=(None, None),
            size=(300, 180),
            auto_dismiss=False
        )

        def on_yes(instance):
            popup.dismiss()
            cleanUp(True, self.used_pines.values(), self.flow) # Execute cleaning
            self.ids.srtButton.disabled = False  # Active button

        def on_no(instance):
            popup.dismiss()
            self.ids.srtButton.disabled = False

        btn_yes.bind(on_release=on_yes)
        btn_no.bind(on_release=on_no)
        
        popup.open()

    def rxnY(self, *args):
        self.pps = [24,17,27,22,13,2,18,25,4,7] # Pines GPIO  <---------- this change!!!
        self.strpins = [12, 20] 
        self.flow = {0: 28, 17: 0.2481, 27: 0.1892, 22: 0.2099, 13: 0.2285, 2: 0.22, 18: 0.22, 25: 0.2409, 4: 0.22, 7: 0.22} # Flow per pump {key} = pin {value} = flow (mL/s) <--------- this also change with calibration
        self.tc=[2,18,19,20,17,18,17,18,19,10] # Time charge per pump
        self.used_pines = {}
        
        def wmk():
            self.tmstr = int(self.ids.stir_time.text)  if self.ids.stir_time.text.strip() else 0
            self.vs = int(self.ids.vol0.text) if self.ids.vol0.text.strip() else 0
            self.v1 = int(self.ids.vol1.text) if self.ids.vol1.text.strip() else 0
            self.v2 = int(self.ids.vol2.text) if self.ids.vol2.text.strip() else 0
            self.v3 = int(self.ids.vol3.text) if self.ids.vol3.text.strip() else 0
            self.v4 = int(self.ids.vol4.text) if self.ids.vol4.text.strip() else 0
            self.v5 = int(self.ids.vol5.text) if self.ids.vol5.text.strip() else 0
            self.v6 = int(self.ids.vol6.text) if self.ids.vol6.text.strip() else 0
            self.v7 = int(self.ids.vol7.text) if self.ids.vol7.text.strip() else 0
            self.v8 = int(self.ids.vol8.text) if self.ids.vol8.text.strip() else 0
            self.v9 = int(self.ids.vol9.text) if self.ids.vol9.text.strip() else 0
            
            if self.tmstr != 0:    
                def stir1():
                    stirring(self.strpin[0],self.strpin[1],self.tmstr*60+(self.v1/flow[self.pps[1]]+tc[1])+(self.v2/self.flow[self.pps[2]]+self.tc[2])+(self.v3/self.flow[self.pps[3]]+self.tc[3])+(self.v4/self.flow[self.pps[4]]+self.tc[4])+(self.v5/self.flow[self.pps[5]]+self.tc[5])+(self.v6/self.flow[self.pps[6]]+self.tc[6])+(self.v7/self.flow[self.pps[7]]+self.tc[7])+(self.v8/self.flow[self.pps[8]]+self.tc[8])+(self.v9/self.flow[self.pps[9]]+self.tc[9]))
                def stir2():
                    stirring(self.strpin[0],self.strpin[1],(self.tmstr*60)+(self.v2/self.flow[self.pps[2]]+self.tc[2])+(self.v3/self.flow[self.pps[3]]+self.tc[3])+(self.v4/self.flow[self.pps[4]]+self.tc[4])+(self.v5/self.flow[self.pps[5]]+self.tc[5])+(self.v6/self.flow[self.pps[6]]+self.tc[6])+(self.v7/self.flow[self.pps[7]]+self.tc[7])+(self.v8/self.flow[self.pps[8]]+self.tc[8])+(self.v9/self.flow[self.pps[9]]+self.tc[9]))
                def stir3():
                    stirring(self.strpin[0],self.strpin[1],self.tmstr*60+(self.v3/self.flow[self.pps[3]]+self.tc[3])+(self.v4/self.flow[self.pps[4]]+self.tc[4])+(self.v5/self.flow[self.pps[5]]+self.tc[5])+(self.v6/self.flow[self.pps[6]]+self.tc[6])+(self.v7/self.flow[self.pps[7]]+self.tc[7])+(self.v8/self.flow[self.pps[8]]+self.tc[8])+(self.v9/self.flow[self.pps[9]]+self.tc[9]))
            elif self.tmstr == 0:
                def stir1():
                    stirring(self.strpin[0],self.strpin[1],1)
                def stir2():
                    stirring(self.strpin[0],self.strpin[1],1)
                def stir3():
                    stirring(self.strpin[0],self.strpin[1],1)
            else:
                def stir1():
                    x=1
                def stir2():
                    s=1
                def stir3():
                    d=1
                    
            if self.vs != 0:
                def Pmps():
                    pumpsWork(0,int(self.pps[0]),self.vs/self.flow[self.pps[0]]+self.tc[0])
                    self.used_pines[0] = self.pps[0]
                
                def PmpsTD():
                    pumpsWorkTC(0,int(self.pps[0]),(self.v2/self.flow[self.pps[2]])+(self.v1/self.flow[self.pps[1]]),self.vs/self.flow[self.pps[0]]+self.tc[0])
                    self.used_pines[0] = self.pps[0]
            elif self.vs == 0:
                def Pmps():
                    a=1
                def PmpsTD():
                    ax=1
                    
            if self.v1 != 0:
                def Pmp1():
                    pumpsWork(1,int(self.pps[1]),self.vs/self.flow[self.pps[1]]+self.tc[1])
                    self.used_pines[1] = self.pps[1]
            elif self.v1 == 0:
                def Pmp1():
                    a=1
                    
            if self.v2 != 0:
                def Pmp2():
                    pumpsWork(2,int(self.pps[2]),self.vs/self.flow[self.pps[2]]+self.tc[2])
                    self.used_pines[2] = self.pps[2]
                
                def Pmp2TD():
                    pumpsWorkTC(2,int(self.pps[2]),self.v1/self.flow[self.pps[1]],self.v2/self.flow[self.pps[2]]+self.tc[2])
                    self.used_pines[2] = self.pps[2]
            else:
                def Pmp2():
                    a=1
                def Pmp2TD():
                    ax=1
                    
            if self.v3 != 0:
                def Pmp3():
                    pumpsWork(3,int(self.pps[3]),self.vs/self.flow[self.pps[3]]+self.self.tc[3])
                    self.used_pines[3] = self.pps[3]
                
                def Pmp3TD():
                    pumpsWorkTC(3,int(self.pps[3]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]]),self.v3/self.flow[self.pps[3]]+self.tc[3])
                    self.used_pines[3] = self.pps[3]
            else:
                def Pmp3():
                    a=1
                def Pmp3TD():
                    ax=1
                    
            if self.v4 != 0:
                def Pmp4():
                    pumpsWork(4,int(self.pps[4]),self.vs/self.flow[self.pps[4]]+self.tc[4])
                    self.used_pines[4] = self.pps[4]
                
                def Pmp4TD():
                    pumpsWorkTC(4,int(self.pps[4]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]]),self.v4/self.flow[self.pps[4]]+self.tc[4])
                    self.used_pines[4] = self.pps[4]
            else:
                def Pmp4():
                    a=1
                def Pmp4TD():
                    ax=1

            if self.v5 != 0:
                def Pmp5():
                    pumpsWork(5,int(self.pps[5]),self.vs/self.flow[self.pps[5]]+self.tc[5])
                    self.used_pines[5] = self.pps[5]
                
                def Pmp5TD():
                    pumpsWorkTC(5,int(self.pps[5]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]]),self.v5/self.flow[self.pps[5]]+self.tc[5])
                    self.used_pines[5] = self.pps[5]
            else:
                def Pmp5():
                    a=1
                def Pmp5TD():
                    ax=1

            if self.v6 != 0:
                def Pmp6():
                    pumpsWork(6,int(self.pps[6]),self.vs/self.flow[self.pps[6]]+self.tc[6])
                    self.used_pines[6] = self.pps[6]
            
                def Pmp6TD():
                    pumpsWorkTC(6,int(self.pps[6]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]])+(self.v5/self.flow[self.pps[5]]),self.v6/self.flow[self.pps[6]]+self.tc[6])
                    self.used_pines[6] = self.pps[6]
            else:
                def Pmp6():
                    a=1
                def Pmp6TD():
                    ax=1
                    
            if self.v7 != 0:
                def Pmp7():
                    pumpsWork(7,int(self.pps[7]),self.vs/self.flow[self.pps[7]]+self.tc[7])
                    self.used_pines[7] = self.pps[7]
            
                def Pmp7TD():
                    pumpsWorkTC(7,int(self.pps[7]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]])+(self.v5/self.flow[self.pps[5]])+(self.v6/self.flow[self.pps[6]]),self.v7/self.flow[self.pps[7]]+self.tc[7])
                    self.used_pines[7] = self.pps[7]
            else:
                def Pmp7():
                    a=1
                def Pmp7TD():
                    ax=1
                    
            if self.v8 != 0:
                def Pmp8():
                    pumpsWork(8,int(self.pps[8]),self.vs/self.flow[self.pps[8]]+self.tc[8])
                    self.used_pines[8] = self.pps[8]
            
                def Pmp8TD():
                    pumpsWorkTC(8,int(self.pps[8]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]])+(self.v5/self.flow[self.pps[5]])+(self.v6/self.flow[self.pps[6]])+(self.v7/self.flow[self.pps[7]]),self.v8/self.flow[self.pps[8]]+self.tc[8])
                    self.used_pines[8] = self.pps[8]
            else:
                def Pmp8():
                    a=1
                def Pmp8TD():
                    ax=1
                    
            if self.v9 != 0:
                def Pmp9():
                    pumpsWork(9,int(self.pps[9]),self.vs/self.flow[self.pps[9]]+self.tc[9])
                    self.used_pines[9] = self.pps[9]
            
                def Pmp9TD():
                    pumpsWorkTC(9,int(self.pps[9]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]])+(self.v5/self.flow[self.pps[5]])+(self.v6/self.flow[self.pps[6]])+(self.v7/(self.flow[self.pps[7]]))+(self.v8/self.flow[self.pps[8]]),self.v9/self.flow[self.pps[9]]+self.tc[9])
                    self.used_pines[9] = self.pps[9]
            else:
                def Pmp9():
                    a=1
                def Pmp9TD():
                    ax=1
            hilo_ms1=threading.Thread(target=stir1)
            hilo_ms2=threading.Thread(target=stir2)
            hilo_ms3=threading.Thread(target=stir3)
            hilo_s=threading.Thread(target=Pmps)
            hilo_1=threading.Thread(target=Pmp1)
            hilo_2=threading.Thread(target=Pmp2)
            hilo_3=threading.Thread(target=Pmp3)
            hilo_4=threading.Thread(target=Pmp4)
            hilo_5=threading.Thread(target=Pmp5)
            hilo_6=threading.Thread(target=Pmp6)
            hilo_7=threading.Thread(target=Pmp7)
            hilo_8=threading.Thread(target=Pmp8)
            hilo_9=threading.Thread(target=Pmp9)
            h_2=threading.Thread(target=Pmp2TD)
            h_3=threading.Thread(target=Pmp3TD)
            h_4=threading.Thread(target=Pmp4TD)
            h_5=threading.Thread(target=Pmp5TD)
            h_6=threading.Thread(target=Pmp6TD)
            h_7=threading.Thread(target=Pmp7TD)
            h_8=threading.Thread(target=Pmp8TD)
            h_9=threading.Thread(target=Pmp9TD)
            
            if self.selection_mood == "Parallel":
                hilo_s.start()
                hilo_ms1.start()
                hilo_1.start()
                hilo_2.start()
                hilo_3.start()
                hilo_4.start()
                hilo_5.start()
                hilo_6.start()
                hilo_7.start()
                hilo_8.start()
                hilo_9.start()

                hilo_s.join()
                hilo_ms1.join()
                hilo_1.join()
                hilo_2.join()
                hilo_3.join()
                hilo_4.join()
                hilo_5.join()
                hilo_6.join()
                hilo_7.join()
                hilo_8.join()
                hilo_9.join()
                GPIO.cleanup()
                    
                self.reaction_finished()
            if self.selection_mood == "In-Order":
                if self.stir_stage == 0:
                    Pmp1()
                    Pmp2()
                    Pmp3()
                    Pmp4()
                    Pmp5()
                    Pmp6()
                    Pmp7()
                    Pmp8()
                    Pmp9()
                    GPIO.cleanup()
                    
                    self.reaction_finished()
                if self.stir_stage == 1:
                    hilo_1.start()
                    h_2.start()
                    hilo_ms1.start()
                    h_3.start()
                    h_4.start()
                    h_5.start()
                    h_6.start()
                    h_7.start()
                    h_8.start()
                    h_9.start()

                    hilo_1.join()
                    h_2.join()
                    hilo_ms1.join()
                    h_3.join()
                    h_4.join()
                    h_5.join()
                    h_6.join()
                    h_7.join()
                    h_8.join()
                    h_9.join()
                    GPIO.cleanup()
                    
                    self.reaction_finished()
                if self.stir_stage == 2:
                    Pmp1()
                    hilo_ms2.start()
                    h_2.start()
                    h_3.start()
                    h_4.start()
                    h_5.start()
                    h_6.start()
                    h_7.start()
                    h_8.start()
                    h_9.start()

                    hilo_ms2.join()
                    h_2.join()
                    h_3.join()
                    h_4.join()
                    h_5.join()
                    h_6.join()
                    h_7.join()
                    h_8.join()
                    h_9.join()
                    GPIO.cleanup()
                    
                    self.reaction_finished()
                if self.stir_stage == 3:
                    Pmp1()
                    Pmp2()
                    hilo_ms3.start()
                    h_3.start()
                    h_4.start()
                    h_5.start()
                    h_6.start()
                    h_7.start()
                    h_8.start()
                    h_9.start()

                    hilo_ms3.join()
                    h_3.join()
                    h_4.join()
                    h_5.join()
                    h_6.join()
                    h_7.join()
                    h_8.join()
                    h_9.join()
                    GPIO.cleanup()
                    
                    self.reaction_finished()
            
        confirm_popup = Popup(title='Confirm', size_hint=(None, None), size=(300, 200))
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Do you want to start the reaction?",font_size=18))
        buttons = BoxLayout(size_hint_y=0.4)
        yes_btn = Button(text="YES")
        no_btn = Button(text="NO")
        yes_btn.bind(on_press=lambda x: [confirm_popup.dismiss(), wmk()])
        no_btn.bind(on_press=lambda x: [confirm_popup.dismiss()])
        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        content.add_widget(buttons)
        confirm_popup.content = content
        confirm_popup.open()
                
                
    def rxnN(self, *args):
        self.pps = [24,17,27,22,13,2,18,25,4,7]
        self.strpin = [12, 20] 
        self.flow = {0: 28, 17: 0.2481, 27: 0.1892, 22: 0.2099, 13: 0.2285, 2: 0.22, 18: 0.22, 25: 0.2409, 4: 0.22, 7: 0.22} 
        self.tc=[2,18,19,20,17,18,17,18,19,10]
        self.used_pines = {}
        
        def wmk2():
            self.tmstr = int(self.ids.stir_time.text)  if self.ids.stir_time.text.strip() else 0
            self.vs = int(self.ids.vol0.text)  if self.ids.vol0.text.strip() else 0
            self.v1 = int(self.ids.vol1.text)  if self.ids.vol1.text.strip() else 0
            self.v2 = int(self.ids.vol2.text)  if self.ids.vol2.text.strip() else 0
            self.v3 = int(self.ids.vol3.text)  if self.ids.vol3.text.strip() else 0
            self.v4 = int(self.ids.vol4.text)  if self.ids.vol4.text.strip() else 0
            self.v5 = int(self.ids.vol5.text)  if self.ids.vol5.text.strip() else 0
            self.v6 = int(self.ids.vol6.text)  if self.ids.vol6.text.strip() else 0
            self.v7 = int(self.ids.vol7.text)  if self.ids.vol7.text.strip() else 0
            self.v8 = int(self.ids.vol8.text)  if self.ids.vol8.text.strip() else 0
            self.v9 = int(self.ids.vol9.text)  if self.ids.vol9.text.strip() else 0
            
            if self.tmstr != 0:    
                def stir1():
                    stirring(self.strpin[0],self.strpin[1],self.tmstr*60+(self.v1/self.flow[self.pps[1]]+self.tc[1])+(self.v2/self.flow[self.pps[2]]+self.tc[2])+(self.v3/self.flow[self.pps[3]]+self.tc[3])+(self.v4/self.flow[self.pps[4]]+self.tc[4])+(self.v5/self.flow[self.pps[5]]+self.tc[5])+(self.v6/self.flow[self.pps[6]]+self.tc[6])+(self.v7/self.flow[self.pps[7]]+self.tc[7])+(self.v8/self.flow[self.pps[8]]+self.tc[8])+(self.v9/self.flow[self.pps[9]]+self.tc[9]))
                def stir2():
                    stirring(self.strpin[0],self.strpin[1],(self.tmstr*60)+(self.v2/self.flow[self.pps[2]]+self.tc[2])+(self.v3/self.flow[self.pps[3]]+self.tc[3])+(self.v4/self.flow[self.pps[4]]+self.tc[4])+(self.v5/self.flow[self.pps[5]]+self.tc[5])+(self.v6/self.flow[self.pps[6]]+self.tc[6])+(self.v7/self.flow[self.pps[7]]+self.tc[7])+(self.v8/self.flow[self.pps[8]]+self.tc[8])+(self.v9/self.flow[self.pps[9]]+self.tc[9]))
                def stir3():
                    stirring(self.strpin[0],self.strpin[1],self.tmstr*60+(self.v3/self.flow[self.pps[3]]+self.tc[3])+(self.v4/self.flow[self.pps[4]]+self.tc[4])+(self.v5/self.flow[self.pps[5]]+self.tc[5])+(self.v6/self.flow[self.pps[6]]+self.tc[6])+(self.v7/self.flow[self.pps[7]]+self.tc[7])+(self.v8/self.flow[self.pps[8]]+self.tc[8])+(self.v9/self.flow[self.pps[9]]+self.tc[9]))
            elif self.tmstr == 0:
                def stir1():
                    stirring(self.strpin[0],self.strpin[1],1)
                def stir2():
                    stirring(self.strpin[0],self.strpin[1],1)
                def stir3():
                    stirring(self.strpin[0],self.strpin[1],1)
            else:
                def stir1():
                    x=1
                def stir2():
                    s=1
                def stir3():
                    d=1
                    
            if self.vs != 0:
                def Pmps():
                    pumpsWork(0,int(self.pps[0]),self.vs/self.flow[self.pps[0]])
                    self.used_pines[0] = self.pps[0]
                
                def PmpsTD():
                    pumpsWorkTC(0,int(self.pps[0]),(self.v2/self.flow[self.pps[2]])+(self.v1/self.flow[self.pps[1]]),self.vs/self.flow[self.pps[0]])
                    self.used_pines[0] = self.pps[0]
            elif self.vs == 0:
                def Pmps():
                    a=1
                def PmpsTD():
                    ax=1
                    
            if self.v1 != 0:
                def Pmp1():
                    pumpsWork(1,int(self.pps[1]),self.v1/self.flow[self.pps[1]])
                    self.used_pines[1] = self.pps[1]
            elif self.v1 == 0:
                def Pmp1():
                    a=1
                    
            if self.v2 != 0:
                def Pmp2():
                    pumpsWork(2,int(self.pps[2]),self.v2/self.flow[self.pps[2]])
                    self.used_pines[2] = self.pps[2]
                
                def Pmp2TD():
                    pumpsWorkTC(2,int(self.pps[2]),self.v1/self.flow[self.pps[1]],self.v2/self.flow[self.pps[2]])
                    self.used_pines[2] = self.pps[2]
            else:
                def Pmp2():
                    a=1
                def Pmp2TD():
                    ax=1
                    
            if self.v3 != 0:
                def Pmp3():
                    pumpsWork(3,int(self.pps[3]),self.v3/self.flow[self.pps[3]])
                    self.used_pines[3] = self.pps[3]
                
                def Pmp3TD():
                    pumpsWorkTC(3,int(self.pps[3]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]]),self.v3/self.flow[self.pps[3]])
                    self.used_pines[3] = self.pps[3]
            else:
                def Pmp3():
                    a=1
                def Pmp3TD():
                    ax=1
                    
            if self.v4 != 0:
                def Pmp4():
                    pumpsWork(4,int(self.pps[4]),self.v4/self.flow[self.pps[4]])
                    self.used_pines[4] = self.pps[4]
                
                def Pmp4TD():
                    pumpsWorkTC(4,int(self.pps[4]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]]),self.v4/self.flow[self.pps[4]])
                    self.used_pines[4] = self.pps[4]
            else:
                def Pmp4():
                    a=1
                def Pmp4TD():
                    ax=1

            if self.v5 != 0:
                def Pmp5():
                    pumpsWork(5,int(self.pps[5]),self.v5/self.flow[self.pps[5]])
                    self.used_pines[5] = self.pps[5]
                
                def Pmp5TD():
                    pumpsWorkTC(5,int(self.pps[5]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]]),self.v5/self.flow[self.pps[5]])
                    self.used_pines[5] = self.pps[5]
            else:
                def Pmp5():
                    a=1
                def Pmp5TD():
                    ax=1

            if self.v6 != 0:
                def Pmp6():
                    pumpsWork(6,int(self.pps[6]),self.v6/self.flow[self.pps[6]])
                    self.used_pines[6] = self.pps[6]
            
                def Pmp6TD():
                    pumpsWorkTC(6,int(self.pps[6]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]])+(self.v5/self.flow[self.pps[5]]),self.v6/self.flow[self.pps[6]])
                    self.used_pines[6] = self.pps[6]
            else:
                def Pmp6():
                    a=1
                def Pmp6TD():
                    ax=1
                    
            if self.v7 != 0:
                def Pmp7():
                    pumpsWork(7,int(self.pps[7]),self.v7/self.flow[self.pps[7]])
                    self.used_pines[7] = self.pps[7]
            
                def Pmp7TD():
                    pumpsWorkTC(7,int(self.pps[7]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]])+(self.v5/self.flow[self.pps[5]])+(self.v6/self.flow[self.pps[6]]),self.v7/self.flow[self.pps[7]])
                    self.used_pines[7] = self.pps[7]
            else:
                def Pmp7():
                    a=1
                def Pmp7TD():
                    ax=1
                    
            if self.v8 != 0:
                def Pmp8():
                    pumpsWork(8,int(self.pps[8]),self.v8/self.flow[self.pps[8]])
                    self.used_pines[8] = self.pps[8]
            
                def Pmp8TD():
                    pumpsWorkTC(8,int(self.pps[8]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]])+(self.v5/self.flow[self.pps[5]])+(self.v6/self.flow[self.pps[6]])+(self.v7/self.flow[self.pps[7]]),self.v8/self.flow[self.pps[8]])
                    self.used_pines[8] = self.pps[8]
            else:
                def Pmp8():
                    a=1
                def Pmp8TD():
                    ax=1
                    
            if self.v9 != 0:
                def Pmp9():
                    pumpsWork(9,int(self.pps[9]),self.v9/self.flow[self.pps[9]])
                    self.used_pines[9] = self.pps[9]
            
                def Pmp9TD():
                    pumpsWorkTC(9,int(self.pps[9]),(self.v1/self.flow[self.pps[1]])+(self.v2/self.flow[self.pps[2]])+(self.vs/self.flow[self.pps[0]])+(self.v3/self.flow[self.pps[3]])+(self.v4/self.flow[self.pps[4]])+(self.v5/self.flow[self.pps[5]])+(self.v6/self.flow[self.pps[6]])+(self.v7/(self.flow[self.pps[7]]))+(self.v8/self.flow[self.pps[8]]),self.v9/self.flow[self.pps[9]])
                    self.used_pines[9] = self.pps[9]
            else:
                def Pmp9():
                    a=1
                def Pmp9TD():
                    ax=1
                    
            hilo_ms1=threading.Thread(target=stir1)
            hilo_ms2=threading.Thread(target=stir2)
            hilo_ms3=threading.Thread(target=stir3)
            hilo_s=threading.Thread(target=Pmps)
            hilo_1=threading.Thread(target=Pmp1)
            hilo_2=threading.Thread(target=Pmp2)
            hilo_3=threading.Thread(target=Pmp3)
            hilo_4=threading.Thread(target=Pmp4)
            hilo_5=threading.Thread(target=Pmp5)
            hilo_6=threading.Thread(target=Pmp6)
            hilo_7=threading.Thread(target=Pmp7)
            hilo_8=threading.Thread(target=Pmp8)
            hilo_9=threading.Thread(target=Pmp9)
            h_2=threading.Thread(target=Pmp2TD)
            h_3=threading.Thread(target=Pmp3TD)
            h_4=threading.Thread(target=Pmp4TD)
            h_5=threading.Thread(target=Pmp5TD)
            h_6=threading.Thread(target=Pmp6TD)
            h_7=threading.Thread(target=Pmp7TD)
            h_8=threading.Thread(target=Pmp8TD)
            h_9=threading.Thread(target=Pmp9TD)
            
            if self.selection_mood == "Parallel":
                hilo_ms1.start()
                hilo_s.start()
                hilo_1.start()
                hilo_2.start()
                hilo_3.start()
                hilo_4.start()
                hilo_5.start()
                hilo_6.start()
                hilo_7.start()
                hilo_8.start()
                hilo_9.start()


                hilo_s.join()
                hilo_ms1.join()
                hilo_1.join()
                hilo_2.join()
                hilo_3.join()
                hilo_4.join()
                hilo_5.join()
                hilo_6.join()
                hilo_7.join()
                hilo_8.join()
                hilo_9.join()
                GPIO.cleanup()
                    
                self.reaction_finished()
            if self.selection_mood == "In-Order":
                if self.stir_stage == 0:
                    Pmp1()
                    Pmp2()
                    Pmp3()
                    Pmp4()
                    Pmp5()
                    Pmp6()
                    Pmp7()
                    Pmp8()
                    Pmp9()
                    GPIO.cleanup()
                    
                    self.reaction_finished()
                if self.stir_stage == 1:
                    hilo_1.start()
                    h_2.start()
                    hilo_ms1.start()
                    h_3.start()
                    h_4.start()
                    h_5.start()
                    h_6.start()
                    h_7.start()
                    h_8.start()
                    h_9.start()

                    hilo_1.join()
                    h_2.join()
                    hilo_ms1.join()
                    h_3.join()
                    h_4.join()
                    h_5.join()
                    h_6.join()
                    h_7.join()
                    h_8.join()
                    h_9.join()
                    GPIO.cleanup()
                    
                    self.reaction_finished()
                if self.stir_stage == 2:
                    Pmp1()
                    hilo_ms2.start()
                    h_2.start()
                    h_3.start()
                    h_4.start()
                    h_5.start()
                    h_6.start()
                    h_7.start()
                    h_8.start()
                    h_9.start()

                    hilo_ms2.join()
                    h_2.join()
                    h_3.join()
                    h_4.join()
                    h_5.join()
                    h_6.join()
                    h_7.join()
                    h_8.join()
                    h_9.join()
                    GPIO.cleanup()
                    
                    self.reaction_finished()
                if self.stir_stage == 3:
                    Pmp1()
                    Pmp2()
                    hilo_ms3.start()
                    h_3.start()
                    h_4.start()
                    h_5.start()
                    h_6.start()
                    h_7.start()
                    h_8.start()
                    h_9.start()

                    hilo_ms3.join()
                    h_3.join()
                    h_4.join()
                    h_5.join()
                    h_6.join()
                    h_7.join()
                    h_8.join()
                    h_9.join()
                    GPIO.cleanup()
                    
                    self.reaction_finished()

                    
        confirm_popup = Popup(title='CONFIRM', size_hint=(None, None), size=(300, 200))
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Do you want to start the reaction?",font_size=18))
        buttons = BoxLayout(size_hint_y=0.4)
        yes_btn = Button(text="YES")
        no_btn = Button(text="NO")
        yes_btn.bind(on_press=lambda x: [confirm_popup.dismiss(), wmk2()])
        no_btn.bind(on_press=lambda x: [confirm_popup.dismiss()])
        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        content.add_widget(buttons)
        confirm_popup.content = content
        confirm_popup.open()
    
    # Select if consider the time charge or not 
    def chyorn(self):

        if self.selection_mood == "":
            Popup(title='Error', content=Label(text='Select the addition!',font_size=18), size_hint=(None, None), size=(300, 150)).open()
            return
        
        elif self.stir_stage is None:
            Popup(title='Error', content=Label(text='Select the stir stage!',font_size=18), size_hint=(None, None), size=(300, 150)).open()
            return            

        try:
            self.volumes = [int(self.ids[f'vol{i}'].text) for i in range(10)]
            self.tmstr = int(self.ids.stir_time.text)
        except ValueError:
            Popup(title='Error', content=Label(text='Only numbers allowed!',font_size=18), size_hint=(None, None), size=(300, 150)).open()
            return

        confirm_popup = Popup(title='CONFIRM', size_hint=(None, None), size=(300, 200))
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Consider the load time?", font_size=18))
        buttons = BoxLayout(size_hint_y=0.4)
        yes_btn = Button(text="YES")
        no_btn = Button(text="NO")
        yes_btn.bind(on_press=lambda x: [confirm_popup.dismiss(), self.rxnY()])
        no_btn.bind(on_press=lambda x: [confirm_popup.dismiss(), self.rxnN()])
        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        content.add_widget(buttons)
        confirm_popup.content = content
        confirm_popup.open()


class MikiApp(App):
    def build(self):
        Builder.load_file("interface/mikiscreen_fixed.kv")
        return MikiScreen()

if __name__ == '__main__':
    MikiApp().run()