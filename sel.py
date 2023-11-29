import pandas as pd
import os
from tkinter import messagebox
from selenium import webdriver
import tkinter as tk
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECt
from tkinter import ttk,scrolledtext
from firebase_admin import auth, credentials,initialize_app


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.signinOrsignup()
        # Your application setup code here
 

    def search_jobs(self,job_title,job_location,job_info_text):
        
        os.environ['MOZ_HEADLESS'] = '1'
    
        driver = webdriver.Firefox()
    

        # driver.get('https://www.linkedin.com/jobs/search/?keywords={job_title}&location=London')
        driver.get(f'https://www.linkedin.com/jobs/search/?keywords={quote(job_title)}&location={job_location}')
        sleep(0.5)

        # job_links=driver.find_elements(By.CSS_SELECTOR,'.scaffold-layout__list-container a')
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        all_job_links = []
        for i in range(1,20):
            # job_links = WebDriverWait(driver, 30).until(
            # EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[3]/div/main/section[2]/ul/li[{i}]/div/a"))
            # )
            job_links=driver.find_elements(By.XPATH,f'/html/body/div[3]/div/main/section[2]/ul/li[{i}]/div/a')
            all_job_links.extend(job_links)
        

        job_info_text.config(state=tk.NORMAL)  # Enable the Text widget for updates
        job_info_text.delete(1.0, tk.END) 
        # Display job postings in GUI

        count=0
    # Extract and print the href links
        for job_link in all_job_links:
            href = job_link.get_attribute('href')
            count+=1
            job_info_text.insert(tk.END, f"Job {count}\n")
            job_info_text.insert(tk.END, href + '\n')
            job_info_text.insert(tk.END, '\n')
            job_info_text.insert(tk.END, '\n')

            
            
            # print(href)
        job_info_text.config(state=tk.DISABLED)
    
        # search_jobs=driver.find_element(By.XPATH,'/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[3]')
        # search_jobs.send_keys('python developer')

        # search_jobs.send_keys(Keys.ENTER)


        sleep(0.5)
        
    # def searchWindow(self):
    #     # Create the root window
    #     root = tk.Toplevel(self)
    #     root.title("Job Scraper")
    #     root.geometry("600x400")  # Set the initial window size

    #     # Style configuration
    #     style = ttk.Style()
    #     style.configure("TButton", padding=5, font=("Arial", 12))
    #     style.configure("TLabel", font=("Arial", 12))
    #     style.configure("TEntry", padding=5, font=("Arial", 12))

    #     # Create and pack widgets using grid layout
    #     ttk.Label(root, text="Job Title:").grid(row=0, column=0, pady=(10, 5), sticky="w")
    #     job_title_entry = ttk.Entry(root)
    #     job_title_entry.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="ew")

    #     ttk.Label(root, text="Job Location:").grid(row=1, column=0, pady=5, sticky="w")
    #     job_title_entry_location = ttk.Entry(root)
    #     job_title_entry_location.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

    #     search_button = ttk.Button(root, text="Search", command=lambda: self.search_jobs(job_title_entry.get(), job_title_entry_location.get(),job_info_text))
    #     search_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="ew")

    #     job_info_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 12), bg="#EEEEEE", fg="#000000")
    #     job_info_text.grid(row=3, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="nsew")

    #     # Insert initial text
    #     initial_text = "Job postings will appear here..."
    #     job_info_text.insert(tk.END, initial_text)
    #     job_info_text.tag_configure("center", justify="center")
    #     job_info_text.tag_add("center", "1.0", "end")

    #     # Disable the Text widget after setting the initial text
    #     job_info_text.config(state=tk.DISABLED)

    #     # Column and row weights for resizing
    #     root.columnconfigure(0, weight=1)
    #     root.rowconfigure(3, weight=1)

    #     # Run the Tkinter main loop
    #     root.mainloop()
    def searchWindow(self):
        # Create the root window
        root = tk.Toplevel(self)
        root.title("Job Scraper")
        root.geometry("600x400")  # Set the initial window size

        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=5, font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", padding=5, font=("Arial", 12))

        # Create and pack widgets using grid layout
        ttk.Label(root, text="Job Title:").grid(row=0, column=0, pady=(10, 5), padx=10, sticky="e")
        job_title_entry = ttk.Entry(root)
        job_title_entry.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="w")

        ttk.Label(root, text="Job Location:").grid(row=1, column=0, pady=5, padx=10, sticky="e")
        job_title_entry_location = ttk.Entry(root)
        job_title_entry_location.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        search_button = ttk.Button(root, text="Search", command=lambda: self.search_jobs(job_title_entry.get(), job_title_entry_location.get(), job_info_text))
        search_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="ew")

        job_info_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 12), bg="#EEEEEE", fg="#000000")
        job_info_text.grid(row=3, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="nsew")

        # Insert initial text
        initial_text = "Job postings will appear here..."
        job_info_text.insert(tk.END, initial_text)
        job_info_text.tag_configure("center", justify="center")
        job_info_text.tag_add("center", "1.0", "end")

        # Disable the Text widget after setting the initial text
        job_info_text.config(state=tk.DISABLED)

        # Center the labels and entry widgets
        for i in range(2):
            root.columnconfigure(i, weight=1)
        for i in range(4):
            root.rowconfigure(i, weight=1)

        # Run the Tkinter main loop
        root.mainloop()


    def create_user(self,root,email, password):
        root.destroy()
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            if user:
                email = user.email
              
                print(f'Successfully created new user: {email} )')

            self.searchWindow()
            print(f'Successfully created user: {user.uid}')
        except:
            if messagebox.askyesno(title='User already exists', message='User already exists. Login?'):
                self.login_window()
        

            print(f'User already exists.')



    def login(self,email, password,root):
        if not email or not password:
            messagebox.showerror(title='Error', message='Email and password are required.')
            return
        try:
            user = auth.get_user_by_email(email)
           

      

           

      
            print(f'Successfully logged in. User ID: {user.uid}')
            root.destroy()
            self.searchWindow()
            
        except ValueError as e:
            # Handle authentication errors
            error_message = str(e)
            if 'INVALID_PASSWORD' in error_message:
                messagebox.showerror(title='Incorrect password', message='Incorrect password for the given email.')
            elif 'EMAIL_NOT_FOUND' in error_message:
                text = f'User with email {email} does not exist. Do you want to register?'
                if messagebox.askyesno(title='User not found', message=text):
                    self.create_user(email, password)
                    root.destroy()
                    self.searchWindow()
            else:
                messagebox.showerror(title='Authentication Error', message=f'Error: {error_message}')

        except Exception as e:
            # Handle other exceptions
            messagebox.showerror(title='Error', message=f'An unexpected error occurred: {str(e)}')
                    

    def create_user_window(self):
     
        root = tk.Tk()
        root.title("Register")

        style = ttk.Style()
        style.configure("TButton", padding=5, font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", padding=5, font=("Arial", 12))

        ttk.Label(root, text="Email:").grid(row=0, column=0, pady=(10, 5), sticky="w")
        email_entry = ttk.Entry(root)
        email_entry.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="ew")

        ttk.Label(root, text="Password:").grid(row=1, column=0, pady=5, sticky="w")
        password_entry = ttk.Entry(root, show="*")
        password_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        register_button = ttk.Button(root, text="Register", command=lambda: self.create_user(root,email_entry.get(), password_entry.get()))
        register_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="ew")

        root.mainloop()

       


    



    def signinOrsignup(self):
        self.title("Login or Register")
        self.geometry("400x200")

        style = ttk.Style()
        style.configure("TButton", padding=5, font=("Arial", 12))
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill="both")

        tk.Button(button_frame, text="Login", command=self.login_window).grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")
        tk.Button(button_frame, text="Register", command=self.create_user_window).grid(row=0, column=1, pady=(10, 5), padx=10, sticky="ew")

        # Make columns and rows expandable
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.rowconfigure(0, weight=1)
        
    def login_window(self):
        root = tk.Tk()
        root.title("Login")
        root.geometry("400x200")

        style = ttk.Style()
        style.configure("TButton", padding=5, font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", padding=5, font=("Arial", 12))

        email_label = ttk.Label(root, text="Email:")
        email_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="e")

        email_entry = ttk.Entry(root)
        email_entry.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="w")

        password_label = ttk.Label(root, text="Password:")
        password_label.grid(row=1, column=0, pady=5, padx=10, sticky="e")

        password_entry = ttk.Entry(root, show="*")
        password_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        login_button = ttk.Button(root, text="Login", command=lambda: self.login(email_entry.get(), password_entry.get(), root))
        login_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="nsew")

        # Make columns expandable
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        # Make rows expandable
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        # Center the window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

        root.mainloop()

    def applicationSupportsSecureRestorableState(self):
        return True





cred = credentials.Certificate('credentials.json')
initialize_app(cred)


if __name__ == '__main__':
   
    app = MyApp()
    app.mainloop()
    # login_window()






