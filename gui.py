from tkinter import *
from tkinter import filedialog, ttk
from dateutil.relativedelta import relativedelta
import datetime


#create choose file function
def chooseFile():
    choose_file_text.delete(0,END)
    filepath = filedialog.askopenfilename(initialdir='',
                                          title="Select your template file.")
    return choose_file_text.insert(END,filepath)

#dropdown options. good case for a Lambda func???
dropdown_values = []
current_month = datetime.datetime.now()
def get_current_filing_month():
    for i in range(12):
            last_month = current_month - relativedelta(months=i)
            text = last_month.strftime('%b %Y')
            dropdown_values.append(text)
get_current_filing_month()

#create window and change title     
root = Tk()
root.title("VA-Sales-Tax-Filer")
root.geometry("800x575")


#create grid for widget placement 
for i in range(9):
    root.rowconfigure(i, weight=1)
for i in range(9):
    root.columnconfigure(i, weight=1)

#labels and boxes
myheader = Label(root, text="VA-Sales-Tax-Filer")
select_month = Label(root, text="Select filing Period: ")
dropdown = ttk.Combobox(root, values=dropdown_values)
taxid = Label(root, text="Tax ID/EIN: ")
username = Label(root, text="Username: ")
password = Label(root, text="Password: ")
choose_file = Button(root, text="Choose File: ",command=chooseFile)
choose_file_text = Entry(root, border=3)
file_now_button = Button(root, text="File Now!")
taxid_entry = Entry(root, border=3)
username_entry = Entry(root, border=3)
password_entry = Entry(root, border=3,show="*")
file_entry = Entry(root)


#grid placement
select_month.grid(row=1, column=1, sticky='ew')
dropdown.grid(row=1,column=2, columnspan=2,sticky='w')
taxid.grid(row=2, column=1, sticky='ew')
taxid_entry.grid(row=2, column=2, columnspan=3, sticky='w')
username.grid(row=3, column=1, sticky='ew')
username_entry.grid(row=3, column=2, columnspan=3, sticky='w')
password.grid(row=4, column=1, sticky='ew')
password_entry.grid(row=4, column=2, columnspan=3, sticky='w')
choose_file.grid(row=5, column=1, sticky='')
choose_file_text.grid(row=5, column=2,columnspan=3, sticky='we')
file_now_button.grid(row=6, column=4, sticky='w')


root.mainloop()