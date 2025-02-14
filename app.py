from flask import Flask, render_template, request, redirect, url_for, session, Response
from datetime import datetime, timedelta
import uuid
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'demo'

# Generate 5 recent dates for the price history
recent_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(4, -1, -1)]

flights = [
    {
        'id': str(uuid.uuid4()),
        'number': 'AA101',
        'airline': 'American Airlines',
        'origin': 'JFK',
        'full_origin': 'New York',
        'destination': 'LAX',
        'full_destination': 'Los Angeles',
        'logo': 'american_airlines.png',
        'prices': [
            {'date': recent_dates[0], 'price': 300},
            {'date': recent_dates[1], 'price': 310},
            {'date': recent_dates[2], 'price': 320},
            {'date': recent_dates[3], 'price': 315},
            {'date': recent_dates[4], 'price': 305}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'DL202',
        'airline': 'Delta Airlines',
        'origin': 'ATL',
        'full_origin': 'Atlanta',
        'destination': 'ORD',
        'full_destination': 'Chicago',
        'logo': 'delta_airlines.png',
        'prices': [
            {'date': recent_dates[0], 'price': 200},
            {'date': recent_dates[1], 'price': 210},
            {'date': recent_dates[2], 'price': 205},
            {'date': recent_dates[3], 'price': 215},
            {'date': recent_dates[4], 'price': 220}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'UA303',
        'airline': 'United Airlines',
        'origin': 'SFO',
        'full_origin': 'San Francisco',
        'destination': 'DEN',
        'full_destination': 'Denver',
        'logo': 'united_airlines.png',
        'prices': [
            {'date': recent_dates[0], 'price': 180},
            {'date': recent_dates[1], 'price': 190},
            {'date': recent_dates[2], 'price': 195},
            {'date': recent_dates[3], 'price': 200},
            {'date': recent_dates[4], 'price': 205}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'SW404',
        'airline': 'Southwest Airlines',
        'origin': 'DAL',
        'full_origin': 'Dallas',
        'destination': 'MCO',
        'full_destination': 'Orlando',
        'logo': 'southwest_airlines.png',
        'prices': [
            {'date': recent_dates[0], 'price': 150},
            {'date': recent_dates[1], 'price': 155},
            {'date': recent_dates[2], 'price': 160},
            {'date': recent_dates[3], 'price': 158},
            {'date': recent_dates[4], 'price': 162}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'JB505',
        'airline': 'JetBlue Airways',
        'origin': 'BOS',
        'full_origin': 'Boston',
        'destination': 'FLL',
        'full_destination': 'Fort Lauderdale',
        'logo': 'jetblue_airways.png',
        'prices': [
            {'date': recent_dates[0], 'price': 220},
            {'date': recent_dates[1], 'price': 225},
            {'date': recent_dates[2], 'price': 230},
            {'date': recent_dates[3], 'price': 235},
            {'date': recent_dates[4], 'price': 240}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'FR606',
        'airline': 'Frontier Airlines',
        'origin': 'DEN',
        'full_origin': 'Denver',
        'destination': 'LAS',
        'full_destination': 'Las Vegas',
        'logo': 'frontier_airlines.png',
        'prices': [
            {'date': recent_dates[0], 'price': 120},
            {'date': recent_dates[1], 'price': 125},
            {'date': recent_dates[2], 'price': 130},
            {'date': recent_dates[3], 'price': 128},
            {'date': recent_dates[4], 'price': 132}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'SP707',
        'airline': 'Spirit Airlines',
        'origin': 'FLL',
        'full_origin': 'Fort Lauderdale',
        'destination': 'DTW',
        'full_destination': 'Detroit',
        'logo': 'spirit_airlines.png',
        'prices': [
            {'date': recent_dates[0], 'price': 140},
            {'date': recent_dates[1], 'price': 145},
            {'date': recent_dates[2], 'price': 150},
            {'date': recent_dates[3], 'price': 148},
            {'date': recent_dates[4], 'price': 152}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'AL808',
        'airline': 'Alaska Airlines',
        'origin': 'SEA',
        'full_origin': 'Seattle',
        'destination': 'PDX',
        'full_destination': 'Portland',
        'logo': 'alaska_airlines.png',
        'prices': [
            {'date': recent_dates[0], 'price': 110},
            {'date': recent_dates[1], 'price': 115},
            {'date': recent_dates[2], 'price': 120},
            {'date': recent_dates[3], 'price': 118},
            {'date': recent_dates[4], 'price': 122}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'VA909',
        'airline': 'Virgin America',
        'origin': 'SFO',
        'full_origin': 'San Francisco',
        'destination': 'SEA',
        'full_destination': 'Seattle',
        'logo': 'virgin_america.png',
        'prices': [
            {'date': recent_dates[0], 'price': 250},
            {'date': recent_dates[1], 'price': 255},
            {'date': recent_dates[2], 'price': 260},
            {'date': recent_dates[3], 'price': 265},
            {'date': recent_dates[4], 'price': 270}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'NK010',
        'airline': 'Air Canada',
        'origin': 'YYZ',
        'full_origin': 'Toronto',
        'destination': 'YVR',
        'full_destination': 'Vancouver',
        'logo': 'air_canada.png',
        'prices': [
            {'date': recent_dates[0], 'price': 350},
            {'date': recent_dates[1], 'price': 355},
            {'date': recent_dates[2], 'price': 360},
            {'date': recent_dates[3], 'price': 365},
            {'date': recent_dates[4], 'price': 370}
        ]
    },
    {
        'id': str(uuid.uuid4()),
        'number': 'BA111',
        'airline': 'British Airways',
        'origin': 'LHR',
        'full_origin': 'London',
        'destination': 'JFK',
        'full_destination': 'New York',
        'logo': 'british_airways.png',
        'prices': [
            {'date': recent_dates[0], 'price': 400},
            {'date': recent_dates[1], 'price': 405},
            {'date': recent_dates[2], 'price': 410},
            {'date': recent_dates[3], 'price': 415},
            {'date': recent_dates[4], 'price': 420}
        ]
    }
]

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'demo' and password == 'password123':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login', error=1))
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', flights=flights)

@app.route('/flight/<flight_id>')
def flight_details(flight_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    flight = next((f for f in flights if f['id'] == flight_id), None)
    if not flight:
        return "Flight not found", 404
    return render_template('flight_details.html', flight=flight)

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        flight_number = request.form.get('flight_number')
        airline = request.form.get('airline')
        origin = request.form.get('origin')
        full_origin = request.form.get('full_origin')
        destination = request.form.get('destination')
        full_destination = request.form.get('full_destination')
        logo = request.form.get('logo')
        new_flight = {
            'id': str(uuid.uuid4()),
            'number': flight_number,
            'airline': airline,
            'origin': origin,
            'full_origin': full_origin,
            'destination': destination,
            'full_destination': full_destination,
            'logo': logo,
            'prices': [
                {'date': recent_dates[0], 'price': 0},
                {'date': recent_dates[1], 'price': 0},
                {'date': recent_dates[2], 'price': 0},
                {'date': recent_dates[3], 'price': 0},
                {'date': recent_dates[4], 'price': 0}
            ]
        }
        flights.append(new_flight)
        return redirect(url_for('dashboard'))
    return render_template('add_flight.html')

@app.route('/export/<flight_id>')
def export(flight_id):
    flight = next((f for f in flights if f['id'] == flight_id), None)
    if not flight:
        return "Flight not found", 404
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Price'])
    for price in flight['prices']:
        cw.writerow([price['date'], price['price']])
    output = si.getvalue()
    si.close()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={flight['number']}_prices.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
