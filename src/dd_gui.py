import tkinter
from tkinter import *
from tkinter import ttk
from dd_scheduler import DailyDigestScheduler
from dd_email import DailyDigestEmail

class DailyDigestGUI:
    FONT = ('Arial',11, 'bold')
    HEADER_FONT = ('Arial', 13, 'bold')

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Daily Digest")

        self.wikipedia_var = IntVar()
        self.weather_var = IntVar()
        self.quote_var = IntVar()
        self.__add_recipient_var = StringVar()
        self.__recipient_list_var = Variable()
        self.__hour_var = StringVar()
        self.__minute_var = StringVar()
        self.__sender_email_var = StringVar()
        self.__sender_password_var = StringVar()


        # To set initial values for variables
        self.__email = DailyDigestEmail()

        self.__add_recipient_var.set('')
        self.__recipient_list_var.set(self.__email.recipients)

        self.__hour_var.set('07')   # default time to send email
        self.__minute_var.set('30')

        self.quote_var.set(self.__email.content['quote']['include'])
        self.weather_var.set(self.__email.content['weather']['include'])
        self.wikipedia_var.set(self.__email.content['wikipedia']['include'])

        self.__sender_email_var.set(self.__email.credentials['user'])
        self.__sender_password_var.set(self.__email.credentials['password'])

        #  initial scheduler

        self.__scheduler = DailyDigestScheduler()
        self.__scheduler.start()
        self.window.protocol('WM_DELETE_WINDOW',self.shutdown)

        ### digest content

        digest_contents = tkinter.Label(text="Digest Contents:", font=self.HEADER_FONT, pady=10)
        digest_contents.grid(row=0, columnspan=2)

        motivational_quote = tkinter.Checkbutton(text='Motivational Quote', variable=self.quote_var)
        motivational_quote.grid(row=1, column=0, sticky='W', padx=5, pady=5)

        weather_forecast = tkinter.Checkbutton(text='Weather Forecast', variable=self.weather_var)
        weather_forecast.grid(row=1, column=1, sticky='W', padx=5, pady=5)

        wikipedia_article = tkinter.Checkbutton(text='Wikipedia article', variable=self.wikipedia_var)
        wikipedia_article.grid(row=2, column=0, sticky='W', padx=5, pady=5)

        ### recipients

        recipient = tkinter.Label(text='Recipienets:', font=self.HEADER_FONT)
        recipient.grid(row=3, columnspan=2, padx=5, pady=5)

        self.recipient_to_add = tkinter.Entry(width=40, textvariable=self.__add_recipient_var)
        self.recipient_to_add.grid(row=4, columnspan=2, padx=5, pady=5)

        add_recipient_btn = tkinter.Button(text='add recipient', width=15, font=self.FONT ,bg='orange',
                                           foreground='white', command=self.__add_recipient)
        add_recipient_btn.grid(row=5, columnspan=2, padx=5, pady=5)

        self.recipient_scrollbar = ttk.Scrollbar(self.window, orient=VERTICAL)
        self.recipient_scrollbar.grid(row=6, column=1, sticky=W)
        self.recipients_list = tkinter.Listbox(self.window, width=35, height=5, listvariable= self.__recipient_list_var,
                                       selectmode='multiple')
        self.recipients_list.configure(yscrollcommand = self.recipient_scrollbar.set)
        self.recipient_scrollbar.config(command=self.recipients_list.yview)
        self.recipients_list.grid(row=6, column=0, sticky=E, pady=8)


        remove_recipients_btn = tkinter.Button(text="Remove Selected", width=15, bg= 'orange', font=self.FONT,
                                               foreground='white', command=lambda: self.remove_selected(self.recipients_list.curselection()))
        remove_recipients_btn.grid(row=7, columnspan=2, padx=5)

        ###### Schedule time

        schedule_time = tkinter.Label(text='Schedule Time (24hr):', font=self.HEADER_FONT, pady=10)
        schedule_time.grid(row=8, columnspan=2, padx=5, pady=5)

        schedule_hour = tkinter.Spinbox(from_=0, to=23, width=3, textvariable=self.__hour_var)
        schedule_hour.grid(row=9, column=0, sticky='E', padx=5, pady=5)

        schedule_minute = tkinter.Spinbox(from_=0, to=59, width=3, textvariable=self.__minute_var)
        schedule_minute.grid(row=9, column=1, sticky='W', padx=5, pady=5)

        ##### sender credentials

        sender_credentials = Label(text='Sender Credentials:', font=self.HEADER_FONT, pady=10)
        sender_credentials.grid(row=10, columnspan=2, padx=5, pady=5)

        email= Label(text='Email: ')
        email.grid(row=11, column=0, sticky='E', padx=5, pady=5)

        email_entry = Entry(width=33, textvariable=self.__sender_email_var)
        email_entry.grid(row=11, column=1, sticky='W', padx=5, pady=5)

        password = Label(text='Password: ')
        password.grid(row=12, column=0, sticky='E', padx=5, pady=5)

        password_entry= Entry(width=33, textvariable=self.__sender_password_var, show='*')
        password_entry.grid(row=12, column=1, padx=5, pady=5)

        #### update settings

        update_settings_btn = Button(text='Update Settings', width=15, bg='green', font=self.FONT, foreground='white', command=self.update_settings)
        update_settings_btn.grid(row=13, column=0, padx=5, pady=5)

        manual_send_btn = Button(text='Manual Send', width=15, bg='green', font=self.FONT, foreground='white', command=self.manual_send)
        manual_send_btn.grid(row=13, column=1, padx=5, pady=5)

        self.window.mainloop()


        # Functionalities to assign to the buttons

    def __add_recipient(self):
        """to add a recipient to the recipients' list"""
        new_recipient = self.recipient_to_add.get()
        if new_recipient != '':
            recipient_list = self.__recipient_list_var.get()
            if recipient_list != '':
                self.__recipient_list_var.set(recipient_list + (new_recipient,))
            else:
                self.__recipient_list_var.set([new_recipient])
            self.__add_recipient_var.set('')

    def remove_selected(self, selection):      # to remove the selected recipients from recipients' list
        recipients_list = list(self.__recipient_list_var.get())
        for index in reversed(selection):
             recipients_list.pop(index)
        self.__recipient_list_var.set(recipients_list)


    def manual_send(self):          # to build and send an email
        print('manually sending an email ... ')
        self.__email.send_email()

    def update_settings(self):      # to update values
        print("Updating the settings ...")
        self.__email.recipients = list(self.__recipient_list_var.get())
        self.__email.content['wikipedia']['include'] = self.wikipedia_var.get()
        self.__email.content['weather']['include'] = self.weather_var.get()
        self.__email.content['quote']['include'] = self.quote_var.get()
        self.__email.credentials = {'user': self.__sender_email_var.get(),
                                    'password': self.__sender_password_var.get() }
        self.__scheduler.schedule_daily(int(self.__hour_var.get()), int(self.__minute_var.get()),
                                        self.__email.send_email)

    def shutdown(self):
        print('Shutting down the scheduler ... ')
        self.__scheduler.stop()
        self.__scheduler.join()
        self.window.destroy()


if __name__ == '__main__':
    app = DailyDigestGUI()
