from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from firebase import firebase
import requests
import json

all_team1 = []
all_team2 =[]
matches = []

def match_odds (j):
    team1 = []
    team2 = []
    odds_list = []
    margin = 0
    a = 0 
    b = 0
    link_list = []

    upcoming_match = driver.find_elements_by_css_selector(".upcomingMatch.removeBackground")[j]
    upcoming_match.click()

    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # mydivs = soup.findAll("td", class_= "odds-cell border-left")
    # for mydiv in mydivs:
    #     link = mydiv.find("a")["href"]
    #     if link[:20] not in link_list:
    #         link_list.append(link[:20])
    #         print(link)

    #upcoming match
    odds = driver.find_elements_by_css_selector(".odds-cell.border-left")

    for odd in odds:            #separate the odds from empty fields
        text = odd.text
        if text == "" or text == "-":
            continue
        else:
            odds_list.append(text)

    for index, element in enumerate(odds_list):     #add the odds to the team they belong
        if index % 2 == 0:
            team1.append(element)
        else:
            team2.append(element)

    try:
        a = float(max(team1))
        b = float(max(team2))
        margin = (1/a + 1/b)

        print(str(team1) + "    Max: " + str(a))
        print(str(team2) + "    Max: " + str(b))

        if margin < 1.0 and margin != 0:
            print("Good fucking match to bet on")
            print(round(margin, 3))
        else:
            print("Sadly not the game")
    except:
        print("No odds for this match ")

    matches.append({
        "team1" : team1,
        "team2" : team2
    })

    driver.back()

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)  # Optional argument, if not specified will search path.

page_hltv = driver.get('https://www.hltv.org/matches')

for i in range(10):
    match_odds(i)

driver.quit()

firebase = firebase.FirebaseApplication("https://scrape-853ad-default-rtdb.europe-west1.firebasedatabase.app/", None)
result = firebase.post('/scrape-853ad-default-rtdb/', matches)

# Ta oddsen ut en tagg och försöka få länk och odds direkt ur <tr> taggen. Även ignorera de <tr> som inte innhåller classnamn med odds-cell / ignorera de <tr> som inte har två odds