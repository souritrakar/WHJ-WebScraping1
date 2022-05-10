
from bs4 import BeautifulSoup
import requests
import csv

url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, 'html.parser')

headers = ['NAME', 'DISTANCE', 'MASS', 'RADIUS']


def webscrape():

    data = []
    # Accessing table
    table = soup.find("table", attrs={'class', 'wikitable'})
    table_body = table.find('tbody')
    # Table Row Tags
    tr_tags = table_body.find_all('tr')
    for i in tr_tags:
        td_tags = i.find_all('td')
        temp = []
        # Looping through row
        for index, j in enumerate(td_tags):
            # For <a> tag value
            if(index == 1):
                a_tag = j.find_all('a')
                # Some of them are plain text, not <a>
                if(a_tag):
                    temp.append(a_tag[0].contents[0])
                else:
                    temp.append(j.text)
            #Distance, Mass, Radius
            elif(index == 3 or index == 5 or index == 6):
                temp.append(j.text.strip("0").strip('\n'))

        data.append(temp)
        print(data)
        with open('data.csv', 'w') as f:
            fs = csv.writer(f)
            fs.writerow(headers)
            fs.writerows(data)


webscrape()
