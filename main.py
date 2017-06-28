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
    response = requests.get('http://swapi.co/api/planets/?page=2').json()
    print(response['results'][0]['name'])
    return render_template('index.html', table_heads=table_heads)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
