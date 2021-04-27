import requests
import keys
import pandas as pd
from time import sleep

def get_crypto_rates(base_currency='USD', assets = 'BTC,ETH,XRP,ADA,BAT,LINK,DOGE,DOT'):
    
    url = "https://api.nomics.com/v1/currencies/ticker"

    payload = {'key' : keys.API_KEY, 'convert':base_currency, 'ids' : assets, 'interval':'1d'}
    response = requests.get(url,params=payload)
    data = response.json()

    crypto_currency, crypto_price , crypto_timestamp = [], [], []

    for asset in data:
        crypto_currency.append(asset['currency'])
        crypto_price.append(asset['price'])

    raw_data = {
        'assets' : crypto_currency,
        'rates' : crypto_price,
    }

    df = pd.DataFrame(raw_data)
    return df

def set_alert(dataframe, asset , alert_high_price ):

    crypto_value = float(dataframe[dataframe['assets'] == asset]['rates'].item())
    details = f'{asset}: {crypto_value}, Target : {alert_high_price}'

    if crypto_value >= alert_high_price:
        print(details + "Target Reached!")
    else:
        print(details)
    

loop = 0
while True:
    print(f'--------------------({loop})---------------------------')

    try:
        df = get_crypto_rates()

        set_alert(df,'BTC',60000)
        set_alert(df,'ETH',10000)
        set_alert(df,'XRP',5)
        set_alert(df,'ADA',5)
        set_alert(df,'BAT',5)
        set_alert(df,'LINK',100)
        set_alert(df,'DOGE',1)
        set_alert(df,'DOT',100)
    except Exception as e:
        print("Couldn't fetch data.Try Again!")
    
    loop+=1
    sleep(30)
