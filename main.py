import requests

from datetime import date, timedelta, datetime
from flask import Flask, render_template
from calendar import monthrange

app = Flask(__name__)

url = 'https://family.titank12.com/api/FamilyMenu?buildingId=8cd2d37f-ccbc-eb11-a2cb-9175c0a39769&districtId=93f76ff0-2eb7-eb11-a2c4-e816644282bd&startDate={}'

@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    m = datetime.now().month
    y = datetime.now().year
    for sunday in all_sundays(y, m):
        response = requests.get(url.format(sunday)).json()
        print(len(response['FamilyMenuSessions']))
    return render_template('index.html', times=all_sundays(y, m))


def all_sundays(y, m):
    all_days = range(1, monthrange(y, m)[1] + 1)
    def is_sun(weekday):
        return is_sunday(weekday, m, y)
    return ['{:02d}-{:02d}-{:04d}'.format(m, d, y) for d in filter(is_sun, all_days)]


def is_sunday(weekday, month, year):
    dt = datetime(year, month, day=weekday)
    return dt.weekday() == 6


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
