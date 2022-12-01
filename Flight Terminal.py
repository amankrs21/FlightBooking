# Program for FLIGHT BOOKING SYSTEM         ---created by Aman Singh Rajput


import os                       # basic directory that help in clear screen in this program
import time                     # this directory will pause program for given time
import pyttsx3                  # this directory will help program to speak up voice
from art import tprint          # this directory print words in bigger format using art
import mysql.connector as sql   # this directory will help program to connect with SQL server and edit the data
from print_color import print   # this directory will help to print statements in different color
from tabulate import tabulate   # this directory will help to print data in the proper Table format

# os.system('cls')    # this syntax will clear the screen


# this funtion will help to print flight details which is stored in SQL table
def flight_details(conn):
    os.system('cls')

    try:
        print("\n\t\t Flight Details",color='purple')
        cursor = conn.cursor()
        cursor.execute("SELECT Flight_ID, Flight_status, Departure, Destination, Flight_time from flight")
        myresult = cursor.fetchall()
        print(tabulate(myresult, headers=['Flight ID', 'Flight Status', 'Departure Point', 'Destination Point' ,'Time'], tablefmt='psql'),color="blue")
        speak("Above is all the Flight Details")

    except:
        print("\n Something Error when Fetching All Flight Details")

    time.sleep(0.5)


# this funtion will help to search flight between departure place and destination place
def search_flight(conn):
    os.system('cls')

    flight_dep = str(input("\n\n Enter Departure Place : "))
    flight_des = str(input(" Enter Destination Place : "))

    try:
        cursor = conn.cursor()
        query = "select Flight_ID, Flight_status, Departure, Destination, Flight_time from flight where Departure = '{}' and Destination = '{}';".format(flight_dep,flight_des)
        cursor.execute(query)
        myresult = cursor.fetchall()
        print(tabulate(myresult, headers=['Flight ID', 'Flight Status', 'Departure Point', 'Destination Point' ,'Time'], tablefmt='psql'),color="blue")

    except:
        print("\n Sorry Flight Not Found from ",flight_dep," to",flight_des,color='red')

    again = str(input("\n\n\n Want to Search Another[y|n] -> "))
    if again == 'y':
        search_flight(conn)
    else:
        print()


# this funtion will help to add flight details in the SQL table
def add_flight(conn):
    os.system('cls')


    flight_no = str(input("\n\n\t Enter Flight ID : "))
    flight_dep = str(input("\t Enter Departure Place : "))
    flight_des = str(input("\t Enter Destination Place : "))
    flight_tim = str(input("\t Enter Flight Time : "))
    flight_status()

    try:
        query = "INSERT INTO flight(Flight_ID,Flight_time,Departure,Destination,Flight_status) values('{}','{}','{}','{}','{}');".format(flight_no,flight_tim,flight_dep,flight_des,f_status)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("\n Flight Added Successfully",color='green')
        speak(" Flight Added Successfully")
        view_fli = str(input("\n Want to VIEW Flight Details\n\t [y|n] -> "))
        if (view_fli == 'y'):
            try:
                cursor.execute("SELECT Flight_ID, Flight_status, Departure, Destination, Flight_time from flight where Flight_ID = '{}';".format(flight_no))
                myresult = cursor.fetchall()
                print(tabulate(myresult, headers=['Flight ID', 'Flight Status', 'Departure Point', 'Destination Point' ,'Time'], tablefmt='psql'),color="blue")
            except:
                print("\n Something Error when Fetching Flight",color='red')
        else :
            admin()

    except:
        print("\n Flight ID ",flight_no," is already Exit",color='green')
        speak("Flight Already existed")

    adm_po = str(input("\n Want to Add Another Flight\n\t [y|n] -> "))
    if (adm_po == 'y'):
        add_flight(conn)
    else:
        admin()


# this funtion will help to update flight details in the SQL table
def update_flight(conn):
    os.system('cls')
    flight_no = str(input("\n\n Enter Flight ID for update : "))
    flight_dep = str(input(" Enter New Daparture Place : "))
    flight_des = str(input(" Enter New Destination Place : "))
    flight_tim = str(input(" Enter Flight Time : "))
    flight_status()

    try :
        query = "UPDATE flight set Flight_time = '{}', Departure = '{}', Destination = '{}', Flight_status = '{}' where Flight_ID = '{}';".format(flight_tim,flight_dep,flight_des,f_status,flight_no)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("\n Updating of Flight Number ",flight_no,"is -> SUCCESSFULLY",color='green')
        speak(" Flight Updated Successfully")

        view_fli = str(input("\n Want to VIEW Flight\n\t [y|n] -> "))
        if (view_fli == 'y'):
            try:
                cursor.execute("SELECT Flight_ID, Flight_status, Departure, Destination, Flight_time from flight where Flight_ID = '{}';".format(flight_no))
                myresult = cursor.fetchall()
                print(tabulate(myresult, headers=['Flight ID', 'Flight Status', 'Departure Point', 'Destination Point' ,'Time'], tablefmt='psql'),color="blue")
            except:
                print("\n Something Error when Finding Flight",color='red')
        else :
            admin()

    except:
        print("\n Updating of Flight Number ",flight_no,"is -> FAILED",color='red')
        speak(" Failed when Updating Flight")

    adm_po = str(input("\n Want to Update Another Flight\n\t [y|n] -> "))
    if (adm_po == 'y'):
        update_flight(conn)
    else:
        admin()


# this funtion will help to delete flight details in the SQL table
def delete_flight(conn):
    os.system('cls')


    flight_no = str(input("\n\n\n\n\t Enter exsting Flight ID to Delete : "))

    try:
        query = "DELETE FROM flight where Flight_ID = '{}';".format(flight_no)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("\n Flight Deleted Successfully",color='green')
        speak(" Flight Deleted Successfully")
    except:
        print("\n\n Error while Deleting Flight... Try Once more",color='red')

    adm_po = str(input("\n Want to Delete Another Flight\n\t [y|n] -> "))
    if (adm_po == 'y'):
        delete_flight(conn)
    else:
        admin()


# this funtion will help to print booked ticket details which is stored in SQL table
def ticket_details(conn):
    os.system('cls')

    print("\n\t\t Booked Ticket Details",color='purple')

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT T_Status, Name, Age, Aadhar, Mob_no, Class, Departure, Destination, Flight_ID from ticket")
        myresult = cursor.fetchall()
        print(tabulate(myresult, headers=['Ticket Status','Name', 'Age', 'Aadhar' ,'Mobile Number', 'Ticket Class', 'Departure Point', 'Destination Point', 'Flight No'], tablefmt='psql'),color="blue")
        speak("Above is all the Booked Ticket Details")

    except:
        print("\n Something Error when fetching all Booked Ticket",color='red')

    time.sleep(0.5)

    adm_po = str(input("\n Want to GO Back\n\t [y|n] -> "))
    if (adm_po == 'y'):
        admin()
    else:
        os.system('cls')
        exit()


# this funtion will help the user to check current ticket status and booking
def search_ticket(conn):
    os.system('cls')

    name = str(input("\n\n\n\t Enter Name : "))
    mob_no = int(input("\t Enter Phone Number : "))

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT T_Status, Name, Age, Aadhar, Mob_no, Class, Departure, Destination, Flight_ID from ticket where Mob_no = {} and Name = '{}';".format(mob_no,name))
        myresult = cursor.fetchall()
        print(tabulate(myresult, headers=['Ticket Status','Name', 'Age', 'Aadhar' ,'Mobile Number', 'Ticket Class', 'Departure Point', 'Destination Point', 'Flight No'], tablefmt='psql'),color="blue")

    except:
        print("\n Sorry Ticket Not Found",color='red')
    
    check_ano = str(input("\n\n Want to Check Another Flight\n\t[y|n] -> "))
    if (check_ano == 'y'):
        search_ticket(conn)
    else:
        client()


# this funtion will help to book flight ticket details in the SQL table
def book_ticket(conn):
    os.system('cls')

    t_status = 'Confirmed'
    limit = int(input("\n Enter the total Number to Book Ticket : "))
    depa = str(input(" Enter your Departure Point : "))
    dest = str(input(" Enter your Destination Point : "))
    try:
        cursor = conn.cursor()
        query = "select Flight_ID, Flight_status, Departure, Destination, Flight_time from flight where Departure = '{}' and Destination = '{}';".format(depa,dest)
        cursor.execute(query)
        myresult = cursor.fetchall()
        print(tabulate(myresult, headers=['Flight ID', 'Flight Status', 'Departure Point', 'Destination Point' ,'Time'], tablefmt='psql'),color="blue")
        flight_no = str(input("\n Choose/Enter Flight ID : "))
        ticket_class()
        mob_no = int(input(" Enter your Phone Number : "))
        for i in range(limit):
            # os.system('cls')
            if i==0:
                print("\n\n\n Now Fillup Some Personal Details to Book Flight Tickets",color='green')
            else:
                print("\n\n\n Now Fillup Personal Details of another Person to Book Ticket",color='green')
            
            name = str(input(" Enter your Name : "))
            age = int(input(" Enter your AGE : "))
            aadhar = int(input(" Enter your Last 4 digit of Aadhar Number : "))
            try:
                query = "INSERT INTO ticket(Mob_no,Name,Departure,Destination,Class,Age,Aadhar,Flight_ID,T_Status) values({},'{}','{}','{}','{}',{},{},'{}','{}');".format(mob_no,name,depa,dest,t_class,age,aadhar,flight_no,t_status)
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
            except:
                print("\n Some Error during Booking Ticket",color='red')

            print("\n\t***********************************************",color='yellow')
            print("\t|\tTicket Booked Successfully",color='yellow')
            print("\t|----------------------------------------------",color='yellow')
            print("\t| Ticket Status     ->    Confirmed",color='yellow')
            print("\t| Flight Number     ->   ",flight_no,color='yellow')
            print("\t| Name              ->   ",name,color='yellow')
            print("\t| Mobile Number     ->   ",mob_no,color='yellow')
            print("\t| Age               ->   ",age,color='yellow')
            print("\t| Aadhar (4-Digit)  ->   ",aadhar,color='yellow')
            print("\t| Departure Point   ->   ",depa,color='yellow')
            print("\t| Destination Point ->   ",dest,color='yellow')
            print("\t| Class Type        ->   ",t_class,color='yellow')
            print("\t***********************************************",color='yellow')
            speak("  Congratulation, Your Ticket Booked Successfully")
    except:
        print("\n Sorry Flight Not Found from ",depa," to",dest,color='red')

    print("\n Total Fare Charges --> Rs",price*limit,color='red')
    home = str(input("\n Want to GO Back\n\t [y|n] -> "))
    if (home == 'y'):
        client()
    else:
        os.system('cls')
        exit()


# this funtion will help to select ticket class type and then stored in the funtioon book_ticket(conn)
def ticket_class():

    print("\n\t+---------------------------------------+",color='yellow')
    print("\t|      --Choose Ticket Class--          |",color='blue')
    print("\t| Press 1 for Standard Class (Rs 4500)  |",color='blue')
    print("\t| Press 2 for Economy Class  (Rs 9000)  |",color='blue')
    print("\t| Press 3 for Business Class (Rs 18000) |",color='blue')
    print("\t| Press 4 for First Class    (Rs 25000) |",color='blue')
    print("\t+---------------------------------------+\n",color='yellow')
    speak(" Please Choose Ticket Class for book your Ticket")
    choice = int(input(" Enter your Choice : "))
    global t_class
    global price
    if (choice == 1):
        t_class = 'Standard'
        price = 4500.00
    elif (choice == 2):
        t_class = 'Economy'
        price = 9000.00
    elif (choice == 3):
        price = 18000.00
        t_class = 'Business'
    elif (choice == 4):
        t_class = 'First'
        price = 25000.00
    else:
        print(" Please enter valid input",color='red')
        speak(" Please Enter Valid Choice")
        ticket_class()


# this funtion will help to select ticket class type and then stored in the funtioon book_ticket(conn)
def flight_status():

    print("\n\t+-------------------------------+",color='yellow')
    print("\t|   -Choose Flight Status-      |",color='blue')
    print("\t+-------------------------------+",color='yellow')
    print("\t| Press 1 if Flight On Time     |",color='blue')
    print("\t| Press 2 if Flight Delayed     |",color='blue')
    print("\t| Press 3 if Flight Rescheduled |",color='blue')
    print("\t| Press 4 if Flight Canceled    |",color='blue')
    print("\t+-------------------------------+\n",color='yellow')
    speak(" Please Choose Current Flight Status")
    choice = int(input(" Enter your Choice : "))
    global f_status
    if (choice == 1):
        f_status = 'On Time'
    elif (choice == 2):
        f_status = 'Delayed'
    elif (choice == 3):
        f_status = 'Rescheduled'
    elif (choice == 4):
        f_status = 'Canceled'
    else:
        print("\n Please enter valid input",color='red')
        speak(" Enter Correct Choice")
        flight_status()


# this funtion will help to delete flight ticket details in the SQL table
def delete_ticket(conn):
    os.system('cls')

    mob_no = int(input("\n\n Enter Phone Number : "))
    name = str(input(" Enter Name : "))

    try:
        query = "DELETE FROM ticket where Mob_no = {} and Name = '{}';".format(mob_no,name)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("\n Flight Deleted Successfully",color='green')
        speak(" Ticket Deleted Successfully")
    except:
        print("\n Something Error while Deleting Ticket",color='red')

    adm_po = str(input("\n Want to Delete Another Ticket\n\t [y|n] -> "))
    if (adm_po == 'y'):
        delete_ticket(conn)
    else:
        admin()


# this funtion will let you in, in the admin user portal and we can take beniefits of admin user
def admin():
    time.sleep(0.5)
    os.system('cls')

    tprint("\n           ADMIN")
    print("\t +=======================================+",color='red')
    print("\t | Press 1 --> For Fetch all Flights     |",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 2 --> For Add a NEW Flight      |",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 3 --> For Update existing Flight|",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 4 --> For Delete existing Flight|",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 5 --> For Fetch all Tickets     |",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 6 --> For Delete existing Ticket|",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 7 --> For Logout                |",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 8 --> For Exit                  |",color='cyan')
    print("\t +=======================================+",color='red')

    choice = int(input("\n\t Enter Your Choice -> "))
    if (choice == 1):
        flight_details(conn)
        adm_po = str(input("\n Want to GO Back\n\t [y|n] -> "))
        if (adm_po == 'y'):
            admin()
        else:
            os.system('cls')
            exit()
    elif (choice == 2):
        add_flight(conn)
    elif (choice == 3):
        update_flight(conn)
    elif (choice == 4):
        delete_flight(conn)
    elif (choice == 5):
        ticket_details(conn)
    elif (choice == 6):
        delete_ticket(conn)
    elif (choice == 7):
        login()
    elif (choice == 8):
        os.system('cls')
        exit()
    else:
        print(" Please Enter valid Input",color='red')
        time.sleep(2.5)
        admin()


# this funtion will let you in, in the client user portal and we can take beniefits of client user
def client():
    time.sleep(0.5)
    os.system('cls')

    tprint("\n          CLIENT")
    print("\t +======================================+",color='red')
    print("\t | Press 1 --> For Search Flight        |",color='cyan')
    print("\t +--------------------------------------+",color='green')
    print("\t | Press 2 --> For Check Ticket Status  |",color='cyan')
    print("\t +--------------------------------------+",color='green')
    print("\t | Press 3 --> For BOOK Flight Ticket   |",color='cyan')
    print("\t +--------------------------------------+",color='green')
    print("\t | Press 4 --> For Logout               |",color='cyan')
    print("\t +--------------------------------------+",color='green')
    print("\t | Press 5 --> For EXIT                 |",color='cyan')
    print("\t +======================================+",color='red')

    choice = int(input("\n\t Enter Your Choice -> "))
    if (choice == 1):
        search_flight(conn)
        client()
    elif (choice == 2):
        search_ticket(conn)
    elif (choice == 3):
        book_ticket(conn)
    elif (choice == 4):
        login()
    elif (choice == 5):
        os.system('cls')
        exit()
    else:
        print(" Please Enter valid Input",color='red')
        time.sleep(1.5)
        client()


# this funtion will let you in, in the visitor user portal and we can take beniefits of visitor user
def visitor():
    time.sleep(0.5)
    os.system('cls')

    tprint("\n          VISITOR")
    print("\t +=======================================+",color='red')
    print("\t | Press 1 --> For Search Flight         |",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 2 --> For Logout                |",color='cyan')
    print("\t +---------------------------------------+",color='green')
    print("\t | Press 3 --> For Exit                  |",color='cyan')
    print("\t +=======================================+",color='red')

    choice = int(input("\n\t Enter Your Choice -> "))
    if (choice == 1):
        search_flight(conn)
        visitor()
    elif (choice == 2):
        login()
    elif (choice == 3):
        os.system('cls')
        exit()
    else:
        print(" Please Enter valid Input",color='red')
        time.sleep(2.5)
        admin()


# this funtion is rosponsible for your login ID
def login():
    os.system('cls')

    tprint("\n        HOME")

    speak(" Please Enter your username")
    username = str(input("\t Enter Your USERNAME : "))
    if (username == 'admin'):
        speak(" Please Enter Your Password")
        admin_password()
    elif (username == 'client'):
        speak(" Please Enter Your Password")
        client_password()
    elif (username == 'visitor'):
        print("\t Login Successfully as...VISITOR",color='green')
        speak(" Login Successfully in Visitor Portal")
        visitor()
    else:
        print("\t Invalid USERNAME, Try Again...",color='red')
        speak(" Please Enter correct username")
        time.sleep(0.5)
        login()


# this funtion is responsible password when your login as admin
def admin_password():
    password = str(input("\t Enter Your PASSWORD : "))
    if (password == 'admin'):
        print("\t Login Successfully as...ADMIN",color='green')
        speak(" Login Successfully in Admin Portal")
        admin()
    else:
        print("\t Invalid Password, Try Again...",color='red')
        speak(" Please Enter correct Password")
        admin_password()


# this funtion is responsible password when your login as client
def client_password():
    password = str(input("\t Enter Your PASSWORD : "))
    if (password == 'client'):
        print("\t Login Successfully as...CLIENT",color='green')
        speak(" Login Successfully in Client Portal")
        client()
    else:
        print("\t Invalid Password, Try Again...",color='red')
        speak(" Please Enter correct Password")
        client_password()


# this funtion is show all the guidline's of this mangament system
def guidline():
    print("\n\t\t --- Read the Guidline's Carefully ---",color='red')
    print("------------------------------------------------------------------------------------------------------------------------------",color='blue')
    print(" 1). In this system there is 3 user (Admin, Client and Visitor)",color='green')
    print(" 2). Every User have there specific task... Just like Visitor can Only View the Flight details",color='green')
    print(" 3). Client can view Flight details and Book Flight ticket",color='green')
    print(" 4). Admin has many access like manage flights, delete tickets etc...",color='green')
    print(" 5). This Management system is Case sensitive... So be carefull when typing your input",color='green')
    print(" 6). If you are delting or updating flight/ticket then please give your input which is already exit",color='green')
    print("     (Just like if program is asking you to Enter Flight Number to delete then Enter the flight Number which is already exit",color='green')
    print("        otherwise it will give you a error and you will exit from this Program)",color='green')
    print("\n\n\n\n\n\n\n\t\t\t\t\t\tCredit :- Aman, Roshani and Mitanshi",color='yellow')
    print("------------------------------------------------------------------------------------------------------------------------------",color='blue')

    speak("     Read the Guideline's Carefully")

    time.sleep(5)      # It will pause the program for 10 second
    login()


# Below statements will be used for voice assistant, it will only speak
engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')
voices= engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate', 125)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Program will Start From Here
print("\n\n\n\n\n\n\t Please Wait...\n\t System is Connecting with SQL Database...",color='cyan')
speak("Please wait System is Connecting with SQL Database")
time.sleep(3)       # It will pause program for 3 second


# below statements will help this program to connect to SQL server with the help of pyodbc directory
try:
    conn = sql.connect(host='localhost',user='root', password='',database='flight')
    cursor = conn.cursor()
    # print(conn)
    print(" Successfully Connected with SQL Database",color='green')
    time.sleep(1.5)
    os.system('cls')                                    # then it will clear the screen

    tprint("\n Flight   Booking   System")              # it will print in big letters
    speak("Hello, Welcome to Flight Booking System")    # it will speak the given code

except: 
    print("Can't connect with SQL Database",color='red')
    time.sleep(2)
    os.system('cls')
    exit()

guidline()      # program will enter into guidline UDF

conn.close()    # this command will close the connection with SQL server
    
# --coded by Aman Kumar Singh
