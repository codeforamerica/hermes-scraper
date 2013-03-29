from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from models.case import Case
from models.case_event_historical import CaseEventHistorical
from db import connection
from sqlalchemy.sql import exists
from sqlalchemy.orm import joinedload

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

def save_cases(cases):
    print "Saving cases to DB..."

    session = connection.Session()
    for number in cases:

        # Save new case in DB if it doesn't exist already
        cs = session.query(Case).filter(Case.number == number).all()
        if len(cs) == 0:
            c = Case(number, cases[number]['title'])
            session.add(c)
        else:
            c = cs[0]

        # Unflag previously-flagged latest events for the case
        for latest_event in session.query(CaseEventHistorical) \
                                   .options(joinedload(CaseEventHistorical.case)) \
                                   .filter(CaseEventHistorical.latest) \
                                   .filter(CaseEventHistorical.case == c) \
                                   .all():
            latest_event.latest = False
            session.add(latest_event)

        # Save latest events for the case
        for event_datetime in cases[number]['events']:
            event = cases[number]['events'][event_datetime]
            ce = CaseEventHistorical(c, event_datetime, event['title'], '')
            session.add(ce)

    session.commit()

# Main
driver = webdriver.Firefox()

totalNumCases = 0
for lastname_prefix in generate_lastname_prefixes():
    submit_search_form(driver, lastname_prefix)
    cases = {}
    parse_cases_from_results_page(driver, cases)
    totalNumCases += len(cases)
    save_cases(cases)
    print "Harvested " + str(totalNumCases) + " cases so far."
    

driver.close()
