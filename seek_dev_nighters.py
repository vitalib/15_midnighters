import datetime
import requests
import pytz


def load_attempts():
    devman_api_url = "https://devman.org/api/challenges/solution_attempts/"
    page = 1
    while True:
        attempts_response = requests.get(devman_api_url,
                                         params={'page': page}
                                         ).json()
        attempts_list = attempts_response['records']
        yield from attempts_list
        total_pages = attempts_response['number_of_pages']
        if page == total_pages:
            break
        else:
            page += 1


def get_midnighters(attempts):
    midnighters = set()
    for attempt in attempts:
        time_zone = pytz.timezone(attempt['timezone'])
        attempt_time = datetime.datetime.fromtimestamp(
                                                       attempt['timestamp'],
                                                       time_zone
                                                       )

        if 0 <= attempt_time.hour < 6:
            midnighters.add(attempt['username'])
    return midnighters


if __name__ == '__main__':
    all_attempts = load_attempts()
    midnighters = get_midnighters(all_attempts)
    print('Midnighters of DevMan are:')
    for index, midnighter in enumerate(midnighters, 1):
        print(index, midnighter)
