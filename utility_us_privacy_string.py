# This basic code came from Jan Charatan's GitHub at https://github.com/jancharatan/thesis-code

import multiprocessing
from selenium import webdriver
#from selenium.webdriver.firefox.options import FirefoxOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import re
import datetime
# from resources.utils import convert_list
# from resources.constants import opt_out_links
from time import sleep
import utility_functions

day = datetime.datetime.now().day
month = datetime.datetime.now().month
global monthday
monthday = str(month) + "-" + str(day)


def run_usp_api(filename, websites_csv, nrows):
    websites = convert_list(websites_csv, nrows)
    with open("./results/" + filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "opt_out_link", "off_string", "off_version", "on_string", "on_version"])
        for i in range(0, len(websites), 100):
            with multiprocessing.Pool(processes=8) as pool:
                for result in pool.map(try_one_url, websites[i:i+100]):
                    writer.writerow(result)

def try_one_url(url):
    # print("Trying " + url + "...")
    (opt_out_link_on, on_string, on_version) = uspapi(url, True)
    (opt_out_link_off, off_string, off_version) = uspapi(url, False)
    return [url, opt_out_link_on or opt_out_link_off, off_string, off_version, on_string, on_version]

def uspapi(url, gpc_on):
    #options = FirefoxOptions()
    options = Options()
    options.headless = True
    options.page_load_strategy = "eager"
    options.set_preference("privacy.globalprivacycontrol.enabled", gpc_on)
    options.set_preference("privacy.globalprivacycontrol.functionality.enabled", gpc_on)
    #options.add_argument("privacy.globalprivacycontrol.enabled")
    #options.add_argument("privacy.globalprivacycontrol.functionality.enabled")
    service = Service('./drivers/geckodriver')
    driver = webdriver.Firefox(options=options)    # removed argues "service=service, options=options"
    driver.set_page_load_timeout(30)
    link_present = False
    
    try:
        driver.get("https://www." + url)

        driver.execute_script('window.scrollBy(0, 10000);')
        sleep(4)
        driver.execute_script('window.scrollBy(0,-10000)')

        # soup = BeautifulSoup(driver.page_source, "html.parser")
        # for possible_link in opt_out_links:
        #     opt_out_link = soup.find(text=re.compile(possible_link, flags=re.IGNORECASE))
        #     if opt_out_link:
        #         link_present = True

        driver.save_screenshot("results/screenshots/" + monthday + "/" + url.replace(".", "-") + "_" + ("TRUE" if gpc_on else "FALSE") + ".png")
        driver.execute_script("__uspapi('getUSPData', 1 , (uspData, success) => { if(success) { console.log(uspData); localStorage.setItem('uspData', uspData.uspString); localStorage.setItem('uspVersion', uspData.version); } else { localStorage.setItem('uspData', 4) ; localStorage.setItem('uspVersion', 4); } } ) ;")
        uspString = uspVersion = ""
        while not (uspString and uspVersion):
            uspString = driver.execute_script("return localStorage.getItem('uspData')")
            uspVersion = driver.execute_script("return localStorage.getItem('uspVersion')")
            driver.execute_script("__uspapi('getUSPData', 1 , (uspData, success) => { if(success) { console.log(uspData); localStorage.setItem('uspData', uspData.uspString); localStorage.setItem('uspVersion', uspData.version); } else { localStorage.setItem('uspData', 4) ; localStorage.setItem('uspVersion', 4); } } ) ;")
        driver.quit()
        return (True, uspString, uspVersion)    # changed link_present to True as know true
    except Exception:
        driver.quit()
        return (True, 0, 0)

def analyze_uspapi_data(csv_name):
    opt_out = []
    no_opt_out = []
    opt_out_ns = no_opt_out_ns = 0

    f = open(csv_name, "r")
    next(f)
    for line in f:
        line_data = line.split(",")
        if "d" in line_data[2]:
            print(line_data[2])
        ans = ""

        if line_data[2] == "0":
            ans += "0"
        elif len(line_data[2]) == 4:
            ans += line_data[2][2]
        else:
            ans += "9"
        
        if line_data[4] == "0":
            ans += "0"
        elif len(line_data[4]) == 4:
            ans += line_data[4][2]
        else:
            ans += "9"

        if ans != "00":
            opt_out.append(ans) if line_data[1] == "True" else no_opt_out.append(ans)
        
        if line_data[1] == "True":
            opt_out_ns += 1
        else:
            no_opt_out_ns += 1
    f.close()

    print(len(opt_out), len(no_opt_out))
    print(sorted(opt_out), sorted(no_opt_out))
    print(opt_out_ns, no_opt_out_ns)

def resultsDEFG():
    # before = datetime.datetime.now().replace(microsecond=0)
    # run_usp_api("usp_api_" + str(datetime.datetime.now().month) + "_" + str(datetime.datetime.now().day) + ".csv", "./resources/top-1m-091522.csv", 100)
    # after = datetime.datetime.now().replace(microsecond=0)
    # print(after - before)
    #print(try_one_url('meliopayments.com'))    #use this for testing one single url

    # Added this code to Charatan's to manage intake from csv
    header = ['URL', 'CCPA', 'gpc_json', 'usp_string_off', 'usp_off_version', 'usp_string_on', 'usp_on_version']  
    test_list_from_csv = utility_functions.csv_to_list('resultsABC.csv')

        #print(*test_list_from_csv, sep = '\n')
        #result_list = []
    with open('resultsABCDEFG.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        counter = 1
        for line in test_list_from_csv:
            result = try_one_url(line[0])
            writer.writerow([line[0], line[1], line[2], result[2], result[3], result[4], result[5]])
            print(counter, line[0], result)
            counter += 1

if __name__ == "__main__":
    resultsDEFG()