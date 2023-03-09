from tkinter import messagebox


try:
    import os
    from tkinter import *
    from tkinter import ttk
except ImportError:
    print("\n Module Not Found...\n Installing Module")
    os.system("sudo apt-get install python3-tk")
    from tkinter import *
    from tkinter import ttk
try:
    import mysql.connector as sql
except ImportError:
    print("\n Module Not Found...\n Installing Module")
    os.system("pip3 install mysql-connector")
    import mysql.connector as sql


def Connection():
    try:
        global conn, cursor
        # conn = sql.connect(host='sql6.freemysqlhosting.net',user='sql6425281',password='AvxHGEPT5i',database='sql6425281', auth_plugin='mysql_native_password')
        conn = sql.connect(host='db4free.net',user='amankrs21',password='amansingh',database='amankrs21')
        cursor = conn.cursor()
    except ConnectionError:
        print("Connection Error")
        exit()


def flight_details():
    flight_screen = Toplevel(home)
    flight_screen.title("All Flight Details")
    flight_screen.resizable(0,0)
    flight_screen.geometry("900x800")
    # flight_screen.attributes('-fullscreen', True)
    try:
        Connection()
        query = "SELECT Flight_ID, Flight_status, Departure, Destination, Flight_time from flight"
        cursor.execute(query)

        tree = ttk.Treeview(flight_screen)
        tree['show']='headings'
        s = ttk.Style(flight_screen)
        s.theme_use("clam")
        s.configure(".",font=('Times New Roman',13))
        s.configure("Treeview.Heading",foreground='red',background='yellow',font=('Arial Bold',13))

        tree['columns'] = ("Flight_ID","Flight_status","Departure","Destination","Flight_time")

        tree.column("Flight_ID",width=170,minwidth=100,anchor=CENTER)
        tree.column("Flight_status",width=170,minwidth=100,anchor=CENTER)
        tree.column("Departure",width=170,minwidth=100,anchor=CENTER)
        tree.column("Destination",width=170,minwidth=100,anchor=CENTER)
        tree.column("Flight_time",width=170,minwidth=100,anchor=CENTER)

        tree.heading("Flight_ID",text="Flight ID",anchor=CENTER)
        tree.heading("Flight_status",text="Flight Status",anchor=CENTER)
        tree.heading("Departure",text="Departure",anchor=CENTER)
        tree.heading("Destination",text="Destination",anchor=CENTER)
        tree.heading("Flight_time",text="Flight Time",anchor=CENTER)

        i = 0
        for ro in cursor:
            tree.insert('',i,values=(ro[0],ro[1],ro[2],ro[3],ro[4]))
            i = i + 1

        vsb = ttk.Scrollbar(flight_screen, orient="vertical")
        vsb.configure(command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(fill=Y,side=RIGHT)
        tree.pack(fill=BOTH, expand=1)
        conn.close()
    except ConnectionError:
        Label(flight_screen, text="Connection Error with SQL Server",font=("Arial Bold",30),fg='red')


def search_flight():
    global search_screen
    search_screen = Toplevel(home)
    search_screen.title("Search Flight")
    search_screen.geometry("950x500")
    search_screen.resizable(0,0)
    search_screen.configure(bg="#FDD7E4")

    Label(search_screen,bg="#FDD7E4",text="", width=20).grid(row=0,column=0)
    Label(search_screen,bg="#FDD7E4",text="Seach Flight",width=20,fg='green',font=('arial bold',15)).grid(row=1,column=0)

    global departure_point
    global destination_point
    departure_point = StringVar()
    destination_point = StringVar()

    Label(search_screen,bg="#FDD7E4",text="\n Departure Point * : ",width=20).grid(row=2,column=0)
    dept_entry_ = Entry(search_screen, textvariable=departure_point,width=20)
    dept_entry_.grid(row=3,column=0)
    Label(search_screen,bg="#FDD7E4",text="\n Destination Point * : ",width=20).grid(row=4,column=0)
    dest_entry_ = Entry(search_screen, textvariable=destination_point,width=20)
    dest_entry_.grid(row=5,column=0)
    Label(search_screen,bg="#FDD7E4",text="", width=20).grid(row=6,column=0)
    Button(search_screen, text="Search",width=15,height=1, command=search_flight2,bg='cyan').grid(row=7,column=0)

def search_flight2():
    dept_point = departure_point.get()
    dest_point = destination_point.get()
    try:
        Connection()
        query = "select Flight_ID, Flight_status, Departure, Destination, Flight_time from flight where Departure = '{}' and Destination = '{}';".format(dept_point,dest_point)
        cursor.execute(query)
        myresult = cursor.fetchall()

        Label(search_screen,bg="#FDD7E4",text="\n",width=10).grid(row=8,column=1)
        Label(search_screen,borderwidth=2,relief='ridge',anchor="w",bg='yellow',font=('arial bold',13),width=15,text="Flight ID ",).grid(row=9,column=0)
        Label(search_screen,borderwidth=2,relief='ridge',anchor="w",bg='yellow',font=('arial bold',13),width=15,text="Flight Status").grid(row=9,column=1)
        Label(search_screen,borderwidth=2,relief='ridge',anchor="w",bg='yellow',font=('arial bold',13),width=15,text="Departure Point").grid(row=9,column=2)
        Label(search_screen,borderwidth=2,relief='ridge',anchor="w",bg='yellow',font=('arial bold',13),width=15,text="Destination Point").grid(row=9,column=3)
        Label(search_screen,borderwidth=2,relief='ridge',anchor="w",bg='yellow',font=('arial bold',13),width=15,text="  Time").grid(row=9,column=4)
        i=10
        for flight in myresult: 
            for j in range(len(flight)):
                e = Label(search_screen,width=15, text=flight[j],borderwidth=2,relief='ridge',anchor="w",bg='cyan',font=('arial bold',13))
                e.grid(row=i, column=j)
            i=i+1
        conn.close()
    except ConnectionError:
        messagebox.showinfo("Notification", "Connection Error with SQL Server")


def add_flight():
    global add_flight_screen
    add_flight_screen = Toplevel(home)
    add_flight_screen.geometry("600x650")
    add_flight_screen.resizable(0,0)
    add_flight_screen.configure(bg="#FDD7E4")
    add_flight_screen.title("Add New Flight")
    Label(add_flight_screen,bg="#FDD7E4",font=("Arial Bold",21),text="Enter Details to Add New Flight").pack(fill=X)
    Label(add_flight_screen,bg="#FDD7E4",text="",font=17).pack()

    global flight_id, flight_status, depr, dest, flight_time
    flight_id = StringVar()
    flight_status = StringVar()
    depr = StringVar()
    dest = StringVar()
    flight_time = StringVar()

    Label(add_flight_screen,bg="#FDD7E4",text="Flight ID* : ").pack()
    f_id = Entry(add_flight_screen, textvariable=flight_id)
    f_id.pack()
    Label(add_flight_screen,bg="#FDD7E4",text="Departure* : ").pack()
    dep = Entry(add_flight_screen, textvariable=depr)
    dep.pack()
    Label(add_flight_screen,bg="#FDD7E4",text="Destination* : ").pack()
    des = Entry(add_flight_screen, textvariable=dest)
    des.pack()
    Label(add_flight_screen,bg="#FDD7E4",text="Flight Time* : ").pack()
    f_time = Entry(add_flight_screen, textvariable=flight_time)
    f_time.pack()
    Label(add_flight_screen,font=('Times New Roman',15),bg="#FDD7E4",fg='black',text="\nChoose Current Flight Status").pack()
    Radiobutton(add_flight_screen,variable=flight_status,bg="#FDD7E4",font=('Times New Roman',13),width=25,text="On Time", value="On Time").pack()
    Radiobutton(add_flight_screen,variable=flight_status,bg="#FDD7E4",font=('Times New Roman',13),width=25,text="Delayed", value="Delayed").pack()
    Radiobutton(add_flight_screen,variable=flight_status,bg="#FDD7E4",font=('Times New Roman',13),width=25,text="Rescheduled", value="Rescheduled").pack()
    Radiobutton(add_flight_screen,variable=flight_status,bg="#FDD7E4",font=('Times New Roman',13),width=25,text="Canceled", value="Canceled").pack()

    Label(add_flight_screen,bg="#FDD7E4",text="").pack()
    Button(add_flight_screen,height=2,width=20,font=('Calibri',12),text="Add Flight",bg='cyan',command=add_flight2).pack()

def add_flight2():
    flight_id_info = flight_id.get()
    depart_info = depr.get()
    destin_info = dest.get()
    flight_time_info = flight_time.get()
    flight_status_info = flight_status.get()
    
    try:
        Connection()
        query = "INSERT INTO flight(Flight_ID,Flight_time,Departure,Destination,Flight_status) values('{}','{}','{}','{}','{}');".format(flight_id_info.upper(), flight_time_info, depart_info.upper(), destin_info.upper(), flight_status_info.upper())
        cursor.execute(query)
        conn.commit()
        messagebox.showinfo("Notification", "Flight added succesfully")
        add_flight_screen.destroy()
        conn.close()
    except:
        messagebox.showinfo("Notification", "Flight Already Exist")


def update_flight():
    global update_flight_screen
    update_flight_screen = Toplevel(home)
    update_flight_screen.geometry("600x650")
    update_flight_screen.resizable(0,0)
    update_flight_screen.configure(bg="#FDD7E4")
    update_flight_screen.title("Update Flight")
    Label(update_flight_screen,bg="#FDD7E4",font=("Arial Bold",21),text="Enter Details to Update Flight").pack(fill=X)
    Label(update_flight_screen,bg="#FDD7E4",text="",font=17).pack()

    global flight_id, flight_status, depr, dest, flight_time
    flight_id = StringVar()
    flight_status = StringVar()
    depr = StringVar()
    dest = StringVar()
    flight_time = StringVar()

    Label(update_flight_screen,bg="#FDD7E4",text="Exsting Flight ID* : ").pack()
    f_id = Entry(update_flight_screen, textvariable=flight_id)
    f_id.pack()
    Label(update_flight_screen,bg="#FDD7E4",text="New Departure* : ").pack()
    dep = Entry(update_flight_screen, textvariable=depr)
    dep.pack()
    Label(update_flight_screen,bg="#FDD7E4",text=" New Destination* : ").pack()
    des = Entry(update_flight_screen, textvariable=dest)
    des.pack()
    Label(update_flight_screen,bg="#FDD7E4",text="New Flight Time* : ").pack()
    f_time = Entry(update_flight_screen, textvariable=flight_time)
    f_time.pack()
    Label(update_flight_screen,bg="#FDD7E4",font=('Times New Roman',15),fg='black',text="\nChoose Updated Flight Status").pack()
    Radiobutton(update_flight_screen,variable=flight_status,bg="#FDD7E4",font=('Times New Roman',13),width=25,text="On Time", value="On Time").pack()
    Radiobutton(update_flight_screen,variable=flight_status,bg="#FDD7E4",font=('Times New Roman',13),width=25,text="Delayed", value="Delayed").pack()
    Radiobutton(update_flight_screen,variable=flight_status,bg="#FDD7E4",font=('Times New Roman',13),width=25,text="Rescheduled", value="Rescheduled").pack()
    Radiobutton(update_flight_screen,variable=flight_status,bg="#FDD7E4",font=('Times New Roman',13),width=25,text="Canceled", value="Canceled").pack()

    Label(update_flight_screen,bg="#FDD7E4",text="").pack()
    Button(update_flight_screen,text="Update Flight",font=('calibri',12),width=20,height=2,bg='cyan',command=update_flight2).pack()

def update_flight2():
    flight_id_info = flight_id.get()
    depart_info = depr.get()
    destin_info = dest.get()
    flight_time_info = flight_time.get()
    flight_status_info = flight_status.get()
    
    try:
        Connection()
        query = "SELECT * FROM flight where Flight_ID = '{}';".format(flight_id_info)
        cursor.execute(query)
        mydata = cursor.fetchall()
        if mydata:
            query = "UPDATE flight set Flight_time = '{}', Departure = '{}', Destination = '{}', Flight_status = '{}' where Flight_ID = '{}';".format(flight_time_info,depart_info.upper(),destin_info.upper(),flight_status_info.upper(),flight_id_info)
            cursor.execute(query)
            conn.commit()
            messagebox.showinfo("Notification", "Flight Updated Succesfully")
            update_flight_screen.destroy()
        else:
            messagebox.showinfo("Notification", "Flight ID does't Exit")
        conn.close()
    except:
        messagebox.showinfo("Notification", "Please try again")


def delete_flight():
    global delete_flight_screen
    delete_flight_screen = Toplevel(home)
    delete_flight_screen.geometry("450x350")
    delete_flight_screen.resizable(0,1)
    delete_flight_screen.configure(bg="#FDD7E4")
    delete_flight_screen.title("Delete Flight")
    Label(delete_flight_screen,bg="#FDD7E4",font=("Arial Bold",19),text="Enter Details to Delete Flight").pack(fill=X)
    Label(delete_flight_screen,bg="#FDD7E4",text="",font=30).pack()

    global flight_id_
    flight_id_ = StringVar()

    Label(delete_flight_screen,bg="#FDD7E4", text="Exsting Flight ID* : ").pack()
    f_id = Entry(delete_flight_screen, textvariable=flight_id_)
    f_id.pack()
    Label(delete_flight_screen,bg="#FDD7E4", text="").pack()
    Button(delete_flight_screen,text="Delete Flight",bg='cyan',command=delete_flight2).pack()

def delete_flight2():
    flight_id_info = flight_id_.get()
    Label(delete_flight_screen,bg="#FDD7E4", text="",font=17).pack()
    try:
        Connection()
        query = "SELECT * FROM flight WHERE Flight_ID = '{}';".format(flight_id_info)
        cursor.execute(query)
        mydata = cursor.fetchall()
        if mydata:
            query = "DELETE FROM flight where Flight_ID = '{}';".format(flight_id_info)
            cursor.execute(query)
            conn.commit()
            messagebox.showinfo("Notification", "Flight Deleted Successfully")
            delete_flight_screen.destroy()
        else:
            messagebox.showinfo("Notification", "Flight Doesn't Exist")
        conn.close()
    except ConnectionError:
        messagebox.showinfo("Notification", "Connection Error")


def book_ticket():
    global book_tic_frame1
    book_tic_frame1 = Toplevel(home)
    book_tic_frame1.geometry("300x350")
    book_tic_frame1.resizable(0,0)
    book_tic_frame1.configure(bg="#FDD7E4")
    book_tic_frame1.title("Ticket Booking")
    Label(book_tic_frame1,bg="#FDD7E4",font=("Algerian",21),text="Enter Details").pack(fill=X)

    global dep1, des1
    dep1 = StringVar()
    des1 = StringVar()

    Label(book_tic_frame1,bg="#FDD7E4",text="\n\n\nDeparture Point* : ").pack()
    deprt__ = Entry(book_tic_frame1, textvariable=dep1)
    deprt__.pack()
    Label(book_tic_frame1,bg="#FDD7E4",text="Destination Point* : ").pack()
    destp__ = Entry(book_tic_frame1, textvariable=des1)
    destp__.pack()
    Label(book_tic_frame1,text="",bg="#FDD7E4").pack()
    Button(book_tic_frame1,width=17,text="Next",bg='cyan',command=book_ticket2).pack()
    
def book_ticket2():
    depr_ = dep1.get()
    dest_ = des1.get()
    try:
        Connection()
        query = "SELECT * FROM flight WHERE Departure='{}' and Destination='{}';".format(depr_,dest_)
        cursor.execute(query)
        myresult = cursor.fetchall()
        if myresult:
            global flight_id_, flight_time_
            flight_id_ = myresult[0][0]
            flight_time_ = myresult[0][1]
            book_ticket3()
        else:
            messagebox.showinfo("Notification", "Sorry, No Flight Found")
        conn.close()
        
    except ConnectionError:
        messagebox.showinfo("Notification", "Connection Error")

def book_ticket3():
    book_tic_frame1.destroy()
    global book_tic_frame2
    book_tic_frame2 = Toplevel(home)
    book_tic_frame2.resizable(0,0)
    book_tic_frame2.geometry("450x600")
    book_tic_frame2.configure(bg="#FDD7E4")
    book_tic_frame2.title("Ticket Booking")
    Label(book_tic_frame2,bg="#FDD7E4",font=("Algerian",21),text="Enter Details").pack(fill=X)

    global nAme_, aGe_, mobno_, date_, tclass
    nAme_ = StringVar()
    aGe_ = IntVar()
    mobno_ = IntVar()
    date_ = StringVar()
    tclass = StringVar()

    Label(book_tic_frame2,bg="#FDD7E4",text="\n\n\n Enter Your Name* : ").pack()
    deprt__ = Entry(book_tic_frame2, textvariable=nAme_)
    deprt__.pack()
    Label(book_tic_frame2,bg="#FDD7E4",text="Enter Your Age* : ").pack()
    destp__ = Entry(book_tic_frame2, textvariable=aGe_)
    destp__.pack()
    Label(book_tic_frame2,bg="#FDD7E4",text="Mobile Number* : ").pack()
    destp__ = Entry(book_tic_frame2, textvariable=mobno_)
    destp__.pack()
    Label(book_tic_frame2,bg="#FDD7E4",text="Date(yyyy-mm-dd)* : ").pack()
    destp__ = Entry(book_tic_frame2, textvariable=date_)
    destp__.pack()
    Label(book_tic_frame2,text="\n",bg="#FDD7E4").pack()
    Label(book_tic_frame2,bg="#FDD7E4",font=("Algerian",21),text="Choose Ticket Class\n").pack()
    Radiobutton(book_tic_frame2,variable=tclass,bg="#FDD7E4",font=('Arial Bold',13),width=25,text="Economy Class (Rs 4700)", value="Economy").pack()
    Radiobutton(book_tic_frame2,variable=tclass,bg="#FDD7E4",font=('Arial Bold',13),width=25,text="Business Class (Rs 29,000)", value="Business").pack()
    Radiobutton(book_tic_frame2,variable=tclass,bg="#FDD7E4",font=('Arial Bold',13),width=25,text="First Class (Rs 85,000)", value="First").pack()
    Label(book_tic_frame2,text="",bg="#FDD7E4").pack()
    Button(book_tic_frame2,width=17,text="Submit",bg='cyan',command=book_ticket4).pack()

def book_ticket4():
    usern = username_verify.get()
    t_status = 'Confirmed'
    naMe_ = nAme_.get()
    mobno = mobno_.get()
    depr_ = dep1.get()
    dest_ = des1.get()
    tclass_ = tclass.get()
    AgE_ = aGe_.get()
    dAte = date_.get()
    global t_price
    if tclass_ == 'Economy':
        t_price = 4700
    elif tclass_ == 'Business':
        t_price = 29000
    elif tclass_ == 'First':
        t_price = 85000
    try:
        Connection()
        query = "INSERT INTO ticket VALUES ('{}','{}','{}',{},'{}','{}','{}',{},'{}','{}','{}');".format(usern,t_status.upper(),naMe_.upper(),mobno,depr_.upper(),dest_.upper(),tclass_.upper(),AgE_,flight_id_,dAte,flight_time_)
        cursor.execute(query)
        conn.commit()
        Label(book_tic_frame2,font=('\nArial Bold',13),bg="#FDD7E4",text="Total Ticket Charges = Rs {}".format(t_price)).pack()
        messagebox.showinfo("Notification", "Ticket Booked Successfully and Price Rs {}".format(t_price))
        book_tic_frame2.destroy()
        conn.close()
    except:
        messagebox.showinfo("Notification", "Something Error")


def my_bookings():
    bookings_frame = Toplevel(home)
    bookings_frame.title('My Bookings')
    # bookings_frame.geometry("1600x900")
    try:
        bookings_frame.attributes("-zoomed",True)
    except:
        bookings_frame.state("zoomed")
    bookings_frame.resizable(0,0)
    ticket_get = username_verify.get()
    try:
        Connection()
        query = "SELECT T_Status, Name, Mob_no, Departure, Destination, Class, Age, Flight_ID, f_date, f_time FROM ticket where username='{}'".format(ticket_get)
        cursor.execute(query)

        tree = ttk.Treeview(bookings_frame)
        tree['show']='headings'
        s = ttk.Style(bookings_frame)
        s.theme_use("clam")
        s.configure(".",font=('Times New Roman',13))
        s.configure("Treeview.Heading",foreground='red',background='yellow',font=('Arial Bold',13))

        tree['columns'] = ("T_Status","Name","Mob_no","Departure","Destination","Class","Age","Flight_ID","f_date","f_time")

        tree.column("T_Status",width=120,minwidth=100,anchor=CENTER)
        tree.column("Name",width=170,minwidth=100,anchor=CENTER)
        tree.column("Mob_no",width=170,minwidth=100,anchor=CENTER)
        tree.column("Departure",width=150,minwidth=100,anchor=CENTER)
        tree.column("Destination",width=150,minwidth=100,anchor=CENTER)
        tree.column("Class",width=110,minwidth=100,anchor=CENTER)
        tree.column("Age",width=50,minwidth=100,anchor=CENTER)
        tree.column("Flight_ID",width=100,minwidth=100,anchor=CENTER)
        tree.column("f_date",width=100,minwidth=100,anchor=CENTER)
        tree.column("f_time",width=80,minwidth=100,anchor=CENTER)

        tree.heading("T_Status",text="Ticket Status",anchor=CENTER)
        tree.heading("Name",text="Name",anchor=CENTER)
        tree.heading("Mob_no",text="Mob No",anchor=CENTER)
        tree.heading("Departure",text="Departure",anchor=CENTER)
        tree.heading("Destination",text="Destination",anchor=CENTER)
        tree.heading("Class",text="Class",anchor=CENTER)
        tree.heading("Age",text="Age",anchor=CENTER)
        tree.heading("Flight_ID",text="Flight_ID",anchor=CENTER)
        tree.heading("f_date",text="Date",anchor=CENTER)
        tree.heading("f_time",text="Time",anchor=CENTER)

        i = 0
        for ro in cursor:
            tree.insert('',i,values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5],ro[6],ro[7],ro[8],ro[9]))
            i = i + 1

        vsb = ttk.Scrollbar(bookings_frame, orient="vertical")
        vsb.configure(command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(fill=Y,side=RIGHT)
        tree.pack(fill=BOTH, expand=1)
        conn.close()
    except:
        messagebox.showinfo("Notification", "Error while Fetching Data from SQL Table")


def ticket_details():
    tic_details_frame = Toplevel(home)
    tic_details_frame.title('All Tickets')
    tic_details_frame.resizable(0,0)
    try:
        tic_details_frame.attributes('-zoomed',True)
    except:
        tic_details_frame.state("zoomed")
    # tic_details_frame.attributes('-fullscreen', True)
    # tic_details_frame.state("zoomed")
    # tic_details_frame.geometry("1600x900")
    try:
        Connection()
        query = "SELECT username,T_Status, Name, Mob_no, Departure, Destination, Class, Age, Flight_ID, f_date, f_time FROM ticket"
        cursor.execute(query)

        tree = ttk.Treeview(tic_details_frame)
        tree['show']='headings'
        s = ttk.Style(tic_details_frame)
        s.theme_use("clam")
        s.configure(".",font=('Times New Roman',13))
        s.configure("Treeview.Heading",foreground='red',background='yellow',font=('Arial Bold',13))

        tree['columns'] = ("username","T_Status","Name","Mob_no","Departure","Destination","Class","Age","Flight_ID","f_date","f_time")

        tree.column("username",width=100,minwidth=80,anchor=CENTER)
        tree.column("T_Status",width=100,minwidth=80,anchor=CENTER)
        tree.column("Name",width=160,minwidth=100,anchor=CENTER)
        tree.column("Mob_no",width=150,minwidth=100,anchor=CENTER)
        tree.column("Departure",width=130,minwidth=100,anchor=CENTER)
        tree.column("Destination",width=130,minwidth=100,anchor=CENTER)
        tree.column("Class",width=100,minwidth=80,anchor=CENTER)
        tree.column("Age",width=50,minwidth=100,anchor=CENTER)
        tree.column("Flight_ID",width=120,minwidth=100,anchor=CENTER)
        tree.column("f_date",width=100,minwidth=100,anchor=CENTER)
        tree.column("f_time",width=80,minwidth=100,anchor=CENTER)

        tree.heading("username",text="Username",anchor=CENTER)
        tree.heading("T_Status",text="Ticket Status",anchor=CENTER)
        tree.heading("Name",text="Name",anchor=CENTER)
        tree.heading("Mob_no",text="Mob No",anchor=CENTER)
        tree.heading("Departure",text="Departure",anchor=CENTER)
        tree.heading("Destination",text="Destination",anchor=CENTER)
        tree.heading("Class",text="Class",anchor=CENTER)
        tree.heading("Age",text="Age",anchor=CENTER)
        tree.heading("Flight_ID",text="Flight_ID",anchor=CENTER)
        tree.heading("f_date",text="Date",anchor=CENTER)
        tree.heading("f_time",text="Time",anchor=CENTER)

        i = 0
        for ro in cursor:
            tree.insert('',i,values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5],ro[6],ro[7],ro[8],ro[9],ro[10]))
            i = i + 1

        vsb = ttk.Scrollbar(tic_details_frame, orient="vertical")
        vsb.configure(command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(fill=Y,side=RIGHT)
        tree.pack(fill=BOTH, expand=1)
        conn.close()
    except:
        messagebox.showinfo("Notification", "Error while Fetching Data from SQL Table")


def cancel_booking():
    global cancel_tic_frame
    cancel_tic_frame = Toplevel(home)
    cancel_tic_frame.title('Cancel Booking')
    cancel_tic_frame.geometry("500x350")
    cancel_tic_frame.resizable(0,0)
    cancel_tic_frame.configure(bg="#FDD7E4")
    Label(cancel_tic_frame,bg="#FDD7E4",font=("Times New Roman",15),text="Note :- \n10% Money will Be Charges for Ticket Cancellation").pack()

    global nAme_1, mobno_1
    nAme_1 = StringVar()
    mobno_1 = IntVar()

    Label(cancel_tic_frame,bg="#FDD7E4",text="\n\n Enter Your Name* : ").pack()
    deprt__ = Entry(cancel_tic_frame, textvariable=nAme_1)
    deprt__.pack()
    Label(cancel_tic_frame,bg="#FDD7E4",text="Mobile Number* : ").pack()
    destp__ = Entry(cancel_tic_frame, textvariable=mobno_1)
    destp__.pack()
    Label(cancel_tic_frame,text="",bg="#FDD7E4").pack()
    Button(cancel_tic_frame,width=17,text="Submit",bg='cyan',command=cancel_booking2).pack()

def cancel_booking2():
    user_get = username_verify.get()
    name_ = nAme_1.get()
    mobno_ = mobno_1.get()
    try:
        Connection()
        query = "SELECT * FROM ticket where username='{}' AND Name ='{}' AND Mob_no={}".format(user_get,name_,mobno_)
        cursor.execute(query)
        data_has = cursor.fetchall()
        if data_has:
            query = "UPDATE ticket SET T_Status='CANCELLED' where username='{}' AND Name ='{}' AND Mob_no={}".format(user_get,name_,mobno_)
            cursor.execute(query)
            conn.commit()
            messagebox.showinfo("Notification", "Ticket Cancelled Successfully. Refund will be refunded in your Original Payment method in 5 days")
            cancel_tic_frame.destroy()
        else:
            messagebox.showinfo("Notification", "Enter Valid Credentials")
        conn.close()
    except:
        messagebox.showinfo("Notification", "Connection Error")


def user_details():
    flight_screen = Toplevel(home)
    flight_screen.title("All Flight Details")
    flight_screen.resizable(0,0)
    flight_screen.geometry("600x650")
    flight_screen.configure(bg="#FDD7E4")
    # flight_screen.attributes('-fullscreen', True)
    Label(flight_screen,bg="#FDD7E4",text="").pack()
    Button(flight_screen,bg='cyan',text='Delete User',width=21,height=2,command=delete_user).pack()
    Label(flight_screen,bg="#FDD7E4",text="").pack()
    try:
        Connection()
        query = "SELECT username, password, Mobileno from login"
        cursor.execute(query)

        tree = ttk.Treeview(flight_screen)
        tree['show']='headings'
        s = ttk.Style(flight_screen)
        s.theme_use("clam")
        s.configure(".",font=('Times New Roman',13))
        s.configure("Treeview.Heading",foreground='red',background='yellow',font=('Arial Bold',13))

        tree['columns'] = ("username", "password", "Mobileno")

        tree.column("username",width=150,minwidth=100,anchor=CENTER)
        tree.column("password",width=150,minwidth=100,anchor=CENTER)
        tree.column("Mobileno",width=170,minwidth=100,anchor=CENTER)

        tree.heading("username",text="Usernames",anchor=CENTER)
        tree.heading("password",text="Passwords",anchor=CENTER)
        tree.heading("Mobileno",text="Mobile No",anchor=CENTER)

        i = 0
        for ro in cursor:
            tree.insert('',i,values=(ro[0],ro[1],ro[2]))
            i = i + 1

        vsb = ttk.Scrollbar(flight_screen, orient="vertical")
        vsb.configure(command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(fill=Y,side=RIGHT)
        tree.pack(fill=BOTH, expand=1)
        conn.close()
    except ConnectionError:
        messagebox.showinfo("Notification", "Connection Error")

def delete_user():
    messagebox.showinfo("Alert", "If you delete Client User then all tickets are also deleted of that User.")
    global delete_user_screen
    delete_user_screen = Toplevel(home)
    delete_user_screen.geometry("450x350")
    delete_user_screen.resizable(0,1)
    delete_user_screen.configure(bg="#FDD7E4")
    delete_user_screen.title("Delete Client User")
    Label(delete_user_screen,bg="#FDD7E4",text="",font=17).pack()

    global client_user
    client_user = StringVar()

    Label(delete_user_screen,bg="#FDD7E4",text="Exsting Username* : ").pack()
    f_id = Entry(delete_user_screen, textvariable=client_user)
    f_id.pack()
    Label(delete_user_screen,bg="#FDD7E4",text="").pack()
    Button(delete_user_screen,text="Delete User",bg='cyan',width=15,command=delete_user2).pack()

def delete_user2():
    clientuser = client_user.get()
    Label(delete_user_screen,bg="#FDD7E4",text="",font=17).pack()
    try:
        Connection()
        query = "SELECT * FROM login WHERE username = '{}';".format(clientuser)
        cursor.execute(query)
        mydata = cursor.fetchall()
        if mydata:
            query1 = "DELETE FROM login where username = '{}';".format(clientuser)
            cursor.execute(query1)
            conn.commit()
            query2 = "DELETE FROM ticket where username = '{}';".format(clientuser)
            cursor.execute(query2)
            conn.commit()
            messagebox.showinfo("Notification", "USER Deleted Successfully")
            delete_user_screen.destroy()
        else:
            messagebox.showinfo("Notification", "Username Doesn't Exist")
        conn.close()
    except:
        messagebox.showinfo("Notification", "Connection Error")


def register_client():
    global register_screen
    register_screen = Toplevel(home)
    register_screen.title("Client Registeration")
    register_screen.geometry("300x300")
    register_screen.resizable(0,0)
    register_screen.configure(bg="#FDD7E4")
    Label(register_screen,bg="#FDD7E4",font=("Arial Bold",17),text="Enter Details to Register\ninto CLIENT Portal\n").pack(fill=X)

    global username_register, password_register, mob_register
    username_register = StringVar()
    password_register = StringVar()
    mob_register = IntVar()

    Label(register_screen,bg="#FDD7E4",text="Username * : ").pack()
    username_registration = Entry(register_screen, textvariable=username_register)
    username_registration.pack()
    Label(register_screen,bg="#FDD7E4",text="Mobile Number * : ").pack()
    username_registration = Entry(register_screen, textvariable=mob_register)
    username_registration.pack()
    Label(register_screen,bg="#FDD7E4",text="Password * : ").pack()
    password_registration = Entry(register_screen, textvariable=password_register, show="*")
    password_registration.pack()
    Button(register_screen, text="Register",width=10,height=1, command=register_client2,bg='cyan').pack()

def register_client2():
    username3 = username_register.get()
    password3 = password_register.get()
    mob_no = mob_register.get()
    try:
        Connection()
        query = "INSERT INTO login VALUES ('{}','{}',{})".format(username3,password3,mob_no)
        cursor.execute(query)
        conn.commit()
        messagebox.showinfo("Notification", "You have Registered Successfully in the System")
        register_screen.destroy()
        conn.close()
    except:
        messagebox.showinfo("Notification", "Username Already exist")


def login():
    global login_screen
    login_screen = Toplevel(home)
    login_screen.title(" Login into Admin")
    login_screen.geometry("300x250")
    login_screen.resizable(0,0)
    login_screen.configure(bg="#FDD7E4")
    Label(login_screen,bg="#FDD7E4",font=("Arial Bold",17),text="Enter Details to Login\ninto ADMIN Portal\n").pack(fill=X)

    global password_verify_
    password_verify_ = StringVar()

    Label(login_screen,bg="#FDD7E4",text="\nPassword * : ").pack()
    password_login_entry_ = Entry(login_screen, textvariable=password_verify_, show="*")
    password_login_entry_.pack()
    Button(login_screen,text="Login",width=10,height=1, command=login_verify,bg='cyan').pack()

def login_verify():
    password = password_verify_.get()
    if (password == 'admin') or (password == 'ADMIN'):
        Label(login_screen,bg="#FDD7E4",text="Login Success",fg='green',font=('arial bold',11)).pack()
        login_screen.destroy()
        admin()
    else:
        messagebox.showinfo("Notification", "Wrong Password... Please try again")


def login2():
    global login_screen2
    login_screen2 = Toplevel(home)
    login_screen2.title("Login into Client")
    login_screen2.geometry("300x250")
    login_screen2.resizable(0,0)
    login_screen2.configure(bg="#FDD7E4")
    Label(login_screen2,bg="#FDD7E4",font=("Arial Bold",17),text="Enter Details to Login\ninto CLIENT Portal\n").pack(fill=X)

    global username_verify
    global password_verify
    username_verify = StringVar()
    password_verify = StringVar()

    Label(login_screen2,bg="#FDD7E4",text="Username * : ").pack()
    username_login_entry = Entry(login_screen2, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen2,bg="#FDD7E4",text="Password * : ").pack()
    password_login_entry = Entry(login_screen2, textvariable=password_verify, show="*")
    password_login_entry.pack()
    Button(login_screen2, text="Login",width=10,height=1, command=login2_verify,bg='cyan').pack()

def login2_verify():
    username = username_verify.get()
    password = password_verify.get()
    try:
        Connection()
        query = "SELECT username, password FROM login where username='{}';".format(username)
        cursor.execute(query)
        user = cursor.fetchall()
        us = user[0][0]
        ps = user[0][1]
        if (us == username) and (ps == password):
            Label(login_screen2,bg="#FDD7E4",text="Login Success",fg='green',font=('arial bold',11)).pack()
            login_screen2.destroy()
            client()
        else:
            messagebox.showinfo("Notification", "Wrong Password... Please try again")
        conn.close()
    except:
        messagebox.showinfo("Notification", "Username Not found")


def login_register():
    global login_reg_screen
    login_reg_screen = Toplevel(home)
    login_reg_screen.title("Login OR Register")
    login_reg_screen.geometry("300x250")
    login_reg_screen.resizable(0,0)
    login_reg_screen.configure(bg="#FDD7E4")
    Label(login_reg_screen,bg="#FDD7E4",font=("Arial Bold",17),text="Select Your Choice\n\n").pack()
    Button(login_reg_screen,text="Login",command=login2,bg='cyan',height='2',width='30').pack()
    Label(login_reg_screen,bg="#FDD7E4",text="").pack()
    Button(login_reg_screen, text="Register",command=register_client,bg='cyan',height='2',width='30').pack()

 
def admin():
    login_screen.destroy()
    admin_frame = Toplevel(home)
    admin_frame.title("Admin Portal")
    admin_frame.configure(bg="#FFE5B4")
    # admin_frame.geometry("1600x900")
    try:
        admin_frame.attributes('-zoomed',True)
    except:
        admin_frame.state("zoomed")
    admin_frame.resizable(0,0)
    Label(admin_frame ,font=("Algerian",50),bg='#FFE5B4',text="ADMIN  PORTAL").pack()
    Label(admin_frame ,text="\n\n+------------------------------------------+",bg="#FFE5B4").pack()
    Button(admin_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Fetch all Flight Details",command=flight_details).pack()
    Label(admin_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(admin_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Add New Flight",command=add_flight).pack()
    Label(admin_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(admin_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Update Existing Flight",command=update_flight).pack()
    Label(admin_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(admin_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Delete Existing Flight",command=delete_flight).pack()
    Label(admin_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(admin_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Fetch all Booked Ticket",command=ticket_details).pack()
    Label(admin_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(admin_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="View / Delete Clients",command=user_details).pack()
    Label(admin_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(admin_frame,font=('Times New Roman',15),height=2,width=50,bg="#FFFF66",text="Logout",command=admin_frame.destroy).pack()
    Label(admin_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(admin_frame,font=('Times New Roman',15),height=2,width=50,bg="#F08080",text="Exit",command=home.destroy).pack()
    Label(admin_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    admin_frame.mainloop()


def client():
    login_reg_screen.destroy()
    login_screen2.destroy()
    client_frame = Toplevel(home)
    client_frame.title("Client Portal")
    client_frame.configure(bg="#FFE5B4")
    # client_frame.geometry("1600x900")
    try:
        client_frame.attributes("-zoomed",True)
    except:
        client_frame.state("zoomed")
    client_frame.resizable(0, 0)
    Label(client_frame ,font=("Algerian",50),bg='#FFE5B4',text="CLIENT PORTAL").pack()
    Label(client_frame ,text="\n\n\n+------------------------------------------+",bg="#FFE5B4").pack()
    Button(client_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Search Flight",command=search_flight).pack()
    Label(client_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(client_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Book Ticket",command=book_ticket).pack()
    Label(client_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(client_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Cancel Ticket",command=cancel_booking).pack()
    Label(client_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(client_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="My Bookings",command=my_bookings).pack()
    Label(client_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(client_frame,font=('Times New Roman',15),height=2,width=50,bg="#FFFF66",text="Logout",command=client_frame.destroy).pack()
    Label(client_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(client_frame,font=('Times New Roman',15),height=2,width=50,bg="#F08080",text="Exit",command=home.destroy).pack()
    Label(client_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()


def visitor():
    visitor_frame = Toplevel(home)
    visitor_frame.title("Visitor Portal")
    visitor_frame.configure(bg="#FFE5B4")
    visitor_frame.geometry("1600x900")
    try:
        visitor_frame.attributes("-zoomed",True)
    except:
        visitor_frame.state("zoomed")
    visitor_frame.resizable(0, 0)
    Label(visitor_frame ,font=("Algerian",50),bg='#FFE5B4',text="VISITOR PORTAL").pack()
    Label(visitor_frame ,text="\n\n\n\n\n+------------------------------------------+",bg="#FFE5B4").pack()
    Button(visitor_frame,font=('Times New Roman',15),height=2,width=50,bg="#808080",text="Search Flight",command=search_flight).pack()
    Label(visitor_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(visitor_frame,font=('Times New Roman',15),height=2,width=50,bg="#FFFF66",text="Logout",command=visitor_frame.destroy).pack()
    Label(visitor_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()
    Button(visitor_frame,font=('Times New Roman',15),height=2,width=50,bg="#F08080",text="Exit",command=home.destroy).pack()
    Label(visitor_frame ,text="+------------------------------------------+",bg="#FFE5B4").pack()


def HOME():
    global home
    home = Tk()
    home.title("Account Login")
    home.resizable(0,0)
    home.geometry("300x270")
    home.configure(bg="#FDD7E4")
    Label(home,bg="#FDD7E4",font=("Arial Bold",17),text="Select Your Choice").pack(fill=X)
    Label(bg="#FDD7E4",text="").pack()
    Button(text="Admin", height="2", width="30", command = login,bg='cyan').pack()
    Label(bg="#FDD7E4",text="").pack()
    Button(text="Client", height="2", width="30", command = login_register,bg='cyan').pack()
    Label(bg="#FDD7E4",text="").pack()
    Button(text="Visitor", height="2", width="30", command=visitor,bg='cyan').pack()
    home.mainloop()

HOME()
conn.close()
