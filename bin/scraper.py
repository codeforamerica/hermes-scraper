from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

def parse_cases_from_results_page(driver, cases):
    for case_row_el in driver.find_elements_by_xpath("//tr[@class='caseItem' or @class='caseAlternateItem']"):
        case = {}

        case_number_el = case_row_el.find_element_by_xpath("td/div[@class='dataCase']")
        cases[case_number_el.text] = case
        
        case_title_el = case_row_el.find_element_by_xpath("td/div[@class='dataTitle']")
        case['title'] = case_title_el.text

        case_events = {}
        case['events'] = case_events
        case_event_els = case_title_el.find_elements_by_xpath("../div[span/@class='itemEvent']")
        for case_event_el in case_event_els:
            case_event_detail_els = case_event_el.find_elements_by_tag_name("span")
            case_events[case_event_detail_els[1].text] = {
                "title": case_event_detail_els[0].text
            }

    next_els = driver.find_elements_by_link_text("Next")
    if len(next_els) > 0:
        next_el = next_els[0]
        if not next_el.get_attribute("disabled"):
            print "... next page..."
            next_el.click()
            time.sleep(random.randint(1,2))
            parse_cases_from_results_page(driver, cases)
    
def generate_lastname_prefixes():
    prefixes = []
    chars = range(65, 65+26)
    for i1 in chars:
        for i2 in chars:
            for i3 in chars:
                prefixes.append(chr(i1) + chr(i2) + chr(i3))

    random.shuffle(prefixes)
    return prefixes
        
# Submit search form
def submit_search_form(driver, lastname_prefix):
    print "Searching for cases with lastname prefix = " + lastname_prefix + "..."
    driver.get("http://kcoj.kycourts.net/CourtRecords/Search.aspx")
    driver.find_element_by_name("ctl00$ContentPlaceHolder_Content$tab_container_search$tab_party$cmb_PS_county").send_keys("JEFFERSON")
    driver.find_element_by_name("ctl00$ContentPlaceHolder_Content$tab_container_search$tab_party$cmb_PS_party_type").send_keys("DEFENDANT")
    lastnameEl = driver.find_element_by_name("ctl00$ContentPlaceHolder_Content$tab_container_search$tab_party$tb_PS_last_name")
    lastnameEl.clear()
    lastnameEl.send_keys(lastname_prefix)
    driver.find_element_by_name("ctl00$ContentPlaceHolder_Content$tab_container_search$tab_party$btn_PS_search").click()
    time.sleep(random.randint(1,4))

# Main
driver = webdriver.Firefox()

cases = {}
for lastname_prefix in generate_lastname_prefixes():
    submit_search_form(driver, lastname_prefix)
    parse_cases_from_results_page(driver, cases)
    print "Harvested " + str(len(cases)) + " cases so far."
    

print cases
driver.close()
