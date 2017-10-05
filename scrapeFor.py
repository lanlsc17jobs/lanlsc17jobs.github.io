#file to scrape lanl external jobsite by keyword
#dumps content to json

from selenium import webdriver
import bs4, json, sys

def grabInfo(source, url):
    """Will grab the contents of the source sent from a url and split that"""
    """content by the values in splitOn. The content is then returned as  """
    """a dictionary with the keys as the splitOn values and the values as """
    """the results of the split"""
    soup = bs4.BeautifulSoup(source, "lxml")
    irc = soup.select('tr')[10].getText()[14:]
    desc = soup.select('tr')[18].getText()
    contents = {"VacancyNumber" : irc, "Site" : url}
    splitOn = ["Job Title", "Location", "Organization Name", "What You Will Do", "What You Need"]
    sp = desc.split("Job Title")
    for s in range(len(splitOn) - 1):
        sp = sp[1].split(splitOn[s + 1])
        contents[splitOn[s].replace(" ", "")] = sp[0]
    #contents = {"vacancy number": irc, "job title" : desc.split("Job Title")[1].split("Location")[0]}
    return contents

keyword = "ccs"
jsonFile = "jout.json"
info = []

browser = webdriver.Firefox()
browser.get('https://jobszp1.lanl.gov/OA_HTML/OA.jsp?OAFunc=IRC_VIS_HOME_ALL_JOBS')
browser.find_element_by_id('Keywords').send_keys(keyword)
browser.find_element_by_id('Go').click()

i = 0
hasLink = True
while hasLink:
    try:
        elem = browser.find_element_by_id('JobSearchTable:JobName:' + str(i))
        elem.click()
        info.append(grabInfo(browser.page_source, browser.current_url))
        i += 1
        browser.back()
    except:
        hasLink = False

browser.close()

out = {"jobs" : info}
with open(jsonFile, 'w+') as f:
    f.write(json.dumps(out))
