# a.py (Flask backend)
from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
from datetime import datetime

app = Flask(__name__)
EXCEL_FILE = "registrations.xlsx"
CLIENT_PASSWORD = "hyundai123"

# Create Excel file if not exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=[
        'Student Name', 'Student Mobile', 'Student Email', 'Student Address', 'Internship Type',
        'College', 'Discipline', 'HOD Name', 'HOD Email', 'HOD Mobile',
        'Employee Name', 'Designation', 'Employee ID', 'Department', 'Employee Mobile', 'Relationship', 'Date',
        'Project Title', 'Project Guide Name', 'Section', 'Project Department', 'Project Employee ID', 'Project Mobile'
    ])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'Student Name': request.form['student_name'],
        'Student Mobile': request.form['student_mobile'],
        'Student Email': request.form['student_email'],
        'Student Address': request.form['student_address'],
        'Internship Type': request.form['internship_type'],
        'College': request.form['college'],
        'Discipline': request.form['discipline'],
        'HOD Name': request.form['hod_name'],
        'HOD Email': request.form['hod_email'],
        'HOD Mobile': request.form['hod_mobile'],
        'Employee Name': request.form['employee_name'],
        'Designation': request.form['designation'],
        'Employee ID': request.form['employee_id'],
        'Department': request.form['employee_department'],
        'Employee Mobile': request.form['employee_mobile'],
        'Relationship': request.form['relationship'],
        'Date': datetime.today().strftime('%Y-%m-%d'),
        'Project Title': request.form['project_title'],
        'Project Guide Name': request.form['project_guide_name'],
        'Section': request.form['section'],
        'Project Department': request.form['project_department'],
        'Project Employee ID': request.form['project_employee_id'],
        'Project Mobile': request.form['project_mobile'],
    }

    df = pd.read_excel(EXCEL_FILE)
    df.loc[len(df)] = data
    df.to_excel(EXCEL_FILE, index=False)

    return "<h2>Form submitted successfully!</h2><a href='/'>Back to form</a>"

@app.route('/enter_pass')
def enter_pass():
    return render_template('enter_pass.html')

@app.route('/verify_pass', methods=['POST'])
def verify_pass():
    if request.form['password'] == CLIENT_PASSWORD:
        return redirect('/client')
    else:
        return "<h3>Invalid password!</h3><a href='/enter_pass'>Try again</a>"

@app.route('/client')
def client():
    return render_template("client.html")

@app.route('/download', methods=['GET'])
def download():
    return send_file(EXCEL_FILE, as_attachment=True)

@app.route('/chart')
def chart():
    df = pd.read_excel(EXCEL_FILE)

    if df.empty or 'College' not in df.columns:
        return "<h3>No data available to generate chart.</h3><a href='/client'>Back</a>"

    college_counts = df['College'].value_counts()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(college_counts, labels=college_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Students per College")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
