import browser_cookie3
import time
import utility_functions


# run twice, once with GPC off then with GPC on
def cookie_to_dict(filename):
    dct = utility_functions.csv_to_dict(filename) # changed from manual input
    for key in dct:
        dct[key].append('not_found')  # removed because overwrites previous results
    cookies = list(browser_cookie3.chrome())
    for cookie in cookies:
        url = cookie.domain
        i = cookie.domain.rfind('.')
        temp = cookie.domain[:i]
        i = temp.rfind('.')
        if i > -1:
            url = url[i+1:]
        if cookie.name == 'OptanonConsent':    
            if 'isGpcEnabled=0' in cookie.value:
                if url in dct:
                    print(url, '0')
                    dct[url][-1] = '0'
            elif 'isGpcEnabled=1' in cookie.value:
                if url in dct:
                    print(url, '1')
                    dct[url][-1] = '1'
    return dct


def optanon_with_gpc_off():
    # Manual work required: run First Step then run Second step
    # Part One First Step: clear cookies in Chrome, set GPC extension to "off", open Chrome,then visit_sites(start, stop)
    utility_functions.visit_sites(0, 'resultsABCDEFG.csv')  # open Chrome before each run
    time.sleep(5)

    # Part One Second step: close Chrome
    header = ['URL', 'CCPA', 'gpc_json', 'usp_string_off', 'usp_off_version', 'usp_string_on', 'usp_on_version', 'Optanon_GPC_off']
    utility_functions.dict_to_csv(header, cookie_to_dict('resultsABCDEFG.csv'), 'resultsABCDEFGH.csv')   # correct file names

def optanon_with_gpc_on():
    # Part Two First Step: clear cookies in Chrome, set GPC extension to "on", open Chrome, then visit_sites(start, stop)
    utility_functions.visit_sites(0, 'resultsABCDEFGH.csv') # open Chrome before each run
    time.sleep(5)

    # Part Two Second step: close Chrome
    header = ['URL', 'CCPA', 'gpc_json', 'usp_string_off', 'usp_off_version', 'usp_string_on', 'usp_on_version', 'Optanon_GPC_off', 'Optanon_GPC_on']
    utility_functions.dict_to_csv(header, cookie_to_dict('resultsABCDEFGH.csv'), 'resultsABCDEFGHI.csv')

def find_individual_cookie():   # utility not needed for main process
    cookies = browser_cookie3.chrome()
    for cookie in cookies:
        print(cookie)
        if cookie.name == 'OGPC':
            print(cookie)
