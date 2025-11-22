from flask import Flask, jsonify, request, render_template
import psycopg2
import os

app = Flask(__name__)

# Read database credentials from environment variables
DB_HOST = os.environ.get("DATABASE_HOST", "localhost")
DB_NAME = os.environ.get("DATABASE_NAME", "healthcare")
DB_USER = os.environ.get("DATABASE_USER", "postgres")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres")
DB_PORT = os.environ.get("DATABASE_PORT", 5432)

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

@app.route("/patients", methods=["GET"])
def get_patients():
    """Return all patients or filter by medical condition if query param is provided."""
    condition = request.args.get("condition")
    conn = get_db_connection()
    cur = conn.cursor()
    
    if condition:
        cur.execute("SELECT * FROM patients WHERE medical_condition = %s LIMIT 100", (condition,))
    else:
        cur.execute("SELECT * FROM patients LIMIT 100")
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # Convert rows to list of dictionaries
    patients = []
    colnames = ["id","name","age","gender","blood_type","medical_condition","date_of_admission",
                "doctor","hospital","insurance_provider","billing_amount","room_number",
                "admission_type","discharge_date","medication","test_results"]
    for row in rows:
        patients.append(dict(zip(colnames, row)))
    
    return jsonify(patients)

@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "OK"})

@app.route("/analytics/disease_probabilities", methods=["GET"])
def disease_probabilities():
    conn = get_db_connection()
    cur = conn.cursor()

    # get total number of patients
    cur.execute("SELECT COUNT(*) FROM patients")
    total = cur.fetchone()[0]

    # get counts for each disease
    cur.execute("""
        SELECT medical_condition, COUNT(*)
        FROM patients
        GROUP BY medical_condition
        ORDER BY COUNT(*) DESC
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # compute probabilities
    results = []
    for condition, count in rows:
        results.append({
            "medical_condition": condition,
            "count": count,
            "probability": count / total
        })

    return jsonify(results)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients LIMIT 50")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    colnames = ["id","name","age","gender","blood_type","medical_condition",
                "date_of_admission","doctor","hospital","insurance_provider",
                "billing_amount","room_number","admission_type","discharge_date",
                "medication","test_results"]

    table_rows = [dict(zip(colnames, r)) for r in rows]

    return render_template("patients.html", columns=colnames, rows=table_rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

