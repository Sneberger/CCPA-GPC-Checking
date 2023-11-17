import csv
import bsexplore
from tranco import Tranco
import utility_functions
import utility_us_privacy_string
import utility_optanon


def url_column(num_urls = 60000):
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
            result = bsexplore.explore(line[0], None, 0)  # replace function as desired
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

def main():
    url_column(30)
    ccpa_column()
    gpc_json_column()
    utility_us_privacy_string.resultsDEFG()
    # On local Chrome turn GPC off and clear browsing cookies
    utility_optanon.optanon_with_gpc_off()
    # On local Chrome turn GPC on and clear browsing cookies
    # utility_optanon.optanon_with_gpc_on()

if __name__ == "__main__":
    main()