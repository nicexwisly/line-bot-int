from flask import Flask, render_template, request, redirect

app = Flask(__name__)
orders = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    item = request.form["item"]
    detail = request.form["detail"]
    customer = request.form["customer"]
    department = request.form["department"]
    orders.append({
        "item": item,
        "detail": detail,
        "customer": customer,
        "department": department
    })
    return redirect("/")

@app.route("/orders/fish")
def orders_fish():
    fish_orders = [o for o in orders if o["department"] == "fish"]
    return render_template("orders_fish.html", orders=fish_orders)

@app.route("/orders/pork")
def orders_pork():
    pork_orders = [o for o in orders if o["department"] == "pork"]
    return render_template("orders_pork.html", orders=pork_orders)

if __name__ == "__main__":
    app.run(debug=True)
