from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pyshark
from time import sleep
import utility_functions


def initialize_driver(gpc_on):
    options = Options()
    options.headless = True
    options.page_load_strategy = "eager"
    options.set_preference("privacy.globalprivacycontrol.enabled", gpc_on)
    options.set_preference("privacy.globalprivacycontrol.functionality.enabled", gpc_on)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("network.cookie.lifetimePolicy", 0)
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("network.http.use-cache", False)
    return webdriver.Firefox(options=options)

def count_packets(driver, url):
    driver.get("https://www." + url)
    capture = pyshark.LiveCapture(interface='Wi-Fi')
    capture.sniff(timeout=2)
    sleep(5)
    return len(capture)

def try_one_url(url):
    driver = initialize_driver(gpc_on=False)
    off_packets = count_packets(driver, url)
    driver.quit()

    driver = initialize_driver(gpc_on=True)
    on_packets = count_packets(driver, url)
    driver.quit()

    if off_packets == 0:
        percentage_change = float('inf')
    else:
        percentage_change = (off_packets - on_packets) / off_packets

    return [off_packets, on_packets, percentage_change]



def resultsJKL():
    list_from_csv = utility_functions.csv_to_list('resultsABCDEFGHI.csv')
    header = ['URL', 'CCPA', 'gpc_json', 'usp_string_off', 'usp_off_version', 'usp_string_on', 'usp_on_version', 'Optanon_GPC_off', 'Optanon_GPC_on', 'packets_gpc_off', 'packets_gpc_on', 'packet_change']

    with open('resultsABCDEFGHIJKL.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        # Start processing from the 58th website
        for counter, line in enumerate(list_from_csv):
            try:
                url = line[0]
                results = try_one_url(url)
                writer.writerow([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], results[0], results[1], results[2]])
            except Exception as e:
                print(f"Error processing {url}: {e}")
                writer.writerow([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], 'Gen_Error', 'Gen_Error', 'N/A'])


def main():
    url = input("Enter a URL to analyze (without 'https://www.'): ")
    try:
        off_packets, on_packets = try_one_url(url)
        print(f"Results for {url}:")
        print(f"Off Packets: {off_packets}")
        print(f"On Packets: {on_packets}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()