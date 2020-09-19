import requests
import datetime
import json


class PolisenAPI:
    def __init__(self):
        self.datetime_now = datetime.datetime.now()
        self.date = self.datetime_now.date()
        self.date_string = self.date.strftime('%Y-%m-%d')
        self.base_url = 'https://polisen.se/api/events'

    def get_mass_events(self):
        response = requests.get(self.base_url)

        return response.json()

    def get_date_events(self, date):
        # date must be in a text str on format %Y-%m-%d
        response = requests.get(self.base_url + '?DateTime=' + date)

        return response.json()
