import requests
from bs4 import BeautifulSoup
import pprint

# This section provides the site and parses out the info wanted
# This example uses the Hacker News Arrticles page
# Line 12-15 are the specific attributes you want to find
res = requests.get('https://news.ycombinator.com/front')
res2 = requests.get('https://news.ycombinator.com/front?day=2020-10-12&p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')
links = soup.select('.storylink')
links2 = soup2.select('.storylink')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

# Combines the two pages into one long string
mega_links = links + links2
mega_subtext = subtext + subtext2


# Sorts the output from highest vote count to lowest
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


# This function does all of the sorting work
# It will look for articles with a vote count of more than 99
def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href')
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(mega_links, mega_subtext))
