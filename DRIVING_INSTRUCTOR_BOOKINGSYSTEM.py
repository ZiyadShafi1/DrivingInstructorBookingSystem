import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import os
import customtkinter as ctk
from PIL import Image
import hashlib
import random
import smtplib
from email.message import EmailMessage
import re
from datetime import datetime, timedelta
import requests

class MainWindow(ctk.CTk):
    def __init__(self, title, size):

        #Main Setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.CreateDatabase()
        self.CreateMainMenu()
        

    def CreateMaterialButton(self, master, text, command, width=200, height=50):
        BUTTON_COLOR = "white"
        HOVER_COLOR = "#2196F3" 
        TEXT_COLOR = "black"

        button = ctk.CTkButton(master, text=text, width=width, height=height, command=command, 
                               fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        return button
    
    def CreateLogoutButton(self, master, text, command, width=200, height=50):
        BUTTON_COLOR = "#FFFFFF"  
        HOVER_COLOR = "red" 
        TEXT_COLOR = "#000000"    

        button = ctk.CTkButton(master, text=text, width=width, height=height, command=command, 
                               fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        return button


##Sets up the Main menu and login windows    
    def CreateMainMenu(self):
        self.ClearAllWidgets()

        
        BannerFrame = ctk.CTkFrame(self, fg_color="#7e7e7e")  
        BannerFrame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        BannerFrame.grid_rowconfigure(0, weight=1)
        BannerFrame.grid_columnconfigure(0, weight=1)

        
        LogoPath = os.path.join(os.getcwd(), 'logo.png')
        PilImage = Image.open(LogoPath)  
        LogoImage = ctk.CTkImage(light_image=PilImage, size=(350, 140))  
        LogoLabel = ctk.CTkLabel(BannerFrame, image=LogoImage, text="")
        LogoLabel.grid(row=0, column=0, pady=10, padx=10)

       
        self.StudentLoginButton = self.CreateMaterialButton(self, "Student Login", self.StudentLoginWindow)
        self.InstructorLoginButton = self.CreateMaterialButton(self, "Instructor Login", self.InstructorLoginWindow)
        self.AdminLoginButton = self.CreateMaterialButton(self, "Administrator Login", self.AdminLoginWindow)
        self.ChangePasswordButton = self.CreateMaterialButton(self, "Change Password", self.ChangePassword)

        
        self.StudentLoginButton.grid(row=1, column=1, pady=10)
        self.InstructorLoginButton.grid(row=2, column=1, pady=10)
        self.AdminLoginButton.grid(row=3, column=1, pady=10)
        self.ChangePasswordButton.grid(row=4, column=1, pady=10, padx = 10,sticky = "se")
        self.grid_columnconfigure(0, weight=1)

        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(4, weight = 1)

    def StudentLoginWindow(self):
        self.CreateLoginWindow("Student Login Window",self.ValidateStudentLogin)
    
    def InstructorLoginWindow(self):
        self.CreateLoginWindow("Instructor Login Window",self.ValidateInstructorLogin)
    
    def AdminLoginWindow(self):
        self.CreateLoginWindow("Administrator Login Window",self.ValidateAdminLogin)

    def CreateLoginWindow(self,title, userfunction):
        self.LoginWindow = ctk.CTkToplevel(self)
        self.LoginWindow.title (title)
        self.LoginWindow.geometry("300x200")
        

        self.AddLoginWidgets(self.LoginWindow,userfunction)
        self.LoginWindow.wm_attributes("-topmost", True)

    ##CreateLoginWindow creates a new top-level window (self.LoginWindow) with a given title and size, 
    ## then calls AddLoginWidgets to fill that window with the necessary login UI elements.
    ## Finally, it sets the new window to always be on top of other windows using wm_attributes.


    def CreateDatabase(self):
       
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS instructors (
                                instructorid INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL,
                                emailaddress TEXT NOT NULL,
                                accounttype TEXT NOT NULL,
                                firstname TEXT NOT NULL,
                                surname TEXT NOT NULL,
                                dob DATE NOT NULL,
                                sex CHAR NOT NULL,
                                postcode TEXT NOT NULL)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                                studentid INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL,
                                emailaddress TEXT NOT NULL,
                                accounttype TEXT NOT NULL,
                                firstname TEXT NOT NULL,
                                surname TEXT NOT NULL,
                                dob DATE NOT NULL,
                                sex CHAR NOT NULL,
                                postcode TEXT NOT NULL,
                                instructorid INTEGER NOT NULL,
                                FOREIGN KEY(instructorid) REFERENCES instructors(instructorid))''')
        
       

        cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                                adminid INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL,
                                emailaddress TEXT NOT NULL,
                                accounttype TEXT NOT NULL,
                                firstname TEXT NOT NULL,
                                surname TEXT NOT NULL,
                                dob DATE NOT NULL,
                                sex CHAR NOT NULL,
                                postcode TEXT NOT NULL)''')
        

        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                                bookingid INTEGER PRIMARY KEY AUTOINCREMENT,
                                startpostcode TEXT NOT NULL,
                                endpostcode TEXT NOT NULL,
                                date DATE NOT NULL,
                                time TIME NOT NULL,
                                studentid INTEGER NOT NULL,
                                instructorid INTEGER NOT NULL,
                                FOREIGN KEY(instructorid) REFERENCES instructors(instructorid),
                                FOREIGN KEY(studentid) REFERENCES students(studentid))''')
        
        cursor.execute("SELECT * FROM admins WHERE accounttype = ?", ('Administrator',))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO admins (username, password, emailaddress, accounttype, firstname, surname, dob, sex, postcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8','admin@roadsense.com','Administrator', 'Admin', 'Admin', '04/03/2020', 'm', 'LE22HL', '2'))
            conn.commit()
            conn.close()

    def AddLoginWidgets(self, window, usertype):
        
        UsernameLabel = ctk.CTkLabel(window, text="Username:")
        UsernameLabel.grid(row=0, column=0,pady=5)
        
        self.UsernameField = ctk.CTkEntry(window, width=200)
        self.UsernameField.grid(row=1, column=0,pady=5)
        
        PasswordLabel = ctk.CTkLabel(window, text="Password:")
        PasswordLabel.grid(row=2, column=0,pady=5)
        
        self.PasswordField = ctk.CTkEntry(window, width=200, show="*")
        self.PasswordField.grid(row=3, column=0,pady=5)
        
        LoginButton = self.CreateMaterialButton(window, "Login", usertype, width=150, height=40)
        LoginButton.grid(row=4, column=0,pady=10)
        window.grid_columnconfigure(0, weight=1)

##Login Validation
    def ValidateStudentLogin(self):
        Username = self.UsernameField.get().lower()
        Password = self.PasswordField.get()

        HashVar = hashlib.new("SHA256")
        HashVar.update(Password.encode())
        HashedPassword = (HashVar.hexdigest())

    
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE username = ? AND password = ?", (Username, HashedPassword))
        user = cursor.fetchone()
        
        

        if user:
            self.AccountType = str(user[4])
            self.StudentID = str(user[0])
            self.AccountName = str(user[1])

        if user and self.AccountType == "student":
            tk.messagebox.showinfo("Student Login Success", f"Welcome {Username}!")
            self.LoginWindow.destroy() 
            self.ShowStudentPortal()

        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")

    def ValidateInstructorLogin(self):
        Username = self.UsernameField.get().lower()
        Password = self.PasswordField.get()
        HashVar = hashlib.new("SHA256")
        HashVar.update(Password.encode())
        HashedPassword = (HashVar.hexdigest())

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM instructors WHERE username = ? AND password = ?", (Username, HashedPassword))
        user = cursor.fetchone()
        
        

        if user:
            self.AccountType = str(user[4])
            self.InstructorID = str(user[0])
            self.AccountName = str(user[1])

        if user and self.AccountType == "Instructor":
                tk.messagebox.showinfo("Instructor Login Success", f"Welcome {Username}!")
                self.LoginWindow.destroy() 
                self.ShowInstructorPortal()
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")

    def ValidateAdminLogin(self):
        Username = self.UsernameField.get().lower()
        Password = self.PasswordField.get()
        HashVar = hashlib.new("SHA256")
        HashVar.update(Password.encode())
        HashedPassword = (HashVar.hexdigest())

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(""" SELECT * FROM admins
                                WHERE username = ? AND password = ?""", (Username, HashedPassword))
        user = cursor.fetchone()
        
        

        if user:
            self.AccountType = str(user[4])
            self.AdminID = str(user[0])
            self.AccountName = str(user[1])


        if user and self.AccountType == "Administrator":
            tk.messagebox.showinfo("Admin Login Success", f"Welcome {Username}!")
            self.LoginWindow.destroy() 
            self.ShowAdminPortal()

        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")

##Sorting Algorithm
    def MergeSort(self, Array):
        if len(Array)>1:
            LeftArray = Array[0:len(Array)//2]
            RightArray = Array[len(Array)//2:len(Array)]

            ##Recursion Part
            self.MergeSort(LeftArray)
            self.MergeSort(RightArray)

            ##Merging

            LMELeftArray = 0##Leftarray index
            LMERightArray = 0 ##rightarray index
            MergedIndex = 0 ##Merged array index
            while LMELeftArray < len(LeftArray) and LMERightArray < len(RightArray):
                if LeftArray[LMELeftArray] < RightArray[LMERightArray]:
                    Array[MergedIndex] = LeftArray[LMELeftArray]

                    LMELeftArray += 1
                else:
                    Array[MergedIndex] = RightArray[LMERightArray]
                    LMERightArray += 1

                MergedIndex += 1

            while LMELeftArray < len(LeftArray):
                Array[MergedIndex] = LeftArray[LMELeftArray]
                LMELeftArray +=1
                MergedIndex +=1
            
            while LMERightArray < len(RightArray):
                Array[MergedIndex] = RightArray[LMERightArray]
                LMERightArray +=1
                MergedIndex +=1
        
    def MergeSortReverser(self,array):
        self.MergeSort(array)
        array.reverse()



##Change Password Stuff
    def ChangePassword(self):
        
        changepassword(self)
        
    def ClearAllWidgets(self):
       
        for widget in self.winfo_children():
            widget.grid_forget()   
            widget.pack_forget()   
            widget.place_forget()


## Student Portal
    def ShowStudentPortal(self):
            self.StudentLoginButton.grid_forget()
            self.InstructorLoginButton.grid_forget()
            self.AdminLoginButton.grid_forget()
            self.rowconfigure(4, weight = 0)
            
            self.ViewFeedbackButton = self.CreateMaterialButton(self, "View All Reports/Feedback", self.ViewFeedbackReports)
            self.ViewFeedbackButton.grid(row=1, column=0, pady=10,padx = 10,sticky="W")
            self.ViewLessonHistoryButton = self.CreateMaterialButton(self, "View All Lessons (History and Upcoming)", self.ViewHistory)
            self.ViewLessonHistoryButton.grid(row=2, column=0, pady=10, padx = 10, sticky="W")
            
            
            
            self.BookLessonButton = self.CreateMaterialButton(self, "Book a Lesson", command=self.OpenStudentBooking)
            self.BookLessonButton.grid(row=3, column=0, pady=10, padx = 10, sticky="W")

            

            self.SignOutButton = self.CreateLogoutButton(self, "Sign Out", self.CreateMainMenu, width=150, height=40)
            self.SignOutButton.grid(row=0, column=1, padx=10, pady=10, sticky="NE")

            IDText = "StudentID:"+(self.StudentID)
            self.AccountIdLabel = ctk.CTkLabel(self, text=IDText)
            self.AccountIdLabel.grid(row=5, column=1, pady=10, padx = 5, sticky="SE")

            AccountText = "Username: "+(self.AccountName)
            self.AccountNameLabel = ctk.CTkLabel(self, text=AccountText)
            self.AccountNameLabel.grid(row=6, column=1, pady=10, padx = 5, sticky="SE")

            AccountTypeText = "Account Type: "+(self.AccountType)
            self.AccountNameLabel = ctk.CTkLabel(self, text=AccountTypeText)
            self.AccountNameLabel.grid(row=7, column=1, pady=10, padx = 5, sticky="SE")

    def ViewHistory(self):
        self.FetchAllStudentBookings()
        root = tk.Tk()
        app = TableViewingApp(root, self.ReturnedBookings)
        root.mainloop()
    
    def FetchAllStudentBookings(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        ##Use crosstable SQL to select student name and instructor name
        cursor.execute("""SELECT bookingid, date, time, 
           (SELECT username FROM students WHERE students.studentid = bookings.studentid), 
           (SELECT username FROM instructors WHERE instructors.instructorid = bookings.instructorid), 
           startpostcode, endpostcode
            FROM bookings
            WHERE studentid = ?
            """, (self.StudentID))

        self.ReturnedBookings = cursor.fetchall()

    def OpenStudentBooking(self):
        self.FetchAllStudentUsernames()
        self.FetchAllInstructorUsernames()

        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT instructorid FROM students WHERE studentid = ?",(self.StudentID))
        instructorid = cursor.fetchone()[0]
        cursor.execute("SELECT username FROM instructors WHERE instructorid = ?",(instructorid,))
        instructorname = cursor.fetchone()[0]
        print(instructorname)
        print(instructorid)
        conn.close

        root = ctk.CTk()
        app = StudentBookLessonApp(root,self.InstructorsList,self.StudentsList,instructorid,instructorname,self.AccountName,self.StudentID)
        root.mainloop()
    
    def ViewFeedbackReports(self):
        self.FetchAllStudentBookings()
        root = ctk.CTk()
        app = ViewFeedbackReports(root, self.ReturnedBookings)
        root.mainloop()

##Admin Portal
    def ShowAdminPortal(self):
            self.StudentLoginButton.grid_forget()
            self.InstructorLoginButton.grid_forget()
            self.AdminLoginButton.grid_forget()
            self.rowconfigure(4, weight = 0)
            
            self.CreateAccountButton = self.CreateMaterialButton(self, "Create Account", self.OpenCreateAccount)
            self.CreateAccountButton.grid(row=1, column=0, pady=10, padx = 10, sticky="W")
    
            self.RemoveAccountButton = self.CreateMaterialButton(self, "Remove an account", self.RemoveAccountMenu)
            self.RemoveAccountButton.grid(row=2, column=0, pady=10, padx = 10, sticky="W")
            
            self.ViewAllUpcomingButton = self.CreateMaterialButton(self, "View/Remove/Modify All Lessons", self.OpenViewUpcomingWindow)
            self.ViewAllUpcomingButton.grid(row=3, column=0, pady=10, padx = 10, sticky="W")
            
            self.OpenBookLessonManual = self.CreateMaterialButton(self, "Book a Lesson (Manual)", self.BookaLesson)
            self.OpenBookLessonManual.grid(row=4, column=0, pady=10, padx = 10, sticky="W")
            

            self.SignOutButton = self.CreateLogoutButton(self, "Sign Out", self.CreateMainMenu, width=150, height=40)
            self.SignOutButton.grid(row=0, column=1, padx=10, pady=10, sticky="NE")

            idtext = "AdminID:"+(self.AdminID)
            self.AccountIdLabel = ctk.CTkLabel(self, text=idtext)
            self.AccountIdLabel.grid(row=5, column=1, pady=10, padx = 5, sticky="SE")

            accounttext = "Username: "+(self.AccountName)
            self.AccountNameLabel = ctk.CTkLabel(self, text=accounttext)
            self.AccountNameLabel.grid(row=6, column=1, pady=10, padx = 5, sticky="SE")

            accounttypetext = "Account Type: "+(self.AccountType)
            self.AccountNameLabel = ctk.CTkLabel(self, text=accounttypetext)
            self.AccountNameLabel.grid(row=7, column=1, pady=10, padx = 5, sticky="SE")

    ##Remove account function
    def RemoveAccountMenu(self):
        self.RemoveAccountWindow = ctk.CTkToplevel(self)
        self.RemoveAccountWindow.title("Remove an Account")
        self.RemoveAccountWindow.geometry("631x400")
        self.RemoveAccountWindow.wm_attributes("-topmost", True)

        selectstudent = self.CreateMaterialButton(self.RemoveAccountWindow, "Students", self.RemoveStudents)
        selectstudent.grid(row=1, column=1,padx=5,pady=5)

        selectinstructor = self.CreateMaterialButton(self.RemoveAccountWindow, "Instructors", self.RemoveInstructors)
        selectinstructor.grid(row=1, column=2,padx=5,pady=5)

        selectadministrators = self.CreateMaterialButton(self.RemoveAccountWindow, "Administrators", self.RemoveAdmins)
        selectadministrators.grid(row=1, column=3,padx=5,pady=5)

        self.UserTypeLabel = ctk.CTkLabel(self.RemoveAccountWindow, text='',font=(None,18))
        self.UserTypeLabel.grid(row=2, column=2, pady=5)

        removeaccountbutton = self.CreateLogoutButton(self.RemoveAccountWindow, "Remove Account", self.OpenConfirmAccount)
        
        removeaccountbutton.grid(row=4, column=2,padx=5,pady=10)
        self.RemoveAccountWindow.rowconfigure(4, weight = 4)

        updatefilter = self.CreateMaterialButton(self.RemoveAccountWindow, "Refresh Filters/Accounts", self.UpdateFilter)
        updatefilter.grid(row=5, column=3,padx=5,pady=5)
        self.FiltersDropdown = ctk.CTkOptionMenu(  
            self.RemoveAccountWindow, values=['ID Number [Low to High]','ID Number [High to Low]','Alphabetical [Low to High]','Alphabetical [High to Low]']
        )  
        self.FiltersDropdown.grid(row=6, column=3, pady=10)
        
    def RemoveStudents(self):
        self.UserTypeLabel.configure(text = 'Selected: Students')
        self.FetchAllStudentUsernames()
        self.SelectedListIDOrder = self.StudentsList
        self.SelectedList = self.StudentsList 
        self.AccountsDropdown = ctk.CTkOptionMenu(  
            self.RemoveAccountWindow, values=self.SelectedList
        )  
        self.AccountsDropdown.grid(row=3, column=2, pady=10)
    
    def UpdateFilter(self):
        IDOrderUsers = self.SelectedListIDOrder.copy()
        AlphabeticalOrderUsers = self.SelectedList.copy()
        self.MergeSort(AlphabeticalOrderUsers)
        IDOrderUsersReverse = IDOrderUsers.copy()
        IDOrderUsersReverse.reverse()

        AlphabeticalOrderUsersReverse = self.SelectedList.copy()
        self.MergeSortReverser(AlphabeticalOrderUsersReverse)
        AlphabeticalOrderUsersReverse.remove

        
        

        if self.FiltersDropdown.get() == ('ID Number [Low to High]'):
            self.SelectedList = IDOrderUsers
            self.AccountsDropdown.configure(values = self.SelectedList)
            
        elif self.FiltersDropdown.get() == ('ID Number [High to Low]'):
            self.SelectedList = IDOrderUsersReverse
            self.AccountsDropdown.configure(values = self.SelectedList)
            
        elif self.FiltersDropdown.get() == ('Alphabetical [Low to High]'):
            self.SelectedList = AlphabeticalOrderUsers
            self.AccountsDropdown.configure(values = self.SelectedList)

        elif self.FiltersDropdown.get() == ('Alphabetical [High to Low]'):
            self.SelectedList = AlphabeticalOrderUsersReverse
            self.AccountsDropdown.configure(values = self.SelectedList)

    def RemoveInstructors(self):
        self.UserTypeLabel.configure(text = 'Selected: Instructors')
        self.FetchAllInstructorUsernames()
        self.SelectedListIDOrder = self.InstructorsList 
        self.SelectedList = self.InstructorsList 
        self.AccountsDropdown = ctk.CTkOptionMenu(  
            self.RemoveAccountWindow, values=self.SelectedList 
        )  
        self.AccountsDropdown.grid(row=3, column=2, pady=10)

    def RemoveAdmins(self):
        self.UserTypeLabel.configure(text = 'Selected: Administrators')
        self.FetchAllAdminUsernames()
        self.SelectedListIDOrder = self.AdminsList 
        self.SelectedList = self.AdminsList  
        self.AccountsDropdown = ctk.CTkOptionMenu(  
            self.RemoveAccountWindow, values=self.SelectedList
        )  
        self.AccountsDropdown.grid(row=3, column=2, pady=10)

    def OpenConfirmAccount(self):
        if self.AccountsDropdown.get() == ("N/A"):
            tk.messagebox.showerror("Account Deletion FAILED", "Please Select a User.")
        else:

            self.ConfirmAccountWindow = ctk.CTkToplevel(self)
            self.ConfirmAccountWindow.title("Are you sure?")
            self.ConfirmAccountWindow.geometry("400x200")
            self.ConfirmAccountWindow.wm_attributes("-topmost", True)
            self.AccountToRemove = self.AccountsDropdown.get()

            # Configure grid layout
            self.ConfirmAccountWindow.rowconfigure(0, weight=1)
            self.ConfirmAccountWindow.rowconfigure(1, weight=1)
            self.ConfirmAccountWindow.rowconfigure(2, weight=1)
            self.ConfirmAccountWindow.columnconfigure(0, weight=1)
            self.ConfirmAccountWindow.columnconfigure(1, weight=1)
            self.ConfirmAccountWindow.columnconfigure(2, weight=1)

            # Confirmation message
            areyousurelabel = ctk.CTkLabel(self.ConfirmAccountWindow, text='Are you sure you want to remove this account?', anchor="center",font=(None,18))
            areyousurelabel.grid(row=0, column=0, columnspan=3, pady=20)

            # Buttons
        

            cancel = self.CreateMaterialButton(self.ConfirmAccountWindow, 'Cancel', self.CloseConfirmWindow)
            cancel.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

            confirm = self.CreateLogoutButton(self.ConfirmAccountWindow, 'Remove', self.ConfirmedRemoval)
            confirm.grid(row=1, column=2, padx=20, pady=10, sticky="ew")

    def CloseConfirmWindow(self):
            self.ConfirmAccountWindow.destroy()

    def ConfirmedRemoval(self):

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE username = ?", (self.AccountToRemove,))
        cursor.execute("DELETE FROM instructors WHERE username = ?", (self.AccountToRemove,))
        cursor.execute("DELETE FROM admins WHERE username = ?", (self.AccountToRemove,))
        conn.commit()

        self.ConfirmAccountWindow.destroy()

    ##Create account function
    def OpenCreateAccount(self):
        self.CreateAccountWindow = ctk.CTkToplevel(self)
        self.CreateAccountWindow.title("Create an Account: ")
        self.CreateAccountWindow.geometry("400x900")
        self.CreateAccountWindow.wm_attributes("-topmost", True)

        self.UsernameLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Username:")
        self.UsernameLabel.grid(row=0, column=0,pady=5)
        
        self.UsernameField = ctk.CTkEntry(self.CreateAccountWindow, width=200)
        self.UsernameField.grid(row=1, column=0,pady=5, padx=100)

        self.PasswordLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Password:")
        self.PasswordLabel.grid(row=2, column=0,pady=5)
        
        self.PasswordField = ctk.CTkEntry(self.CreateAccountWindow, width=200, show="*")
        self.PasswordField.grid(row=3, column=0,pady=5)

        self.FirstNameLabel = ctk.CTkLabel(self.CreateAccountWindow, text="First Name:")
        self.FirstNameLabel.grid(row=4, column=0,pady=5)
        
        self.FirstNameField = ctk.CTkEntry(self.CreateAccountWindow, width=200)
        self.FirstNameField.grid(row=5, column=0,pady=5, padx=100)

        self.LastNameLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Last Name:")
        self.LastNameLabel.grid(row=6, column=0,pady=5)
        
        self.LastNameField = ctk.CTkEntry(self.CreateAccountWindow, width=200)
        self.LastNameField.grid(row=7, column=0,pady=5, padx=100)

        self.EmailLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Email Address:")
        self.EmailLabel.grid(row=8, column=0,pady=5)
        
        self.EmailField = ctk.CTkEntry(self.CreateAccountWindow, width=200)
        self.EmailField.grid(row=9, column=0,pady=5)

        
        self.SexLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Sex:")  
        self.SexLabel.grid(row=10, column=0, pady=5) 
        
        
        self.SexDropdown = ctk.CTkOptionMenu(  
            self.CreateAccountWindow, values=["Male", "Female"]  
        )  
        self.SexDropdown.grid(row=11, column=0, pady=5)
        
        self.AccountTypeLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Account Type:")  
        self.AccountTypeLabel.grid(row=12, column=0, pady=5)  

        self.AccountTypeDropdown = ctk.CTkOptionMenu(  
            self.CreateAccountWindow, values=["Student", "Instructor", "Administrator"]  
        )  
        self.AccountTypeDropdown.grid(row=13, column=0, pady=5)

        self.DOBLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Date Of Birth (DD/MM/YYYY):")
        self.DOBLabel.grid(row=14, column=0,pady=5)
        
        self.DOBField = ctk.CTkEntry(self.CreateAccountWindow, width=200)
        self.DOBField.grid(row=15, column=0,pady=5)

        self.FetchAllInstructorUsernames()
        self.InstructorLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Instructor Username:")
        self.InstructorLabel.grid(row=16, column=0,pady=5)
        
        self.InstructorsDropdown = ctk.CTkOptionMenu(  
            self.CreateAccountWindow, values=self.InstructorsList  
        )  
        self.InstructorsDropdown.grid(row=17, column=0, pady=5)

        self.PostcodeLabel = ctk.CTkLabel(self.CreateAccountWindow, text="Postcode :")
        self.PostcodeLabel.grid(row=18, column=0,pady=5)
        
        self.PostcodeField = ctk.CTkEntry(self.CreateAccountWindow, width=200)
        self.PostcodeField.grid(row=19, column=0,pady=5)

        self.SignUpButton = self.CreateMaterialButton(self.CreateAccountWindow, "Create Account", self.InsertAccount)
        self.SignUpButton.grid(row=20, column=0,pady=15)

    def InsertAccount(self):
        SelectedUsername = self.UsernameField.get().lower()
        SelectedPassword = self.PasswordField.get()
        selectedfirstname = self.FirstNameField.get()
        SelectedLastname = self.LastNameField.get()
        SelectedEmail = self.EmailField.get()
        SelectedSex = self.SexDropdown.get()
        SelectedDOB = self.DOBField.get()
        SelectedInstructorUsername = self.InstructorsDropdown.get()
        SelectedPostcode = self.PostcodeField.get()
        self.SelectedAccountType = self.AccountTypeDropdown.get()   ##USE THIS TO GRAB THE DATA FROM DROPDOWN
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        ##Grab instructor id from selection:
        if SelectedInstructorUsername != ("N/A"):
            cursor.execute("""SELECT instructorid FROM instructors WHERE username = ?""", (SelectedInstructorUsername,))
            SelectedInstructorID = cursor.fetchone()[0]



        ##### Validation
        if self.ValidateEmail(SelectedEmail) == True:

            valid_email = True
            self.EmailLabel.configure(text_color = 'black', text = 'Email Address: ')
        else:
            valid_email = False
            self.EmailLabel.configure(text_color = 'red', text = 'Email Address: Please enter a valid email address.')



        if self.ValidateDob(SelectedDOB) == True:
            valid_dob = True

            self.DOBLabel.configure(text_color = 'black', text = 'Date of Birth (DD/MM/YYYY):')
        else:
            valid_dob = False

            self.DOBLabel.configure(text_color = 'red', text = 'Date of Birth (DD/MM/YYYY): Invalid, Please follow the format.')

        if self.ValidatePostcode(SelectedPostcode.upper()) == True:
            valid_postcode = True

            self.PostcodeLabel.configure(text_color = 'black', text = 'Postcode: ')
        else:
            valid_postcode = False

            self.PostcodeLabel.configure(text_color = 'red', text = 'Postcode: Please enter a valid postcode.')

        if self.ValidateNames(selectedfirstname) == True:
            valid_firstname = True

            self.FirstNameLabel.configure(text_color = 'black', text = 'First Name: ')
        else:
            valid_firstname = False

            self.FirstNameLabel.configure(text_color = 'red', text = 'First Name: Please enter a valid first name, with no digits')

        if self.ValidateNames(SelectedLastname) == True:
            valid_lastname = True

            self.LastNameLabel.configure(text_color = 'black', text = 'Last Name:')
        else:
            valid_lastname = False

            self.LastNameLabel.configure(text_color = 'red', text = 'Last Name: Please enter a valid first name, with no digits')

        if self.CheckUsernameExists(SelectedUsername) == False:
            valid_username = True

            self.UsernameLabel.configure(text_color = 'black', text = 'Username:')
            
        else:

            valid_username = False

            self.UsernameLabel.configure(text_color = 'red', text = 'Username: already exists, please choose another')

        if self.CheckEmailExists(SelectedEmail) == False:
            valid_email = True

            self.EmailLabel.configure(text_color = 'black', text = 'Email Address:')
            if self.ValidateEmail(SelectedEmail) == False:
                valid_email = False
                self.EmailLabel.configure(text_color = 'red', text = 'Email Address: Please enter a valid email address.')

        else:
            valid_email = True

            self.EmailLabel.configure(text_color = 'red', text = 'Email Address: already exists, please choose another')

        if self.SelectedAccountType == ("Student") and SelectedInstructorUsername == ("N/A"):
            valid_instructor_select = False

            self.InstructorLabel.configure(text_color = 'red', text = 'Please select an Instructor: ')
        else:
            self.InstructorLabel.configure(text_color = 'black', text = 'Instructor: ')
            valid_instructor_select = True
        

        if valid_lastname == True and valid_dob == True and valid_email == True and valid_firstname == True and valid_postcode == True and valid_instructor_select:
            hashvar = hashlib.new("SHA256")
            hashvar.update(SelectedPassword.encode())
            hashed_password = (hashvar.hexdigest())

       
        
            
            if self.SelectedAccountType == ("Student"):
                cursor.execute("""SELECT * FROM students WHERE username = ?
                                                            AND password = ?""", (SelectedUsername,hashed_password))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO students (username, password, emailaddress, accounttype, firstname, surname, dob, sex, postcode, instructorid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (SelectedUsername, hashed_password, SelectedEmail, 'student', selectedfirstname, SelectedLastname, SelectedDOB, SelectedSex, SelectedPostcode,SelectedInstructorID))
                    conn.commit()
                    tk.messagebox.showinfo("Account Created", f"Account Created!")
                    self.CreateAccountWindow.destroy() 
                else:
                    tk.messagebox.showerror("Account Creation Failed", "User already Exists.")





            if self.SelectedAccountType == ("Administrator"):
                cursor.execute("""SELECT * FROM admins WHERE username = ?
                                                            AND password = ?""", (SelectedUsername,hashed_password))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO admins (username, password, emailaddress, accounttype, firstname, surname, dob, sex, postcode,instructorid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (SelectedUsername, hashed_password, SelectedEmail, 'Administrator', selectedfirstname, SelectedLastname, SelectedDOB, SelectedSex, SelectedPostcode))
                    conn.commit()
                    tk.messagebox.showinfo("Account Created", f"Account Created!")
                    self.CreateAccountWindow.destroy() 
                else:
                    tk.messagebox.showerror("Account Creation Failed", "User already Exists.")

            if self.SelectedAccountType == ("Instructor"):
                cursor.execute("""SELECT * FROM instructors WHERE username = ?
                                                            AND password = ?""", (SelectedUsername,hashed_password))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO instructors (username, password, emailaddress, accounttype, firstname, surname, dob, sex, postcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )", (SelectedUsername, hashed_password, SelectedEmail, 'Instructor', selectedfirstname, SelectedLastname, SelectedDOB, SelectedSex, SelectedPostcode))
                    conn.commit()
                    tk.messagebox.showinfo("Account Created", f"Account Created!")
                    self.CreateAccountWindow.destroy() 
                else:
                    tk.messagebox.showerror("Account Creation Failed", "User already Exists.")
    
    #Validation Stuff
    def ValidateEmail(self,email):
        # Define the regex pattern for email validation
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        # Use re.match to check if the email matches the pattern
        if re.match(pattern, email):
            return True
        else:
            return False

    def ValidatePostcode(self,dob):
        # Define the regex pattern for postcode validation
        pattern = r'^([A-PR-UWYZ][A-HK-Y]?[0-9][0-9A-HJKMNP-Z]? ?[0-9][ABD-HJLNP-UW-Z]{2})$'
        
        # Use re.match to check if the postcode matches the pattern
        if re.match(pattern, dob):
            return True
        else:
            return False
   
    def ValidateDob(self,dob):
        # Define the regex pattern for dob validation
        pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19[0-9]{2}|20[0-2][0-9])$'
        
        # Use re.match to check if the dob matches the pattern
        if re.match(pattern, dob):
            return True
        else:
            return False

    def ValidateNames(self,name):
        # Define the regex pattern for names validation
        pattern = r'^[A-Za-z]+$'
        
        # Use re.match to check if the names matches the pattern
        if re.match(pattern, name):
            return True
        else:
            return False

    def CheckUsernameExists(self, username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()




        # Check if email exists in any of the three tables
        cursor.execute("SELECT 1 FROM students WHERE username = ? LIMIT 1", (username,))
        student = cursor.fetchone() is not None

        cursor.execute("SELECT 1 FROM admins WHERE username = ? LIMIT 1", (username,))
        admin = cursor.fetchone() is not None

        cursor.execute("SELECT 1 FROM instructors WHERE username = ? LIMIT 1", (username,))
        instructor = cursor.fetchone() is not None

        # If the email exists in ANY of the tables, return True
        return student or admin or instructor

    def CheckEmailExists(self, email):

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        # Check if email exists in any of the three tables
        cursor.execute("SELECT 1 FROM students WHERE emailaddress = ? LIMIT 1", (email,))
        student = cursor.fetchone() is not None

        cursor.execute("SELECT 1 FROM admins WHERE emailaddress = ? LIMIT 1", (email,))
        admin = cursor.fetchone() is not None

        cursor.execute("SELECT 1 FROM instructors WHERE emailaddress = ? LIMIT 1", (email,))
        instructor = cursor.fetchone() is not None

        conn.close

        # If the email exists in ANY of the tables, return True
        return student or admin or instructor

    
    ##Book A lesson
    def BookaLesson(self):
        self.FetchAllStudentUsernames()
        self.FetchAllInstructorUsernames()
        root = ctk.CTk()
        app = BookLessonApp(root,self.InstructorsList,self.StudentsList)
        root.mainloop()
    
    ##Fetching and listing usernames
    def FetchAllInstructorUsernames(self):

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM instructors WHERE accounttype = ?", ('Instructor',))
        instructor_fetch = cursor.fetchall()
        self.InstructorsList = [sublist[0] for sublist in instructor_fetch]
        self.InstructorsList.insert(0,"N/A")
        
    def FetchAllStudentUsernames(self):


        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM students WHERE accounttype = ?", ('student',))
        StudentsFetch = cursor.fetchall()
        self.StudentsList = [sublist[0] for sublist in StudentsFetch]
        self.StudentsList.insert(0,"N/A")
        
    def FetchAllAdminUsernames(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM admins WHERE accounttype = ?", ('Administrator',))
        AdminsFetch = cursor.fetchall()
        self.AdminsList = [sublist[0] for sublist in AdminsFetch]
        self.AdminsList.insert(0,"N/A")

    ##View Upcoming Lessons(All instructors)
    def OpenViewUpcomingWindow(self):
        self.ViewUpcomingWindow = ctk.CTkToplevel(self)
        self.ViewUpcomingWindow.title("View Upcoming Lessons: ")
        self.ViewUpcomingWindow.geometry("800x200")
        self.ViewUpcomingWindow.wm_attributes("-topmost", True)

        self.SelectDateButton = self.CreateMaterialButton(self.ViewUpcomingWindow, "Select Date", self.OpenCalendarWindow)
        self.SelectDateButton.grid(row=0, column=0, pady=10, padx = 10)

        self.SelectInstructorButton = self.CreateMaterialButton(self.ViewUpcomingWindow, "Select Instructor", self.SelectInstructorWindow)
        self.SelectInstructorButton.grid(row=0, column=2, pady=10, padx = 10)

        self.FetchAppointmentsButton = self.CreateMaterialButton(self.ViewUpcomingWindow, "Fetch Appointments", self.OpenAppointmentsWindow)
        self.FetchAppointmentsButton.grid(row=0, column=3, pady=10, padx = 10)

    def OpenAppointmentsWindow(self):
        self.FetchBookingsAdmin()
        root = tk.Tk()
        app = TableApp(root, self.ReturnedBookings)
        root.mainloop()

    def OpenCalendarWindow(self):
        # Create a new window for the calendar
        self.CalendarWindow = ctk.CTkToplevel(self)
        self.CalendarWindow.title("Select a Date")
        self.CalendarWindow.geometry("400x400")
        self.CalendarWindow.wm_attributes("-topmost", True)
        
        # Calendar Widget
        self.Calendar = Calendar(self.CalendarWindow, selectmode="day",
        weekendbackground="white",  
        weekendforeground="black",
        date_pattern="dd/mm/yyyy"   
        )
        self.Calendar.pack(pady=20)
        # Select Date Button
        self.SelectDateButton = ctk.CTkButton(self.CalendarWindow, text="Select Date", command=self.ReturnSelectedDate)
        self.SelectDateButton.pack(pady=10)
    
    def ReturnSelectedDate(self):
        
        
        self.SelectedDate = str(self.Calendar.get_date())
        self.SelectDateButton.configure(text = "Selected Date: "+self.SelectedDate)

    def SelectInstructorWindow(self):
        self.SelectInstructorWindow = ctk.CTkToplevel(self)
        self.SelectInstructorWindow.title("Select Instructor")
        self.SelectInstructorWindow.geometry("700x400")
        self.SelectInstructorWindow.wm_attributes("-topmost", True)

        self.FetchAllInstructorUsernames()
        self.SelectedListIDOrder = self.InstructorsList
        self.SelectedList = self.InstructorsList

        # Configure grid layout
        self.SelectInstructorWindow.columnconfigure(0, weight=1)
        self.SelectInstructorWindow.columnconfigure(1, weight=1)
        self.SelectInstructorWindow.columnconfigure(2, weight=1)

        self.SelectInstructorWindow.rowconfigure(0, weight=1)
        self.SelectInstructorWindow.rowconfigure(1, weight=1)
        self.SelectInstructorWindow.rowconfigure(2, weight=1)

        # Dropdown for instructor selection
        self.AccountsDropdown = ctk.CTkOptionMenu(self.SelectInstructorWindow, values=self.SelectedList)
        self.AccountsDropdown.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Refresh Filters/Accounts button
        updatefilter = self.CreateMaterialButton(self.SelectInstructorWindow, "Refresh Filters/Accounts", self.UpdateFilter)
        updatefilter.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        # Filters dropdown
        self.FiltersDropdown = ctk.CTkOptionMenu(
            self.SelectInstructorWindow, 
            values=[
                'ID Number [Low to High]',
                'ID Number [High to Low]',
                'Alphabetical [Low to High]',
                'Alphabetical [High to Low]'
            ]
        )
        self.FiltersDropdown.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

    # Select Instructor button
        SelectButton = self.CreateMaterialButton(self.SelectInstructorWindow, "Select Instructor", self.ReturnSelectedInstructor)
        SelectButton.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def ReturnSelectedInstructor(self):
        self.SelectedInstructor = self.AccountsDropdown.get()
        self.SelectInstructorButton.configure(text = "Selected Instructor: "+self.SelectedInstructor )

    def FetchBookingsAdmin(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        ##Use crosstable SQL to select student name and instructor name
        if self.SelectedInstructor != ("N/A"):
            cursor.execute("""SELECT instructorid FROM instructors WHERE username = ?""", (self.SelectedInstructor,))
            SelectedInstructorID = cursor.fetchone()[0]
        cursor.execute("""SELECT bookingid, date, time, 
           (SELECT username FROM students WHERE students.studentid = bookings.studentid), 
           (SELECT username FROM instructors WHERE instructors.instructorid = bookings.instructorid), 
           startpostcode, endpostcode
            FROM bookings
            WHERE date = ? AND instructorid = ?
            """, (self.SelectedDate, SelectedInstructorID))

        self.ReturnedBookings = cursor.fetchall()
        
    ###INSTRUCTOR PORTAL      
    def ShowInstructorPortal(self):
            self.StudentLoginButton.grid_forget()
            self.InstructorLoginButton.grid_forget()
            self.AdminLoginButton.grid_forget()
            self.rowconfigure(4, weight = 0)
                
            self.OpenViewRecourcesButton = self.CreateMaterialButton(self, "View Learning Recources", lambda:self.ViewLearningRecources())
            self.OpenViewRecourcesButton.grid(row=1, column=0, pady=10, padx = 10, sticky="W")
        
            self.OpenCreateFeedbackReportButton = self.CreateMaterialButton(self, "Create Feedback Report", lambda: self.InstructorViewUpcomingWindow(self.FeedbackReportWindow))
            self.OpenCreateFeedbackReportButton.grid(row=2, column=0, pady=10, padx = 10, sticky="W")
                
            self.OpenViewUpcomings = self.CreateMaterialButton(self, "View/Remove/Modify Lessons", lambda: self.InstructorViewUpcomingWindow(self.InstructorViewLessons))
            self.OpenViewUpcomings.grid(row=3, column=0, pady=10, padx = 10, sticky="W")
                
            self.OpenBookLessonManual = self.CreateMaterialButton(self, "Book a Lesson (Manual)", self.InstructorBookLesson)
            self.OpenBookLessonManual.grid(row=4, column=0, pady=10, padx = 10, sticky="W")

            self.OpenDistanceCalculatorButton = self.CreateMaterialButton(self, "Open Distance Calculator", self.DistanceCalculator)
            self.OpenDistanceCalculatorButton.grid(row=5, column=0, pady=10, padx = 10, sticky="W")

            self.SignOutButton = self.CreateLogoutButton(self, "Sign Out", self.CreateMainMenu, width=150, height=40)
            self.SignOutButton.grid(row=0, column=1, padx=10, pady=10, sticky="NE")

            IDText = "InstructorID:"+(self.InstructorID)
            self.AccountIdLabel = ctk.CTkLabel(self, text=IDText)
            self.AccountIdLabel.grid(row=5, column=1, pady=10, padx = 5, sticky="SE")

            AccountText = "Account Name: "+(self.AccountName)
            self.AccountNameLabel = ctk.CTkLabel(self, text=AccountText)
            self.AccountNameLabel.grid(row=6, column=1, pady=10, padx = 5, sticky="SE")

            AccountTypeText = "Account Type: "+(self.AccountType)
            self.AccountNameLabel = ctk.CTkLabel(self, text=AccountTypeText)
            self.AccountNameLabel.grid(row=7, column=1, pady=10, padx = 5, sticky="SE")

    def FeedbackReportWindow(self):
        self.FetchBookingsInstructor()
        root = ctk.CTk()
        FeedbackreportApp(root,self.ReturnedBookings)
        root.mainloop()
    
    def InstructorBookLesson(self):
        self.FetchAllStudentUsernames()
        self.FetchAllInstructorUsernames()
        root = ctk.CTk()
        app = InstructorBookLessonApp(root,self.InstructorsList,self.StudentsList,self.InstructorID,self.AccountName)
        root.mainloop()

    def InstructorViewUpcomingWindow(self,fetchmethod):
        self.ViewUpcomingWindow = ctk.CTkToplevel(self)
        self.ViewUpcomingWindow.title("View Upcoming Lessons")
        self.ViewUpcomingWindow.geometry("800x200")
        self.ViewUpcomingWindow.wm_attributes("-topmost", True)

        self.SelectDateButton = self.CreateMaterialButton(self.ViewUpcomingWindow, "Select Date", self.OpenCalendarWindow)
        self.SelectDateButton.grid(row=0, column=0, pady=10, padx = 10)

        self.FetchAppointmentsButton = self.CreateMaterialButton(self.ViewUpcomingWindow, "Fetch Appointments", fetchmethod)
        self.FetchAppointmentsButton.grid(row=0, column=2, pady=10, padx = 10)

    def InstructorViewLessons(self):
        self.FetchBookingsInstructor()
        
        root = tk.Tk()
        app = TableAppInstructor(root, self.ReturnedBookings)
        root.mainloop()
    
    def FetchBookingsInstructor(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        ##Use crosstable SQL to select student name and instructor name
        
        cursor.execute("""SELECT bookingid, date, time, 
           (SELECT username FROM students WHERE students.studentid = bookings.studentid), 
           (SELECT username FROM instructors WHERE instructors.instructorid = bookings.instructorid), 
           startpostcode, endpostcode
            FROM bookings
            WHERE date = ? AND instructorid = ?
            """, (self.SelectedDate, self.InstructorID))

        self.ReturnedBookings = cursor.fetchall()
        conn.commit()
        conn.close()
    
    def ViewLearningRecources(self):
        root = ctk.CTk()
        LearningRecourcesApp(root)
        root.mainloop()

    def DistanceCalculator(self):
        root = tk.Tk()
        app = ETAApp(root)
        root.mainloop()

class TableApp:
    def __init__(self, root, data):
        self.root = root
        self.root.title("View Lessons")
        self.root.geometry("900x600")
        self.root.wm_attributes("-topmost", True)

        # Create Treeview (Table)
        self.tree = ttk.Treeview(root, columns=("Column1", "Column2", "Column3","Column4",'Column5','Column6','Column7'), show="headings")
        
        # Define Column Headings
        self.tree.heading("Column1", text="BookingID")
        self.tree.heading("Column2", text="Date")
        self.tree.heading("Column3", text="Time")
        self.tree.heading("Column4", text="Student Name")
        self.tree.heading("Column5", text="Instructor Name")
        self.tree.heading("Column6", text="Starting Location")
        self.tree.heading("Column7", text="Ending Location")

        # Set Column Widths
        self.tree.column("Column1", width=100)
        self.tree.column("Column2", width=100)
        self.tree.column("Column3", width=50)
        self.tree.column("Column4", width=150)
        self.tree.column("Column5", width=150)
        self.tree.column("Column6", width=150)
        self.tree.column("Column7", width=150)

        # Pack the table
        self.tree.pack(pady=20)

        # Insert Data from the List
        self.InsertData(data)

        # Button to add more data (for testing)
        

        self.SelectButton = ctk.CTkButton(root, text="Select Appointment", command = self.RowSelected)
        self.SelectButton.pack(pady=10)

        self.SelectedLabel = ctk.CTkLabel(root,text="Selected: ")
        self.SelectedLabel.pack(pady=10)

        self.ModifyButton = ctk.CTkButton(root, text="Modify Booking (Manually)", command = self.ModifyBookingMenu)
        self.ModifyButton.pack(pady=10)

        self.RemoveButton = ctk.CTkButton(root, text="Remove Booking", command = self.RemoveBooking)
        self.RemoveButton.pack(pady=10)

        

    def InsertData(self, data_list):
        """Insert a 2D list (list of lists) into the table."""
        for row in data_list:
            self.tree.insert("", "end", values=row)

    def RemoveBooking(self):
        ##Exception handling
        try:

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE bookingid = ?", (int(self.SelectedBookingID),))
            conn.commit()
            conn.close()
            tk.messagebox.showinfo("Booking Removed", f"Remove Booking!")
            self.root.destroy()
        except:
            tk.messagebox.showerror("Failed Deletion", "Could not remove the selected booking.")
    
    

    def ModifyBookingMenu(self):
        try:
            self.ModifyBookingWindow = ctk.CTkToplevel(self.root)
            self.ModifyBookingWindow.title("Modify Booking ")
            self.ModifyBookingWindow.geometry("400x500")
            self.ModifyBookingWindow.wm_attributes("-topmost", True)


            DateLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Date:")
            DateLabel.pack()
            
            
            self.DateField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.DateField.pack()
            self.DateField.insert(0,str(self.SelectedRowDate))

            TimeLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Starting Time:")
            TimeLabel.pack()
            
            
            self.TimeField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.TimeField.pack()
            self.TimeField.insert(0,str(self.SelectedRowTime))

            
            self.StudentNameLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Student Name: ")
            self.StudentNameLabel.pack()
            
            self.StudentNameField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.StudentNameField.pack()
            self.StudentNameField.insert(0,str(self.SelectedStudentName))

            self.InstructorNameLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Instructor Name: ")
            self.InstructorNameLabel.pack()
            
            
            self.InstructorNameField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.InstructorNameField.pack()
            self.InstructorNameField.insert(0,str(self.SelectedInstructorName))

            self.StartLocationLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Starting location:")
            self.StartLocationLabel.pack()
            
            self.StartLocationField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.StartLocationField.pack()
            self.StartLocationField.insert(0,str(self.SelectedStartPostcode))

            self.EndLocationLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Ending Location:")
            self.EndLocationLabel.pack()
            
            
            self.EndLocationField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.EndLocationField.pack()
            self.EndLocationField.insert(0,str(self.SelectedEndPostcode))

            self.ModifyButton = tk.Button(self.ModifyBookingWindow, text="Modify Booking", command = self.ModifyBooking)
            self.ModifyButton.pack(pady=10)
        except:
            tk.messagebox.showerror("Couldn't Modify Booking", "Couldn't Modify Booking, Please Ensure you have selected a booking.")

    def ValidateDetails(self):
        pass
    
    def ModifyBooking(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT studentid FROM students WHERE username = ?",(str(self.StudentNameField.get()),))
            StudentID = cursor.fetchone()[0]

            cursor.execute("SELECT instructorid FROM instructors WHERE username = ?",(str(self.InstructorNameField.get()),))
            InstructorID = cursor.fetchone()[0]

            cursor.execute('''UPDATE bookings 
                            SET date = ?, time = ?, studentid = ?, instructorid = ?, startpostcode = ?, endpostcode = ? 
                            WHERE bookingid = ?''', 
                        (str(self.DateField.get()), 
                            str(self.TimeField.get()), 
                            StudentID, 
                            InstructorID, 
                            str(self.StartLocationField.get()), 
                            str(self.EndLocationField.get()), 
                            int(self.SelectedBookingID)))

            conn.commit()
            conn.close()
            self.root.destroy()
        except:
            tk.messagebox.showerror("Error", "Could Not Modify Booking.")
            


    def RowSelected(self):
        SelectedItem = self.tree.selection()
        RowData = self.tree.item(SelectedItem, "values")
        self.SelectedBookingID = RowData[0]
        self.SelectedRowDate = RowData[1]
        self.SelectedRowTime = RowData[2]
        self.SelectedStudentName = RowData[3]
        self.SelectedInstructorName = RowData[4]
        self.SelectedStartPostcode = RowData[5]
        self.SelectedEndPostcode = RowData[6]
        self.SelectedLabel.configure(text = 'Selected: '+str(RowData))
        print(self.SelectedBookingID)
        
class TableViewingApp(TableApp):
    def __init__(self,root,data):
        super().__init__(root,data)
        self.RemoveButton.pack_forget()
        self.ModifyButton.pack_forget()
        self.SelectButton.pack_forget()
        self.SelectedLabel.pack_forget()

class TableAppInstructor(TableApp):
    def __init__(self,root,data):
        super().__init__(root,data)
    
    def ModifyBookingMenu(self):
        try:
            self.ModifyBookingWindow = ctk.CTkToplevel(self.root)
            self.ModifyBookingWindow.title("Modify Booking ")
            self.ModifyBookingWindow.geometry("400x500")
            self.ModifyBookingWindow.wm_attributes("-topmost", True)


            DateLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Date:")
            DateLabel.pack()
            
            
            self.DateField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.DateField.pack()
            self.DateField.insert(0,str(self.SelectedRowDate))

            TimeLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Time:")
            TimeLabel.pack()
            
            
            self.TimeField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.TimeField.pack()
            self.TimeField.insert(0,str(self.SelectedRowTime))

            
            StudentNameLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Student Name: ")
            StudentNameLabel.pack()
            
            self.StudentNameField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.StudentNameField.pack()
            self.StudentNameField.insert(0,str(self.SelectedStudentName))

            self.InstructorNameLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Instructor Name: "+self.SelectedInstructorName)
            self.InstructorNameLabel.pack()
            
            StartLocationLabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Starting location:")
            StartLocationLabel.pack()
            
            self.StartLocationField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.StartLocationField.pack()
            self.StartLocationField.insert(0,str(self.SelectedStartPostcode))

            EndLocationlabel = ctk.CTkLabel(self.ModifyBookingWindow, text="Ending Location:")
            EndLocationlabel.pack()
            
            
            self.EndLocationField = ctk.CTkEntry(self.ModifyBookingWindow, width=200)
            self.EndLocationField.pack()
            self.EndLocationField.insert(0,str(self.SelectedEndPostcode))

            self.ModifyButton = tk.Button(self.ModifyBookingWindow, text="Modify Booking", command = self.ModifyBooking)
            self.ModifyButton.pack(pady=10)
        except:
            tk.messagebox.showerror("Couldn't Modify Booking", "Couldn't Modify Booking, Please Ensure you have selected a booking.")

    def ModifyBooking(self):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT studentid FROM students WHERE username = ?",(str(self.StudentNameField.get()),))
            StudentID = cursor.fetchone()[0]

            cursor.execute("SELECT instructorid FROM instructors WHERE username = ?",(str(self.SelectedInstructorName),))
            InstructorID = cursor.fetchone()[0]

            cursor.execute('''UPDATE bookings 
                            SET date = ?, time = ?, studentid = ?, instructorid = ?, startpostcode = ?, endpostcode = ? 
                            WHERE bookingid = ?''', 
                        (str(self.DateField.get()), 
                            str(self.TimeField.get()), 
                            StudentID, 
                            InstructorID, 
                            str(self.StartLocationField.get()), 
                            str(self.EndLocationField.get()), 
                            int(self.SelectedBookingID)))

            conn.commit()
            conn.close()
            self.root.destroy()
        except:
            tk.messagebox.showerror("Error", "Could Not Modify Booking.")

class BookLessonApp:
        def __init__(self, root,InstructorList,StudentList):
            self.root = root
            self.Instructor = InstructorList
            self.StudentList = StudentList
            self.root.title("Book Lesson")
            self.root.geometry("600x600")
            self.Calendar = Calendar(root, selectmode="day",
            weekendbackground="white",  
            weekendforeground="black",
            date_pattern="dd/mm/yyyy"   
            )
            self.Calendar.pack(pady=20)
            # Select Date Button
            self.DateSelectLabel = ctk.CTkLabel(root,text="Date Selected:")
            self.DateSelectLabel.pack()
            self.SelectDateLabel = ctk.CTkButton(root, text="Select Date", command=self.ReturnDate)
            self.SelectDateLabel.pack(pady=10)

            self.hour10 = ctk.CTkButton(root, text="10:00 - 11:00",command = lambda:self.BookingDetailsMenu('10:00'))
            self.hour11 = ctk.CTkButton(root, text="11:20 - 12:20",command = lambda:self.BookingDetailsMenu('11:20'))
            self.hour12 = ctk.CTkButton(root, text="12:40 - 13:40",command = lambda:self.BookingDetailsMenu('12:40'))
            self.hour13 = ctk.CTkButton(root, text="14:00 - 15:00",command = lambda:self.BookingDetailsMenu('14:00'))
            self.hour14 = ctk.CTkButton(root, text="15:20 - 16:20",command = lambda:self.BookingDetailsMenu('15:20'))
            self.hour15 = ctk.CTkButton(root, text="16:40 - 17:40",command = lambda:self.BookingDetailsMenu('16:40'))
            
        def ReturnDate(self):
            self.SelectedDate = self.Calendar.get_date()
            self.DateSelectLabel.configure(text = "Date Selected:"+str(self.SelectedDate))
            self.CheckSlotsBooked()
            self.RefreshSlots()
        
        def CheckSlotsBooked(self):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute('''SELECT time FROM bookings WHERE date = ?''', (self.SelectedDate,))
            TimesFetch = cursor.fetchall()
            self.TimesList = [sublist[0] for sublist in TimesFetch]
            print(self.TimesList)
            conn.close
        def PackSlots(self):
            self.hour10.pack(pady = 10)
            self.hour11.pack(pady = 10)
            self.hour12.pack(pady = 10)
            self.hour13.pack(pady = 10)
            self.hour14.pack(pady = 10)
            self.hour15.pack(pady = 10)
            

        def UnpackSlots(self):
            self.hour10.pack_forget()
            self.hour11.pack_forget()
            self.hour12.pack_forget()
            self.hour13.pack_forget()
            self.hour14.pack_forget()
            self.hour15.pack_forget()
            
        def RefreshSlots(self):
            self.UnpackSlots()
            self.PackSlots()
            if '10:00' in self.TimesList:
                self.hour10.pack_forget()
            if '11:20' in self.TimesList:
                self.hour11.pack_forget()
            if '12:40' in self.TimesList:
                self.hour12.pack_forget()
            if '14:00' in self.TimesList:
                self.hour13.pack_forget()
            if '15:20' in self.TimesList:
                self.hour14.pack_forget()
            if '16:40' in self.TimesList:
                self.hour15.pack_forget()
            
        
        def BookingDetailsMenu(self,Time):
            self.TimeSelected = Time
            self.BookingWindow = ctk.CTkToplevel(self.root)
            self.BookingWindow.title("Enter Booking Details")
            self.BookingWindow.geometry("400x500")
            self.BookingWindow.wm_attributes("-topmost", True)




            
            self.StudentNameLabel = ctk.CTkLabel(self.BookingWindow, text="Student Name: ")
            self.StudentNameLabel.pack()
            
            self.StudentDropdown = ctk.CTkOptionMenu(self.BookingWindow, values=self.StudentList)
            self.StudentDropdown.pack()

            self.InstructorNameLabel = ctk.CTkLabel(self.BookingWindow, text="Instructor Name: ")
            self.InstructorNameLabel.pack()
            
            self.InstructorDropdown = ctk.CTkOptionMenu(self.BookingWindow, values=self.Instructor)
            self.InstructorDropdown.pack()

            self.StartLocationLabel = ctk.CTkLabel(self.BookingWindow, text="Starting location:")
            self.StartLocationLabel.pack()
            
            self.StartLocationField = ctk.CTkEntry(self.BookingWindow, width=200)
            self.StartLocationField.pack()
            

            self.EndLocationLabel = ctk.CTkLabel(self.BookingWindow, text="Ending Location:")
            self.EndLocationLabel.pack()
            
            
            self.EndLocationField = ctk.CTkEntry(self.BookingWindow, width=200)
            self.EndLocationField.pack()
           

            self.BookButton = ctk.CTkButton(self.BookingWindow, text="Book Appointment", command = self.ValidateBookingDetails)
            self.BookButton.pack(pady=10)

        def ValidateBookingDetails(self):
            StartPostcodeValid = False
            EndPostcodeValid = False
            if self.ValidatePostcode(self.StartLocationField.get()) == False:
                self.StartLocationLabel.configure(text = 'Starting Location: Please Enter a Valid UK Postcode')
            else:
                StartPostcodeValid = True
            
            if self.ValidatePostcode(self.EndLocationField.get()) == False:
                self.EndLocationLabel.configure(text = 'Ending Location: Please Enter a Valid UK Postcode')
            else:
                EndPostcodeValid = True
            
            if EndPostcodeValid and StartPostcodeValid:
                self.BookAppointment()

        
        def BookAppointment(self):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            StudentUsername = self.StudentDropdown.get()
            InstructorUsername = self.InstructorDropdown.get()
            cursor.execute('''SELECT studentid FROM students WHERE username = ?''', (StudentUsername,))
            SelectedStudentID = cursor.fetchone()
            if SelectedStudentID:
                SelectedStudentID = SelectedStudentID[0]

            cursor.execute('''SELECT instructorid FROM instructors WHERE username = ?''', (InstructorUsername,))
            SelectedInstructorID = cursor.fetchone()
            if SelectedInstructorID:
                SelectedInstructorID = SelectedInstructorID[0]
            cursor.execute("INSERT INTO bookings (date,time,studentid,instructorid,startpostcode,endpostcode) VALUES (?, ?, ?, ?, ?, ?)", (self.SelectedDate,self.TimeSelected,SelectedStudentID,SelectedInstructorID,self.StartLocationField.get(),self.EndLocationField.get()))
            tk.messagebox.showinfo("Booking Created", f"Booking Created!")
            self.BookingWindow.destroy()

            conn.commit()
            conn.close()
            
            self.CheckSlotsBooked()
            self.RefreshSlots()

        def ValidatePostcode(self,dob):
            # Define the regex pattern for email validation
            pattern = r'^([A-PR-UWYZ][A-HK-Y]?[0-9][0-9A-HJKMNP-Z]? ?[0-9][ABD-HJLNP-UW-Z]{2})$'
            
            # Use re.match to check if the email matches the pattern
            if re.match(pattern, dob):
                return True
            else:
                return False
      
class InstructorBookLessonApp(BookLessonApp):
        def __init__(self, root,InstructorList,StudentList,InstructorID,InstructorName):
            self.InstructorID = InstructorID
            self.InstructorName = InstructorName
            super().__init__(root,InstructorList,StudentList)

        def BookingDetailsMenu(self,time):
            self.TimeSelected = time
            self.BookingWindow = ctk.CTkToplevel(self.root)
            self.BookingWindow.title("Enter Booking Details")
            self.BookingWindow.geometry("400x500")
            self.BookingWindow.wm_attributes("-topmost", True)

            self.StudentNameLabel = ctk.CTkLabel(self.BookingWindow, text="Student Name: ")
            self.StudentNameLabel.pack()
            
            self.StudentDropdown = ctk.CTkOptionMenu(self.BookingWindow, values=self.StudentList)
            self.StudentDropdown.pack()

            self.InstructorNameLabel = ctk.CTkLabel(self.BookingWindow, text="Instructor Name: "+self.InstructorName)
            self.InstructorNameLabel.pack()

            self.StartLocationLabel = ctk.CTkLabel(self.BookingWindow, text="Starting location:")
            self.StartLocationLabel.pack()
            
            self.StartLocationField = ctk.CTkEntry(self.BookingWindow, width=200)
            self.StartLocationField.pack()
            

            self.EndLocationLabel = ctk.CTkLabel(self.BookingWindow, text="Ending Location:")
            self.EndLocationLabel.pack()
            
            
            self.EndLocationField = ctk.CTkEntry(self.BookingWindow, width=200)
            self.EndLocationField.pack()
           

            self.BookButton = ctk.CTkButton(self.BookingWindow, text="Book Appointment", command = self.ValidateBookingDetails)
            self.BookButton.pack(pady=10)

        def BookAppointment(self):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            StudentUsername = self.StudentDropdown.get()
            cursor.execute('''SELECT studentid FROM students WHERE username = ?''', (StudentUsername,))
            SelectedStudentID = cursor.fetchone()
            if SelectedStudentID:
                SelectedStudentID = SelectedStudentID[0]

            
            cursor.execute("INSERT INTO bookings (date,time,studentid,instructorid,startpostcode,endpostcode) VALUES (?, ?, ?, ?, ?, ?)", (self.SelectedDate,self.TimeSelected,SelectedStudentID,self.InstructorID,self.StartLocationField.get(),self.EndLocationField.get()))
            tk.messagebox.showinfo("Booking Created", f"Booking Created!")
            self.BookingWindow.destroy()

            conn.commit()
            conn.close()
            
            self.CheckSlotsBooked()
            self.RefreshSlots()

class StudentBookLessonApp(BookLessonApp):
    def __init__(self, root,InstructorList,StudentList,InstructorID,InstructorName,StudentName,StudentID):
            self.InstructorID = InstructorID
            self.InstructorName = InstructorName
            self.StudentName = StudentName
            self.StudentID = StudentID
            super().__init__(root,InstructorList,StudentList)
            self.SelectDateLabel.configure(text = "Search Appointments")
            self.StartingPostcodeLabel = ctk.CTkLabel(root, text = 'Starting Postcode:')
            self.StartingPostcodeField = ctk.CTkEntry(root)
            self.EndingPostcodeLabel = ctk.CTkLabel(root, text = 'Ending Postcode:')
            self.EndingPostcodeField = ctk.CTkEntry(root)
            self.StartingPostcodeLabel.pack()
            self.StartingPostcodeField.pack()
            self.EndingPostcodeLabel.pack()
            self.EndingPostcodeField.pack()

    def BookingDetailsMenu(self,Time):
        self.TimeSelected = Time
        self.BookingWindow = ctk.CTkToplevel(self.root)
        self.BookingWindow.title("Enter Booking Details")
        self.BookingWindow.geometry("400x500")
        self.BookingWindow.wm_attributes("-topmost", True)

        self.StudentNameLabel = ctk.CTkLabel(self.BookingWindow, text="Student Name: "+self.StudentName)
        self.StudentNameLabel.pack()
        
        self.InstructorNameLabel = ctk.CTkLabel(self.BookingWindow, text="Instructor Name: "+self.InstructorName)
        self.InstructorNameLabel.pack()

        self.StartLocationLabel = ctk.CTkLabel(self.BookingWindow, text="Starting location:")
        self.StartLocationLabel.pack()
        
        self.StartLocationField = ctk.CTkEntry(self.BookingWindow, width=200)
        self.StartLocationField.pack()
        

        self.EndLocationLabel = ctk.CTkLabel(self.BookingWindow, text="Ending Location:")
        self.EndLocationLabel.pack()
        
        
        self.EndLocationField = ctk.CTkEntry(self.BookingWindow, width=200)
        self.EndLocationField.pack()
        

        self.BookButton = ctk.CTkButton(self.BookingWindow, text="Book Appointment", command = self.ValidateBookingDetails)
        self.BookButton.pack(pady=10)

    def BookAppointment(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT studentid FROM students WHERE username = ?''', (self.StudentName,))
        SelectedStudentID = cursor.fetchone()
        SelectedStudentID = SelectedStudentID[0]

        
        cursor.execute("INSERT INTO bookings (date,time,studentid,instructorid,startpostcode,endpostcode) VALUES (?, ?, ?, ?, ?, ?)", (self.SelectedDate,self.TimeSelected,SelectedStudentID,self.InstructorID,self.StartLocationField.get(),self.EndLocationField.get()))
        tk.messagebox.showinfo("Booking Created", f"Booking Created!")
        self.BookingWindow.destroy()

        conn.commit()
        conn.close()
        
        self.CheckSlotsBooked()
        self.RefreshSlots()

    def ReturnDate(self):
        self.StartingPostcodeField.get()
        self.EndingPostcodeField.get()
        self.StartingPostcodeLabel.configure(text = 'Selected Starting Postcode: '+self.StartingPostcodeField.get())
        self.EndingPostcodeLabel.configure(text = 'Selected Ending Postcode: '+self.EndingPostcodeField.get())
        self.SelectedDate = self.Calendar.get_date()
        self.DateSelectLabel.configure(text = "Date Selected:"+str(self.SelectedDate))
        self.CheckSlotsBooked()
        self.GetAllPostcodes()
        self.RefreshSlots()
        self.ReturnSlotsLocation()

    def GetAllPostcodes(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT startpostcode FROM bookings WHERE date = ?''', (self.SelectedDate,))
        StartPostcodeFetch = cursor.fetchall()
        self.StartPostcodesList = [sublist[0] for sublist in StartPostcodeFetch]

        cursor.execute('''SELECT endpostcode FROM bookings WHERE date = ?''', (self.SelectedDate,))
        EndPostcodesFetch = cursor.fetchall()
        self.EndPostcodesList = [sublist[0] for sublist in EndPostcodesFetch]

        print(EndPostcodesFetch)
        conn.close
    
    def ReturnSlotsLocation(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        ETAapp = ETAcomparer()
        if '10:00' not in self.TimesList:
            pass
        if '11:20' not in self.TimesList:
            StartClear = False
            EndClear = False
            if '10:00' not in self.TimesList:
                StartClear = True
            else:
                cursor.execute('''SELECT endpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'10:00'))
                PostCodeBefore = cursor.fetchone()[0]
                if ETAapp.CalculateETA(PostCodeBefore,self.StartingPostcodeField.get()) > 20:
                    StartClear = False
                else:
                    StartClear = True

            if '12:40' not in self.TimesList:
                EndClear = True
            else:
                cursor.execute('''SELECT startpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'12:40'))
                PostCodeAfter = cursor.fetchone()[0]
                if (ETAapp.CalculateETA(PostCodeAfter,self.EndingPostcodeField.get())) > 20:
                    EndClear = False
                else:
                    EndClear = True
            
            if StartClear and EndClear:
                print('cleared')
            else:
                self.hour11.pack_forget()

        if '12:40' not in self.TimesList:
            StartClear = False
            EndClear = False
            if '11:20' not in self.TimesList:
                StartClear = True
            else:
                cursor.execute('''SELECT endpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'11:20'))
                PostCodeBefore = cursor.fetchone()[0]
                if ETAapp.CalculateETA(PostCodeBefore,self.StartingPostcodeField.get()) > 20:
                    StartClear = False
                else:
                    StartClear = True

            if '14:00' not in self.TimesList:
                EndClear = True
            else:
                cursor.execute('''SELECT startpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'14:00'))
                PostCodeAfter = cursor.fetchone()[0]
                if (ETAapp.CalculateETA(PostCodeAfter,self.EndingPostcodeField.get())) > 20:
                    EndClear = False
                else:
                    EndClear = True
            
            if StartClear and EndClear:
                print('cleared')
            else:
                self.hour12.pack_forget()


        if '14:00' not in self.TimesList:
            StartClear = False
            EndClear = False
            if '12:40' not in self.TimesList:
                StartClear = True
            else:
                cursor.execute('''SELECT endpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'12:40'))
                PostCodeBefore = cursor.fetchone()[0]
                if ETAapp.CalculateETA(PostCodeBefore,self.StartingPostcodeField.get()) > 20:
                    StartClear = False
                else:
                    StartClear = True

            if '15:20' not in self.TimesList:
                EndClear = True
            else:
                cursor.execute('''SELECT startpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'15:20'))
                PostCodeAfter = cursor.fetchone()[0]
                if (ETAapp.CalculateETA(PostCodeAfter,self.EndingPostcodeField.get())) > 20:
                    EndClear = False
                else:
                    EndClear = True
            
            if StartClear and EndClear:
                print('cleared')
            else:
                self.hour13.pack_forget()
        
        if '15:20' not in self.TimesList:
            StartClear = False
            EndClear = False
            if '14:00' not in self.TimesList:
                StartClear = True
            else:
                cursor.execute('''SELECT endpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'14:00'))
                PostCodeBefore = cursor.fetchone()[0]
                if ETAapp.CalculateETA(PostCodeBefore,self.StartingPostcodeField.get()) > 20:
                    StartClear = False
                else:
                    StartClear = True

            if '16:40' not in self.TimesList:
                EndClear = True
            else:
                cursor.execute('''SELECT startpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'16:40'))
                PostCodeAfter = cursor.fetchone()[0]
                if (ETAapp.CalculateETA(PostCodeAfter,self.EndingPostcodeField.get())) > 20:
                    EndClear = False
                else:
                    EndClear = True
            
            if StartClear and EndClear:
                print('cleared')
            else:
                self.hour14.pack_forget()
        if '16:40' not in self.TimesList:
            StartClear = False
            EndClear = False
            if '15:20' not in self.TimesList:
                StartClear = True
            else:
                cursor.execute('''SELECT endpostcode FROM bookings WHERE date = ? AND time = ?''', (self.SelectedDate,'15:20'))
                PostCodeBefore = cursor.fetchone()[0]
                if ETAapp.CalculateETA(PostCodeBefore,self.StartingPostcodeField.get()) > 20:
                    StartClear = False
                else:
                    StartClear = True

            
            PostCodeAfter = 'LE2 2HL'
            if (ETAapp.CalculateETA(PostCodeAfter,self.EndingPostcodeField.get())) > 30:
                EndClear = False
            else:
                EndClear = True
            
            if StartClear and EndClear:
                print('cleared')
            else:
                self.hour15.pack_forget()

class changepassword(MainWindow):
    def __init__(self,Main):
        self.MainWindow = Main
        self.ChangePassword()
        
    def ChangePassword(self):
        
        self.Verified = False

        self.ChangePasswordWindow = ctk.CTkToplevel(self.MainWindow)
        self.ChangePasswordWindow.title("Change password")
        self.ChangePasswordWindow.geometry("400x300")
        self.ChangePasswordWindow.wm_attributes("-topmost", True)

        EmailLabel = ctk.CTkLabel(self.ChangePasswordWindow, text="Enter Email Address:")
        EmailLabel.grid(row=0, column=0,pady=5)
        
        self.EmailField = ctk.CTkEntry(self.ChangePasswordWindow, width=200)
        self.EmailField.grid(row=1, column=0,pady=5, padx=100)

        AccountTypeLabel = ctk.CTkLabel(self.ChangePasswordWindow, text="Select Account Type:")
        AccountTypeLabel.grid(row=2, column=0,pady=5)

        self.AccountTypeDropdown = ctk.CTkOptionMenu(  
            self.ChangePasswordWindow, values=["Student", "Instructor", "Administrator"]  
        )  
        self.AccountTypeDropdown.grid(row=3, column=0, pady=5)

        
        ConfirmAccount = self.CreateMaterialButton(self.ChangePasswordWindow, "Confirm", self.EmailValidation)
        ConfirmAccount.grid(row=20, column=0,pady=15)
    
    def EmailValidation(self):
        if self.ValidateEmail(self.EmailField.get()) == False:
            tk.messagebox.showinfo("Invalid Email", f"Enter a Valid Email Address.")
        elif self.CheckEmailExists(self.EmailField.get()) == False:
            tk.messagebox.showinfo("Invalid Email", f"Email Address doesn't exist.")
        else:
            self.SelectAccount()

    def SelectAccount(self):
        self.CodeLabel = ctk.CTkLabel(self.ChangePasswordWindow, text="Enter Verification Code:")
        self.CodeField = ctk.CTkEntry(self.ChangePasswordWindow, width=200)
        self.ConfirmCode = self.CreateMaterialButton(self.ChangePasswordWindow, "Confirm Code", self.NewPassword)


        self.RecieverEmail = self.EmailField.get()
        self.UserType = self.AccountTypeDropdown.get()

        for widget in self.ChangePasswordWindow.winfo_children():
            widget.grid_forget()   
            widget.pack_forget()   
            widget.place_forget()

    
        self.CodeLabel.grid(row=0, column=0,pady=5)
        self.CodeField.grid(row=1, column=0,pady=5, padx=100)
        self.ConfirmCode.grid(row=2, column=0,pady=5, padx=100)

        self.OTP = ""
        for i in range(6):
            self.OTP += str(random.randint(0,9))
        print(self.OTP)
        
        EmailServer = smtplib.SMTP('smtp.gmail.com',587)
        EmailServer.starttls()

        SenderMail = 'drivinginstructorbookingsystem@gmail.com'
        EmailServer.login(SenderMail,'kuar srwu bzxp mtxa')

    

        ResetMsg = EmailMessage()
        ResetMsg['Subject'] = "Change Password Verification Code"
        ResetMsg['From'] = SenderMail
        ResetMsg['To'] = self.RecieverEmail
        ResetMsg.set_content("Your Verification Code is: "+self.OTP)
        EmailServer.send_message(ResetMsg)

    def NewPassword(self):
        if self.CodeField.get() == self.OTP:
            print("self.verified")
            self.Verified = True
            tk.messagebox.showinfo("Verified", f"User Verified!")
        else:
            tk.messagebox.showerror("Failed Verification", "Verification Failed! Please check and try again.")

        self.UserType = self.AccountTypeDropdown.get()
        if self.Verified == True:
            for widget in self.ChangePasswordWindow.winfo_children():
                widget.grid_forget()   
                widget.pack_forget()   
                widget.place_forget()
            self.NewPassLabel = ctk.CTkLabel(self.ChangePasswordWindow, text="Enter New Password:")
            self.NewPassLabel.grid(row=1, column=0,pady=5, padx=100)
            self.NewPassEntry = ctk.CTkEntry(self.ChangePasswordWindow, width=200)
            self.NewPassEntry.grid(row=2, column=0,pady=5, padx=100)
            ConfirmCode = self.CreateMaterialButton(self.ChangePasswordWindow, "Confirm Code", self.SetNewPassword)
            ConfirmCode.grid(row=3, column=0,pady=5, padx=100)
        
    def SetNewPassword(self):
        ChangedPassword = self.NewPassEntry.get()
        HashVar = hashlib.new("SHA256")
        HashVar.update(ChangedPassword.encode())
        HashedPassword = (HashVar.hexdigest())

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()

                if self.UserType == 'Student' and self.Verified:
                    cursor.execute('''UPDATE students SET password = ? WHERE emailaddress = ?''', (HashedPassword, self.RecieverEmail))
                    tk.messagebox.showinfo("Student Password Changed", "Password Changed Successfully!")

                elif self.UserType == 'Instructor' and self.Verified:
                    cursor.execute('''UPDATE instructors SET password = ? WHERE emailaddress = ?''', (HashedPassword, self.RecieverEmail))
                    tk.messagebox.showinfo("Instructor Password Changed", "Password Changed Successfully!")

                elif self.UserType == 'Administrator' and self.Verified:
                    cursor.execute('''UPDATE admins SET password = ? WHERE emailaddress = ?''', (HashedPassword, self.RecieverEmail))
                    tk.messagebox.showinfo("Administrator Password Changed", "Password Changed Successfully!")

                conn.commit()

        except sqlite3.Error as e:
            tk.messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            self.ChangePasswordWindow.destroy()

class FeedbackreportApp():
    def __init__(self,root,data):
        self.root = root
        self.data = data
        self.root.title("Create Feedback Report")
        self.root.geometry("1200x900")
        
        
        
        #####Manoevures
        manoeuvreslabel = ctk.CTkLabel(root, text="Manoeuvres:",font=(None,18))
        manoeuvreslabel.grid(row=0, column=0,pady=3)

        self.acctype_dropdown = ctk.CTkOptionMenu(  
            root, values=["Reverse/Right", "Reverse Park(Road)", "Reverse Park (car park)", "Forward Park"]
        )  
        self.acctype_dropdown.grid(row=1, column=1, pady=3)

        manoeuvrescontrol = ctk.CTkLabel(root, text="Control:")
        manoeuvrescontrol.grid(row=2, column=0,pady=3)

        self.mano_control_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.mano_control_sfault.grid(row=2, column=1,pady=3)
        self.mano_control_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.mano_control_dfault.grid(row=2, column=2,pady=3)

        manoeuvresobservation = ctk.CTkLabel(root, text="Observation:",)
        manoeuvresobservation.grid(row=3, column=0,pady=3)

        self.mano_obs_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.mano_obs_sfault.grid(row=3, column=1,pady=3)
        self.mano_obs_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.mano_obs_dfault.grid(row=3, column=2,pady=3)

        ####Show Me tell me
        showtelllabel = ctk.CTkLabel(root, text="Show Me/Tell Me:", font=(None,18))
        showtelllabel.grid(row=4, column=0,pady=3)

        self.showtell_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.showtell_sfault.grid(row=5, column=1,pady=3)
        self.showtell_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.showtell_dfault.grid(row=5, column=2,pady=3)

        ##Controlled Stop
        controlstoplabel = ctk.CTkLabel(root, text="Controlled Stop:",font=(None,18))
        controlstoplabel.grid(row=6, column=0,pady=3)

        self.controlstop_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.controlstop_sfault.grid(row=7, column=1,pady=3)
        self.controlstop_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.controlstop_dfault.grid(row=7, column=2,pady=3)

        ##Control
        controllabel = ctk.CTkLabel(root, text="Control:",font=(None,18))
        controllabel.grid(row=8, column=0,pady=3)

        acceleratorlabel = ctk.CTkLabel(root, text="Accelerator:",font=(None,14))
        acceleratorlabel.grid(row=9, column=0,pady=3)

        self.accelerator_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.accelerator_sfault.grid(row=9, column=1,pady=3)
        self.accelerator_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.accelerator_dfault.grid(row=9, column=2,pady=3)

        clutchlabel = ctk.CTkLabel(root, text="Clutch:",font=(None,14))
        clutchlabel.grid(row=10, column=0,pady=3)

        self.clutch_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.clutch_sfault.grid(row=10, column=1,pady=3)
        self.clutch_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.clutch_dfault.grid(row=10, column=2,pady=3)

        gearslabel = ctk.CTkLabel(root, text="Gears:",font=(None,14))
        gearslabel.grid(row=11, column=0,pady=3)

        self.gears_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.gears_sfault.grid(row=11, column=1,pady=3)
        self.gears_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.gears_dfault.grid(row=11, column=2,pady=3)



        footbrakelabel = ctk.CTkLabel(root, text="Footbrake:",font=(None,14))
        footbrakelabel.grid(row=12, column=0,pady=3)

        self.footbrake_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.footbrake_sfault.grid(row=12, column=1,pady=3)
        self.footbrake_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.footbrake_dfault.grid(row=12,column=2,pady=3)

        parkbrakelabel = ctk.CTkLabel(root, text="Parking Brake:",font=(None,14))
        parkbrakelabel.grid(row=13, column=0,pady=3)

        self.parkbrake_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.parkbrake_sfault.grid(row=13, column=1,pady=3)
        self.parkbrake_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.parkbrake_dfault.grid(row=13, column=2,pady=3)

        steeringlabel = ctk.CTkLabel(root, text="Steering:",font=(None,14))
        steeringlabel.grid(row=14, column=0,pady=3)

        self.steering_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.steering_sfault.grid(row=14, column=1,pady=3)
        self.steering_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.steering_dfault.grid(row=14, column=2,pady=3)

        precautionslabel = ctk.CTkLabel(root, text="Precautions:",font=(None,14))
        precautionslabel.grid(row=15, column=0,pady=3)

        self.precautions_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.precautions_sfault.grid(row=15, column=1,pady=3)
        self.precautions_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.precautions_dfault.grid(row=15, column=2,pady=3)

        ancillarycontrolslabel = ctk.CTkLabel(root, text="ancillarycontrols:",font=(None,14))
        ancillarycontrolslabel.grid(row=16, column=0,pady=3)

        self.ancillarycontrols_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.ancillarycontrols_sfault.grid(row=16, column=1,pady=3)
        self.ancillarycontrols_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.ancillarycontrols_dfault.grid(row=16, column=2,pady=3)

        ##Move Off
        moveofflabel = ctk.CTkLabel(root, text="Move Off:",font=(None,18))
        moveofflabel.grid(row=0, column=3,pady=3)

        safetylabel = ctk.CTkLabel(root, text="Safety:",font=(None,14))
        safetylabel.grid(row=1, column=3,pady=3)
        self.safety_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.safety_sfault.grid(row=1, column=4,pady=3)
        self.safety_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.safety_dfault.grid(row=1, column=5,pady=3)

        controllabel = ctk.CTkLabel(root, text="Control:",font=(None,14))
        controllabel.grid(row=2, column=3,pady=3)
        self.control_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.control_sfault.grid(row=2, column=4,pady=3)
        self.control_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.control_dfault.grid(row=2, column=5,pady=3)

        ##UseOfMirrors
        useofmirrorslabel = ctk.CTkLabel(root, text="Use of Mirrors:",font=(None,18))
        useofmirrorslabel.grid(row=3, column=3,pady=3)

        signallinglabel = ctk.CTkLabel(root, text="Signalling:",font=(None,14))
        signallinglabel.grid(row=4, column=3,pady=3)
        self.signalling_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.signalling_sfault.grid(row=4, column=4,pady=3)
        self.signalling_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.signalling_dfault.grid(row=4, column=5,pady=3)

        changedirectionlabel = ctk.CTkLabel(root, text="Change Direction:",font=(None,14))
        changedirectionlabel.grid(row=5, column=3,pady=3)
        self.changedirection_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.changedirection_sfault.grid(row=5, column=4,pady=3)
        self.changedirection_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.changedirection_dfault.grid(row=5, column=5,pady=3)

        changespeedlabel = ctk.CTkLabel(root, text="Change Speed:",font=(None,14))
        changespeedlabel.grid(row=6, column=3,pady=3)
        self.changespeed_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.changespeed_sfault.grid(row=6, column=4,pady=3)
        self.changespeed_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.changespeed_dfault.grid(row=6, column=5,pady=3)

        ##Signals
        Signalslabel = ctk.CTkLabel(root, text="Signals:",font=(None,18))
        Signalslabel.grid(row=7, column=3,pady=3)

        neccesarylabel = ctk.CTkLabel(root, text="Neccesary:",font=(None,14))
        neccesarylabel.grid(row=8, column=3,pady=3)
        self.neccesary_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.neccesary_sfault.grid(row=8, column=4,pady=3)
        self.neccesary_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.neccesary_dfault.grid(row=8, column=5,pady=3)

        correctlylabel = ctk.CTkLabel(root, text="Correctly:",font=(None,14))
        correctlylabel.grid(row=9, column=3,pady=3)
        self.correctly_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.correctly_sfault.grid(row=9, column=4,pady=3)
        self.correctly_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.correctly_dfault.grid(row=9, column=5,pady=3)

        timedlabel = ctk.CTkLabel(root, text="Timed:",font=(None,14))
        timedlabel.grid(row=10, column=3,pady=3)
        self.timed_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.timed_sfault.grid(row=10, column=4,pady=3)
        self.timed_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.timed_dfault.grid(row=10, column=5,pady=3)

        ##Junctions
        junctionslabel = ctk.CTkLabel(root, text="Junctions:",font=(None,18))
        junctionslabel.grid(row=11, column=3,pady=3)

        approachspeedlabel = ctk.CTkLabel(root, text="Approach Speed:",font=(None,14))
        approachspeedlabel.grid(row=12, column=3,pady=3)
        self.approachspeed_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.approachspeed_sfault.grid(row=12, column=4,pady=3)
        self.approachspeed_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.approachspeed_dfault.grid(row=12, column=5,pady=3)

        observationlabel = ctk.CTkLabel(root, text="Observation:",font=(None,14))
        observationlabel.grid(row=13, column=3,pady=3)
        self.observation_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.observation_sfault.grid(row=13, column=4,pady=3)
        self.observation_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.observation_dfault.grid(row=13, column=5,pady=3)

        turningrightlabel = ctk.CTkLabel(root, text="Turning Right:",font=(None,14))
        turningrightlabel.grid(row=14, column=3,pady=3)
        self.turningright_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.turningright_sfault.grid(row=14, column=4,pady=3)
        self.turningright_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.turningright_dfault.grid(row=14, column=5,pady=3)

        turningleftlabel = ctk.CTkLabel(root, text="Turning Left:",font=(None,14))
        turningleftlabel.grid(row=15, column=3,pady=3)
        self.turningleft_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.turningleft_sfault.grid(row=15, column=4,pady=3)
        self.turningleft_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.turningleft_dfault.grid(row=15, column=5,pady=3)

        cuttingcornerslabel = ctk.CTkLabel(root, text="Cutting Corners:",font=(None,14))
        cuttingcornerslabel.grid(row=16, column=3,pady=3)
        self.cuttingcorners_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.cuttingcorners_sfault.grid(row=16, column=4,pady=3)
        self.cuttingcorners_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.cuttingcorners_dfault.grid(row=16, column=5,pady=3)

        ##Judgement
        judgementlabel = ctk.CTkLabel(root, text="Judgement:",font=(None,18))
        judgementlabel.grid(row=17, column=3,pady=3)

        overtakinglabel = ctk.CTkLabel(root, text="Overtaking:",font=(None,14))
        overtakinglabel.grid(row=18, column=3,pady=3)
        self.overtaking_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.overtaking_sfault.grid(row=18, column=4,pady=3)
        self.overtaking_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.overtaking_dfault.grid(row=18, column=5,pady=3)

        meetinglabel = ctk.CTkLabel(root, text="Meeting:",font=(None,14))
        meetinglabel.grid(row=19, column=3,pady=3)
        self.meeting_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.meeting_sfault.grid(row=19, column=4,pady=3)
        self.meeting_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.meeting_dfault.grid(row=19, column=5,pady=3)

        crossinglabel = ctk.CTkLabel(root, text="Crossing:",font=(None,14))
        crossinglabel.grid(row=20, column=3,pady=3)
        self.crossing_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.crossing_sfault.grid(row=20, column=4,pady=3)
        self.crossing_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.crossing_dfault.grid(row=20, column=5,pady=3)

        ##Positioning
        positioninglabel = ctk.CTkLabel(root, text="Positioning:",font=(None,18))
        positioninglabel.grid(row=0, column=6,pady=3)

        normaldrivinglabel = ctk.CTkLabel(root, text="Normal Driving: ",font=(None,14))
        normaldrivinglabel.grid(row=1, column=6,pady=3)
        self.normaldriving_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.normaldriving_sfault.grid(row=1, column=7,pady=3)
        self.normaldriving_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.normaldriving_dfault.grid(row=1, column=8,pady=3)

        lanedisciplinelabel = ctk.CTkLabel(root, text="Lane Discipline:  ",font=(None,14))
        lanedisciplinelabel.grid(row=2, column=6,pady=3)
        self.lanediscipline_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.lanediscipline_sfault.grid(row=2, column=7,pady=3)
        self.lanediscipline_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.lanediscipline_dfault.grid(row=2, column=8,pady=3)

        pedestriancrossingslabel = ctk.CTkLabel(root, text="Pedestrian Crossings:  ",font=(None,14))
        pedestriancrossingslabel.grid(row=3, column=6,pady=3)
        self.pedestriancrossings_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.pedestriancrossings_sfault.grid(row=3, column=7,pady=3)
        self.pedestriancrossings_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.pedestriancrossings_dfault.grid(row=3, column=8,pady=3)

        positionnormalstoplabel = ctk.CTkLabel(root, text="Position/Normal Stop:  ",font=(None,14))
        positionnormalstoplabel.grid(row=4, column=6,pady=3)
        self.positionnormalstop_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.positionnormalstop_sfault.grid(row=4, column=7,pady=3)
        self.positionnormalstop_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.positionnormalstop_dfault.grid(row=4, column=8,pady=3)

        awarenessplanninglabel = ctk.CTkLabel(root, text="Awareness Planning:  ",font=(None,14))
        awarenessplanninglabel.grid(row=5, column=6,pady=3)
        self.awarenessplanning_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.awarenessplanning_sfault.grid(row=5, column=7,pady=3)
        self.awarenessplanning_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.awarenessplanning_dfault.grid(row=5, column=8,pady=3)

        Clearancelabel = ctk.CTkLabel(root, text="Clearance :  ",font=(None,14))
        Clearancelabel.grid(row=6, column=6,pady=3)
        self.Clearance_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.Clearance_sfault.grid(row=6, column=7,pady=3)
        self.Clearance_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.Clearance_dfault.grid(row=6, column=8,pady=3)

        followingdistancelabel = ctk.CTkLabel(root, text="Following Distance:  ",font=(None,14))
        followingdistancelabel.grid(row=7, column=6,pady=3)
        self.followingdistance_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.followingdistance_sfault.grid(row=7, column=7,pady=3)
        self.followingdistance_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.followingdistance_dfault.grid(row=7, column=8,pady=3)

        useofspeedlabel = ctk.CTkLabel(root, text="Use Of Speed:  ",font=(None,14))
        useofspeedlabel.grid(row=8, column=6,pady=3)
        self.useofspeed_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.useofspeed_sfault.grid(row=8, column=7,pady=3)
        self.useofspeed_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.useofspeed_dfault.grid(row=8, column=8,pady=3)

        ##Progress
        progresslabel = ctk.CTkLabel(root, text="Progress:",font=(None,18))
        progresslabel.grid(row=9, column=6,pady=3)

        appropriatespeedlabel = ctk.CTkLabel(root, text="Appropriate Speed:  ",font=(None,14))
        appropriatespeedlabel.grid(row=10, column=6,pady=3)
        self.appropriatespeed_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.appropriatespeed_sfault.grid(row=10, column=7,pady=3)
        self.appropriatespeed_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.appropriatespeed_dfault.grid(row=10, column=8,pady=3)

        unduehesitationlabel = ctk.CTkLabel(root, text="Undue Hesitation:  ",font=(None,14))
        unduehesitationlabel.grid(row=11, column=6,pady=3)
        self.unduehesitation_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.unduehesitation_sfault.grid(row=11, column=7,pady=3)
        self.unduehesitation_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.unduehesitation_dfault.grid(row=11, column=8,pady=3)

        ##Response to signs/signals
        responsetosignssignalslabel = ctk.CTkLabel(root, text="Response to signs/signals: ",font=(None,18))
        responsetosignssignalslabel.grid(row=12, column=6,pady=3)

        trafficsignslabel = ctk.CTkLabel(root, text="Traffic Signs:  ",font=(None,14))
        trafficsignslabel.grid(row=13, column=6,pady=3)
        self.trafficsigns_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.trafficsigns_sfault.grid(row=13, column=7,pady=3)
        self.trafficsigns_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.trafficsigns_dfault.grid(row=13, column=8,pady=3)

        roadmarkingslabel = ctk.CTkLabel(root, text="Road Markings:  ",font=(None,14))
        roadmarkingslabel.grid(row=14, column=6,pady=3)
        self.roadmarkings_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.roadmarkings_sfault.grid(row=14, column=7,pady=3)
        self.roadmarkings_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.roadmarkings_dfault.grid(row=14, column=8,pady=3)

        trafficlightslabel = ctk.CTkLabel(root, text="Traffic Lights:  ",font=(None,14))
        trafficlightslabel.grid(row=15, column=6,pady=3)
        self.trafficlights_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.trafficlights_sfault.grid(row=15, column=7,pady=3)
        self.trafficlights_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.trafficlights_dfault.grid(row=15, column=8,pady=3)

        trafficcontrollerslabel = ctk.CTkLabel(root, text="Traffic Controllers:  ",font=(None,14))
        trafficcontrollerslabel.grid(row=16, column=6,pady=3)
        self.trafficcontrollers_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.trafficcontrollers_sfault.grid(row=16, column=7,pady=3)
        self.trafficcontrollers_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.trafficcontrollers_dfault.grid(row=16, column=8,pady=3)

        otherroaduserslabel = ctk.CTkLabel(root, text="Other Road Users:  ",font=(None,14))
        otherroaduserslabel.grid(row=16, column=6,pady=3)
        self.otherroadusers_sfault = ctk.CTkCheckBox(root,text = "S Fault")
        self.otherroadusers_sfault.grid(row=16, column=7,pady=3)
        self.otherroadusers_dfault = ctk.CTkCheckBox(root,text = "D Fault")
        self.otherroadusers_dfault.grid(row=16, column=8,pady=3)
        
        


        ##Additional Comments
        
        additionalcommentslabel = ctk.CTkLabel(root, text="Additional Comments:  ",font=(None,14))
        additionalcommentslabel.grid(row=18, column=6,pady=3)

        self.additionalcommentsfield = ctk.CTkTextbox(root, width = 400,height = 150,wrap = 'word')
        self.additionalcommentsfield.grid(row=19, column=6,columnspan=3,rowspan=4,pady=3)
        

        createreportbutton = self.CreateMaterialButton(root, 'Create Report', self.CreateReport)
        createreportbutton.grid(row = 23, column = 8,padx = 5)

        selectbooking = self.CreateMaterialButton(root, 'Select Booking', self.InstructorViewLessons)
        selectbooking.grid(row = 19, column = 0)


       
    def InstructorViewLessons(self):
        root = tk.Tk()
        self.TableApp = TableApp(root, self.data)
        root.mainloop()
        

    def CreateReport(self):
        self.SelectedBookingID = self.TableApp.SelectedBookingID
        filename = os.path.join("Driving_Reports",f"id_{self.SelectedBookingID}_feedback_report.txt")

        # Open the file once and write all content
        with open(filename, "w") as file:
            file.write("🚗 Driving Instructor Feedback Report 🚗\n")
            file.write("=" * 50 + "\n\n")

            # Introductory Explanation
            file.write("This report contains a summary of the faults recorded during your driving lesson.\n\n")
            file.write("⚠ Fault Types:\n")
            file.write("- Serious Faults (_sfault): Lead to a fail.\n")
            file.write("- Driving Faults (_dfault): Recorded but do not immediately result in a fail.\n\n")
            file.write("=" * 50 + "\n\n")

            file.write("🔍 **Recorded Faults:**\n\n")

            # Collect ticked checkboxes
            ticked_values = {
                name: widget.get() for name, widget in vars(self).items()
                if isinstance(widget, ctk.CTkCheckBox) and widget.get() == 1
            }

            # If faults were recorded, list them
            if ticked_values:
                for key in ticked_values.keys():
                    formatted_key = key.replace("_", " ").title()  # Make it more readable
                    file.write(f"- {formatted_key}\n")
            else:
                file.write("✅ No faults recorded.\n")

            file.write("\n" + "=" * 50 + "\n\n")

            # Additional Comments
            file.write("📝 **Instructor Comments:**\n")
            comments = self.additionalcommentsfield.get("1.0", "end-1c").strip()
            if comments:
                file.write(comments + "\n")
            else:
                file.write("No additional comments provided.\n")

        tk.messagebox.showinfo("Report Created!", f"Report Created!")
        self.root.destroy()

    

    

    def CreateMaterialButton(self, master, text, command, width=200, height=50):
        BUTTON_COLOR = "white"
        HOVER_COLOR = "#2196F3" 
        TEXT_COLOR = "black"

        button = ctk.CTkButton(master, text=text, width=width, height=height, command=command, 
                               fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        return button

    '''def instructorviewlessons(self):
        root = ctk.CTk()
        learningrecourcesapp(root,self.returnedbookings)
        root.mainloop()'''
        
class ETAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Postcode ETA Calculator")
        self.root.geometry("400x300")

        # OpenRouteService API Key (Replace with your own)
        self.api_key = "INSERT CODE HERE"

        # Labels and Entry Fields
        tk.Label(root, text="Start Postcode:").pack(pady=5)
        self.start_entry = tk.Entry(root)
        self.start_entry.pack(pady=5)

        tk.Label(root, text="Destination Postcode:").pack(pady=5)
        self.end_entry = tk.Entry(root)
        self.end_entry.pack(pady=5)

        # Button to Calculate ETA
        self.calculate_button = tk.Button(root, text="Calculate ETA", command=self.CalculateETA)
        self.calculate_button.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=10)

    def GetCoordinates(self, postcode):
        """Convert UK postcode to latitude and longitude using OpenRouteService."""
        url = f"https://api.openrouteservice.org/geocode/search?api_key={self.api_key}&text={postcode},UK"
        response = requests.get(url)
        
        if response.status_code != 200:
            return None

        data = response.json()
        if "features" in data and len(data["features"]) > 0:
            coords = data["features"][0]["geometry"]["coordinates"]
            return coords[0], coords[1]  # Longitude, Latitude
        return None

    def GetTravelTime(self, start_coords, end_coords):
        """Get travel time (in minutes) between two coordinates using OpenRouteService."""
        url = "https://api.openrouteservice.org/v2/directions/driving-car/json"
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        payload = {
            "coordinates": [start_coords, end_coords],
            "format": "geojson"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return None

        data = response.json()
        if "routes" in data and len(data["routes"]) > 0:
            duration_sec = data["routes"][0]["summary"]["duration"]
            return int(duration_sec / 60)  # Convert seconds to minutes
        return None

    def CalculateETA(self):
        """Calculate and display ETA based on user input."""
        StartPostcode = self.start_entry.get().strip()
        EndPostcode = self.end_entry.get().strip()

        if not StartPostcode or not EndPostcode:
            messagebox.showerror("Error", "Please enter both postcodes.")
            return

        StartCoords = self.GetCoordinates(StartPostcode)
        EndCoords = self.GetCoordinates(EndPostcode)

        if not StartCoords or not EndCoords:
            messagebox.showerror("Error", "Invalid postcode(s). Please check and try again.")
            return

        TravelTime = self.GetTravelTime(StartCoords, EndCoords)

        if TravelTime is None:
            messagebox.showerror("Error", "Could not fetch travel time. Try again later.")
            return

        eta = datetime.now() + timedelta(minutes=TravelTime)
        eta_str = eta.strftime("%H:%M %p")

        self.result_label.config(text=f"ETA: {eta_str} ({TravelTime} mins)")
    
class LearningRecourcesApp():
    def __init__(self, root):
        self.root = root
        self.root.title("Learning Recources")
        self.root.geometry("800x600")
        self.ManoeuvresButton = ctk.CTkButton(root,text = 'Manoeuvres',command = self.LoadManoeuvres)
        self.RoundaboutsButton = ctk.CTkButton(root,text = 'Roundabouts',command = self.LoadRoundabouts)
        self.JunctionsButton = ctk.CTkButton(root,text = 'Junctions',command = self.LoadJunctions)
        self.BackButton = ctk.CTkButton(root,text = 'Go Back',command =self.PackMainScreen)
        self.RecourcesDropdown = ctk.CTkOptionMenu(self.root, values=None)
        self.OpenRecource =ctk.CTkButton(self.root,text = 'Open Recource')
        self.PackMainScreen()
        
    
    def LoadManoeuvres(self):
        self.ClearScreen()
        self.BackButton.pack(pady=15)

        # Path to Learning_Recources folder
        FolderPath = os.path.join("Learning_Recources", "Manoeuvres")  # Access the Manoeuvres folder
        if os.path.exists(FolderPath) and os.path.isdir(FolderPath):
            files = os.listdir(FolderPath)  # Get list of files
        self.RecourcesDropdown = ctk.CTkOptionMenu(self.root, values=files)
        self.RecourcesDropdown.pack(pady=10)
        self.OpenRecource =ctk.CTkButton(self.root,text = 'Open Recource',command=lambda:self.OpenRecourceButton('Learning_recources/Manoeuvres/'))
        self.OpenRecource.pack(pady=10)
          

    def LoadRoundabouts(self):
        self.ClearScreen()
        self.BackButton.pack(pady=15)
        FolderPath = os.path.join("Learning_Recources", "Roundabouts")  # Access the Manoeuvres folder
        if os.path.exists(FolderPath) and os.path.isdir(FolderPath):
            files = os.listdir(FolderPath)  # Get list of files
        self.RecourcesDropdown = ctk.CTkOptionMenu(self.root, values=files)
        self.RecourcesDropdown.pack(pady=10)
        self.OpenRecource =ctk.CTkButton(self.root,text = 'Open Recource',command=lambda:self.OpenRecourceButton('Learning_recources/Roundabouts/'))
        self.OpenRecource.pack(pady=10)
        

    def LoadJunctions(self):
        self.ClearScreen()
        self.BackButton.pack(pady=15)
        FolderPath = os.path.join("Learning_Recources", "Junctions")  # Access the Manoeuvres folder
        if os.path.exists(FolderPath) and os.path.isdir(FolderPath):
            files = os.listdir(FolderPath)  # Get list of files
        self.RecourcesDropdown = ctk.CTkOptionMenu(self.root, values=files)
        self.RecourcesDropdown.pack(pady=10)
        self.OpenRecource =ctk.CTkButton(self.root,text = 'Open Recource.',command=lambda:self.OpenRecourceButton('Learning_recources/Junctions/'))
        self.OpenRecource.pack(pady=10)
        

    def ClearScreen(self):
        self.ManoeuvresButton.pack_forget()
        self.RoundaboutsButton.pack_forget()
        self.JunctionsButton.pack_forget()
        self.RecourcesDropdown.pack_forget()
        self.OpenRecource.pack_forget()

    def PackMainScreen(self):
        self.BackButton.pack_forget()
        self.ClearScreen()
        self.ManoeuvresButton.pack(pady=15)
        self.RoundaboutsButton.pack(pady=15)
        self.JunctionsButton.pack(pady=15)

    def OpenRecourceButton(self,path):
        try:
            ImagePath = path+str(self.RecourcesDropdown.get())  # Change to your image file
            Img = Image.open(ImagePath)  # Open the image
            Img.show()  # Display the image
        except:
            tk.messagebox.showerror("Load Failed", "Failed to Load Image.")

class ViewFeedbackReports(TableApp):
    def __init__(self,root,data):
        super().__init__(root,data)
        self.RemoveButton.pack_forget()
        self.ModifyButton.pack_forget()
        self.ViewReportButton = ctk.CTkButton(root, text="View Feedback Report", command = self.ViewFeedbackReport)
        self.ViewReportButton.pack(pady=10)
    
    def ViewFeedbackReport(self):
        try:

            FileName = ("id_"+str(self.SelectedBookingID)+"_feedback_report.txt")
            FilePath = os.path.join(os.getcwd(),"Driving_reports", FileName)

            # Open the file using the default application
            with open(FilePath, "r", encoding="utf-8") as file:
                content = file.read()
                print(content)  # Prints the content of the file

            FeedbackWindow = ctk.CTkToplevel()
            FeedbackWindow.title("Feedback Report")
            FeedbackWindow.geometry("600x400")
            FeedbackWindow.wm_attributes("-topmost", True)

            # Add a ScrolledText widget for better readability
            TextArea = ctk.CTkTextbox(FeedbackWindow, wrap="word", width=70, height=20)
            TextArea.pack(expand=True, fill="both", padx=10, pady=10)

            # Insert file content into the text area
            TextArea.insert("1.0", content)
            TextArea.configure(state="disabled")  # Make it read-only

            # Run the Tkinter event loop
            FeedbackWindow.mainloop()
        except:
            tk.messagebox.showerror("Couldn't Find Feedback Report", "Please Retry, or Contact your Instructor.")

class ETAcomparer:
    def __init__(self):
        self.api_key = '5b3ce3597851110001cf6248b2ec1f5395df4a34b03870732a500c65'

    def GetCoordinates(self, postcode):
        """Convert UK postcode to latitude and longitude using OpenRouteService."""
        url = f"https://api.openrouteservice.org/geocode/search?api_key={self.api_key}&text={postcode},UK"
        response = requests.get(url)
        
        if response.status_code != 200:
            return None

        data = response.json()
        if "features" in data and len(data["features"]) > 0:
            coords = data["features"][0]["geometry"]["coordinates"]
            return coords[0], coords[1] # Longitude, Latitude
        return None

    def GetTravelTime(self, start_coords, end_coords):
        """Get travel time (in minutes) between two coordinates using OpenRouteService."""
        url = "https://api.openrouteservice.org/v2/directions/driving-car/json"
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        payload = {
            "coordinates": [start_coords, end_coords],
            "format": "geojson"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return None

        data = response.json()
        if "routes" in data and len(data["routes"]) > 0:
            duration_sec = data["routes"][0]["summary"]["duration"]
            return int(duration_sec / 60)  # Convert seconds to minutes
        return None

    def CalculateETA(self,startpostcode,endpostcode):
        """Calculate and display ETA based on user input."""
        StartPostcode = startpostcode.strip()
        EndPostcode = endpostcode.strip()

        if not StartPostcode or not EndPostcode:
            print("Error: Please enter both postcodes.")
            return

        StartCoords = self.GetCoordinates(StartPostcode)
        EndCoords = self.GetCoordinates(EndPostcode)

        if not StartCoords or not EndCoords:
            print("Error: Invalid postcode(s). Please check and try again.")
            return

        TravelTime = self.GetTravelTime(StartCoords, EndCoords)

        if TravelTime is None:
            print("Error: Could not fetch travel time. Try again later.")
            return

        ETA = datetime.now() + timedelta(minutes=TravelTime)
        ETAStr = ETA.strftime("%H:%M %p")

        print(f"Estimated Arrival Time: {ETAStr} ({TravelTime} minutes)")
        return int(TravelTime)



'''app = ETAApp()
app.calculate_eta('le24ff','le181jt')''' ##Code to call api comparison


        
App = MainWindow("Driving Instructor Booking System", (1600,900)) 
App.mainloop()


