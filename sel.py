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



def search_jobs(job_title,job_location,job_info_text):
    
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
    
def create_user(email, password):
 
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f'Successfully created user: {user.uid}')
    except:
        print(f'Error creating user:')





def searchWindow():
    # Create the root window
    root = tk.Tk()
    root.title("LinkedIn Job Scraper")
    root.geometry("600x400")  # Set the initial window size

    # Style configuration
    style = ttk.Style()
    style.configure("TButton", padding=5, font=("Arial", 12))
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TEntry", padding=5, font=("Arial", 12))

    # Create and pack widgets using grid layout
    ttk.Label(root, text="Job Title:").grid(row=0, column=0, pady=(10, 5), sticky="w")
    job_title_entry = ttk.Entry(root)
    job_title_entry.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="ew")

    ttk.Label(root, text="Job Location:").grid(row=1, column=0, pady=5, sticky="w")
    job_title_entry_location = ttk.Entry(root)
    job_title_entry_location.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

    search_button = ttk.Button(root, text="Search", command=lambda: search_jobs(job_title_entry.get(), job_title_entry_location.get(),job_info_text))
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

    # Column and row weights for resizing
    root.columnconfigure(0, weight=1)
    root.rowconfigure(3, weight=1)

    # Run the Tkinter main loop
    root.mainloop()




def login(email, password,root):
    if not email or not password:
        messagebox.showerror(title='Error', message='Email and password are required.')
        return
    try:
        user = auth.get_user_by_email(email)
        # If the above line doesn't raise an exception, the user is logged in successfully
        print(f'Successfully logged in. User ID: {user.uid}')
        root.destroy()
        searchWindow()
       
    except:
        # If the user doesn't exist, an exception is raised

        text = f'User with email {email} does not exist.'  
        if messagebox.askyesno(title='User not found', message=text):
            create_user(email, password)
            root.destroy()
            searchWindow()
            

        

def login_window():
    root = tk.Tk()
    root.title("Login")

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

    login_button = ttk.Button(root, text="Login", command=lambda: login(email_entry.get(), password_entry.get(),root))
    login_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="ew")

    root.mainloop()





cred = credentials.Certificate('/Users/affankhalid/Desktop/credentials.json')
initialize_app(cred)


if __name__ == '__main__':
     login_window()
    




