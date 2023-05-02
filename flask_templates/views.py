from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "views")

#Render html with template variables
@views.route("/")
def home():
    return render_template("index.html", name="Alvaro")

#Dinamic url
@views.route("/profile/<username>")
def profile(username):
    return render_template("profile.html", name=username)

#Query parameters
@views.route("/name")
def profile2():
    args = request.args
    name = args.get('name')
    return render_template("index.html", name=name)

#Returning json
@views.route("/json")
def get_json():
    return jsonify({'name':'Pepe', 'age':10})

#Getting json data
@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

#Redirect to anothe link
@views.route("/go_home")
def go_home():
    return redirect(url_for("views.home"))
