from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///village_complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Database Model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')

def initialize_database():
    with app.app_context():
        db.create_all()

# Route to display homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to submit a complaint
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    data = request.form
    new_complaint = Complaint(
        name=data['name'],
        contact=data['contact'],
        category=data['category'],
        description=data['description']
    )
    db.session.add(new_complaint)
    db.session.commit()
    return render_template('success.html', message='Complaint submitted successfully!')

# Route to fetch all complaints
@app.route('/complaints', methods=['GET'])
def get_complaints():
    complaints = Complaint.query.all()
    return render_template('complaints.html', complaints=complaints)

# Route to update complaint status
@app.route('/update_status/<int:complaint_id>', methods=['POST'])
def update_status(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return render_template('error.html', message='Complaint not found')
    
    complaint.status = request.form.get('status', complaint.status)
    db.session.commit()
    return render_template('success.html', message='Status updated successfully!')

# Route to delete a complaint
@app.route('/delete_complaint/<int:complaint_id>', methods=['POST'])
def delete_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return render_template('error.html', message='Complaint not found')
    
    db.session.delete(complaint)
    db.session.commit()
    return render_template('success.html', message='Complaint deleted successfully!')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
