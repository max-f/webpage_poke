#!/usr/bin/env python

import time
import argparse
import itertools

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help='URL to poke', type=str)
    args = parser.parse_args()

    start_url = args.url
    timings = create_page_statistics(start_url)
    avg_time = sum(timings) / float(len(timings))
    print('Noiiice!')
    print(f'Avg time: {avg_time}')


def create_page_statistics(start_url, n=20):
    timings = []
    query_parameter_creation_pool = 'abcdefg'
    browser = webdriver.Firefox()

    for i in range(n):
        # (n+r-1)! / r! / (n-1)! combinations where r = 7 here
        query_params = list(itertools.combinations_with_replacement(
            query_parameter_creation_pool, 7))
        # length of query_params should always be > n
        tmp_url = f'{start_url}?{"".join(query_params[i])}'
        start = time.time()
        # browser.implicitly_wait(10)  # seconds
        browser.get(tmp_url)
        wait_for_ajax(browser)
        end = time.time()
        timings.append(end - start)

    browser.close()
    return timings


def wait_for_ajax(browser):
    wait = WebDriverWait(browser, 15)  # 15 seconds
    try:
        wait.until(lambda browser: browser.execute_script(
            'return jQuery.active') == 0)
        wait.until(lambda browser: browser.execute_script(
            'return document.readyState') == 'complete')
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
