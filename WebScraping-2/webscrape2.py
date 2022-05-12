from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, 'html.parser')

headers = ['NAME', 'DISTANCE', 'MASS', 'RADIUS']


def webscrape():

    data = []
    # Fetching list of tables with classname 'wikitable'
    tables = soup.findAll("table", attrs={'class', 'wikitable'})
    # Accessing <tr> tags of the 'Field brown dwarfs' table
    tr_tags = tables[1].find_all('tr')
    # Table row tags
    for i in tr_tags:
        td_tags = i.find_all('td')
        temp = []
        # Looping through row
        for index, j in enumerate(td_tags):
            # For <a> tag value
            if(index == 0):
                a_tag = j.find_all('a')
                # Some of them are plain text, not <a>
                if(a_tag):
                    temp.append(a_tag[0].contents[0])
                else:
                    temp.append(j.text)
            #Distance, Mass, Radius
            elif(index == 5 or index == 7 or index == 8):
                if(len(j.text) > 0):

                    temp.append(j.text.strip("0").strip('\n'))
                else:
                    temp.append("N/A")

        data.append(temp)

    # Creating dataframe from array and writing to csv file
    df = pd.DataFrame(data, columns=headers)
    df.to_csv('star_data.csv', index=False)


webscrape()
