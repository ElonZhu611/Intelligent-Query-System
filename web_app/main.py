import pandas as pd
import json
import mysql.connector
import data_query
from IPython.display import HTML
from datetime import datetime
from flask import Flask, request, render_template, jsonify, make_response, redirect, url_for



app = Flask(__name__)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('panel'))
    return render_template('login.html', error=error)


# Route for handling the panel page logic
@app.route('/panel', methods=['GET','POST'])
def panel():
    table_names = data_query.get_all_table()
    macro_names = data_query.get_macro()

    return render_template("panel.html", table_names=table_names, macro_names=macro_names)

@app.route('/gentable', methods=['GET', 'POST'])
def gentable():

    if request.method == 'POST':

        data = request.get_json("data")

        table_list = data["add_table_area"].split("\n")

        col_list = []
 
        for table in table_list:
            df_temp = data_query.get_onetable(table)
            cols = list(df_temp.columns)
            del cols[0]
            for i in range(len(cols)):
                cols[i] = table + "." + cols[i]
                col_list.append(cols[i])

        cols_dict = {"columns": col_list}

        return cols_dict


@app.route('/query', methods=['GET', 'POST'])
def query():

    if request.method == 'POST':

        data = request.get_json("data")

        table_list = data["tables"].split("\n")
        while("" in table_list):
            table_list.remove("")

        join_list = data["joins"].split("\n")
        while("" in join_list):
            join_list.remove("")

        feature_list = data["features"].split("\n")
        while("" in feature_list):
            feature_list.remove("")

        filter_list = data["filters"].split("\n")
        while("" in filter_list):
            filter_list.remove("")

        group_list = data["groups"].split("\n")
        while("" in group_list):
            group_list.remove("")

        df_final = data_query.get_table(table_list, feature_list, join_list, filter_list, group_list)

        html = df_final.to_html()
        # html = HTML(df_final.to_html(classes='table table-striped'))
          
        # write html to file
        text_file = open("templates/preview.html", "w")
        text_file.write(html)
        text_file.close()

        return data


@app.route('/download', methods=['GET', 'POST'])
def download():

    if request.method == 'POST':

        data = request.get_json("data")

        table_list = data["tables"].split("\n")
        while("" in table_list):
            table_list.remove("")

        join_list = data["joins"].split("\n")
        while("" in join_list):
            join_list.remove("")

        feature_list = data["features"].split("\n")
        while("" in feature_list):
            feature_list.remove("")

        filter_list = data["filters"].split("\n")
        while("" in filter_list):
            filter_list.remove("")

        group_list = data["groups"].split("\n")
        while("" in group_list):
            group_list.remove("")

        df_final = data_query.get_table(table_list, feature_list, join_list, filter_list, group_list)

        df_final.to_csv(f"download/{data['down_name']}.csv", index=False)

        return data


@app.route('/import', methods=['GET', 'POST'])
def macro_import():

    if request.method == 'POST':

        data = request.get_json("data")

        import_data = data_query.macro_import(data.get("name"))

        table_list = import_data["macrotable"].split("\n")

        col_list = []
 
        for table in table_list:
            df_temp = data_query.get_onetable(table)
            cols = list(df_temp.columns)
            del cols[0]
            for i in range(len(cols)):
                cols[i] = table + "." + cols[i]
                col_list.append(cols[i])

        cols_dict = {"columns": col_list}

        import_data.update(cols_dict)

        return import_data


@app.route('/record', methods=['GET', 'POST'])
def record():

    if request.method == 'POST':

        data = request.get_json("data")

        data_query.macro_record(data)

        return data

@app.route('/delete', methods=['GET', 'POST'])
def delete():

    if request.method == 'POST':

        data = request.get_json("data")

        data_query.macro_delete(data)
        
        return data

@app.route('/preview', methods=['GET','POST'])
def preview():

    return render_template("preview.html")


if __name__ == "__main__":
    app.run(debug=True)
