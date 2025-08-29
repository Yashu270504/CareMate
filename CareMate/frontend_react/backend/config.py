import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Now you can access variables
IBM_API_KEY = os.getenv("8daVEaOBR1pxHiUfnHwsNiCH6wSdcIQXdUUwzM42jsb8")
IBM_URL = os.getenv("https://au-syd.ml.cloud.ibm.com")
GRANITE_MODEL_ID = os.getenv("granite-13b-chat-v2")
