import requests
import pandas as pd
import time

now = time.time()
inputMint = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
outputMint = 'So11111111111111111111111111111111111111112'
amounts = [5000, 10000, 50000, 100000]
result = {}
for amount in amounts:
    url = f'https://quote-api.jup.ag/v6/quote?inputMint={inputMint}&outputMint={outputMint}'
    url += f'&amount={amount}&slippageBps=10&onlyDirectRoutes=false&asLegacyTransaction=false'

    try:
        result[amount] = requests.get(url).json()
    except:
        pass

end_now = time.time()
latency = end_now - now
df = pd.DataFrame(result)
df.to_csv("data/jup/SOL-USDC/%i-%i.csv" % (now, latency))
