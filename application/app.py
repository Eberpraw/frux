from flask import Flask, render_template, request, abort

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/items")
def items():
    items = request.args.get("items")
    if not items:
        return abort(400, "No items provided")
    
    return render_template("/items.html", items=items)