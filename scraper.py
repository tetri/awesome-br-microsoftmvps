import requests
from bs4 import BeautifulSoup
import urllib.parse

page_number = 1
page = requests.get(f'https://mvp.microsoft.com/pt-br/MvpSearch?&lo=Brazil&sc=n&ps=48&pn={page_number}')
while True:
    soup = BeautifulSoup(page.content, 'html.parser')
    profiles = soup.find_all('div', class_='profileListItem')
    if len(profiles) == 0:
        break;

    for profile in profiles:
        fullName = profile.find('div', class_='profileListItemFullName').find('a')
        name = fullName.text.strip()
        link = 'https://mvp.microsoft.com' + urllib.parse.quote(fullName.get('href'))

        competency = profile.find('div', class_='profileListItemCompetency')
        competency_content = competency.find('span', class_='subItemContent')
        award_category = competency_content.text.strip()

        profile_page = requests.get(link)
        profile_soup = BeautifulSoup(profile_page.content, 'html.parser')
        
        infoPanel = profile_soup.find('div', class_='infoPanel')
        infoContents = infoPanel.find_all('div', class_='infoContent')
        
        first_year_awarded = int(infoContents[1].text.strip())
        number_of_mvp_awards = int(infoContents[2].text.strip())

        #trophys = '🏆' * number_of_mvp_awards
        print(f'| [{name}]({link}) | {award_category} | {first_year_awarded} | {number_of_mvp_awards} |')
    
    page_number = page_number + 1
    page = requests.get(f'https://mvp.microsoft.com/pt-br/MvpSearch?&lo=Brazil&sc=n&ps=48&pn={page_number}')

    break #temporario
