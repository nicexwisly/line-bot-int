from flask import Flask, render_template, request, redirect, jsonify

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
        "department": department
    })

    return "OK", 200
