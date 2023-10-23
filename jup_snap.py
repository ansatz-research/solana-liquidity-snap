import requests
import pandas as pd
import time

est_prices = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=usd-coin,wrapped-solana&vs_currencies=usd').json()

sol_price = est_prices['wrapped-solana']['usd']

precision_map = {
    'So11111111111111111111111111111111111111112': {'precision': 9, 'name': 'SOL'},
    'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v': {'precision': 6, 'name': 'USDC'},

}

# List of mint pairs
mints = [
    ('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', 'So11111111111111111111111111111111111111112'),
    ('So11111111111111111111111111111111111111112', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'),
    # Add more mint pairs as needed
]

usdc_amounts = [5_000, 10_000, 50_000, 100_000]

for inputMint, outputMint in mints:
    now = time.time()
    result = {}

    for i, usdc_amount in enumerate(usdc_amounts):
        inAmount = 0
        if inputMint == 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v':
            inAmount = int(usdc_amount * (10 ** precision_map[inputMint]['precision']))
        else:
            est_price = sol_price
            inAmount = int(usdc_amount * (10 ** precision_map[inputMint]['precision'] / est_price))
        url = f'https://quote-api.jup.ag/v6/quote?inputMint={inputMint}&outputMint={outputMint}'
        url += f'&amount={inAmount}&slippageBps=10&onlyDirectRoutes=false&asLegacyTransaction=false'

        try:
            jj = requests.get(url).json()
            if 'error' not in list(jj.keys()): 
                result[i] = jj
        except:
            pass

    end_now = time.time()
    latency = end_now - now
    # Map mints to symbols
    mint_symbols = [inputMint, outputMint]
    
    # todo here
    mint_symbols = ['USDC' if mint_symbol != 'So11111111111111111111111111111111111111112' else 'SOL' for mint_symbol in mint_symbols]
    # Generate the filename
    filename = f"data/jup/{mint_symbols[1]}-{mint_symbols[0]}/{int(now)}-{int(latency)}.csv"

    df = pd.DataFrame(result)
    df.to_csv(filename)

    print(f"Data saved to {filename}")
