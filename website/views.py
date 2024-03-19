from flask import Flask, Blueprint, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import datetime
from .models import Mega
from . import db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
from datetime import datetime
import dateutil.parser
from collections import Counter
from sqlalchemy import func

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    mega_list = Mega.query.all()
    message = request.args.get("message", None) #Get any message or success parameter from the request URL
    success = request.args.get("success", None)
    data = Mega.query.all()

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

    plt.figure(figsize=(8, 6))
    plt.bar(days, daily_earnings)
    plt.title('Daily Earnings')
    plt.xlabel('Day')
    plt.ylabel('Earnings')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template("index.html", mega_list=mega_list, message=message, success=success, data=data, common_name = common_name, best_daily_earnings = best_daily_earnings, biggest_basket_earnings = biggest_basket_earnings, common_best_seller = common_best_seller, common_worst_seller = common_worst_seller, graph_url = graph_url)

@my_view.route("/add", methods=["POST"])    #allows post methods
def add():
    if request.method == 'POST':
        try:
            day = request.form.get("day")
            staff_mvp = request.form.get("staff_mvp")
            biggest_basket = request.form.get("biggest_basket")
            daily_earnings = request.form.get ("daily_earnings")
            best_seller = request.form.get ("best_seller")
            worst_seller = request.form.get ("worst_seller")
            existing_entry = Mega.query.filter_by(day=day).first()
            if existing_entry:
                message = "Error adding your task to the ToDo list, you cannot have more than one entry for the same day"
                return redirect(url_for("my_view.home", message=message))
            new_mega = Mega(day = day, biggest_basket = biggest_basket, staff_mvp = staff_mvp, daily_earnings = daily_earnings, best_seller = best_seller, worst_seller = worst_seller)
            db.session.add(new_mega)   #add into db
            db.session.commit() 
            success = "Task added successfully"    #
            return redirect(url_for("my_view.home", success = success))
        except:
            message = "Error adding your task to the ToDo list, you can not have more than one of the same task" # If an error occurs during adding the task, set an error message
            return redirect(url_for("my_view.home", message = message))


# @my_view.route("/graph")
# def graph():
#     days = []
#     daily_earnings = []

#     entries = Mega.query.all()
#     for entry in entries:
#         # Extract day and daily_earnings from each entry
#         days.append(entry.day)
#         daily_earnings.append(entry.daily_earnings)

#     plt.figure(figsize=(8, 6))
#     plt.bar(days, daily_earnings)
#     plt.title('Daily Earnings')
#     plt.xlabel('Day')
#     plt.ylabel('Earnings')

#     img = BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plt.close()

#     graph_url = base64.b64encode(img.getvalue()).decode()
#     return render_template('index.html', graph_url=graph_url)

@my_view.route('/plot')
def plot():
    days = []
    earnings = []

    # Fetch data from the database
    data = Mega.query.all()

    # Extract days and earnings
    for item in data:
        days.append(item.day)
        earnings.append(item.daily_earnings)

    # Plotting the data
    plt.figure(figsize=(10, 5))
    plt.plot(days, earnings, marker='o', linestyle='-')
    plt.title('Daily Earnings')
    plt.xlabel('Day')
    plt.ylabel('Earnings')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Saving the plot to a file
    plt.savefig('static/daily_earnings.png')

    return render_template('index.html')


@my_view.route("/page2")
def page2():
    data = Mega.query.all()
    return render_template("page2.html", data = data)

@my_view.route("/page3")
def page3():
    return render_template("page3.html")

@my_view.route("/page4")
def page4():
    return render_template("page4.html")

@my_view.route("/page5")
def page5():
    return render_template("page5.html")

@my_view.route("/page6")
def page6():
    return render_template("page6.html")

@my_view.route("/page7")
def page7():
    return render_template("page7.html")

@my_view.route("/page8")
def page8():
    return render_template("page8.html")



# @my_view.route("/update/<todo_id>")
# def update (todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first() # Find the todo item by its ID
#     todo.complete = not todo.complete   # Toggle the completion status of the todo item
#     db.session.commit() 
#     return redirect(url_for("my_view.home"))

# @my_view.route("/delete/<todo_id>")
# def delete (todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first() # Find the todo item by its ID
#     db.session.delete(todo) # Delete the todo item from the database
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


# @my_view.route("/page2")
# def page2():
#     data = Todo.query.all()
#     return render_template("page2.html", data = data)

# @my_view.route("/graph")
# def graph():
    
#     completed_count = Todo.query.filter_by(complete=True).count()   # Query the database to get counts of completed and not completed tasks
#     not_completed_count = Todo.query.filter_by(complete=False).count()
    
#     plt.figure(figsize=(8, 6))  # Plotting the graph
#     plt.bar(['Completed', 'Not Completed'], [completed_count, not_completed_count], color=['green', 'red'])
#     plt.title('Tasks Completion Status')
#     plt.xlabel('Status')
#     plt.ylabel('Number of Tasks')
#     plt.show()
    
#     img = BytesIO() # Save the plot as a PNG image in memory
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plt.close()

#     graph_url = base64.b64encode(img.getvalue()).decode()       # Convert the PNG image to base64 string

#     return render_template('graph.html', graph_url=graph_url)       # Render the HTML template with the graph
    
# @my_view.route("/graph2")
# def graph2():
#     dates = []
#     tasks_count = []

#     entries = Todo.query.all()
#     for entry in entries:
#         # Convert entry.date_created to a datetime object
#         date_created = dateutil.parser.parse(entry.date_created)
#         dates.append(date_created.strftime('%Y-%m-%d'))
#         tasks_count = Todo.query.filter_by(complete=True).count()

#     plt.figure(figsize=(8, 6))
#     plt.bar(dates, tasks_count)
#     plt.title('Completed Tasks by Date')
#     plt.xlabel('Date')
#     plt.ylabel('Number of Tasks Completed')

#     img = BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plt.close()

#     date_graph_url = base64.b64encode(img.getvalue()).decode()
#     return render_template('graph2.html', date_graph_url=date_graph_url)