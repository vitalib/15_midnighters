import datetime
import requests
import pytz


def load_attempts():
    devman_api_url = "https://devman.org/api/challenges/solution_attempts/"
    attempts_pages = requests.get(devman_api_url).json()['number_of_pages']
    for page in range(1, attempts_pages+1):
        attempts_page_url = '{}?page={}'.format(devman_api_url, page)
        attempts_list = requests.get(attempts_page_url).json()['records']
        for attempt in attempts_list:
            yield attempt


def get_midnighters(attempts):
    night_period_hours = range(7)
    midnighters = set()
    for attempt in attempts:
        time_zone = pytz.timezone(attempt['timezone'])
        attempt_time = datetime.datetime.fromtimestamp(
                                                       attempt['timestamp'],
                                                       time_zone
                                                       )
        if attempt_time.hour in night_period_hours:
            midnighters.add(attempt['username'])
    return midnighters


if __name__ == '__main__':
    all_attempts = load_attempts()
    midnighters = get_midnighters(all_attempts)
    print('Midnighters of DevMan are:')
    for index, midnighter in enumerate(midnighters, 1):
        print(index, midnighter)
