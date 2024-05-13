import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import random
from datetime import timedelta, time, datetime
import pandas as pd
import os
from plyer import notification


class CreateDetail:
    def __init__(self, code, name, i_time, f_time):
        self.code = code
        self.name = name
        self.i_time = i_time
        self.f_time = f_time


class MainWindow:
    def __init__(self):
        self.WIDTH, self.HEIGHT, self.X_POS, self.Y_POS = 300, 240, 500, 150

        self.root = tk.Tk()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X_POS}+{self.Y_POS}")
        self.root.title("Attendance Register")
        self.root.iconbitmap('images/icon.ico')
        self.root.resizable(False, False)

        self.adm_frame = tk.Frame(self.root, bg='WHITE')
        self.adm_button = tk.Button(self.adm_frame, text='Admin', bg='#E0115F', font='Arial 12 bold', width=27, fg='WHITE', command=PasswordWindow)

        self.name_frame = tk.Frame(self.root, bg='WHITE')
        self.name_label = tk.Label(self.name_frame, text='Name:', bg='WHITE', font='Arial 12 bold', fg='#1E90FF')
        self.name_box = ttk.Combobox(self.name_frame, values=[i.name for i in det_list], state='readonly', background='WHITE', font='Arial 12')

        self.code_frame = tk.Frame(self.root, bg='WHITE')
        self.code_label = tk.Label(self.code_frame, text='Code:', bg='WHITE', font='Arial 12 bold', fg='#1E90FF')
        self.code_box = tk.Entry(self.code_frame, width=3, font='Arial 12 bold', show='•', bg='#FAFAFA', justify=tk.CENTER)

        self.enter_frame = tk.Frame(self.root, bg='WHITE')
        self.enter_button = tk.Button(self.enter_frame, text='Record Entry/Departure', font='Arial 12 bold', bg='#16A085', fg='WHITE', width=20, command=self.set_entry)
        self.error_label = tk.Label(self.enter_frame, text='', bg='WHITE', fg='#801818', font='Arial 12 bold')

        # Packing
        self.adm_frame.pack(fill=tk.X)
        self.adm_button.pack(pady=10)

        self.name_frame.pack(fill=tk.X)
        self.name_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.name_box.pack(side=tk.LEFT)

        self.code_frame.pack(fill=tk.X)
        self.code_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.code_box.pack(side=tk.LEFT, padx=3, ipadx=10)

        self.enter_frame.pack(fill=tk.X)
        self.enter_button.pack(pady=(20, 10), side=tk.TOP)
        self.error_label.pack(side=tk.BOTTOM, pady=(0, 10))

        self.root.bind('<Return>', lambda x: self.set_entry())
        self.root.mainloop()

    def set_entry(self):
        name = self.name_box.get()
        code = self.code_box.get()
        date = datetime.now().date()
        time_ = str(datetime.now().time())[:5]
        is_entry = True
        conf_text = ''

        if not name:
            self.error_label.config(text='*Name field is empty*')
            return
        if not code:
            self.error_label.config(text='*Code field is empty*')
            return

        for det in det_list:
            if det.name == name:
                if det.code.lower() != code.lower():
                    self.error_label.config(text='*Wrong code entered*')
                    return

        self.error_label.config(text='')
        with open('attendance.dat', 'rb') as file:
            text = pickle.load(file)

        att_list = text.split('\n')
        last_att = att_list[-1]

        notif_flag = True
        if last_att:
            last_date = last_att.split(';')[0]
            if str(last_date) == str(date):
                if code not in last_att:
                    store = last_att + f';["{code}","{time_}",""]'
                else:
                    notif_flag = False
                    store = str(date)
                    datas = last_att.split(';')[1:]
                    for data in datas:
                        data = eval(data)
                        if data[0].lower() == code.lower():
                            data[2] = time_
                        store += f';{data}'
                        is_entry = False
            else:
                store = f'{str(date)};["{code}","{time_}",""]'
        else:
            store = f'{str(date)};["{code}","{time_}",""]'

        if is_entry:
            conf_text = f'Are you sure you want to record entry for {name} on {date} at {time_}'
        else:
            conf_text = f'Are you sure you want to record departure for {name} on {date} at {time_}'

        flag = messagebox.askyesno('Record Confirmation', conf_text)

        if flag:
            att_list[-1] = store

            with open('attendance.dat', 'wb') as file:
                pickle.dump('\n'.join(att_list), file)
        return


class PasswordWindow:
    def __init__(self):
        self.WIDTH, self.HEIGHT, self.X_POS, self.Y_POS = 400, 145, 550, 200

        with open('password.dat', 'rb') as file:
            self.password = pickle.load(file)

        self.root = tk.Toplevel()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X_POS}+{self.Y_POS}")
        self.root.resizable(False, False)
        self.root.title('Enter Password')
        self.root.iconbitmap('images/password.ico')

        self.frame = tk.Frame(self.root, bg='WHITE')
        self.pass_box = tk.Entry(self.frame, width=30, font='Arial 12 bold', show='•', bg='#FAFAFA', justify=tk.CENTER)
        self.enter_button = tk.Button(self.frame, text='Enter', bg='#32CD32', width=10, font='Arial 12 bold', fg='WHITE', command=self.check_pass)
        self.error_label = tk.Label(self.frame, text='', bg='WHITE', fg='#801818', font='Arial 12 bold')

        self.frame.pack(fill=tk.BOTH)
        self.pass_box.grid(row=0, column=0, pady=20)
        self.enter_button.grid(row=1, column=0, pady=(0, 10))
        self.error_label.grid(row=2, column=0, pady=(0, 15))

        self.frame.columnconfigure(0, weight=1)
        self.root.bind('<Return>', lambda x: self.check_pass())
        self.root.mainloop()

    def check_pass(self):
        entry = self.pass_box.get()
        if entry:
            if entry == self.password:
                self.root.destroy()
                AdminWindow()
            else:
                self.pass_box.delete(0, tk.END)
                self.error_label.config(text='*Password is incorrect*')
        else:
            self.error_label.config(text='*Password field is empty*')


class AdminWindow:
    def __init__(self):
        self.WIDTH, self.HEIGHT, self.X_POS, self.Y_POS = 300, 197, 550, 200
        self.root = tk.Toplevel()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X_POS}+{self.Y_POS}")
        self.root.title('Admin')
        self.root.iconbitmap('images/admin.ico')
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg='WHITE')
        self.add_button = tk.Button(self.frame, text='Add Name', bg='#138808', fg='WHITE', font='Arial 12 bold', width=40, command=AddName)
        self.rem_button = tk.Button(self.frame, text='Remove Name', bg='#801818', fg='WHITE', font='Arial 12 bold', width=40, command=RemName)
        self.det_button = tk.Button(self.frame, text='Download Employee Details', bg='#E4CD05', fg='WHITE', font='Arial 12 bold', width=40, command=DownloadDetails)
        self.csv_button = tk.Button(self.frame, text='Download Attendance Data', bg='#1520A6', fg='WHITE', font='Arial 12 bold', width=40, command=DownloadAttendance)
        self.pass_button = tk.Button(self.frame, text='Change Password', bg='#333333', fg='WHITE', font='Arial 12 bold', width=40, command=ChangePass)
        self.clean_button = tk.Button(self.frame, text='Clean Data', bg='#02BA0F', fg='WHITE', font='Arial 12 bold', width=40, command=Clean)

        self.frame.pack(fill=tk.BOTH)
        self.add_button.grid(row=0, column=0)
        self.rem_button.grid(row=1, column=0)
        self.det_button.grid(row=2, column=0)
        self.csv_button.grid(row=3, column=0)
        self.pass_button.grid(row=4, column=0)
        self.clean_button.grid(row=5, column=0)

        self.frame.columnconfigure(0, weight=1)
        self.root.mainloop()


class AddName:
    def __init__(self):
        self.WIDTH, self.HEIGHT, self.X_POS, self.Y_POS = 300, 220, 550, 200

        self.root = tk.Toplevel()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X_POS}+{self.Y_POS}")
        self.root.title('Admin')
        self.root.iconbitmap('images/admin.ico')
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg='WHITE')
        self.name_label = tk.Label(self.frame, text='Name:', font='Arial 12 bold', bg='WHITE', fg='#1E90FF')
        self.name_entry = tk.Entry(self.frame, width=20, font='Arial 12', bg='#FAFAFA')
        self.code_label = tk.Label(self.frame, text='Code:', font='Arial 12 bold', bg='WHITE', fg='#1E90FF')
        self.code_entry = tk.Entry(self.frame, width=6, font='Arial 12 bold', bg='#FAFAFA', justify=tk.CENTER)

        self.time_frame = tk.Frame(self.root, bg='WHITE')
        self.time_label = tk.Label(self.time_frame, text='Time:', font='Arial 12 bold', bg='WHITE', fg='#1E90FF')
        self.time_entry_1_hrs = tk.Entry(self.time_frame, width=2, font='Arial 12', bg='#FAFAFA', justify=tk.CENTER)
        self.time_entry_1_min = tk.Entry(self.time_frame, width=2, font='Arial 12', bg='#FAFAFA', justify=tk.CENTER)
        self.colon_label_1 = tk.Label(self.time_frame, text=':', font='Arial 12', bg='WHITE')
        self.hyphen_label = tk.Label(self.time_frame, text='—', font='Arial 12', bg='WHITE')
        self.time_entry_2_hrs = tk.Entry(self.time_frame, width=2, font='Arial 12', bg='#FAFAFA', justify=tk.CENTER)
        self.colon_label_2 = tk.Label(self.time_frame, text=':', font='Arial 12', bg='WHITE')
        self.time_entry_2_min = tk.Entry(self.time_frame, width=2, font='Arial 12', bg='#FAFAFA', justify=tk.CENTER)

        self.button_frame = tk.Frame(self.root, bg='WHITE')
        self.conf_button = tk.Button(self.button_frame, text='Confirm', font='Arial 12 bold', bg='#008080', fg='WHITE', command=self.set_detail)
        self.error_label = tk.Label(self.button_frame, text='', bg='WHITE', fg='#801818', font='Arial 12 bold')

        self.frame.pack(fill=tk.BOTH)
        self.name_label.grid(row=0, column=0, pady=10, padx=10)
        self.name_entry.grid(row=0, column=1, pady=10, sticky='w')
        self.code_label.grid(row=1, column=0, pady=10, padx=10)
        self.code_entry.grid(row=1, column=1, pady=10, sticky='w')

        self.time_frame.pack(fill=tk.BOTH)
        self.time_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.time_entry_1_hrs.pack(side=tk.LEFT)
        self.colon_label_1.pack(side=tk.LEFT)
        self.time_entry_1_min.pack(side=tk.LEFT)
        self.hyphen_label.pack(side=tk.LEFT, padx=3)
        self.time_entry_2_hrs.pack(side=tk.LEFT)
        self.colon_label_2.pack(side=tk.LEFT)
        self.time_entry_2_min.pack(side=tk.LEFT)

        self.button_frame.pack(fill=tk.BOTH)
        self.conf_button.pack(pady=10)
        self.error_label.pack(side=tk.BOTTOM, pady=(0, 10))

        self.code_entry.insert(0, self.get_code())
        self.code_entry.config(state='readonly')

        self.time_entry_1_hrs.insert(0, '00')
        self.time_entry_1_min.insert(0, '00')
        self.time_entry_2_hrs.insert(0, '00')
        self.time_entry_2_min.insert(0, '00')

        self.root.bind('<Return>', lambda x: self.set_detail())

        self.root.mainloop()

    def get_code(self):
        code_list = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)]
        exist_code = []
        for i in range(len(det_list)):
            exist_code.append(det_list[i].code)

        while True:
            code = ''.join(random.choices(code_list, k=4))
            if code not in exist_code:
                return code

    def set_detail(self):
        name = self.name_entry.get()
        code = self.code_entry.get()

        if not name:
            self.error_label.config(text='*Name field is empty*')
            return

        if not (self.time_entry_1_hrs.get() or len(self.time_entry_1_hrs.get()) > 2):
            self.time_entry_1_hrs.insert(0, '00')
        if not (self.time_entry_1_min.get() or len(self.time_entry_1_hrs.get()) > 2):
            self.time_entry_1_min.insert(0, '00')
        if not (self.time_entry_2_hrs.get() or len(self.time_entry_1_hrs.get()) > 2):
            self.time_entry_2_hrs.insert(0, '00')
        if not (self.time_entry_2_min.get() or len(self.time_entry_1_hrs.get()) > 2):
            self.time_entry_2_min.insert(0, '00')

        time1 = time(int(self.time_entry_1_hrs.get()), int(self.time_entry_1_min.get()), 0)
        time2 = time(int(self.time_entry_2_hrs.get()), int(self.time_entry_2_min.get()), 0)
        dummy_date = datetime(1900, 1, 1)
        datetime1 = datetime.combine(dummy_date, time1)
        datetime2 = datetime.combine(dummy_date, time2)

        if datetime2 <= datetime1:
            self.error_label.config(text='*Time is invalid*')
            return

        det_list.append(CreateDetail(name=name, code=code, i_time=f'{self.time_entry_1_hrs.get()}:{self.time_entry_1_min.get()}', f_time=f'{self.time_entry_2_hrs.get()}:{self.time_entry_2_min.get()}'))
        update_detail_file()

        self.root.destroy()


class RemName:
    def __init__(self):
        self.names = []
        self.get_names()
        self.WIDTH, self.HEIGHT, self.X_POS, self.Y_POS = 300, 110, 600, 250

        self.root = tk.Toplevel()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X_POS}+{self.Y_POS}")
        self.root.title('Remove Name')
        self.root.iconbitmap('images/admin.ico')
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg='WHITE')
        self.name_label = tk.Label(self.frame, text='Name:', bg='WHITE', font='Arial 12 bold', fg='#1E90FF')
        self.name_box = ttk.Combobox(self.frame, values=self.names, font='Arial 11', state='readonly')
        self.rem_button = tk.Button(self.frame, text='Remove Name', font='Arial 12 bold', bg='#801818', fg='WHITE', command=self.rem)

        self.frame.pack(fill=tk.BOTH)
        self.name_label.grid(row=0, column=0, pady=(10, 0), padx=10)
        self.name_box.grid(row=0, column=1, pady=(10, 0), sticky='w')
        self.rem_button.grid(row=1, column=0, columnspan=2, pady=20)

        if self.names:
            self.name_box.set(self.names[0])

        self.frame.columnconfigure(1, weight=3)
        self.root.bind('<Return>', lambda x: self.rem())
        self.root.mainloop()

    def get_names(self):
        for i in range(len(det_list)):
            self.names.append(f'{det_list[i].name}:{det_list[i].code}')

    def rem(self):
        sel_code = self.name_box.get()
        for i in range(len(det_list)):
            if det_list[i].code == sel_code[sel_code.index(':') + 1:]:
                flag = messagebox.askyesno('Remove Name', f'Do you really want to remove {sel_code}?')
                if flag:
                    del det_list[i]
                    self.root.destroy()
                    update_detail_file()
                    return


class DownloadDetails:
    def __init__(self):
        self.det = {
            'Code': [i.code for i in det_list],
            'Name': [i.name for i in det_list],
            'Entry Time': [i.i_time for i in det_list],
            'Exit Time': [i.f_time for i in det_list]
        }

        self.df = pd.DataFrame(self.det)
        self.df.to_excel('employee_details.xlsx', index=False)


class ChangePass:
    def __init__(self):
        self.WIDTH, self.HEIGHT, self.X_POS, self.Y_POS = 400, 185, 600, 250

        self.root = tk.Toplevel()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X_POS}+{self.Y_POS}")
        self.root.title('Change Password')
        self.root.iconbitmap('images/admin.ico')
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg='WHITE')
        self.orig_label = tk.Label(self.frame, text='Old Password:', bg='WHITE', fg='#1E90FF', font='Arial 11 bold')
        self.orig_entry = tk.Entry(self.frame, width=25, font='Arial 12 bold', show='•', bg='#FAFAFA', justify=tk.CENTER)
        self.new_label = tk.Label(self.frame, text='New Password:', bg='WHITE', fg='#1E90FF', font='Arial 11 bold')
        self.new_entry = tk.Entry(self.frame, width=25, font='Arial 12 bold', show='•', bg='#FAFAFA', justify=tk.CENTER)
        self.change_button = tk.Button(self.frame, text='Change Password', font='Arial 12 bold', bg='#16A085', fg='WHITE', width=20, command=self.change)
        self.error_label = tk.Label(self.frame, text='', bg='WHITE', fg='#801818', font='Arial 12 bold')

        self.frame.pack(fill=tk.BOTH)
        self.orig_label.grid(row=0, column=0, pady=(20, 10), padx=(10, 0), sticky='w')
        self.orig_entry.grid(row=0, column=1, pady=(20, 10), sticky='w')
        self.new_label.grid(row=1, column=0, pady=10, padx=(10, 0), sticky='w')
        self.new_entry.grid(row=1, column=1, pady=10, sticky='w')
        self.change_button.grid(row=2, column=0, columnspan=2, pady=10, padx=(50, 0))
        self.error_label.grid(row=3, column=0, columnspan=2, padx=(50, 0), pady=(0, 10))

        self.root.bind('<Return>', lambda x: self.change())
        self.root.mainloop()

    def change(self):
        old = self.orig_entry.get()
        new = self.new_entry.get()

        if old == '' or new == '':
            self.error_label.config(text='*One or more fields are empty*')
            return

        with open('password.dat', 'rb') as file:
            password = pickle.load(file)

        if old == password:
            flag = messagebox.askyesno('Confirm Password Change', f'Are you sure you want to change admin password to \'{new}\'?')
            if flag:
                with open('password.dat', 'wb') as file:
                    pickle.dump(new, file)
                self.root.destroy()
        else:
            self.error_label.config(text='*Password is incorrect*')


class DownloadAttendance:
    def __init__(self):
        self.WIDTH, self.HEIGHT, self.X_POS, self.Y_POS = 300, 265, 600, 250
        self.names = [det.name for det in det_list]
        self.dates = ['All'] + [str(i) for i in range(1, 32)]
        self.months = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.years = ['All', str(int(datetime.now().year)-1), str(datetime.now().year)]

        self.root = tk.Toplevel()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X_POS}+{self.Y_POS}")
        self.root.title('Download Attendance')
        self.root.iconbitmap('images/admin.ico')
        self.root.resizable(False, False)

        self.frame1 = tk.Frame(self.root, bg='WHITE')
        self.name_label = tk.Label(self.frame1, text='Name:', bg='WHITE', fg='#1E90FF', font='Arial 11 bold')
        self.name_box = ttk.Combobox(self.frame1, values=self.names, width=25, state='readonly')

        self.date_label = tk.Label(self.frame1, text='Date:', bg='WHITE', fg='#1E90FF', font='Arial 11 bold')
        self.date_box = ttk.Combobox(self.frame1, values=self.dates, width=25, state='readonly')

        self.month_label = tk.Label(self.frame1, text='Month:', bg='WHITE', fg='#1E90FF', font='Arial 11 bold')
        self.month_box = ttk.Combobox(self.frame1, values=self.months, width=25, state='readonly')

        self.year_label = tk.Label(self.frame1, text='Year:', bg='WHITE', fg='#1E90FF', font='Arial 11 bold')
        self.year_box = ttk.Combobox(self.frame1, values=self.years, width=25, state='readonly')

        self.frame2 = tk.Frame(self.root, bg='WHITE')
        self.down_button = tk.Button(self.frame2, text='Download', bg='#FFBF00', fg='WHITE', font='Arial 12 bold', command=self.download)
        self.error_label = tk.Label(self.frame2, text='', bg='WHITE', fg='#801818', font='Arial 12 bold')

        self.frame1.pack(fill=tk.BOTH, side=tk.TOP)
        self.name_label.grid(row=0, column=0, pady=10, padx=10)
        self.name_box.grid(row=0, column=1, pady=10)
        self.date_label.grid(row=1, column=0, pady=10, padx=10)
        self.date_box.grid(row=1, column=1, pady=10)
        self.month_label.grid(row=2, column=0, pady=10, padx=10)
        self.month_box.grid(row=2, column=1, pady=10)
        self.year_label.grid(row=3, column=0, pady=10, padx=10)
        self.year_box.grid(row=3, column=1, pady=10)

        self.frame2.pack(fill=tk.BOTH, side=tk.TOP)
        self.down_button.pack(side=tk.TOP, pady=10)
        self.error_label.pack(side=tk.BOTTOM, pady=(0, 10))

        self.root.bind('<Return>', lambda x: self.download())
        self.root.mainloop()

    def download(self):
        name = self.name_box.get()
        date = self.date_box.get()
        month = self.month_box.get()
        year = self.year_box.get()

        self.error_label.config(text='')
        if name == '' or date == '' or month == '' or year == '':
            self.error_label.config(text='*One or more fields are empty*')
            return

        df = {'Date(YYYY-MM-DD)': [], 'Entry time(hrs:min)': [], 'Time Entered(hrs:min)': [], 'Exit time(hrs:min)': [], 'Time exited(hrs:min)': []}

        for det in det_list:
            if det.name == name:
                code = det.code.lower()
                i_time = det.i_time
                f_time = det.f_time
                break

        with open('attendance.dat', 'rb') as file:
            text = pickle.load(file)
        if text == '':
            return

        att_list = text.split('\n')

        for att in att_list:
            att_year, att_month, att_date = att[:10].split('-')
            if (year == att_year or year == 'All') and (month == att_month or month == 'All') and (date == att_date or date == 'All'):
                datas = att.split(';')[1:]
                for data in datas:
                    data = eval(data)
                    if data[0].lower() == code:
                        df['Date(YYYY-MM-DD)'].append(f'{att_year}-{att_month}-{att_date}')
                        df['Time Entered(hrs:min)'].append(data[1])
                        df['Time exited(hrs:min)'].append(data[2])
                        df['Entry time(hrs:min)'].append(i_time)
                        df['Exit time(hrs:min)'].append(f_time)
                        
        df = pd.DataFrame(df)
        df.to_excel(f'{name}_attendance.xlsx', index=False)


class Clean:
    def __init__(self):
        year = int(datetime.now().year)
        with open('attendance.dat', 'rb') as file:
            text = pickle.load(file)
        if text == '':
            return
        att_list = text.split('\n')
        for att in att_list:
            att = att
            att_year = att[:4]
            if int(att_year) < year-1:
                att_list.remove(att)

        with open('attendance.dat', 'wb') as file:
            pickle.dump('\n'.join(att_list), file)


def update_detail_file():
    text = ''
    for det in det_list:
        text += f'{det.name},{det.code},{det.i_time},{det.f_time}\n'

    with open('details.dat', 'wb') as file:
        pickle.dump(text, file)


def get_time_diff(time1, time2):
    date = datetime(2023, 12, 10)
    time1, time2 = str(time1), str(time2)
    time1 = date.replace(hour=int(time1[:time1.index(':')]), minute=int(time1[time1.index(':')+1:]))
    time2 = date.replace(hour=int(time2[:time2.index(':')]), minute=int(time2[time2.index(':')+1:]))

    if str(time1 - time2).startswith('-1 day'):
        return (time2 - time1).seconds//60
    else:
        return 0


if __name__ == '__main__':
    KEY = 2
    det_list = []
    with open('details.dat', 'rb') as f:
        g_text = pickle.load(f)

    g_details = g_text.split('\n')
    for g_detail in g_details:
        if g_detail:
            detail = g_detail
            g_name, g_code, g_i_time, g_f_time = detail.split(',')
            det_list.append(CreateDetail(code=g_code, name=g_name, i_time=g_i_time, f_time=g_f_time))
    MainWindow()
