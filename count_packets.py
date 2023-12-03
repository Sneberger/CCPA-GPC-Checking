from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pyshark
from time import sleep

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

def uspapi(driver, url):
    driver.get("https://www." + url)
    capture = pyshark.LiveCapture(interface='Wi-Fi')
    capture.sniff(timeout=2)
    sleep(5)
    return len(capture)

def try_one_url(url):
    driver = initialize_driver(gpc_on=False)
    off_packets = uspapi(driver, url)
    driver.quit()

    driver = initialize_driver(gpc_on=True)
    on_packets = uspapi(driver, url)
    driver.quit()

    return [off_packets, on_packets]



def resultsJK(input_csv):
    with open(input_csv, 'r') as file:
        rows = list(csv.reader(file))
        header = rows[0]

        # Start processing from the 58th website
        for counter, row in enumerate(rows[503:], start=503 ):
            try:
                url = row[0]
                results = try_one_url(url)
                row[-2:] = results  # Replace the last two columns (gpc_off, gpc_on) with new results
                print(counter, url, results)
            except Exception as e:
                print(f"Error processing {url}: {e}")
                row[-2:] = ['Error', 'Error']  # Replace with error indication

    # Write the updated rows back to the CSV file
    with open(input_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def main():
    url = input("Enter a URL to analyze (without 'https://www.'): ")
    try:
        off_packets, on_packets = countpackets.try_one_url(url)
        print(f"Results for {url}:")
        print(f"Off Packets: {off_packets}")
        print(f"On Packets: {on_packets}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()