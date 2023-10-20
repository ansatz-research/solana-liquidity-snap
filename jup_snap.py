import requests
import pandas as pd
import time

# List of mint pairs
mints = [
    ('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', 'So11111111111111111111111111111111111111112'),
    ('So11111111111111111111111111111111111111112', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'),
    # Add more mint pairs as needed
]

amounts = [5000, 10000, 50000, 100000]

for inputMint, outputMint in mints:
    now = time.time()
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
    # Map mints to symbols
    mint_symbols = [inputMint, outputMint]
    
    # todo here
    mint_symbols = ['USDC' if mint_symbol != 'So11111111111111111111111111111111111111112' else 'SOL' for mint_symbol in mint_symbols]
    # Generate the filename
    filename = f"data/jup/{mint_symbols[0]}-{mint_symbols[1]}/{int(now)}-{int(latency)}.csv"

    df = pd.DataFrame(result)
    df.to_csv(filename)

    print(f"Data saved to {filename}")
