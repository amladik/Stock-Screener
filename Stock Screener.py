import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def getStockInfo(ticker):
    diction = {}


    URL = "https://www.marketwatch.com/investing/stock/"+ticker+"/company-profile"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

    tables = soup.findAll('table', attrs={'class': 'table value-pairs no-heading'})

    URL = 'https://www.marketwatch.com/investing/stock/' + ticker+'?mod=mw_quote_tab'

    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    parse1 = soup.findAll('div', attrs={'class' : 'column column--aside'})

    MarketCap = parse1[1].findAll('li')[3].find('span').get_text()[1:]

    if(MarketCap[-1] == 'T'):
        MarketCap = float(MarketCap[:-1])*1000000000000

    elif(MarketCap[-1] == 'B'):
        MarketCap = float(MarketCap[:-1])*1000000000

    elif(MarketCap[-1] == 'M'):
        MarketCap = float(MarketCap[:-1])*1000000


    diction['Market Cap'] = MarketCap


    profitability = tables[3]

    valuations = tables[0]



    valuationContent = valuations.findAll('tr')

    profitabilityContent = profitability.findAll('tr')

    ROIC = float(profitabilityContent[7].findAll('td')[1].get_text()[:-1])

    diction['ROIC'] = ROIC

    try:

        PERatio = float(valuationContent[0].findAll('td')[1].get_text().replace(',',''))
        diction['EBIT'] = 1/PERatio

    except:
        PERatio = 0.0
        diction['EBIT'] = 0.0

    
    PricetoBookRatio = float(valuationContent[4].findAll('td')[1].get_text())

    diction['P/B Ratio'] = PricetoBookRatio
    PricetoSalesRatio = float(valuationContent[3].findAll('td')[1].get_text())

    diction['P/S Ratio'] = PricetoSalesRatio



  




    return(diction)


diction = {}

listofstocks = []


file1 = open('stock interests.txt','r')
lines = file1.readlines()

for line in lines:
    listofstocks.append(line.replace('\n',''))

print(listofstocks)
for ticker in listofstocks:
    print(ticker)
    diction[ticker] = getStockInfo(ticker)




data = pd.DataFrame(diction).T

data['MCap Score'] = np.NaN
data['ROIC Score'] = np.NaN
data['EBIT Score'] = np.NaN
data['P/B Score'] = np.NaN
data['P/S Score'] = np.NaN
data['Kunal Score'] = np.NaN

counter = 0
for index,value in data['Market Cap'].sort_values(ascending=False).items():
    counter+=1
    data['MCap Score'][index] = counter

counter = 0
for index,value in data['ROIC'].sort_values(ascending=False).items():
    counter+=1
    data['ROIC Score'][index] = counter

counter = 0
for index,value in data['EBIT'].sort_values(ascending=False).items():
    counter+=1
    data['EBIT Score'][index] = counter

counter = 0
for index,value in data['P/B Ratio'].sort_values(ascending=True).items():
    counter+=1
    data['P/B Score'][index] = counter

counter = 0
for index,value in data['P/S Ratio'].sort_values(ascending=True).items():
    counter+=1
    data['P/S Score'][index] = counter


for stocks in listofstocks:
    data['Kunal Score'][stocks] = data['MCap Score'][stocks] + data['ROIC Score'][stocks] + data['EBIT Score'][stocks] + data['P/B Score'][stocks] + data['P/S Score'][stocks]

data = data.sort_values(['Kunal Score'], ascending=True)

print(data)

data.to_excel('Stock_Screener.xlsx')