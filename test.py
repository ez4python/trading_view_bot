import json
from utils import extract_earnings_info

try:
    with open("data.json", "w") as file:
        data = extract_earnings_info()
        json.dump(data, file, indent=3)
        print("Success!")
except Exception as e:
    print("Exception:", e)
