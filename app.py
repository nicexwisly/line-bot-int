from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

orders = []
orders_fish = []
queue_counter = {"fish": 1, "pork": 1}

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
    
    global queue_counter
    if department not in queue_counter:
        queue_counter[department] = 1

    orders.append({
        "item": item,
        "detail": detail,
        "customer": customer,
        "department": department,
        "status": "new",
        "queue": f"{queue_counter[department]:03}"
    })
    queue_counter +=1
    return "OK", 200

@app.route("/orders/fish")
def orders_fish():
    fish_orders = [o for o in orders if o["department"] == "fish"]
    return render_template("orders_fish.html", orders=fish_orders)

@app.route("/api/orders/fish")
def api_orders_fish():
    fish_orders = [o for o in orders if o["department"] == "fish"]
    return jsonify(fish_orders)

@app.route("/api/orders/pork")
def api_orders_pork():
    pork_orders = [o for o in orders if o["department"] == "pork"]
    return jsonify(pork_orders)

@app.route("/update_status/<int:index>/<status>/<department>")
def update_status(index, status, department):
    filtered_orders = [o for o in orders if o["department"] == department]
    if 0 <= index < len(filtered_orders):
        filtered_orders[index]["status"] = status
    return redirect(f"/orders/{department}")

@app.route("/orders/pork")
def orders_pork():
    pork_orders = [o for o in orders if o["department"] == "pork"]
    return render_template("orders_pork.html", orders=pork_orders, department_name="หมู")
