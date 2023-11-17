import browser_cookie3
import csv
import webbrowser
import AppOpener
import time
import requests
from urllib.parse import urlparse
import os

def get_extension(url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        url = os.path.basename(path)
        url_without_extension, file_extension = os.path.splitext(url)
        return url, file_extension

def csv_to_dict(file_name):
    dct = {}
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file)
        next(csvFile)   
        for line in csvFile:
            dct[line[0]] = line[1:]
    return dct

def dict_to_csv(headers, dct, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for url in dct:
            writer.writerow([url, *dct[url]])

def csv_to_list(file_name):
    test_list_from_csv = []
    with open(file_name, mode ='r')as file:
   
        # reading the CSV file
        csvFile = csv.reader(file)
        next(csvFile)
    
        # move lines from vsc fiel to test_list_from_csv
        for line in csvFile:
            test_list_from_csv.append(line)
    return test_list_from_csv

# clear cookies, set GPC extension appropriately, close Chrome
def visit_sites(start, filename):
    lst = csv_to_list(filename)
        
    count = 0
    batch_size = 10
    for i, line in enumerate(lst[start:]):
        if count == 0:
            AppOpener.open('google chrome')
        #print(line) #removed index [0]
        webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open('https://www.' + line[0]) #removed index [0]
        count += 1
        print(start + i, line[0]) # to assist where ended in case of failure
        if count == batch_size:
            time.sleep(7)
            AppOpener.close('chrome')
            count = 0
    time.sleep(7)
    AppOpener.close('chrome')

def visit_site(url):
    webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open('https://www.' + url)
    cookies = browser_cookie3.chrome()
    print(len(cookies))

'''
This function takes in a URL and checks if a gpc.json exists within the .well-known 
directory on a given site. If it does, it returns the value for the 'gpc' field i.e.
whether the site claims to respect gpc. Otherwise, it returns false.
'''
def check_gpc_json(url):
    try:
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
        r = requests.get("https://www." + url + "/.well-known/gpc.json" , headers=headers, timeout=3)
        if r.status_code != 404 and 'gpc' in r.json():
            return "TRUE" if r.json()['gpc'] else "FALSE"
        else:
            return "NOT_FOUND"
    except Exception:
        return "json_err"