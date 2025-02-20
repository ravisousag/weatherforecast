import hashlib
import os
from tkinter import *
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from login import SytemLogin
from user import User
from weather_forecast import WeatherForecast


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # set window
        self.title("Sistema de previsão do tempo")
        self.geometry("900x600")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        self.current_frame = None

        # inicializate
        self.show_login()
        self.__system_login = SytemLogin()
        self.__forencasts = WeatherForecast()

        # Add default user
        self.__system_login.insert_user(
            User(
                "Ravi Garcindo",
                "ravisg",
                "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
            )
        )

    def switch_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def show_login(self):
        # Getting images in assets
        file_path = os.path.dirname(os.path.realpath(__file__))
        user_icon = ctk.CTkImage(
            Image.open(file_path + "/assets/user_icon.png"), size=(30, 30)
        )
        password_icon = ctk.CTkImage(
            Image.open(file_path + "/assets/password_icon.png"), size=(33, 33)
        )
        show_pass = ctk.CTkImage(
            Image.open(file_path + "/assets/show_pass_icon.png"), size=(20, 20)
        )
        hide_pass = ctk.CTkImage(
            Image.open(file_path + "/assets/hide_pass_icon.png"), size=(20, 20)
        )

        # Dynamic effect for create new account Label
        def on_enter(event):
            new_acc_label.configure(text_color="Purple")

        def on_leave(event):
            new_acc_label.configure(text_color="black")

        def hide_password():
            if self.password_entry.cget("show") == "":
                hide_pass_button.configure(image=hide_pass)
                self.password_entry.configure(show="*")
            else:
                hide_pass_button.configure(image=show_pass)
                self.password_entry.configure(show="")

        def autentication():
            username = self.username_entry.get()
            password = self.password_entry.get()
            hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if self.__system_login.autentication(username, hashed):
                login_frame.destroy()
                self.show_home_frame()
            else:
                messagebox.showerror("Login", "Usuário ou senha incorretos!")

        # Frame for Loggin
        login_frame = ctk.CTkFrame(self, fg_color="white", width=500, height=600)
        background = ctk.CTkImage(
            Image.open("./P2/assets/background_mountain.jpg"), size=(500, 600)
        )
        ctk.CTkLabel(login_frame, text=None, image=background).place(x=-10, y=0)

        # Creating Label on the Frame login
        title = ctk.CTkLabel(
            login_frame,
            text="Bem-vindo!",
            text_color="#7138C4",
            font=("Roboto Bold", 25, "bold"),
        )
        title.place(x=550, y=80)

        label_subheading = ctk.CTkLabel(
            login_frame,
            text="Entre na sua conta",
            text_color="black",
            font=("Roboto Bold", 15),
        )
        label_subheading.place(x=550, y=110)

        # Label for Username
        user_label = ctk.CTkLabel(
            login_frame,
            text="Usuário:",
            text_color="#7138C4",
            font=("Roboto Bold", 19, "bold"),
            image=user_icon,
            compound="left",
        )
        user_label.place(x=550, y=200)

        # Entry box for username
        self.username_entry = ctk.CTkEntry(
            login_frame,
            width=300,
            height=40,
            corner_radius=9,
            border_color="#7138C4",
            border_width=2,
            font=("Roboto Bold", 17),
            text_color="#7138C4",
            fg_color="#E8F0F1",
            placeholder_text_color="#7138C4",
        )
        self.username_entry.place(x=550, y=240)

        # Creating Label for Password
        pass_label = ctk.CTkLabel(
            login_frame,
            text="Senha:",
            text_color="#7138C4",
            font=("Roboto Bold", 19, "bold"),
            image=password_icon,
            compound="left",
        )
        pass_label.place(x=550, y=330)

        # Entry box for password
        self.password_entry = ctk.CTkEntry(
            login_frame,
            width=300,
            height=40,
            corner_radius=9,
            border_color="#7138C4",
            border_width=2,
            font=("Roboto Bold", 17),
            text_color="#7138C4",
            fg_color="#E8F0F1",
            placeholder_text_color="#7138C4",
            show="",
        )
        self.password_entry.place(x=550, y=360)

        # Creating Loging Button
        login_button = ctk.CTkButton(
            login_frame,
            text="Login",
            text_color="white",
            fg_color="#703DF1",
            width=300,
            height=40,
            font=("Roboto Bold", 17, "bold"),
            hover_color="#7138C4",
            command=autentication,
        )
        login_button.place(x=550, y=430)

        # Creating hide password button
        hide_pass_button = ctk.CTkButton(
            master=login_frame,
            text="",
            hover_color="white",
            height=20,
            width=10,
            bg_color="transparent",
            fg_color="transparent",
            corner_radius=15,
            command=hide_password,
            image=hide_pass,
            compound="left",
        )
        hide_pass_button.place(x=850, y=370)

        # Label for creating New Account
        new_acc_label = ctk.CTkLabel(
            master=login_frame,
            text="Crie uma nova conta",
            text_color="#7138C4",
            font=("Arial", 15, "underline"),
        )
        new_acc_label.place(x=550, y=550)
        new_acc_label.bind("<Button-1>", lambda event: self.show_register_frame())
        new_acc_label.bind("<Enter>", on_enter)
        new_acc_label.bind("<Leave>", on_leave)

        self.switch_frame(login_frame)

    def show_register_frame(self):

        def registration():
            name = self.regs_name_entry.get()
            username = self.regs_username_entry.get()
            password = self.regs_password_entry.get()
            hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if self.__system_login.insert_user(User(name, username, hashed)):
                register_frame.destroy()
                messagebox.showerror("Cadastro", "Cadastrado com sucesso!")
                self.show_register_frame()
                
            else:
                ex = self.__system_login.insert_user(name, username, hashed)
                messagebox.showerror(f"Erro ao cadastrar!"(ex))

        # Getting images in assets
        file_path = os.path.dirname(os.path.realpath(__file__))
        show_pass = ctk.CTkImage(
            Image.open(file_path + "/assets/show_pass_icon.png"), size=(20, 20)
        )
        hide_pass = ctk.CTkImage(
            Image.open(file_path + "/assets/hide_pass_icon.png"), size=(20, 20)
        )

        # Dynamic effect for create new account Label
        def on_enter(event):
            new_acc_label.configure(text_color="Purple")

        def on_leave(event):
            new_acc_label.configure(text_color="black")

        # Hiding password
        def hide_password():
            if self.regs_password_entry.cget("show") == "":
                hide_pass_button.configure(image=hide_pass)
                self.regs_password_entry.configure(show="*")
            else:
                hide_pass_button.configure(image=show_pass)
                self.regs_password_entry.configure(show="")

        # Frame for register
        register_frame = ctk.CTkFrame(self, fg_color="white", width=500, height=600)
        background = ctk.CTkImage(
            Image.open("./P2/assets/background_mountain.jpg"), size=(500, 600)
        )
        ctk.CTkLabel(register_frame, text=None, image=background).place(x=-10, y=0)

        # Creating Label on the Frame login
        title = ctk.CTkLabel(
            register_frame,
            text="Crie sua conta",
            text_color="#7138C4",
            font=("Roboto Bold", 25, "bold"),
        )
        title.place(x=550, y=80)

        label_subheading = ctk.CTkLabel(
            register_frame,
            text="Fácil e rápido",
            text_color="black",
            font=("Roboto Bold", 15),
        )
        label_subheading.place(x=550, y=110)

        # Label for name
        self._name_label = ctk.CTkLabel(
            register_frame,
            text="Nome completo:",
            text_color="#7138C4",
            font=("Roboto Bold", 19, "bold"),
            compound="left",
        )
        self._name_label.place(x=550, y=200)

        # Entry box for name
        self.regs_name_entry = ctk.CTkEntry(
            register_frame,
            width=300,
            height=40,
            corner_radius=9,
            border_color="#7138C4",
            border_width=2,
            font=("Roboto Bold", 17),
            text_color="#7138C4",
            fg_color="#E8F0F1",
            placeholder_text_color="#7138C4",
        )
        self.regs_name_entry.place(x=550, y=230)

        # Label for username
        self._username_label = ctk.CTkLabel(
            register_frame,
            text="Usuário:",
            text_color="#7138C4",
            font=("Roboto Bold", 19, "bold"),
            compound="left",
        )
        self._username_label.place(x=550, y=290)

        # Entry box for username
        self.regs_username_entry = ctk.CTkEntry(
            register_frame,
            width=300,
            height=40,
            corner_radius=9,
            border_color="#7138C4",
            border_width=2,
            font=("Roboto Bold", 17),
            text_color="#7138C4",
            fg_color="#E8F0F1",
            placeholder_text_color="#7138C4",
        )
        self.regs_username_entry.place(x=550, y=320)

        # Label for password
        self._password_label = ctk.CTkLabel(
            register_frame,
            text="Senha:",
            text_color="#7138C4",
            font=("Roboto Bold", 19, "bold"),
            compound="left",
        )
        self._password_label.place(x=550, y=380)

        # Entry box for password
        self.regs_password_entry = ctk.CTkEntry(
            register_frame,
            width=300,
            height=40,
            corner_radius=9,
            border_color="#7138C4",
            border_width=2,
            font=("Roboto Bold", 17),
            text_color="#7138C4",
            fg_color="#E8F0F1",
            placeholder_text_color="#7138C4",
        )
        self.regs_password_entry.place(x=550, y=410)

        # Creating Registration button
        registrer_button = ctk.CTkButton(
            register_frame,
            text="Registrar",
            text_color="white",
            fg_color="#703DF1",
            width=300,
            height=40,
            font=("Roboto Bold", 17, "bold"),
            hover_color="#7138C4",
            command=registration,
        )
        registrer_button.place(x=550, y=480)

        # Creating hide password button
        hide_pass_button = ctk.CTkButton(
            register_frame,
            text="",
            hover_color="white",
            height=20,
            width=10,
            bg_color="transparent",
            fg_color="transparent",
            corner_radius=15,
            command=hide_password,
            image=hide_pass,
            compound="left",
        )
        hide_pass_button.place(x=850, y=420)

        # Label for creating New Account
        new_acc_label = ctk.CTkLabel(
            register_frame,
            text="Já possui conta?",
            text_color="grey",
            font=("Arial", 15, "underline"),
        )
        new_acc_label.place(x=550, y=550)

        # Label for creating New Account
        new_acc_label = ctk.CTkLabel(
            register_frame,
            text="Entrar",
            text_color="#7138C4",
            font=("Arial", 15, "underline"),
        )
        new_acc_label.place(x=665, y=550)
        new_acc_label.bind("<Button-1>", lambda event: self.show_login())
        new_acc_label.bind("<Enter>", on_enter)
        new_acc_label.bind("<Leave>", on_leave)

        self.switch_frame(register_frame)

    def show_home_frame(self):
        home_frame = ctk.CTkFrame(self, fg_color="white", width=900, height=600)

        title = ctk.CTkLabel(
            home_frame,
            text="Previsão do tempo",
            text_color="#7138C4",
            font=("Roboto Bold", 25, "bold"),
        )
        title.place(x=20, y=20)

        # Lable for input city
        self._city_label = ctk.CTkLabel(
            home_frame,
            text="Cidade",
            text_color="#7138C4",
            font=("Roboto Bold", 19, "bold"),
            compound="left",
        )
        self._city_label.place(x=20, y=75)

        # entry for name city
        self.city_entry = ctk.CTkEntry(
            home_frame,
            width=200,
            height=40,
            corner_radius=9,
            border_color="#7138C4",
            border_width=2,
            font=("Roboto Bold", 17),
            text_color="#7138C4",
            fg_color="#E8F0F1",
            placeholder_text_color="#7138C4",
        )
        self.city_entry.place(x=100, y=70)

        # Lable for start date
        self._dt_start = ctk.CTkLabel(
            home_frame,
            text="Data incial",
            text_color="#7138C4",
            font=("Roboto Bold", 19, "bold"),
            compound="left",
        )
        self._dt_start.place(x=320, y=75)

        # entry for start date
        self.dt_start_entry = ctk.CTkEntry(
            home_frame,
            width=100,
            height=40,
            corner_radius=9,
            border_color="#7138C4",
            border_width=2,
            font=("Roboto Bold", 17),
            text_color="#7138C4",
            fg_color="#E8F0F1",
            placeholder_text_color="#7138C4",
        )
        self.dt_start_entry.place(x=420, y=70)

        # Lable for end date
        self._dt_end = ctk.CTkLabel(
            home_frame,
            text="Data final",
            text_color="#7138C4",
            font=("Roboto Bold", 19, "bold"),
            compound="left",
        )
        self._dt_end.place(x=540, y=75)

        # entry for end date
        self.dt_end_entry = ctk.CTkEntry(
            home_frame,
            width=100,
            height=40,
            corner_radius=9,
            border_color="#7138C4",
            border_width=2,
            font=("Roboto Bold", 17),
            text_color="#7138C4",
            fg_color="#E8F0F1",
            placeholder_text_color="#7138C4",
        )
        self.dt_end_entry.place(x=630, y=70)

        # Find forecast
        find_forecast = ctk.CTkButton(
            home_frame,
            text="Buscar",
            text_color="white",
            fg_color="#703DF1",
            width=100,
            height=40,
            font=("Roboto Bold", 17, "bold"),
            hover_color="#7138C4",
            command=self.show_forencasts,
        )
        find_forecast.place(x=770, y=70)

        # Find forecast
        back = ctk.CTkButton(
            home_frame,
            text="Voltar",
            text_color="white",
            fg_color="#703DF1",
            width=100,
            height=40,
            font=("Roboto Bold", 17, "bold"),
            hover_color="#7138C4",
            command=self.show_login,
        )
        back.place(x=420, y=550)
        self.switch_frame(home_frame)

    def show_forencasts(self):
        city = self.city_entry.get()
        dt_start = self.dt_start_entry.get()
        dt_end = self.dt_end_entry.get()
        result = self.__forencasts.get_forencast(city, dt_start, dt_end)

        textbox = ctk.CTkTextbox(
            self,
            corner_radius=9,
            border_color="#7138C4",
            text_color="#7138C4",
            fg_color="#E8F0F1",
            width=700,
            height=350,
        )
        textbox.pack()
        textbox.place(x=100, y=150)
        formatted = "\n".join(map(str, result))
        textbox.insert("0.0", formatted)


# Executar o sistema
if __name__ == "__main__":
    interface = App()
    interface.mainloop()
