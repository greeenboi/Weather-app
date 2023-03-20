import tkinter
from tkinter.ttk import *
import os
import tkinter.messagebox
import customtkinter
import requests
import json
import webbrowser
import time
from PIL import *
import urllib.request
from datetime import datetime


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
API_KEY = "39f9436e4d81c8e85a0bc392a13deb51"

normal="#320064"
hover="#230046"

class App(customtkinter.CTk):
    city=""
    desc=""
    temp=""
    humid=""
    clouds=""
    timezone=""
    weather=""
    weather_id=""
    time_now = datetime.now()
    time_city = ""
    citytime=""
    lang="en"
    local_time=time_now.strftime("%H:%M:%S")
    def __init__(self):
        super().__init__()

        # configure window
        self.title("WhatsTheWeather")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140,height=1000, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Weather", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Github" , command=self.openweb("https://github.com/greeenboi"))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text="Support me", command=self.openweb("https://suvangs.netlify.app/"))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.label_time=customtkinter.CTkLabel(self.sidebar_frame,text=self.local_time,fg_color=("#2CC985","#1F1B24"),text_color=("#000000","#CBE4DE"),corner_radius=8,width=50,height=15)
        self.label_time.grid(row=3, column=0)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,text="Refresh Local Time", command=self.refresh)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
                
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        

        # create label        
        self.label =customtkinter.CTkLabel(self,text="ENTER CITY NAME",width=120,height=25,justify="left",fg_color=("#2CC985","#1F1B24"),text_color=("#000000","#CBE4DE"),corner_radius=8)
        
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250 ,height= 100)
        self.tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("City Name")        
        self.tabview.tab("City Name").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
                
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("City Name"), text="Enter city name",command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        self.optionvariable= customtkinter.StringVar(value="English")
        self.language_select= customtkinter.CTkOptionMenu(master=self.tabview.tab("City Name") ,values=["English","Hindi","French"],command=self.selectlang, variable=self.optionvariable)
        self.language_select.grid(row=5, column=0, padx=20, pady=10)
        
        # create pitureview
        self.pictureview = customtkinter.CTkTabview(self, width=250 ,height= 100)
        self.pictureview.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.pictureview.add("Weather status") 
        self.weather_picture = customtkinter.CTkImage(light_image=Image.open("./media/snowflake.png"),size=(128, 128))
        self.imgbutton = customtkinter.CTkButton(self.pictureview, image=self.weather_picture, text="", state="disabled")
        self.imgbutton.grid(row=3, column=0, padx=20, pady=(10, 10))
        
        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        

        # set default values               
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")         
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        #self.textbox.insert("0.0", self.weather)
        self.label.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in the name of a city:", title="Enter city name",button_hover_color="green")
        self.city = str(dialog.get_input())        
        self.get_weather()
    
    def openweb(self,url):   
        print("opengit click") 
        self.open1(url)
            
    def open1(self,url):
        #webbrowser.open(url,new=new)    
        print("no")
    
    def refresh(self):
        self.time_now = datetime.now()
        self.local_time=self.time_now.strftime("%H:%M:%S")
        self.label_time.configure(text=self.local_time)
    
    def selectlang(self,choice):
        print(choice)
        if(choice=="English"):
            self.lang="en"
        elif(choice=="Hindi"):
            self.lang="hi"
        elif(choice=="French"):
            self.lang="fr"
        else:
            self.lang="en"
        self.get_weather()
            
    def get_weather(self):
        city=self.city        
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang={self.lang}"
        response = requests.get(url)
        if response.status_code == 200:
            self.string_input_button.configure(text="LOADING...")
            time.sleep(1)
            data = response.json()
            self.desc = data["weather"][0]["description"].capitalize()
            self.weather_id= data["weather"][0]["id"]
            self.temp = str(data["main"]["temp"])
            self.humid = str(data["main"]["humidity"])
            self.clouds = str(data["clouds"]["all"])
            self.time_city = str(data["timezone"])
            self.citytime=self.city_time()
            print(f"weatherid is {self.weather_id}\n")
            self.weather_status()
            print( f"{self.desc}\nTemperature: {self.temp}°C\nHumidity: {self.humid}%\nCloudiness: {self.clouds}%\nTime in {self.city} is {self.citytime}")
            self.weather= f"Weather Details for {self.city}\n\nDescription: {self.desc}\nTemperature: {self.temp}\nHumidity: {self.humid}\nCloudiness: {self.clouds}%\nTime in {self.city} is {self.citytime}" 
            self.label.configure(text=self.weather,justify="center",font=customtkinter.CTkFont(size=15, weight="bold"))
            self.string_input_button.configure(text="Enter city name")
            
        else:
            print( "Error: Could not retrieve weather data.")
            self.string_input_button.configure(text="Error loading try again")
    
    def weather_status(self):
        iconcode=""
        if(self.weather_id>=200 and self.weather_id<=232):
            iconcode="11d"
        elif((self.weather_id>=300 and self.weather_id<=321)or(self.weather_id>=520 and self.weather_id<=531)):
            iconcode="09d"
        elif(self.weather_id>=500 and self.weather_id<=504):
            iconcode="10d"
        elif(self.weather_id==511 or (self.weather_id>=600 and self.weather_id<=622)):
            iconcode="13d"
        elif(self.weather_id>=701 and self.weather_id<=781):
            iconcode="50d"
        elif(self.weather_id==800):
            iconcode="01d"
        elif(self.weather_id==801):
            iconcode="02d"
        elif(self.weather_id==802):
            iconcode="03d"
        elif(self.weather_id==803 or self.weather_id==804):
            iconcode="04d"
        urllib.request.urlretrieve( f'https://openweathermap.org/img/wn/{iconcode}@4x.png',"wstat.png")
        img = Image.open("wstat.png")
        self.weather_picture.configure(light_image=img,size=(200, 200))
        
    def city_time(self):
        return self.time_city
        

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    

if __name__ == "__main__":
    app = App()    
    
    app.mainloop()