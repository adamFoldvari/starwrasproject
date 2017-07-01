from flask import Flask, render_template, request, redirect, url_for, session, escape
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import data_handler
from database_connection_data import secret_key
from os import urandom

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    # table headers
    table_heads = ['Name',
                   'Diameter',
                   'Climate',
                   'Terrain',
                   'Surface water percentage',
                   'Population',
                   'Residents',
                   ]

    # which page am i?
    act_page = request.args.get('page')
    if act_page is None:
        act_page = '1'

    # concatenate actual pages swapi link
    response = requests.get('http://swapi.co/api/planets/?page=' + act_page).json()

    # set button values
    but_next = None
    but_prev = None
    if response['next'] is not None:
        but_next = str(response['next']).split('=', 1)[1]

    if response['previous'] is not None:
        but_prev = str(response['previous']).split('=', 1)[1]

    # get and format table rows
    rows = []
    for planet in response['results']:
        row = []
        row.append(planet['name'])
        if planet['diameter'] != 'unknown':
            row.append(format(int(planet['diameter']), ',d') + ' km')
        else:
            row.append('unknown')
        row.append(planet['climate'])
        row.append(planet['terrain'])
        if planet['surface_water'] != 'unknown':
            row.append(planet['surface_water'] + '%')
        else:
            row.append('unknown')
        if planet['population'] != 'unknown':
            row.append(format(int(planet['population']), ',d') + ' people')
        else:
            row.append('unknown')
        # residents passed for js
        row.append(planet['residents'])
        # append for table (rows)
        rows.append(row)

    # are we logged in?
    if session.get('username'):
        username = session['username']
    else:
        username = None
    # give index.html everything which needed
    return render_template('index.html', table_heads=table_heads, but_next=but_next, but_prev=but_prev,  rows=rows,
                           username=username)


@app.route('/registration', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
        try:
            data_handler.add_user_to_db(username, password)
            return redirect(url_for('index'))
        except TypeError:
            # if username exists
            return render_template('form.html', error_message='This username already exists!')
    # in case of GET request (when page loads)
    return render_template('form.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if data_handler.user_in_db(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            # bad username or password
            return render_template('form.html', login=True, error_message='Wrong username or password. Try again!')
    # in case of GET request (when page loads)
    return render_template('form.html', login=True)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


def main():
    app.secret_key = urandom(24)
    app.run(debug=True)


if __name__ == '__main__':
    main()
