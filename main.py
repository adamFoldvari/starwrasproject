from flask import Flask, render_template, request, redirect, url_for, session, escape
import requests

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

    # concatenate actual pages swapi link swapi
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
        if len(planet['residents']) > 0:
            row.append(str(len(planet['residents'])) + ' resident(s)')
        else:
            row.append('No known residents')
        rows.append(row)

    # give index.html everything which needed
    return render_template('index.html', table_heads=table_heads, but_next=but_next, but_prev=but_prev,  rows=rows)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
