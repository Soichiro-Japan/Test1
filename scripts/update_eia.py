import os
import requests
import pandas as pd
from pathlib import Path

API_KEY = os.getenv("EIA_API_KEY")
if not API_KEY:
    raise SystemExit("EIA_API_KEY が未設定（GitHub Secretsに入れてね）")

out_dir = Path("data")
out_dir.mkdir(exist_ok=True)

url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"
params = {
    "api_key": API_KEY,
    "frequency": "daily",
    "data[0]": "value",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 0,
    "length": 2000,
}

res = requests.get(url, params=params, timeout=30)
res.raise_for_status()
j = res.json()

data = j["response"]["data"]
df = pd.DataFrame(data)

df.to_csv(out_dir / "eia.csv", index=False)
df.to_excel(out_dir / "eia.xlsx", index=False)

print("Updated rows:", len(df))
