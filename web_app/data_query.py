import mysql.connector
import pandas as pd
from datetime import datetime

def connect_info():
    _host = "127.0.0.1"
    _user = "root"
    _password = "nbsbest"
    _schema = "shopping"
    return _host, _user, _password, _schema

def get_all_table():
    mydb = mysql.connector.connect(
    	host = connect_info()[0],
    	user = connect_info()[1],
    	password = connect_info()[2]
    )
    mycursor = mydb.cursor(dictionary=True)
	# get all tables
    mycursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{connect_info()[3]}'")
    tables = mycursor.fetchall()
    df_tables = pd.DataFrame(tables).TABLE_NAME
    return df_tables


def get_onetable(table):
    mydb = mysql.connector.connect(
        host = connect_info()[0],
        user = connect_info()[1],
        password = connect_info()[2]
        )
    mycursor = mydb.cursor(dictionary=True)

    clause = f"SELECT * FROM {connect_info()[3]}.{table}"

    mycursor.execute(clause)
    data = mycursor.fetchall()

    df_final = pd.DataFrame(data).reset_index()

    return df_final


def get_table(table_list, feature_list, join_list, filter_list, group_list):
    mydb = mysql.connector.connect(
        host = connect_info()[0],
        user = connect_info()[1],
        password = connect_info()[2]
        )
    mycursor = mydb.cursor(dictionary=True)

    clause = f"SELECT "

    feature_len = len(feature_list)
    for i in range(feature_len):
        if i != feature_len-1:
            clause += f"{feature_list[i]}, "
        else:
            clause += f"{feature_list[i]} "

    clause += f"FROM "

    if len(join_list) == 0:
        clause += f"{connect_info()[3]}.{table_list[0]}"
    else: 
        clause += f"{connect_info()[3]}.{join_list[0].split('.')[0]} "
        for i in range(1, len(join_list)):
            if i % 2 != 0:
                clause += f"{join_list[i]} "
            else:
                clause += f"{connect_info()[3]}.{join_list[i].split('.')[0]} ON {join_list[i-2]} = {join_list[i]} "

    if len(filter_list) > 0:
        clause += f"WHERE "
        filter_len = len(filter_list)
        for i in range(filter_len):
            if i != filter_len-1:
                clause += f"{filter_list[i]} AND"
            else:
                clause += f"{filter_list[i]} "

    if len(group_list) > 0:
        clause += f"GROUP BY "
        group_len = len(group_list)
        for i in range(group_len):
            if i != group_len-1:
                clause += f"{group_list[i]}, "
            else:
                clause += f"{group_list[i]} "

    mycursor.execute(clause)
    data = mycursor.fetchall()

    df_final = pd.DataFrame(data)

    return df_final


def get_macro():
    mydb = mysql.connector.connect(
    host = connect_info()[0],
    user = connect_info()[1],
    password = connect_info()[2]
    )
    mycursor = mydb.cursor(dictionary=True)

    clause = f"SELECT macroname FROM {connect_info()[3]}.macro"

    mycursor.execute(clause)
    data = mycursor.fetchall()

    macronames = []
    for record in data:
        macronames.append(record.get("macroname"))

    return macronames


def macro_import(name):
    mydb = mysql.connector.connect(
    host = connect_info()[0],
    user = connect_info()[1],
    password = connect_info()[2]
    )
    mycursor = mydb.cursor(dictionary=True)

    clause = f"SELECT * FROM {connect_info()[3]}.macro WHERE macroname='{name}'"

    mycursor.execute(clause)

    data = mycursor.fetchall()

    return data[0]


def macro_record(raw_data):
    mydb = mysql.connector.connect(
    host = connect_info()[0],
    user = connect_info()[1],
    password = connect_info()[2]
    )
    mycursor = mydb.cursor(dictionary=True)

    name = repr(raw_data["name"])
    cur_date = datetime.today().strftime('%Y-%m-%d')
    tables = repr(raw_data["tables"])
    joins = repr(raw_data["joins"])
    features = repr(raw_data["features"])
    filters = repr(raw_data["filters"])
    groups = repr(raw_data["groups"])

    clause = f"INSERT INTO {connect_info()[3]}.macro (macroname, macrodate, macrotable, macrojoin, macrofeature, macrofilter, macrogroup) VALUES ({name}, '{cur_date}', {tables}, {joins}, {features}, {filters}, {groups});"

    mycursor.execute(clause)
    mydb.commit()


def macro_delete(name):
    mydb = mysql.connector.connect(
    host = connect_info()[0],
    user = connect_info()[1],
    password = connect_info()[2]
    )
    mycursor = mydb.cursor(dictionary=True)

    clause = f"DELETE FROM {connect_info()[3]}.macro WHERE macroname='{name.get('name')}'"

    mycursor.execute(clause)
    mydb.commit()