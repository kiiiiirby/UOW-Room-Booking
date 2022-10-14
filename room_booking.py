import sqlite3
import time
from datetime import datetime
from os import system

# create database connect, current memory,":memory:"
# change to r'room_booking_database.db' for production
db = sqlite3.connect(":memory:")

# create cursor
db_cursor = db.cursor()

# login table
db_cursor.execute(
    """CREATE TABLE Login (
    username text,
    password text,
    typeOfUser text,
    name text
    )"""
)

db_cursor.execute("INSERT INTO Login VALUES ('Staff1', 'Password1', 'Staff', 'Alice')")
db_cursor.execute(
    "INSERT INTO Login VALUES ('Student1', 'Password1', 'Student', 'Bob')"
)

# Rooms table
db_cursor.execute(
    """CREATE TABLE Rooms (roomCode text,
    roomPrice integar,
    roomCap integar,
    promoCode text,
    promoCodeAmount real,
    roomDTStart integar,
    roomDTEnd integar,
    roomLaunched integar
   )"""
)

# 02-02-2022 0700-0900
db_cursor.execute(
    "INSERT INTO Rooms VALUES ('HQ BLK A LT A.1.1', 10, 100, 'PROMO1', 0.9, 1643756400, 1643763600, 1)"
)

# 01-01-2022 0700-0900
db_cursor.execute(
    "INSERT INTO Rooms VALUES ('HQ BLK B LT B.2.2', 10, 100, 'PROMO1', 0.8, 1640991600, 1640998800, 0)"
)

# Bookings table
db_cursor.execute(
    """CREATE TABLE Bookings (
    roomCode text,
    bookingDTStart integar,
    bookingDTEnd integar,
    bookingName text
    )"""
)

# 02-02-2022 0800-1000
db_cursor.execute(
    "INSERT INTO Bookings VALUES ('HQ BLK A LT A.1.1', 1643760000, 1643767200, 'Bob')"
)

print(
    """
---------------------------------
| Welcome to UOW booking system |
---------------------------------
"""
)

input("Press Enter to start...\n")

# login
while True:
    username_input = input("Enter your username: ")
    pw_input = input("Enter your password: ")

    # Login check
    db_cursor.execute(
        f"""SELECT password, typeOfUser, name FROM Login WHERE
         username = '{username_input}' AND password = '{pw_input}'"""
    )
    db_return = db_cursor.fetchall()
    if len(db_return) != 0:
        if pw_input == db_return[0][0]:
            type_of_user = db_return[0][1]
            system("cls")
            break
    else:
        system("cls")
        print("\nUsername or Password incorrect!\n")
        continue


# Room creation and management (staff)
def staff_func():
    while True:
        print(div)
        print("\nPlease enter an option")
        menu_input = input(
            """1) Create a room
2) Launch a room
3) Edit attributes of a room
4) Exit
"""
        )
        system("cls")

        # 1) Create a room
        if menu_input == "1":
            print(div)
            while True:
                room_code_input = input("Enter the new room code: ")
                db_cursor.execute(
                    f"SELECT COUNT(*) FROM Rooms WHERE roomCode = '{room_code_input}'"
                )
                db_return = db_cursor.fetchall()
                if db_return[0][0] != 0:
                    print("The room is already created.")
                    break

                room_price_input = int(input("Enter the price of the new room (/hr): "))
                room_cap_input = int(
                    input("Please enter the capacity of the room (Pax): ")
                )
                room_promocode_input = input(
                    "Please type in a promotion code for the new room, press Enter to skip: "
                )
                if len(room_promocode_input) != 0:
                    promocode_amount = float(
                        input(
                            "Please type in the amount of discount for the promotion code (%): "
                        )
                    )
                    promocode_amount = 1 - (promocode_amount / 100)

                else:
                    promocode_amount = 1.0

                date_input = input(
                    "Enter the dates the room is unavailable, press Enter to skip: (DD-MM-YYYY - DD-MM-YYYY) "
                )

                if len(date_input) == 0:
                    start_unix = 0
                    end_unix = 0

                else:
                    time_input = input(
                        "Enter the hours the room is unavailable: (0700 - 1800) "
                    )
                    start_dt = datetime.strptime(
                        date_input[:10] + "-" + time_input[:4], "%d-%m-%Y-%H%M"
                    )
                    end_dt = datetime.strptime(
                        date_input[13:] + "-" + time_input[7:], "%d-%m-%Y-%H%M"
                    )
                    start_unix = time.mktime(start_dt.timetuple())
                    end_unix = time.mktime(end_dt.timetuple())

                db_cursor.execute(
                    f"""INSERT INTO Rooms VALUES ('{room_code_input}', {room_price_input}, {room_cap_input},
                     '{room_promocode_input}', {promocode_amount}, {start_unix}, {end_unix} , 0)"""
                )
                db.commit()
                system("cls")
                print(f"Room {room_code_input} created.")
                break

        # 2) Launch a room
        elif menu_input == "2":
            print(div)
            room_code_input = input("\nEnter the room code to launch: ")
            system("cls")
            db_cursor.execute(
                f"""SELECT roomPrice, roomCap, promoCode, promoCodeAmount,
                 roomLaunched FROM Rooms WHERE roomCode = '{room_code_input}'"""
            )
            db_return = db_cursor.fetchall()

            # raise exception if room code is invalid
            if len(db_return) == 0:
                print("The room code is invalid")
                break
            else:
                promocode_amount = round((1 - db_return[0][3]) * 100)
                print(
                    f"""
Room Parameters

Room Code: {room_code_input}
Price of room: ${db_return[0][0]}/hr
Room capacity: {db_return[0][1]} pax
Promotion code: {db_return[0][2]}
Promotion code amount: {promocode_amount}%"""
                )

            if db_return[0][4] == 0:
                menu_input = input("\nLaunch room?: (Y/N)")
                if menu_input == "Y":
                    db_cursor.execute(
                        f"UPDATE Rooms SET roomLaunched = 1 WHERE roomCode = '{room_code_input}'"
                    )
                    db.commit()
                    system("cls")
                    print("\nRoom launched.")
                    # DEBUG
                    # db_cursor.execute(
                    #    f"SELECT roomLaunched FROM Rooms WHERE roomCode = '{room_code_input}'"
                    # )
                    # db_return = db_cursor.fetchall()
                    # print(db_return)

            else:
                system("cls")
                print("Room already active.")

        # 3) Adjust the attributes of room
        elif menu_input == "3":
            print(div)
            while True:
                room_code_input = input("Enter the room code to edit attributes: ")
                system("cls")
                db_cursor.execute(
                    f"""SELECT roomPrice, roomCap, promoCode, promoCodeAmount, roomDTStart, roomDTEnd
                     FROM Rooms WHERE roomCode = '{room_code_input}'"""
                )
                db_return = db_cursor.fetchall()

                # raise exception if room code is invalid
                if len(db_return) == 0:
                    print("The room code is invalid")
                    continue
                break
            print(div)

            while True:
                menu_input = input(
                    """Please select an attribute to adjust:
1) Price of room
2) Capacity of room
3) Promotional code and Amount
4) Date and Time
5) Exit
"""
                )
                system("cls")

                # Change price of room
                if menu_input == "1":
                    print(div)
                    print(f"The current price of the room is: ${db_return[0][0]}/hr.")
                    room_price_input = int(
                        input("Enter the new price of the room (/hr): ")
                    )

                    db_cursor.execute(
                        f"UPDATE Rooms SET roomPrice = {room_price_input} WHERE roomCode = '{room_code_input}'"
                    )
                    db.commit()

                    db_cursor.execute(
                        f"SELECT roomPrice FROM Rooms WHERE roomCode = '{room_code_input}'"
                    )
                    db_return = db_cursor.fetchall()
                    system("cls")
                    print(f"\nThe new price of the room is: ${db_return[0][0]}/hr. ")
                    break

                # Change pax of room
                elif menu_input == "2":
                    print(div)
                    print(
                        f"The current capacity of the room is: {db_return[0][1]} pax."
                    )
                    room_cap_input = int(
                        input("Enter the new capacity of the room (pax): ")
                    )
                    db_cursor.execute(
                        f"UPDATE Rooms SET roomCap = {room_cap_input} WHERE roomCode = '{room_code_input}'"
                    )
                    db.commit()

                    db_cursor.execute(
                        f"SELECT roomCap FROM Rooms WHERE roomCode = '{room_code_input}'"
                    )
                    db_return = db_cursor.fetchall()
                    system("cls")
                    print(f"\nThe new capacity of the room is: {db_return[0][0]} pax. ")
                    break

                # Change discount code and amount
                elif menu_input == "3":
                    print(div)
                    print(
                        f"The current discount code of the room is: {db_return[0][2]} and the amount is {db_return[0][3]}"
                    )
                    room_promocode_input = input(
                        "Enter the new promotion code for the room, press Enter to skip: "
                    )

                    if len(room_promocode_input) != 0:
                        promocode_amount = float(
                            input(
                                "Please type in the amount of discount for the promotion code: (0 - 1)"
                            )
                        )
                    else:
                        promocode_amount = 0
                    db_cursor.execute(
                        f"""UPDATE Rooms SET promoCode = {room_promocode_input}, promoCodeAmount = {promocode_amount}
                         WHERE roomCode = '{room_code_input}'"""
                    )
                    db.commit()

                    db_cursor.execute(
                        f"SELECT promoCode, promoCodeAmount FROM Rooms WHERE roomCode = '{room_code_input}'"
                    )
                    db_return = db_cursor.fetchall()
                    system("cls")
                    print(
                        f"\nThe new promotion code of the room is {db_return[0][0]} and the amount is {db_return[0][1]}"
                    )
                    break

                # Change date and time unavailable
                elif menu_input == "4":
                    print(div)
                    start_dt = time.strftime(
                        "%d-%m-%Y %H%M", time.localtime(db_return[0][4])
                    )
                    end_dt = time.strftime(
                        "%d-%m-%Y %H%M", time.localtime(db_return[0][5])
                    )
                    print(
                        f"The current date and time the room is unavailable: {start_dt} to {end_dt}"
                    )
                    date_input = input(
                        "Enter the new dates the room is unavailable: (DD-MM-YYYY - DD-MM-YYYY)"
                    )
                    time_input = input(
                        "Enter the new hours the room is unavailable: (0000 - 2300) "
                    )
                    start_dt = datetime.strptime(
                        date_input[:10] + "-" + time_input[:4], "%d-%m-%Y-%H%M"
                    )
                    end_dt = datetime.strptime(
                        date_input[13:] + "-" + time_input[7:], "%d-%m-%Y-%H%M"
                    )

                    start_unix = time.mktime(start_dt.timetuple())
                    end_unix = time.mktime(end_dt.timetuple())

                    db_cursor.execute(
                        f"""UPDATE Rooms SET roomDTStart = {start_unix}, roomDTEnd = {end_unix}
                         WHERE roomCode = '{room_code_input}'"""
                    )
                    db.commit()

                    db_cursor.execute(
                        f"SELECT roomDTStart, roomDTEnd FROM Rooms WHERE roomCode = '{room_code_input}'"
                    )
                    db_return = db_cursor.fetchall()

                    start_dt = time.strftime(
                        "%d-%m-%Y %H%M", time.localtime(db_return[0][0])
                    )
                    end_dt = time.strftime(
                        "%d-%m-%Y %H%M", time.localtime(db_return[0][1])
                    )
                    system("cls")
                    print(
                        f"\nThe new date and time the room is unavailable: {start_dt} to {end_dt}"
                    )

        # 4) Exit
        elif menu_input == "4":
            system("cls")
            print(div)
            break

        else:
            system("cls")
            print(div)
            print("\nInvalid input.")
            continue


# Room Booking (student)
def student_func():
    while True:
        print(div)
        print("\nPlease enter an option")
        menu_input = input(
            """1) View available rooms
2) Book rooms
3) Modify/Cancel an existing booking
4) Exit
"""
        )
        system("cls")

        # View available rooms (launched)
        if menu_input == "1":
            print(div)
            db_cursor.execute(
                "SELECT roomCode, roomPrice, roomCap FROM Rooms WHERE roomLaunched = 1"
            )
            db_return = db_cursor.fetchall()
            print(
                "\n"
                + "Room Code"
                + "\t "
                + "\t "
                + "Price of room"
                + "\t "
                + "Capacity of room"
            )
            for i in range(len(db_return)):
                print(
                    f"{db_return[i][0]}\t ${db_return[i][1]}/hr\t        {db_return[i][2]} Pax"
                )
            input("\nPress Enter to continue...")
            system("cls")

        # Book rooms
        elif menu_input == "2":
            print(div)
            while True:
                avail_check = 0
                room_code_input = input("Enter the desired room code: ")
                date_input = input("Enter the desired date: (DD-MM-YYYY - DD-MM-YYYY) ")
                time_input = input("Enter the desired hours: (0700 - 1800) ")
                start_dt = datetime.strptime(
                    date_input[:10] + "-" + time_input[:4], "%d-%m-%Y-%H%M"
                )
                end_dt = datetime.strptime(
                    date_input[13:] + "-" + time_input[7:], "%d-%m-%Y-%H%M"
                )
                start_unix = time.mktime(start_dt.timetuple())
                end_unix = time.mktime(end_dt.timetuple())
                # to satisfy 0900 booking on a room where previous booking ends on 0900
                start_unix += 1
                end_unix -= 1

                db_cursor.execute(
                    f"""SELECT COUNT(*) FROM Rooms
                 WHERE roomCode = '{room_code_input}' AND
                  {start_unix} BETWEEN roomDTStart AND roomDTEnd
                   OR {end_unix} BETWEEN roomDTStart AND roomDTEnd
                    OR roomDTStart BETWEEN {start_unix} AND {end_unix}"""
                )
                db_return = db_cursor.fetchall()

                if db_return[0][0] != 0:
                    print("The room is not available at the desired hours.")
                    avail_check += 1

                else:
                    db_cursor.execute(
                        f"""SELECT COUNT(*) FROM Bookings
                         WHERE roomCode = '{room_code_input}' AND
                          {start_unix} BETWEEN bookingDTStart AND bookingDTEnd
                           OR {end_unix} BETWEEN bookingDTStart AND bookingDTEnd
                            OR bookingDTStart BETWEEN {start_unix} AND {end_unix}"""
                    )
                    db_return = db_cursor.fetchall()

                    if db_return[0][0] != 0:
                        print("The room is already booked at the desired hours.")
                        avail_check += 1

                if avail_check > 0:
                    input("Press Enter to continue.")
                    system("cls")
                    continue

                db_cursor.execute(
                    f"INSERT INTO Bookings VALUES ('{room_code_input}', {start_unix}, {end_unix}, '{name}')"
                )
                db.commit()

                # Calculate total time booked in hours
                booking_total_time = (float(end_unix) - float(start_unix)) / (60 * 60)

                while True:
                    promocode_amount = input(
                        "Enter a promotion code: (Press Enter to skip) "
                    )

                    if len(promocode_amount) != 0:
                        db_cursor.execute(
                            f"""SELECT promoCodeAmount, roomPrice FROM Rooms
                         WHERE promoCode = '{promocode_amount}' AND roomCode = '{room_code_input}'"""
                        )
                        db_return = db_cursor.fetchall()

                        if len(db_return) != 0:
                            booking_price = round(
                                (
                                    booking_total_time
                                    * db_return[0][0]
                                    * db_return[0][1]
                                ),
                                1,
                            )
                            break
                        else:
                            print("\nInvalid promotion code")
                            continue

                    else:
                        db_cursor.execute(
                            f"""SELECT roomPrice FROM Rooms
                         WHERE roomCode = '{room_code_input}'"""
                        )
                        db_return = db_cursor.fetchall()
                        booking_price = round((booking_total_time * db_return[0][0]), 1)
                        break

                start_dt = time.strftime("%d-%m-%Y %H%M", time.localtime(start_unix))
                end_dt = time.strftime("%d-%m-%Y %H%M", time.localtime(end_unix))
                system("cls")

                print(
                    f"""
Your booking for Room {room_code_input} will be from {start_dt} to {end_dt}
The estimated cost is ${booking_price}
                """
                )

                menu_input = input("Book another room?: (Y/N) ")
                if menu_input == "Y":
                    continue
                else:
                    break

        # Modify or Cancel current booking
        elif menu_input == "3":
            print(div)
            while True:
                print(
                    """
Here are you current bookings:

Room Code\t       Date/Time
"""
                )
                db_cursor.execute(
                    f"SELECT * FROM Bookings WHERE bookingName = '{name}'"
                )
                db_return = db_cursor.fetchall()

                for i in range(len(db_return)):
                    start_unix = db_return[i][1] - 1
                    end_unix = db_return[i][2] + 1
                    start_dt = time.strftime(
                        "%d-%m-%Y %H%M", time.localtime(start_unix)
                    )
                    end_dt = time.strftime("%d-%m-%Y %H%M", time.localtime(end_unix))
                    print(f"{i+1}) {db_return[i][0]}   {start_dt} to {end_dt}")

                booking_select = int(
                    input("\nSelect the booking you would like to modify: ")
                )
                booking_select -= 1
                start_dt = time.strftime(
                    "%d-%m-%Y %H%M", time.localtime(db_return[booking_select][1])
                )
                end_dt = time.strftime(
                    "%d-%m-%Y %H%M", time.localtime(db_return[booking_select][2])
                )
                old_room_code = db_return[booking_select][0]
                old_start_unix = db_return[booking_select][1]
                system("cls")
                print(
                    f"\nYou have selected: {db_return[booking_select][0]} {start_dt} to {end_dt}"
                )
                print(div)

                menu_input = input(
                    """
Please enter an option
1) Change date and time
2) Cancel booking
"""
                )
                if menu_input == "1":
                    print(div)
                    avail_check = 0
                    date_input = input(
                        "\nEnter the new booking date: (DD-MM-YYYY - DD-MM-YYYY) "
                    )
                    time_input = input("Enter the new booking hours: (0700 - 1800) ")
                    start_dt = datetime.strptime(
                        date_input[:10] + "-" + time_input[:4], "%d-%m-%Y-%H%M"
                    )
                    end_dt = datetime.strptime(
                        date_input[13:] + "-" + time_input[7:], "%d-%m-%Y-%H%M"
                    )
                    start_unix = time.mktime(start_dt.timetuple())
                    end_unix = time.mktime(end_dt.timetuple())

                    start_unix += 1
                    end_unix -= 1

                    db_cursor.execute(
                        f"""SELECT COUNT(*) FROM Rooms
                         WHERE roomCode = '{old_room_code}' AND
                          {start_unix} BETWEEN roomDTStart AND roomDTEnd
                           OR {end_unix} BETWEEN roomDTStart AND roomDTEnd
                            OR roomDTStart BETWEEN {start_unix} AND {end_unix}"""
                    )

                    db_return = db_cursor.fetchall()

                    if db_return[0][0] != 0:
                        print("The room is not available at the desired hours.")
                        avail_check += 1
                        continue

                    else:
                        db_cursor.execute(
                            f"""SELECT COUNT(*) FROM Bookings
                            WHERE roomCode = '{old_room_code}' AND
                            {start_unix} BETWEEN bookingDTStart AND bookingDTEnd
                            OR {end_unix} BETWEEN bookingDTStart AND bookingDTEnd
                            OR bookingDTStart BETWEEN {start_unix} AND {end_unix}"""
                        )

                    db_return = db_cursor.fetchall()

                    if db_return[0][0] != 0:
                        print("The room is already booked at the desired hours.")
                        avail_check += 1

                    if avail_check > 1:
                        system("cls")
                        break

                    db_cursor.execute(
                        f"""UPDATE Bookings SET bookingDTStart = {start_unix}, bookingDTEnd = {end_unix}
                         WHERE roomCode = '{old_room_code}' AND bookingDTStart = {old_start_unix}"""
                    )
                    db.commit()
                    system("cls")
                    print("Booking updated.")
                    break

                elif menu_input == "2":
                    print(div)
                    menu_input = input("Confirm cancellation? (Y/N)")

                    if menu_input == "Y":
                        db_cursor.execute(
                            f"""DELETE FROM Bookings WHERE
                         roomCode = '{old_room_code}' AND bookingDTStart = {old_start_unix}"""
                        )
                        db.commit()
                        system("cls")
                        print("Booking deleted.")
                        break

        elif menu_input == "4":
            system("cls")
            print(div)
            break

        else:
            system("cls")
            print(div)
            print("\nInvalid input.")
            continue


# welcome user message
div = "\n" + "-" * 60
name = db_return[0][2]

print(div)
print(
    f"""
Hello, {name}."""
)
if type_of_user == "Staff":
    staff_func()
else:
    student_func()


# end
print("\nThank you.")

# commit to database
db.commit()

# close database
db.close()

# DEBUG
print("DEBUG: Database commited and closed")
