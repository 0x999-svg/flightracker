from flask import Flask, render_template, request, redirect, session
import random
from datetime import datetime, date


app = Flask(__name__)
app.secret_key = 'demo_secret_key'

# Hardcoded "database"
USERS = {
    'demo': 'password123'
}

FLIGHTS = [
    {
        'id': 1,
        'number': 'AA123',
        'airline': 'American Airlines',
        'origin': 'New York',
        'destination': 'Beijing',
        'prices': [
            {'date': '2024-01-01', 'price': 850},
            {'date': '2024-01-07', 'price': 800},
            {'date': '2024-01-14', 'price': 775},
            {'date': '2024-01-21', 'price': 790},
            {'date': '2024-01-28', 'price': 765}
        ]
    },
    {
        'id': 2,
        'number': 'UA456',
        'airline': 'United Airlines',
        'origin': 'San Francisco', 
        'destination': 'Shanghai',
        'prices': [
            {'date': '2024-01-01', 'price': 900},
            {'date': '2024-01-07', 'price': 850},
            {'date': '2024-01-14', 'price': 825},
            {'date': '2024-01-21', 'price': 840},
            {'date': '2024-01-28', 'price': 815}
        ]
    }
]

@app.route('/')
def home():
    if 'username' not in session:
        return redirect('/login')
    return redirect('/dashboard')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html', flights=FLIGHTS)

@app.route('/flight/<int:flight_id>')
def flight_details(flight_id):
    if 'username' not in session:
        return redirect('/login')
    flight = next((f for f in FLIGHTS if f['id'] == flight_id), None)
    if flight:
        return render_template('flight_details.html', flight=flight)
    return "Flight not found", 404

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        new_flight = {
            'id': len(FLIGHTS) + 1,
            'number': request.form['flight_number'],
            'airline': request.form['airline'],
            'origin': request.form['origin'],
            'destination': request.form['destination'],
            'prices': [{'date': datetime.date.today().isoformat(), 'price': random.randint(500, 1000)}]
        }
        FLIGHTS.append(new_flight)
        return redirect('/dashboard')
    
    return render_template('add_flight.html')

@app.route('/export/<int:flight_id>')
def export_flight(flight_id):
    if 'username' not in session:
        return redirect('/login')
    
    flight = next((f for f in FLIGHTS if f['id'] == flight_id), None)
    if flight:
        # Simulate CSV export
        export_content = "Date,Price\n" + "\n".join([f"{p['date']},{p['price']}" for p in flight['prices']])
        return export_content, 200, {
            'Content-Type': 'text/csv', 
            'Content-Disposition': f'attachment; filename={flight["number"]}_prices.csv'
        }
    return "Flight not found", 404

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)