from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import json
chat_window = None

def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    # check if "Other User" button was clicked
    if username == '' and password == '':
        login_window.destroy()
        open_chat_window()
    else:
        # perform validation
        if username == 'admin' and password == '1234':
            # close the login window
            login_window.destroy()

            # open the chat window
            open_chat_window()
        else:
            # show an error message

            error_label.config(text="Invalid username or password")

def open_chat_window():
    global chat_window
    # chat_window = Tk()
    chat_window.title("Chat")

def open_admin_window():
    admin_window = Toplevel()
    admin_window.title("Admin")
    admin_window.geometry('450x550')

    feedback_label = Label(admin_window, text="User Feedback:")
    feedback_label.pack()

    feedback_text = Text(admin_window)
    feedback_text.pack()

    submit_button = Button(admin_window, text="Submit", command=lambda: submit_feedback(admin_window, feedback_text))
    submit_button.pack()

def submit_feedback(window, feedback_text):
    feedback = feedback_text.get("1.0", "end-1c")

    if not feedback:
        messagebox.showerror("Error", "Feedback cannot be empty.")
        return

    messagebox.showinfo("Success", "Feedback received.")

    # clear the feedback text box
    feedback_text.delete("1.0", "end")

    # close the admin window
    window.destroy()


def admin_function():
    # open the feedback file for writing
    with open('feedback.json', 'w') as f:
        # get the feedback from the user
        feedback = input("Please enter your feedback: ")

        # create a dictionary to store the feedback
        feedback_dict = {'feedback': feedback}

        # write the feedback to the file as JSON
        json.dump(feedback_dict, f)

        # print a confirmation message
        print("Thank you for your feedback!")


# create the login window
login_window = Tk()
login_window.title("Login")
login_window.geometry('450x550')
login_window.configure(bg="light cyan")

college_label = Label(login_window, text="Smt. Indira Gandhi College of Engineering", font=("Helvetica", 16, "bold"), bg="light cyan")
college_label.pack(pady=(5,20))


# add logo and college name
logo_image = ImageTk.PhotoImage(Image.open("college_logo.jpg").resize((150, 150)))
logo_label = Label(login_window, image=logo_image)
logo_label.pack(pady=(20,0))

# add login widgets here
username_label = Label(login_window, text="Username", font=("Helvetica", 14), bg="light cyan")
username_label.pack(pady=(0,10))
username_entry = Entry(login_window, font=("Helvetica", 14))
username_entry.pack()

password_label = Label(login_window, text="Password", font=("Helvetica", 14), bg="light cyan")
password_label.pack(pady=(0,10))
password_entry = Entry(login_window, show="*", font=("Helvetica", 14))
password_entry.pack()

login_button = Button(login_window, text="Login", command=validate_login, font=("Helvetica", 14))
login_button.pack(pady=(10,20))

other_user_button = Button(login_window, text="Other User", command=validate_login, font=("Helvetica", 14))
other_user_button.pack(pady=(0,10))

admin_button = Button(login_window, text="Admin", command=open_admin_window, font=("Helvetica", 14))
admin_button.pack()

error_label = Label(login_window, fg="red", bg="light cyan")
error_label.pack(pady=(10,0))

login_window.mainloop()
