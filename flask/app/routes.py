import sqlite3
import time
from datetime import datetime

from app import app  # imports the app variable that is a member of the app package
from app.forms import (
    BookRoomForm,
    CreateRoomForm,
    EditBookingForm,
    EditRoomForm,
    LoginForm,
)
from flask import flash, redirect, render_template, request, session, url_for


db = sqlite3.connect("room_booking.db", check_same_thread=False)
db_cursor = db.cursor()


@app.route("/")
@app.route("/index")
def index():

    user = {"username": "Test"}

    return render_template(
        "index.html",
        title="Home",
        user=user,
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        db_cursor.execute(
            f"""SELECT typeOfUser, name, userID FROM Login WHERE
             username = '{form.username.data}' AND password = '{form.password.data}'"""
        )
        db_return = db_cursor.fetchall()

        if len(db_return) != 0:
            user_info = {
                "type_of_user": db_return[0][0],
                "name_of_user": db_return[0][1],
                "user_id": db_return[0][2],
            }
            session["user_info"] = user_info

            if user_info["type_of_user"] == "Staff":
                flash("Login successful!", "success")
                return redirect(url_for("staff"))

            else:
                flash("Login successful!", "success")
                return redirect(url_for("student"))

        flash("Login failed!", "danger")
        return redirect(url_for("login"))

    return render_template("login.html", title="Sign In", form=form)


@app.route("/staff")
def staff():

    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]
    name_of_user = user_info["name_of_user"]

    return render_template(
        "staff.html",
        title="Staff",
        type_of_user=type_of_user,
        name_of_user=name_of_user,
    )


@app.route("/staff/1", methods=["GET", "POST"])
def staff1():

    form = CreateRoomForm()
    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]
    name_of_user = user_info["name_of_user"]

    if form.validate_on_submit():

        if len(form.promo_code_input.data) != 0:
            promo_code_amt_input = form.promo_code_amt_input.data
            promo_code_amt_input = 1 - (promo_code_amt_input / 100)

        else:
            promo_code_amt_input = 1.0

        start_dt = datetime.combine(
            form.start_date_input.data, form.start_time_input.data
        )
        end_dt = datetime.combine(form.end_date_input.data, form.end_time_input.data)
        start_unix = time.mktime(start_dt.timetuple())
        end_unix = time.mktime(end_dt.timetuple())

        db_cursor.execute(
            f"""INSERT INTO Rooms VALUES ('{form.room_code_input.data}', {form.room_price_input.data}, {form.room_cap_input.data},
                     '{form.promo_code_input.data}', {promo_code_amt_input}, {start_unix}, {end_unix} , 0)"""
        )
        db.commit()

        flash(f"Room {form.room_code_input.data} created!", "success")
        return redirect(url_for("staff"))

    return render_template(
        "staff1.html",
        title="CreateRoom",
        type_of_user=type_of_user,
        name_of_user=name_of_user,
        form=form,
    )


@app.route("/staff/2", methods=["GET", "POST"])
def staff2():

    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]

    db_cursor.execute("SELECT * FROM Rooms WHERE roomLaunched = 0")
    db_return = db_cursor.fetchall()

    menu_input = request.args.get("type")
    if menu_input is not None:
        db_cursor.execute(
            f"UPDATE Rooms SET roomLaunched = 1 WHERE roomCode = '{menu_input}'"
        )
        db.commit()
        flash(f"Room {menu_input} activated!", "success")
        return redirect(url_for("staff2"))

    return render_template(
        "staff2.html",
        title="Launch Room",
        type_of_user=type_of_user,
        db_return=db_return,
        len=len(db_return),
    )


@app.route("/staff/3", methods=["GET", "POST"])
def staff3():

    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]

    db_cursor.execute("SELECT * FROM Rooms")
    db_return = db_cursor.fetchall()
    db_return_list = list(map(list, db_return))

    for i in range(len(db_return_list)):
        start_unix = db_return_list[i][5]
        end_unix = db_return_list[i][6] + 1
        start_dt = time.strftime("%d-%m-%Y %H%M", time.localtime(start_unix))
        end_dt = time.strftime("%d-%m-%Y %H%M", time.localtime(end_unix))
        db_return_list[i][5] = start_dt
        db_return_list[i][6] = end_dt

    menu_input = request.args.get("type")
    if menu_input is not None:
        session["room_code"] = menu_input
        return redirect(url_for("staff31"))

    return render_template(
        "staff3.html",
        title="Edit Room",
        type_of_user=type_of_user,
        db_return_list=db_return_list,
        len=len(db_return),
    )


@app.route("/staff/3/1", methods=["GET", "POST"])
def staff31():
    form = EditRoomForm()
    room_code = session.get("room_code", None)
    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]

    db_cursor.execute(f"SELECT * FROM Rooms WHERE roomCode='{room_code}'")
    db_return = db_cursor.fetchall()

    promo_amt = db_return[0][4]
    promo_amt = (1 - promo_amt) * 100
    promo_amt = round(promo_amt)

    if form.validate_on_submit():

        if len(form.promo_code_input.data) != 0:
            promo_code_amt_input = form.promo_code_amt_input.data
            promo_code_amt_input = 1 - (promo_code_amt_input / 100)

        else:
            promo_code_amt_input = 1.0

        start_dt = datetime.combine(
            form.start_date_input.data, form.start_time_input.data
        )
        end_dt = datetime.combine(form.end_date_input.data, form.end_time_input.data)
        start_unix = time.mktime(start_dt.timetuple())
        end_unix = time.mktime(end_dt.timetuple())

        db_cursor.execute(
            f"""UPDATE Rooms SET roomPrice = {form.room_price_input.data}, roomCap = {form.room_cap_input.data},
             promoCode = '{form.promo_code_input.data}', promoCodeAmount = '{promo_code_amt_input}', roomDTStart = '{start_unix}', roomDTEnd = '{end_unix}'
              WHERE roomCode = '{room_code}'"""
        )
        db.commit()

        flash(f"Room {room_code} edited!", "success")
        return redirect(url_for("staff"))

    return render_template(
        "staff31.html",
        title=f"Edit Room {room_code}",
        form=form,
        type_of_user=type_of_user,
        room_code=room_code,
        db_return=db_return,
        promo_amt=promo_amt,
    )


@app.route("/student", methods=["GET", "POST"])
def student():
    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]
    name_of_user = user_info["name_of_user"]
    user_id = user_info["user_id"]

    db_cursor.execute(f"SELECT * FROM Bookings WHERE bookingUserID = '{user_id}'")
    db_return = db_cursor.fetchall()
    db_return_list = list(map(list, db_return))

    for i in range(len(db_return_list)):
        start_unix = db_return_list[i][1] - 1
        end_unix = db_return_list[i][2] + 1
        start_dt = time.strftime("%d-%m-%Y %H%M", time.localtime(start_unix))
        end_dt = time.strftime("%d-%m-%Y %H%M", time.localtime(end_unix))
        db_return_list[i][1] = start_dt
        db_return_list[i][2] = end_dt

    start_dt = request.args.get("type")
    if start_dt is not None:
        start_dt = datetime.strptime(start_dt, "%d-%m-%Y %H%M")
        start_unix = time.mktime(start_dt.timetuple()) + 1
        session["start_unix"] = start_unix
        return redirect(url_for("student_edit"))

    return render_template(
        "student.html",
        title="Student",
        type_of_user=type_of_user,
        name_of_user=name_of_user,
        db_return_list=db_return_list,
        len=len(db_return),
    )


@app.route("/student/edit", methods=["GET", "POST"])
def student_edit():

    form = EditBookingForm()
    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]
    user_id = user_info["user_id"]
    start_unix = session.get("start_unix", None)

    db_cursor.execute(
        f"""SELECT * FROM Bookings WHERE 
        bookingUserID = '{user_id}' AND bookingDTStart = {start_unix}"""
    )
    db_return = db_cursor.fetchall()

    old_start_unix = start_unix
    room_code = db_return[0][0]

    if form.validate_on_submit():

        start_dt = datetime.combine(
            form.start_date_input.data, form.start_time_input.data
        )
        end_dt = datetime.combine(form.end_date_input.data, form.end_time_input.data)
        start_unix = time.mktime(start_dt.timetuple())
        end_unix = time.mktime(end_dt.timetuple())
        start_unix += 1
        end_unix -= 1

        db_cursor.execute(
            f"""SELECT COUNT(*) FROM Rooms 
                WHERE roomCode = '{room_code}' AND 
                {start_unix} BETWEEN roomDTStart AND roomDTEnd 
                OR {end_unix} BETWEEN roomDTStart AND roomDTEnd 
                OR roomDTStart BETWEEN {start_unix} AND {end_unix}"""
        )
        db_return = db_cursor.fetchall()

        if db_return[0][0] != 0:
            flash(
                "The room is made unavailable at the desired hour by the administrator.",
                "danger",
            )
            return redirect(url_for("student_edit"))

        else:
            db_cursor.execute(
                f"""SELECT COUNT(*) FROM Bookings 
                WHERE roomCode = '{room_code}' AND 
                {start_unix} BETWEEN bookingDTStart AND bookingDTEnd 
                OR {end_unix} BETWEEN bookingDTStart AND bookingDTEnd 
                OR bookingDTStart BETWEEN {start_unix} AND {end_unix}"""
            )
            db_return = db_cursor.fetchall()

            if db_return[0][0] != 0:
                flash(
                    "The room is have already been booked at the desired hour.",
                    "danger",
                )
                return redirect(url_for("student_edit"))

            else:
                db_cursor.execute(
                    f"""UPDATE Bookings SET bookingDTStart = {start_unix}, bookingDTEnd = {end_unix} 
                WHERE bookingUserID = '{user_id}' AND bookingDTStart = {old_start_unix}"""
                )
                db.commit()

            flash(f"The booking for {room_code} has been edited.", "success")
            return redirect(url_for("student"))

    if request.method == "POST":

        if request.form["delete_button"] == "Cancel":
            db_cursor.execute(
                f"""DELETE FROM Bookings WHERE 
                bookingUserID = '{user_id}' AND bookingDTStart = {start_unix}"""
            )
            db.commit()

            flash("Booking cancelled!", "danger")
            return redirect(url_for("student"))

    return render_template(
        "student_edit.html",
        title="Edit",
        type_of_user=type_of_user,
        form=form,
        db_return=db_return,
    )


@app.route("/student/1", methods=["GET", "POST"])
def student1():

    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]

    db_cursor.execute("SELECT * FROM Rooms WHERE roomLaunched = 1")
    db_return = db_cursor.fetchall()

    menu_input = request.args.get("type")
    session["room_code"] = menu_input
    if menu_input is not None:
        return redirect(url_for("student11"))

    return render_template(
        "student1.html",
        title="ViewRooms",
        type_of_user=type_of_user,
        db_return=db_return,
        len=len(db_return),
    )


@app.route("/student/1/1", methods=["GET", "POST"])
def student11():
    form = BookRoomForm()
    user_info = session.get("user_info", None)
    type_of_user = user_info["type_of_user"]
    user_id = user_info["user_id"]
    room_code = session.get("room_code", None)

    if form.validate_on_submit():
        start_dt = datetime.combine(
            form.start_date_input.data, form.start_time_input.data
        )
        end_dt = datetime.combine(form.end_date_input.data, form.end_time_input.data)
        start_unix = time.mktime(start_dt.timetuple())
        end_unix = time.mktime(end_dt.timetuple())

        # to satisfy 0900 booking on a room where previous booking ends on 0900
        start_unix += 1
        end_unix -= 1

        db_cursor.execute(
            f"""SELECT COUNT(*) FROM Rooms
                 WHERE roomCode = '{room_code}' AND
                  {start_unix} BETWEEN roomDTStart AND roomDTEnd
                   OR {end_unix} BETWEEN roomDTStart AND roomDTEnd
                    OR roomDTStart BETWEEN {start_unix} AND {end_unix}"""
        )
        db_return = db_cursor.fetchall()

        if db_return[0][0] != 0:
            flash(
                "The room is made unavailable at the desired hour by the administrator.",
                "danger",
            )
            return redirect(url_for("student11"))

        else:
            db_cursor.execute(
                f"""SELECT COUNT(*) FROM Bookings 
                WHERE roomCode = '{room_code}' AND 
            (({start_unix} BETWEEN bookingDTStart AND bookingDTEnd)
                OR ({end_unix} BETWEEN bookingDTStart AND bookingDTEnd) 
                OR (bookingDTStart BETWEEN {start_unix} AND {end_unix}))"""
            )
            db_return = db_cursor.fetchall()

            if db_return[0][0] != 0:
                flash(
                    "The room is have already been booked at the desired hour.",
                    "danger",
                )
                return redirect(url_for("student11"))

            promo_code_input = form.promo_code_input.data
            booking_total_time = (float(end_unix) - float(start_unix)) / (60 * 60)

            db_cursor.execute(
                f"""SELECT promoCode, promoCodeAmount, roomPrice FROM Rooms
                    WHERE roomCode = '{room_code}'"""
            )
            db_return = db_cursor.fetchall()

            if len(promo_code_input) != 0:

                if promo_code_input == db_return[0][0]:
                    booking_price = round(
                        (booking_total_time * db_return[0][1] * db_return[0][2]),
                        1,
                    )
                    db_cursor.execute(
                        f"INSERT INTO Bookings VALUES ('{room_code}', {start_unix}, {end_unix}, '{user_id}')"
                    )
                    db.commit()

                    flash(
                        f"Room {room_code} has been booked. Payment due: ${booking_price}",
                        "success",
                    )
                    return redirect(url_for("student"))

                else:
                    flash("Promotion Code Invalid.", "danger")
                    return redirect(url_for("student11"))

            else:
                booking_price = round((booking_total_time * db_return[0][2]), 1)
                db_cursor.execute(
                    f"INSERT INTO Bookings VALUES ('{room_code}', {start_unix}, {end_unix}, '{user_id}')"
                )
                db.commit()

                flash(
                    f"Room {room_code} has been booked. Payment due: ${booking_price}",
                    "success",
                )
                return redirect(url_for("student"))

    return render_template(
        "student1.1.html",
        title="BookRoom",
        type_of_user=type_of_user,
        form=form,
        room_code=room_code,
    )
