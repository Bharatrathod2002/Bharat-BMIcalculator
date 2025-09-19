from tkinter import *
from tkinter import messagebox

# Reset inputs
def reset_entry():
    name_tf.delete(0, 'end')
    age_tf.delete(0, 'end')
    height_tf.delete(0, 'end')
    weight_tf.delete(0, 'end')
    gender_var.set(0)

# Calculate BMI
def calculate_bmi():
    try:
        name = name_tf.get().strip()
        kg = float(weight_tf.get())
        m = float(height_tf.get()) / 100
        bmi = kg / (m * m)
        bmi = round(bmi, 1)
        bmi_index(name, bmi)
    except:
        messagebox.showerror("Error", "Please enter valid inputs!")

# BMI category
def bmi_index(name, bmi):
    if not name:
        name = "User"
    if bmi < 18.5:
        messagebox.showinfo('BMI Result', f'Name: {name}\nBMI = {bmi}\nStatus: Underweight')
    elif 18.5 <= bmi < 24.9:
        messagebox.showinfo('BMI Result', f'Name: {name}\nBMI = {bmi}\nStatus: Normal')
    elif 25 <= bmi < 29.9:
        messagebox.showinfo('BMI Result', f'Name: {name}\nBMI = {bmi}\nStatus: Overweight')
    elif bmi >= 30:
        messagebox.showinfo('BMI Result', f'Name: {name}\nBMI = {bmi}\nStatus: Obesity')
    else:
        messagebox.showerror('BMI Result', 'Something went wrong!')

# ---------------- GUI ----------------
ws = Tk()
ws.title('🎯 BMI Calculator')
ws.geometry('400x360')
ws.config(bg='#2c3e50')

frame = Frame(ws, padx=10, pady=10, bg='#34495e')
frame.pack(expand=True)

label_fg = '#ecf0f1'
entry_bg = '#ecf0f1'
entry_fg = '#2c3e50'
button_bg = '#1abc9c'
button_fg = 'white'

# Name
Label(frame, text="Name", bg=frame["bg"], fg=label_fg, font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=5, sticky=W)
name_tf = Entry(frame, bg=entry_bg, fg=entry_fg)
name_tf.grid(row=0, column=1, pady=5)

# Age
Label(frame, text="Age", bg=frame["bg"], fg=label_fg, font=('Arial', 10, 'bold')).grid(row=1, column=0, pady=5, sticky=W)
age_tf = Entry(frame, bg=entry_bg, fg=entry_fg)
age_tf.grid(row=1, column=1, pady=5)

# Gender
Label(frame, text="Select Gender", bg=frame["bg"], fg=label_fg, font=('Arial', 10, 'bold')).grid(row=2, column=0, pady=5, sticky=W)
gender_var = IntVar()
Radiobutton(frame, text="Male", variable=gender_var, value=1, bg=frame["bg"], fg=label_fg, selectcolor=entry_bg).grid(row=2, column=1, pady=5, sticky=W)
Radiobutton(frame, text="Female", variable=gender_var, value=2, bg=frame["bg"], fg=label_fg, selectcolor=entry_bg).grid(row=2, column=2, pady=5, sticky=W)

# Height
Label(frame, text="Height (cm)", bg=frame["bg"], fg=label_fg, font=('Arial', 10, 'bold')).grid(row=3, column=0, pady=5, sticky=W)
height_tf = Entry(frame, bg=entry_bg, fg=entry_fg)
height_tf.grid(row=3, column=1, pady=5)

# Weight
Label(frame, text="Weight (kg)", bg=frame["bg"], fg=label_fg, font=('Arial', 10, 'bold')).grid(row=4, column=0, pady=5, sticky=W)
weight_tf = Entry(frame, bg=entry_bg, fg=entry_fg)
weight_tf.grid(row=4, column=1, pady=5)

# Buttons
Button(frame, text="Calculate", command=calculate_bmi, bg=button_bg, fg=button_fg).grid(row=5, column=0, pady=20)
Button(frame, text="Reset", command=reset_entry, bg='#e67e22', fg='white').grid(row=5, column=1, pady=20)
Button(frame, text="Exit", command=lambda: ws.destroy(), bg='#e74c3c', fg='white').grid(row=5, column=2, pady=20)

ws.mainloop()
