from flask import Flask, Response, render_template, request, redirect, url_for, send_file
from db_setup import create_connection, app
import csv
import io
import pymysql
import requests
import socket
import time
import csv
import urllib.request
import json

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/see-all', methods=['GET', 'POST'])
def see_all():
    db_connection = create_connection()
    cursor = db_connection.cursor()
    if request.method == 'GET':
        query1 = "SELECT * FROM Transactions;"
        cursor.execute(query1)
        result1 = cursor.fetchall()

        if result1 is None:
            return "No transactions in database"

        cats = []

        for r in result1:
            query2 = 'SELECT category_name FROM Categories WHERE category_id = %s;'
            data = r[4]
            if r[4] == None:
                cats.append(("NULL", "hello"))
            else:
                cursor.execute(query2, data)
                result2 = cursor.fetchone()
                cats.append(result2)


        return render_template('see-all.html', rows=result1, categories=cats)

    elif request.method == 'POST':
        start_date = request.form['start-date']
        end_date=request.form['end-date']

        query1 = "SELECT * FROM Transactions WHERE transaction_date BETWEEN %s AND %s;"
        data = (start_date, end_date)
        cursor.execute(query1, data)
        result1 = cursor.fetchall()

        cats = []

        for r in result1:
            query2 = 'SELECT category_name FROM Categories WHERE category_id = %s;'
            data = r[4]
            cursor.execute(query2, data)
            result2 = cursor.fetchall()
            cats.append(result2)

        cats_list = []

        # c is a tuple
        for c in cats:
            for name in c:
                cats_list.append(name[0])

        return render_template('see-all.html', rows=result1, categories=cats_list)

@app.route('/add-transaction', methods=['POST', 'GET'])
def add_transaction():
    db_connection = create_connection()
    cursor = db_connection.cursor()
    if request.method == 'POST':
        transaction_type = request.form['transaction_type']
        transaction_amount = request.form['transaction_amount']
        transaction_date = request.form['transaction_date']
        transaction_category = request.form['transaction_category']
        transaction_description = request.form['transaction_description']


        query = 'INSERT INTO Transactions (transaction_type, transaction_amount, transaction_date, transaction_category, transaction_description) VALUES (%s, %s, %s, %s, %s);'
        data = (transaction_type, transaction_amount, transaction_date, transaction_category, transaction_description)

        cursor.execute(query, data)
        return redirect('/see-all')
    elif request.method == 'GET':
        query = 'SELECT category_id, category_name FROM Categories;'
        cursor.execute(query)
        result = cursor.fetchall()
        if result == None:
            return "You must add a category before adding a transaction"
        else:
            return render_template('add-transaction.html', rows=result)

@app.route('/edit-transaction/<int:id>', methods=['POST', 'GET'])
def edit_transaction(id):
    db_connection = create_connection()
    cursor = db_connection.cursor()
    if request.method == 'GET':
        transaction_query = 'SELECT * FROM Transactions WHERE transaction_id = %s;' % (
            id)
        cursor.execute(transaction_query)
        transaction_result = cursor.fetchone()

        if transaction_result == None:
            return "Transaction not in database"

        if transaction_result[1] == "Income":
            other_trans_type = "Expense"
        else:
            other_trans_type = "Income"

        # find the transaction's current category
        cat_query = 'SELECT * FROM Categories WHERE category_id = %s;'
        data = (transaction_result[4])

        # if the transaction doesn't have a current category
        if not transaction_result[4]:
            curr_cat = ("hello", "NULL")
            category_query = 'SELECT category_id, category_name FROM Categories;'
        else:
            cursor.execute(cat_query, data)
            curr_cat = cursor.fetchone()
            category_query = 'SELECT category_id, category_name FROM Categories WHERE category_id != %s;' % (curr_cat[0])

        cursor.execute(category_query)
        category_result = cursor.fetchall()

        return render_template('edit-transaction.html', transaction=transaction_result, rows=category_result, category=curr_cat, type=other_trans_type)

    elif request.method == 'POST':
        transaction_id = request.form['transaction_id']
        transaction_type = request.form['transaction_type']
        transaction_amount = request.form['transaction_amount']
        transaction_date = request.form['transaction_date']
        transaction_category = request.form['transaction_category']
        transaction_description = request.form['transaction_description']

        query = 'UPDATE Transactions SET transaction_type = %s, transaction_amount = %s,transaction_date = %s, transaction_category = %s, transaction_description = %s WHERE transaction_id = %s;'
        data = (transaction_type, transaction_amount, transaction_date, transaction_category, transaction_description, transaction_id)
        cursor.execute(query, data)
    return redirect('/see-all')

@app.route('/confirmation-dialogue/<int:id>',  methods=['POST', 'GET'])
def confirmation_dialogue(id):
    db_connection = create_connection()
    cursor = db_connection.cursor()
    if request.method == 'GET':
        query = 'SELECT * FROM Transactions WHERE transaction_id = %s;' % (id)
        cursor.execute(query)
        result = cursor.fetchone()

        query2 = 'SELECT category_name FROM Categories WHERE category_id = %s;'
        data = result[4]
        if result[4] == None:
            result2 = (("NULL", "hello"))
        else:
            cursor.execute(query2, data)
            result2 = cursor.fetchone()
        return render_template('confirmation-dialogue.html', transaction=result, category=result2)
    elif request.method == 'POST':
        query = 'DELETE FROM Transactions WHERE transaction_id = %s;'
        data = (id,)
        cursor.execute(query, data)
        return redirect('/see-all')

@app.route('/see-categories/')
def see_categories():
    db_connection = create_connection()
    cursor = db_connection.cursor()
    query = 'SELECT * FROM Categories;'
    cursor.execute(query)
    result = cursor.fetchall()
    return render_template('see-categories.html', rows=result)

@app.route('/add-category', methods=['POST', 'GET'])
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        category_budget = request.form['category_budget']
        if category_budget == "0.0" or category_budget == "0.00" or category_budget == '':
            category_budget = 'NULL'
        db_connection = create_connection()
        cursor = db_connection.cursor()
        query = 'INSERT INTO Categories(category_name, category_budget) VALUES (%s, %s);'
        data = (category_name, category_budget)
        cursor.execute(query, data)
        return redirect('/see-categories')
    elif request.method == 'GET':
        return render_template('add-category.html')

@app.route('/edit-category/<int:id>', methods=['POST', 'GET'])
def edit_category(id):
    db_connection = create_connection()
    cursor = db_connection.cursor()
    if request.method == 'GET':
        category_query = 'SELECT * FROM Categories WHERE category_id = %s;' % (
            id)
        cursor.execute(category_query)
        category_result = cursor.fetchone()

        if category_result == None:
            return "Category not in database"

        return render_template('edit-category.html', category = category_result)

    elif request.method == 'POST':
        category_id = request.form['category_id']
        category_name = request.form['category_name']
        category_budget = request.form['category_budget']

        query = 'UPDATE Categories SET category_name = %s, category_budget = %s WHERE category_id = %s;'
        data = (category_name, category_budget, category_id)
        cursor.execute(query, data)
        return redirect('/see-categories')

@app.route('/confirmation-dialogue-category/<int:id>',  methods=['POST', 'GET'])
def confirmation_dialogue_category(id):
    db_connection = create_connection()
    cursor = db_connection.cursor()
    if request.method == 'GET':
        query = 'SELECT * FROM Categories WHERE category_id = %s;' % (id)
        cursor.execute(query)
        result = cursor.fetchone()

        return render_template('confirmation-dialogue-category.html', category=result)
    elif request.method == 'POST':
        query = 'DELETE FROM Categories WHERE category_id = %s;'
        data = (id,)
        cursor.execute(query, data)
        return redirect('/see-categories')

@app.route('/see-json', methods=['POST', 'GET'])
def see_json():
    db_connection = create_connection()
    cursor = db_connection.cursor()
    if request.method == 'GET':
        query = 'SELECT category_id, category_name FROM Categories;'
        cursor.execute(query)
        result = cursor.fetchall()
        return render_template('json.html', rows=result)
    elif request.method == 'POST':
        transaction_type = request.form['transaction_type']
        transaction_category = request.form['transaction_category']

        customized = False

        query = 'SELECT * FROM Transactions'
        if transaction_type != "All":
            query += ' WHERE transaction_type = '
            query += '"'
            query += transaction_type
            query += '"'
            customized = True
        if transaction_category != "All":
            if not customized:
                query += ' WHERE transaction_category = '
            else:
                query += ' AND transaction_category = '
            query += transaction_category

        query += ';'

        cursor.execute(query)
        rv = cursor.fetchall()

        data_str = ""
        for result in rv:
            for attribute in result:
                data_str += str(attribute)
                data_str += ','
            data_str = data_str[:-1]
            data_str += '*'

        api_url = 'https://microservice-aviva.herokuapp.com/jsonify/' + data_str
        response = requests.get(api_url)
        return render_template('text.html', intro="Here is the JSON you requested:", text=response.text)


@app.route('/tweet')
def tweet():
    file = open("signal.txt", "w")
    file.write("tweet|I've been taking control of my finances with Personal Finance Tracker! Learn how you can start your personal finance journey here: https://cs361-flask-microservice.herokuapp.com/")
    file.close()
    url = ""
    while url == "":
        file = open('url.txt', 'r')
        url = file.read()
        file.close()


    return render_template('send-tweet.html', url = url)

@app.route('/submit-comment', methods=['GET', 'POST'])
def submit_comment():
    if request.method == 'GET':
        return render_template('user-comment.html')
    else:
        db_connection = create_connection()
        cursor = db_connection.cursor()

        comment_type = request.form['comment_type']
        comment_content = request.form['comment']

        query = 'INSERT INTO Comments (comment_type, comment_content) VALUES (%s, %s);'
        data = (comment_type, comment_content)
        cursor.execute(query, data)

        return render_template('text.html', intro="Thank You!", text="Your comment has been submitted successfully.")

@app.route('/see-stats', methods=['GET', 'POST'])
def see_stats():
    db_connection = create_connection()
    cursor = db_connection.cursor()
    if request.method == 'GET':
        query = 'SELECT category_id, category_name FROM Categories;'
        cursor.execute(query)
        result = cursor.fetchall()
        return render_template('see-stats.html', rows=result)
    else:

        transaction_category = request.form['transaction_category']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        query = 'SELECT * FROM Transactions WHERE transaction_date BETWEEN %s AND %s'

        if transaction_category != "All":
            query += ' AND transaction_category = %s'
            data = (start_date, end_date, transaction_category)
        else:
            data = (start_date, end_date)
        query += ';'

        cursor.execute(query, data)
        result = cursor.fetchall()

        num_transactions = 0
        income = 0
        expenses = 0
        categories = []

        for r in result:
            num_transactions += 1

            if r[4] not in categories:
                if r[4] is None:
                    categories.append("NULL")
                else:
                    categories.append(r[4])
            if r[1] == 'Income':
                income += r[2]
            else:
                expenses += r[2]

        cash_flow = income - expenses
        stats = []
        stats.append(num_transactions)
        stats.append(income)
        stats.append(expenses)
        stats.append(cash_flow)

        cat_stats = []

        # for each unique category
        for cat in categories:
            cat_income = 0
            cat_expense = 0
            cat_cash_flow = 0

            query = 'SELECT * FROM Categories WHERE category_id = %s;'
            if cat == "NULL":
                continue
            cursor.execute(query, cat)
            cat_info = cursor.fetchone()
            cat_budget = cat_info[2]
            cat_name = cat_info[1]


            query = 'SELECT * FROM Transactions WHERE transaction_category = %s;'
            cursor.execute(query, cat)
            cat_transactions = cursor.fetchall()

            for c in cat_transactions:
                if c[1] == "Income":
                    cat_income += int(c[2])
                else:
                    cat_expense += int(c[2])

            if cat_expense > cat_budget:
                over_budget = True
            else:
                over_budget = False

            cat_cash_flow = cat_income - cat_expense
            cat_stats.append((cat, cat_name, cat_income, cat_expense, cat_cash_flow, over_budget))

        return render_template('render-stats.html', overall=stats, stats_by_cat=cat_stats)

















if __name__ == "__main__":
    app.run()