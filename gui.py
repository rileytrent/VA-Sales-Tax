from tkinter import *
from tkinter import filedialog, ttk
from dateutil.relativedelta import relativedelta
import datetime
from va import VA_file_tax
from nc import NC_file_tax


#available states
available_states = ["VA", "NC"]

#create choose file function
def chooseFile():
    choose_file_text.delete(0,END)
    filepath = filedialog.askopenfilename(initialdir='',
                                          title="Select your template file.")
    return choose_file_text.insert(END,filepath)



#dropdown options

dropdown_values = []
current_month = datetime.datetime.now()
def get_current_filing_month():
    for i in range(12):
            last_month = current_month - relativedelta(months=i)
            text = last_month.strftime('%b %Y')
            dropdown_values.append(text)
get_current_filing_month()

#get info from imput boxes
def get_input_info():
    file_month = dropdown.get()
    ein = taxid_entry.get()
    user = username_entry.get()
    pw = password_entry.get()
    file_path = choose_file_text.get()
    state_filed = state_dropdown.get()
    if state_filed == 'VA':
         VA_file_tax(file_month, ein, user, pw, file_path)
    elif state_filed == 'nc':
         pass
        #  NC_file_tax(pass)
    else:
         print(state_filed)

#create window and change title     
root = Tk()
root.title("Sales-Tax-Filer")
root.geometry("800x575")


#create grid for widget placement 
for i in range(9):
    root.rowconfigure(i, weight=1)
for i in range(9):
    root.columnconfigure(i, weight=1)

#labels and boxes
myheader = Label(root, text="Tax-Filer")
select_state = Label(root, text="Select filing State: ")
state_dropdown = ttk.Combobox(root, values=available_states)
select_month = Label(root, text="Select filing Period: ")
dropdown = ttk.Combobox(root, values=dropdown_values)
taxid = Label(root, text="Tax ID/EIN: ")
username = Label(root, text="Username: ")
password = Label(root, text="Password: ")
choose_file = Button(root, text="Choose File: ",command=chooseFile)
choose_file_text = Entry(root, border=3)
file_now_button = Button(root, text="File Now!", command=get_input_info)
taxid_entry = Entry(root, border=3)
username_entry = Entry(root, border=3)
password_entry = Entry(root, border=3,show="*")
file_entry = Entry(root)


#grid placement
select_state.grid(row=1, column=1, sticky='ew')
state_dropdown.grid(row=1,column=2, columnspan=2,sticky='w')
select_month.grid(row=2, column=1, sticky='ew')
dropdown.grid(row=2,column=2, columnspan=2,sticky='w')
taxid.grid(row=3, column=1, sticky='ew')
taxid_entry.grid(row=3, column=2, columnspan=3, sticky='w')
username.grid(row=4, column=1, sticky='ew')
username_entry.grid(row=4, column=2, columnspan=3, sticky='w')
password.grid(row=5, column=1, sticky='ew')
password_entry.grid(row=5, column=2, columnspan=3, sticky='w')
choose_file.grid(row=6, column=1, sticky='')
choose_file_text.grid(row=6, column=2,columnspan=3, sticky='we')
file_now_button.grid(row=7, column=2, sticky='we')


root.mainloop()