from flask import Flask, jsonify, request
from flask_mysql_connector import MySQL

app = Flask(__name__)
app.config["MYSQL_DATABASE"] = "api"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["TRACK_MODIFICATIONS"] = False
app.secret_key = "****"
mysql = MySQL(app)


# --------------------- GET student details----------------------
@app.route("/student/<string:name>")
def get(name):
    cursor = mysql.connection.cursor()
    query = "select * from data where Name =%s"
    cursor.execute(query, (name,))
    row = cursor.fetchone()
    if row:
        student = row
    else:
        return {"Messgae": "Student not found"}, 404
    mysql.connection.close()
    keys = ("ID", "Name", "Address", "Password", "Phone no:", "Test Score")
    return jsonify(dict(zip(keys, student)))


# --------------------- POST student details----------------------
@app.route("/student/<string:name>", methods=["POST"])
def post(name):
    cursor = mysql.connection.cursor()
    data = request.get_json()
    query = "INSERT INTO data (id, Name, password,Address, Phone,Score) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(
        query,
        (
            data["id"],
            data["Name"],
            data["Password"],
            data["Address"],
            data["Phone"],
            data["Score"],
        ),
    )
    mysql.connection.commit()
    mysql.connection.close()
    print(data)
    print(type(data))
    return jsonify(data)


# # --------------------- Update student details----------------------
@app.route("/student/<string:name>", methods=["PUT"])
def update(name):
    cursor = mysql.connection.cursor()
    data = request.get_json()
    query = "update data set id =%s,password=%s, Address=%s,Phone=%s, Score=%s where Name = %s"
    cursor.execute(
        query,
        (
            data["id"],
            data["Password"],
            data["Address"],
            data["Phone"],
            data["Score"],
            data["Name"],
        ),
    )
    mysql.connection.commit()
    mysql.connection.close()
    return jsonify(data)


# # --------------------- Delete student details----------------------
@app.route("/student/<string:name>", methods=["DELETE"])
def delete(name):
    cursor = mysql.connection.cursor()
    query = "delete from data where Name = %s"
    cursor.execute(query, (name,))
    mysql.connection.commit()
    mysql.connection.close()
    return {"Message": "Student deleted"}


app.run(port=5000, debug=True)
