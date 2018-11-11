#!/usr/bin/env python

import argparse
import itertools
import re
import time
from statistics import median
from typing import List

import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help='URL to poke', type=str)
    parser.add_argument('-n', '--requests', metavar='N',
                        help='number of requests', type=int, default=20)
    parser.add_argument('-a', '--basic-auth', metavar='USER@PASSWORD',
                        help='basic auth credentials', type=str)
    args = parser.parse_args()

    url = build_url(args.url, args.basic_auth)
    timings = calculate_page_load_times(url, args.requests)
    plot_statistics(timings, args.url)


def build_url(url: str, basic_auth: str):
    # type: (str, str) -> str
    if basic_auth:
        url = re.sub(r'^(http://|https://|)', r'\1' +
                     basic_auth + '@', url, count=1)
    return url


def calculate_page_load_times(url, requests):
    # type: (str, int) -> List[float]
    timings = []
    query_parameter_creation_pool = 'xyz2456'

    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.http.phishy-userpass-length', 255)
    binary = FirefoxBinary('/usr/bin/firefox-developer-edition')
    driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)

    for i in range(requests):
        # (n+r-1)! / r! / (n-1)! combinations where r = 7 here
        query_params = list(itertools.combinations_with_replacement(
            query_parameter_creation_pool, 7))
        # length of query_params should always be > n
        tmp_url = f'{url}?{"".join(query_params[i])}'
        start = time.time()
        # driver.implicitly_wait(10)  # seconds
        driver.get(tmp_url)
        wait_for_ajax(driver)
        end = time.time()
        timings.append(end - start)

    driver.close()
    return timings


def plot_statistics(timings, start_url):
    # type: (int, str) -> None
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


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)  # 15 seconds
    try:
        wait.until(lambda driver: driver.execute_script(
            'return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script(
            'return document.readyState') == 'complete')
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
