import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv
# import os
#
# # Set the environment variable
# os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
load_dotenv()
import time

# Creating a main tk window
root = tk.Tk()
root.title("LinkedIn Job Search and Apply")
root.geometry("450x250")  # Display the window size
root.resizable(False, False)  

# Creating a variable for tracking the automation status
automation_running = False

# Creating Output display text
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, state=tk.DISABLED)
output_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="w")


# Creating function for output display
def update_output(message):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, message + "\n")
    output_text.see(tk.END)
    output_text.config(state=tk.DISABLED)
    root.update_idletasks()  # Update Gui in current time / immediately


# Tk gui function for performing job search and application
def search_and_apply_jobs():
    global automation_running
    if automation_running:
        return

    email = email_entry.get()
    password = password_entry.get()
    job_keywords = job_keywords_entry.get()

    # Seting up Chromedriver and its configuration

    DRIVER_PATH = r"D:\Projects\chromedriver-win64\chromedriver.exe"
    driver_path = Service(DRIVER_PATH)
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=driver_path, options=chrome_options)

    # Set up the variable that indicates automation is running
    automation_running = True

    try:
        # Navigation begin from here to the LinkedIn jobs page
        URL = f"https://www.linkedin.com/jobs/search/?keywords={job_keywords}&location=India"
        driver.get(URL)
        time.sleep(2)

        # Sign in to the LinkedIn account
        sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")
        sign_in_button.click()
        time.sleep(3)
        email_field = driver.find_element(By.ID, "username")
        email_field.send_keys(email)
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(3)

        jobs_list = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")
        main_window_id = driver.current_window_handle

        applied_count = 0  # Count the number of job successfully saved

        for job in jobs_list:

            if not automation_running:
                break  # Stop the automation if Stop button is pressed

            job.click()
            print("Clicked on a job")  # Update the terminal display
            # Update the tk output display
            update_output("Clicked on a job")
            time.sleep(5)


            try:
                time.sleep(5)
                # Click on easy apply button
                easy_apply_click = driver.find_element(By.CSS_SELECTOR, '.jobs-apply-button--top-card button')
                easy_apply_click.click()
                print("Clicked on Easy Apply button")  # Update the terminal display
                # Update the tk output display
                update_output("Clicked on Easy Apply button")
                time.sleep(5)

                # Checkout  if the application can be submitted
                submit_button = driver.find_element(By.CSS_SELECTOR, ".justify-flex-end button .artdeco-button__text")
                if submit_button.text == 'Submit application':
                    # add_number = driver.find_element(By.CSS_SELECTOR, '.fb-single-line-text input')
                    # if add_number.get_attribute("value") == "":
                    #     #add_number.send_keys(phone)
                    #     print("Entered phone number")

                    # Save the job for future application
                    save_job_button = driver.find_element(By.CSS_SELECTOR, '.jobs-save-button')
                    save_job_button.click()
                    print("Saved the job for future application")  # Update the terminal display
                    # Update the tk output display
                    update_output("Saved the job for future application")
                    time.sleep(4)
                    # Submit the application
                    submit_button.click()
                    print('Applied')  # Update the terminal display
                    # Update the tk output display
                    update_output('Applied')
                    time.sleep(5)

                    try:
                        time.sleep(5)
                        dialog = driver.find_element(By.CSS_SELECTOR, '.artdeco-modal__actionbar--confirm-dialog')
                        save_button = dialog.find_element(By.CSS_SELECTOR,
                                                          '.artdeco-modal__actionbar--confirm-dialog span')
                        save_button.click()
                        print("Clicked on Save in Save and Discard dialog")  # Update the terminal display
                        # Update the tk output display
                        update_output("Clicked on Save in Save and Discard dialog")
                        time.sleep(4)
                    except NoSuchElementException:
                        pass
                    applied_count += 1  # Increment applied_count
                elif 'Continue to Next Step' in submit_button.text:
                    time.sleep(4)
                    continue_button = driver.find_element(By.CSS_SELECTOR, ".jobs-easy-apply__submit-button")
                    continue_button.click()
                    print("Clicked on Continue to Next Step button")
                    # Update the output display
                    update_output("Clicked on Continue to Next Step button")
                    time.sleep(5)

                    # # Fill the  additional information if needed else leave it
                    # additional_info_field = driver.find_element(By.ID, "additional_info_field")
                    # additional_info_field.send_keys(
                    #     "Additional information")
                    #
                    # save_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__confirm-dialog-btn--primary")
                    # save_button.click()
                    # print("Clicked on Save in Save and Discard dialog")

                else:
                    # Handle the dialog box cases
                    try:
                        back_button = driver.find_element(By.CSS_SELECTOR, '.artdeco-modal__dismiss').click()
                        print("Clicked on Back button")
                        # Update the output display
                        update_output("Clicked on Back button")
                        time.sleep(4)
                        discard_button = driver.find_element(By.CSS_SELECTOR,
                                                             '.artdeco-modal__actionbar--confirm-dialog span').click()

                        print("Clicked on Discard button")
                        # Update the tk output display
                        update_output("Clicked on Discard button")
                        time.sleep(4)
                        # Save the job for future application
                        save_job_button = driver.find_element(By.CSS_SELECTOR, '.jobs-save-button')
                        save_job_button.click()
                        print("Saved the job for future application")  # Update the terminal display
                        # Update the tk output display
                        update_output("Saved the job for future application")
                        time.sleep(4)

                    except NoSuchElementException:
                        time.sleep(7)
                        print("Unable to apply. Saving the job for future application.")  # Update the terminal display
                        # Update the tk  output display
                        update_output("Unable to apply. Saving the job for future application.")
                        time.sleep(7)
                        save_job_button = driver.find_element(By.CSS_SELECTOR, '.jobs-save-button')
                        save_job_button.click()
                        print("Saved the job for future application")  # Update the terminal display
                        # Update the tk output display
                        update_output("Saved the job for future application")

            except Exception as e:
                time.sleep(4)
                print("Error occurred:", str(e))
                print("Error in applying to the job. Discarding the job.")
            finally:
                time.sleep(3)
                # Close the current tab which is opened by apply job and switch back to the main window
                all_windows = driver.window_handles
                for tab in all_windows:
                    if tab != main_window_id:
                        driver.switch_to.window(tab)
                        driver.close()
                driver.switch_to.window(main_window_id)
                time.sleep(3)
                if applied_count >= 4:
                    break

        messagebox.showinfo("Success", "Job search and application completed!")
    except TimeoutException as e:
        messagebox.showerror("Error",
                             "Timed out  waiting for the  loading page. Please check your internet connection.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        automation_running = False
        driver.quit()


# Automation stop function
def stop_automation():
    global automation_running
    automation_running = False
    messagebox.showinfo("Stopped", "Automation stopped.")


# Creating the main tk window
root = tk.Tk()
root.title("LinkedIn Job Search and Apply")
root.geometry("400x400")  # Set window size
root.resizable(False, False)  # Disable window resizing

# Setting for center alignment of hte window
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
root.geometry("+{}+{}".format(position_right, position_down))

# Label all the entries
message_label = tk.Label(root, text="LinkedIn Job Search and Apply", font=("Helvetica", 16, "bold"))
email_label = tk.Label(root, text="Email:")
email_entry = tk.Entry(root)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")  # Hide password input
job_keywords_label = tk.Label(root, text="Job Keywords:")
job_keywords_entry = tk.Entry(root)

# Add a label and entry field for job count

submit_button = tk.Button(root, text="Submit", command=search_and_apply_jobs, width=20)
stop_button = tk.Button(root, text="Stop Automation", command=stop_automation, width=20)

# Status update label
status_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"), wraplength=350, justify="center")
operation_count_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"))

# Gui elements
message_label.grid(row=0, columnspan=2, padx=10, pady=10)
email_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
email_entry.grid(row=1, column=1, padx=10, pady=5)
password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
password_entry.grid(row=2, column=1, padx=10, pady=5)
job_keywords_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
job_keywords_entry.grid(row=3, column=1, padx=10, pady=5)
submit_button.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
stop_button.grid(row=6, column=0, padx=10, pady=10, columnspan=2)
status_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
operation_count_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Starts the main tk window
root.mainloop()
