from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# point this at your actual DB on PythonAnywhere
DB_PATH = '/home/SumaiyaBibi/attendance_system/attendance.db'

@app.route('/', methods=['GET', 'POST'])
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    attendance_data = None
    selected_date = ''
    no_data = False

    if request.method == 'POST':
        selected_date = request.form.get('selected_date', '').strip()
        print("📅 Raw date from form:", selected_date)

        if selected_date:
            # --- normalize to YYYY-MM-DD ---
            try:
                if '/' in selected_date:
                    # e.g. 04/18/2025
                    dt = datetime.strptime(selected_date, '%m/%d/%Y')
                else:
                    # e.g. 2025-04-18
                    dt = datetime.strptime(selected_date, '%Y-%m-%d')
                formatted = dt.strftime('%Y-%m-%d')
                print("🔄 Formatted date:", formatted)
            except ValueError as e:
                print("❌ Date parse error:", e)
                no_data = True
                return render_template('index.html',
                                       selected_date=selected_date,
                                       no_data=no_data,
                                       attendance_data=None)

            # --- fetch from SQLite ---
            try:
                conn = sqlite3.connect(DB_PATH)
                cur  = conn.cursor()
                cur.execute("SELECT name, time FROM attendance WHERE date = ?", (formatted,))
                attendance_data = cur.fetchall()
                conn.close()

                print("✅ DB returned:", attendance_data)
                if not attendance_data:
                    no_data = True

            except Exception as e:
                print("❌ DB error:", e)
                no_data = True

    return render_template('index.html',
                           selected_date=selected_date,
                           no_data=no_data,
                           attendance_data=attendance_data)


if __name__ == '__main__':
    app.run(debug=True)
