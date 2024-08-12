import csv
from io import StringIO
from flask import Flask, request, jsonify

app = Flask(__name__)

transactions = []

@app.route('/transactions', methods=['POST'])
def add_transactions():
    global transactions
    file = request.files['file']
    content = file.stream.read().decode('utf-8')
    csv_reader = csv.reader(StringIO(content), delimiter=',')  # Changed delimiter to comma

    # Skip the header
    next(csv_reader)

    for row in csv_reader:
        if row and not row[0].startswith('#'):
            transactions.append({
                "date": row[0],
                "type": row[1],
                "amount": float(row[2]),
                "memo": row[3]
            })

    return jsonify({"message": "Transactions added successfully!"}), 200

@app.route('/report', methods=['GET'])
def report():
    gross_revenue = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    expenses = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    net_revenue = gross_revenue - expenses

    return jsonify({
        "gross-revenue": gross_revenue,
        "expenses": expenses,
        "net-revenue": net_revenue
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
