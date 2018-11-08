#!/usr/bin/env python

import time
import argparse
import itertools

from statistics import median
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help='URL to poke', type=str)
    args = parser.parse_args()

    start_url = args.url
    timings = calculate_page_load_times(start_url)
    create_statistics(timings, start_url)


def create_statistics(timings, start_url):
    avg_time = sum(timings) / float(len(timings))
    median_time = median(timings)
    n, bins, patches = plt.hist(
        timings, range=(0, 11), density=True, facecolor='blue', alpha=0.5)
    plt.xlabel(
        f'time in seconds\n Avg time: {avg_time:2.3} - Median time: {median_time:2.3}')
    plt.ylabel('percentage of requests')
    plt.title(f'Histogram of page loads\n URL: {start_url[:40]}..')
    plt.subplots_adjust(left=0.15)
    plt.show()


def calculate_page_load_times(start_url, n=20):
    timings = []
    query_parameter_creation_pool = 'xyz2456'
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
