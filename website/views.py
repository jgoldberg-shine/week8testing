from flask import Flask, Blueprint, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from .models import Mega
from .models import Voids
from . import db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
from collections import Counter
from sqlalchemy import func, asc, desc
import numpy as np
import matplotlib.pyplot as plt

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    mega_list = Mega.query.all()
    message = request.args.get("message", None) #Get any message or success parameter from the request URL
    success = request.args.get("success", None)
    # data = Mega.query.all()

    staff_mvp_names = [mega.staff_mvp for mega in mega_list]
    if staff_mvp_names:
        common_name = Counter(staff_mvp_names).most_common(1)[0][0]
    else:
        common_name = None

    best_item = [mega.best_seller for mega in mega_list]
    if best_item:
        common_best_seller = Counter(best_item).most_common(1)[0][0]
    else:
        common_best_seller = None

    worst_item = [mega.worst_seller for mega in mega_list]
    if worst_item:
        common_worst_seller = Counter(worst_item).most_common(1)[0][0]
    else:
        common_worst_seller = None

    best_day = [mega.daily_earnings for mega in mega_list]
    if best_day:
        best_day_object = max(mega_list, key=lambda x: str(x.daily_earnings))
        best_daily_earnings = best_day_object.daily_earnings
    else:
        best_daily_earnings = None

    biggest_basket = [mega.biggest_basket for mega in mega_list]
    if biggest_basket:
        biggest_basket_object = max(mega_list, key=lambda x: str(x.biggest_basket))
        biggest_basket_earnings = biggest_basket_object.biggest_basket
    else:
        biggest_basket_earnings = None


    days = []
    daily_earnings = []

    entries = Mega.query.all()
    for entry in entries:
        # Extract day and daily_earnings from each entry
        days.append(entry.day)
        daily_earnings.append(entry.daily_earnings)

    highest_day_earnings = db.session.query(Mega.day, func.max(Mega.daily_earnings)).first()
    best_daily_earnings, highest_day = highest_day_earnings

    plt.figure(figsize=(8, 6))
    plt.scatter(days, daily_earnings, marker='X')
    plt.title('Daily Earnings')
    plt.xlabel('Day')
    plt.ylabel('Earnings')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    graph_url = base64.b64encode(img.getvalue()).decode()

    all_days = []
    for mega in mega_list:
        all_days.append(mega.day)

    return render_template("index.html", mega_list=mega_list, message=message, success=success, common_name = common_name, best_daily_earnings = best_daily_earnings, biggest_basket_earnings = biggest_basket_earnings, common_best_seller = common_best_seller, common_worst_seller = common_worst_seller, graph_url = graph_url, all_days=all_days, highest_day=highest_day)

@my_view.route("/add", methods=["POST"])    #allows post methods
def add():
    if request.method == 'POST':
        try:
            day = request.form.get("day")
            staff_mvp = request.form.get("staff_mvp").title()
            biggest_basket = request.form.get("biggest_basket")
            daily_earnings = request.form.get ("daily_earnings")
            best_seller = request.form.get ("best_seller").title()
            worst_seller = request.form.get ("worst_seller").title()
            existing_entry = Mega.query.filter_by(day=day).first()
            if existing_entry:
                message = "Error adding your entry. You cannot add two entries for the same day. If you wish to delete or edit an entry then go to the 'Data' page."
                return redirect(url_for("my_view.home", message=message))
            new_mega = Mega(day = day, biggest_basket = biggest_basket, staff_mvp = staff_mvp, daily_earnings = daily_earnings, best_seller = best_seller, worst_seller = worst_seller)
            db.session.add(new_mega)   #add into db
            db.session.commit() 
            success = "Entry added successfully"    #
            return redirect(url_for("my_view.home", success = success))
        except:
            message = "Error adding your entry. You cannot add two entries for the same day. If you wish to delete or edit an entry then go to the 'Data' page." # If an error occurs during adding the task, set an error message
            return redirect(url_for("my_view.home", message = message))





@my_view.route("/page2")
def page2():
    data = Mega.query.all()
    return render_template("page2.html", data = data)

@my_view.route("/page3")
def page3():
    data = Mega.query.all()
    return render_template("page3.html", data = data)

@my_view.route("/page4")
def page4():
    data = Mega.query.all()
    return render_template("page4.html", data = data)

@my_view.route("/page5")
def page5():
    data = Mega.query.all()
    return render_template("page5.html", data = data)

@my_view.route("/page6")
def page6():
    data = Mega.query.all()
    return render_template("page6.html", data = data)

@my_view.route("/page7")
def page7():
    data = Mega.query.all()
    return render_template("page7.html", data = data)

@my_view.route("/page8")
def page8():
    data = Mega.query.all()
    return render_template("page8.html", data = data)

@my_view.route("/page9")
def page9():
    data = Mega.query.all()
    return render_template("page9.html", data = data)


@my_view.route("/add2", methods=["POST"])    #allows post methods
def add2():
    if request.method == 'POST':
            name = request.form.get("name")
            voids = request.form.get("voids")
            transactions = request.form.get("transactions")
            new_void= Voids(name = name, voids = voids, transactions = transactions)
            db.session.add(new_void)   #add into db
            db.session.commit() 
    return redirect(url_for("my_view.page10"))

@my_view.route("/delete/<mega_id>", methods =["POST"])
def delete (mega_id):
    mega = Mega.query.filter_by(id=mega_id).first() # Find the todo item by its ID
    db.session.delete(mega) # Delete the todo item from the database
    db.session.commit()
    return redirect(url_for("my_view.page9"))


@my_view.route("/page10", methods=["GET", "POST"])
def page10():
    sort_criteria = request.form.get("sort_criteria")

    name = []
    voids = []


    entries = Voids.query.with_entities(Voids.name, Voids.voids).all()
    for entry in entries:
        name.append(entry.name)
        voids.append(entry.voids)


    if sort_criteria == "name_asc":
        name, voids = zip(*sorted(zip(name, voids)))
    elif sort_criteria == "name_desc":
        name, voids = zip(*sorted(zip(name, voids), reverse=True))
    elif sort_criteria == "voids_asc":
        name, voids= zip(*sorted(zip(name, voids), key=lambda x: x[1]))
    elif sort_criteria == "voids_desc":
        name, voids= zip(*sorted(zip(name, voids), key=lambda x: x[1], reverse=True))

    plt.figure(figsize=(8, 6))
    plt.bar(name, voids, color='skyblue')
    plt.title('Number of Voids')
    plt.xlabel('Name')
    plt.ylabel('Voids')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    graph_url = base64.b64encode(img.getvalue()).decode()
    
    results = db.session.query(
        Voids.name,
        func.sum(func.cast(Voids.voids, db.Integer)).label('void_count'),
        func.sum(func.cast(Voids.transactions, db.Integer)).label('total_count')
    ).group_by(Voids.name).all()

    # Extracting the names, void counts, and total counts from the query results
    names = [result[0] for result in results]
    void_counts = [result[1] for result in results]
    total_counts = [result[2] for result in results]

    # Plotting the graph
    plt.figure(figsize=(10, 6))

    # Create an array of indices for positioning bars
    x = np.arange(len(names))

    # Width of each bar
    width = 0.35  

    # Plotting the graph
    plt.bar(x - width/2, total_counts, width, color='skyblue', label='Total Transactions')
    plt.bar(x + width/2, void_counts, width, color='red', label='Voided Transactions')
    plt.xticks(x, names)  # Set the x-axis labels to be the names
    plt.title('Completed vs Voided Transactions by Name')
    plt.xlabel('Name')
    plt.ylabel('Number of Transactions')
    plt.legend()
    
    # Saving the plot as a PNG image in memory
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Convert the PNG image to base64 string
    graph_transactions = base64.b64encode(img.getvalue()).decode()

    return render_template('page10.html', graph_transactions=graph_transactions, graph_url=graph_url, sort_criteria=sort_criteria)

# @my_view.route("/checklist")
# def checklist():
#     data = Mega.query.all()
#     days_with_data = [mega.day for mega in data]
    
#     all_days = [day for sublist in days_with_data for day in sublist]

#     unique_days = list(set(all_days))
    
#     return render_template("index.html", unique_days=unique_days)


# @my_view.route("/page9/<int:mega_id>", methods=['POST'])
# def page9(mega_id):
#     mega = Mega.query.get(mega_id)  # Retrieve the Mega object by its ID
#     if mega:  # Check if the Mega object exists
#         db.session.delete(mega)  # Delete the Mega object from the database
#         db.session.commit()
#     return redirect(url_for("page9.html"))  # Redirect to the home endpoint



# @my_view.route("/update/<todo_id>")
# def update (todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first() # Find the todo item by its ID
#     todo.complete = not todo.complete   # Toggle the completion status of the todo item
#     db.session.commit() 
#     return redirect(url_for("my_view.home"))


# @my_view.route("/edit/<int:todo_id>", methods=["GET", "POST"])
# def edit_todo(todo_id):
#     try:
#         todo = Todo.query.get(todo_id)
#         if request.method == "POST":    # If the request method is POST, update the task of the todo item
#             todo.task = request.form["edit_task"]  # Corrected input field name
#             db.session.commit()
#             return redirect(url_for("my_view.home"))
#         return render_template("edit_todo.html", todo=todo)
#     except:
#         message = "Error editing your task. Two identical tasks cannot exist"   # If an error occurs during editing the task, set an error message
#         return redirect(url_for("my_view.home", message=message)) # Redirect to the home page with the error message




    

            # max_earnings_entry = Mega.query.order_by(Mega.daily_earnings.desc()).first()
            # if max_earnings_entry:
            #     highest_earning_day = max_earnings_entry.day
            #     print(highest_earning_day)
            # else:
            #     highest_earning_day = None  # Setting a default value when no entries are found
            #     print("No entries found in the database.")
            #     return render_template("home.html", highest_earning_day=highest_earning_day)

    # sort_options = {
    #     'low_to_high': 'Lowest to Highest',
    #     'high_to_low': 'Highest to Lowest',
    #     'alphabetical': 'Alphabetical'
    # }
    # if request.method == 'POST':
    #     selected_option = request.form.get('sort_option')

    #     if selected_option == 'low_to_high':
    #         data = Voids.query.order_by(asc(Voids.voids)).all()
    #     elif selected_option == 'high_to_low':
    #         data = Voids.query.order_by(desc(Voids.voids)).all()
    #     else:
    #         data = Voids.query.order_by(asc(Voids.name)).all()