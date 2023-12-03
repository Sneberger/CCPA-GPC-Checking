import csv
from tranco import Tranco
import utility_functions
import utility_us_privacy_string
import utility_optanon
import browser_cookie3
import utility_count_packets

def url_column(num_urls = 60000):   # number can be reduced for testing
    t = Tranco(cache=True, cache_dir='.tranco')
    base_list = t.list().top(num_urls)
    header = ['URL']
    middle_list = []
    extensions = ['.com', '.net']   # made decision to limit to these extensions

    # add extension to tuple with whole url
    for url in base_list:
        url, extension = utility_functions.get_extension(url)
        if extension in extensions:
            middle_list.append(url)
    
    # writing the data into the file
    with open('resultsA.csv', 'w', newline ='') as file:    
        writer = csv.writer(file)
        writer.writerow(header)
        for url in middle_list:
            writer.writerow([url])

def ccpa_column():
    test_list_from_csv = utility_functions.csv_to_list('resultsA.csv')
    header = ['URL', 'CCPA']

    #print(*test_list_from_csv, sep = '\n')
    #result_list = []
    with open('resultsAB.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        counter = 1

        for line in test_list_from_csv:
            result = utility_functions.explore(line[0], None, 0)  # replace function as desired
            if result == 'True':    # filtering down results for future processing
                writer.writerow([line[0], result])
            print(counter, line[0], result)      # to show progress in terminal
            counter += 1


def gpc_json_column():
    # Input here should be only those urls that = True for CCPA
    # This basic code came from Jan Charatan's GitHub at https://github.com/jancharatan/thesis-code
    # I removed Tranco/list-building/percentage code and added below to pull from csv and build list
    test_list_from_csv = utility_functions.csv_to_list('resultsAB.csv')
    header = ['URL', 'CCPA', 'gpc_json']

    #print(*test_list_from_csv, sep = '\n')
    #result_list = []
    with open('resultsABC.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        counter = 1

        for line in test_list_from_csv:
            result = utility_functions.check_gpc_json(line[0])
            writer.writerow([line[0], True, result])    #True is plug based on narrow input of CCPA = True
            print(counter, line[0], result)
            counter += 1

def cookie_counter():
    cookies = browser_cookie3.chrome()
    print('Aggregate number of cookies =', len(cookies))

def columnsABCDEFGH():
    url_column(30)                             # outputs 'resultsA.csv'
    ccpa_column()                              # outputs 'resultsAB.csv'
    gpc_json_column()                          # outputs 'resultsABC.csv'
    utility_us_privacy_string.resultsDEFG()    # outputs 'resultsABCDEFG.csv'
    utility_optanon.optanon_with_gpc_off()     # outputs 'resultsABCDEFGH.csv'
    cookie_counter()                           # OPTIONAL: outputs total to console
        
def columnsIJKL():
    utility_optanon.optanon_with_gpc_on()      # outputs 'resultsABCDEFGHI.csv'
    utility_count_packets.resultsJKL()         # outputs 'resultABCDEFGHIJKL.csv"
    cookie_counter()                           # OPTIONAL: outputs total to console

def main():
    # This program requires that the user have a browser extension that enables
    # turning the GPC signal on and off in the user's local Chrome browswer (such as
    # 'GPC enable'). The program needs to be run twice as there is no way to automate
    # toggling the GPC setting in the local Chrome browser for some functions. Run
    # columnsABCDEFGH() first with GPC signal off then run columnIJKL() with GPC signal on.
    
    # MANUAL WORK REQUIRED: set GPC signal in local Chrome Browser to off
    columnsABCDEFGH()
    # MANUAL WORK REQUIRED: set GPC signal in local Chrome Browser to on
    #columnsIJKL()
    # In order to continue alphabetic column output this function runs last

if __name__ == "__main__":
    main()
