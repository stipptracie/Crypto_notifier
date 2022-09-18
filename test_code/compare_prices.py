# Import modules

import os
import pandas as pd
import os
import json
import requests
import numpy as np
from pycoingecko import CoinGeckoAPI

# Set Variable for coingecko API
cg = CoinGeckoAPI()

daily_btc = cg.get_price(ids='bitcoin', vs_currencies='usd',include_24hr_change='true')
