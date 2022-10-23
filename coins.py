from pycoingecko import CoinGeckoAPI
import pprint
from datetime import datetime

cg = CoinGeckoAPI()

X = cg.get_coins_list()

print(len(X))
for i in X:
    r = cg.get_coin_by_id(i['id'])
    print(i['id'], r["market_cap_rank"])
#"market_cap_rank"
'''
import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(X, f, ensure_ascii=False, indent=4)
'''