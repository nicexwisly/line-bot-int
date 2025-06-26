from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

orders = []
orders_fish = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()  # รับ JSON จาก fetch

    if not data:
        return jsonify({"error": "ไม่มีข้อมูล"}), 400

    item = data.get("item")
    detail = data.get("detail")
    customer = data.get("customer")
    department = data.get("department")

    if not all([item, detail, customer, department]):
        return jsonify({"error": "ข้อมูลไม่ครบ"}), 400

    orders.append({
        "item": item,
        "detail": detail,
        "customer": customer,
        "department": department,
        "status": "new"
    })

    return "OK", 200

@app.route("/orders/fish")
def orders_fish():
    fish_orders = [o for o in orders if o["department"] == "fish"]
    return render_template("orders_fish.html", orders=fish_orders)

@app.route("/update_status/<int:index>/<status>")
def update_status(index, status):
    fish_orders = [o for o in orders if o["department"] == "fish"]
    if 0 <= index < len(fish_orders):
        fish_orders[index]["status"] = status
    return redirect("/orders/fish")

@app.route("/orders/pork")
def orders_pork():
    pork_orders = [o for o in orders if o["department"] == "pork"]
    return render_template("orders_pork.html", orders=pork_orders, department_name="หมู")

@app.route("/update_status/<int:index>/<status>")
def update_status(index, status):
    pork_orders = [o for o in orders if o["department"] == "pork"]
    if 0 <= index < len(pork_orders):
        pork_orders[index]["status"] = status
    return redirect("/orders/pork")

