from flask import Flask, render_template, request, redirect, url_for, session, escape
import requests

app = Flask(__name__)


@app.route('/')
def index():
    table_heads = ['Name',
                   'Diameter',
                   'Climate',
                   'Terrain',
                   'Surface water percentage',
                   'Population',
                   ]
    response = requests.get('http://swapi.co/api/planets/').json()
    rows = []
    for planet in response['results']:
        row = []
        row.append(planet['name'])
        row.append(format(int(planet['diameter']), ',d') + ' km')
        row.append(planet['climate'])
        row.append(planet['terrain'])
        if planet['surface_water'] != 'unknown':
            row.append(planet['surface_water'] + '%')
        else:
            row.append('unknown')
        try:
            row.append(format(int(planet['population']), ',d') + ' people')
        except ValueError:
            row.append('unknown')
        rows.append(row)
    return render_template('index.html', table_heads=table_heads, rows=rows)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
