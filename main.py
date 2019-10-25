from flask import Flask, render_template, request, json

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("/index.html")

@app.route("/handler/roomHandler", methods=['GET', 'POST']) 
def room_handler():
    return json.dumps({'first':'hello', 'second':'there'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)