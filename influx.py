import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("INFLUX_TOKEN")
print(token)
