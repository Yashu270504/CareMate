import os
from ibm_watsonx_ai.foundation_models import Model
from dotenv import load_dotenv

# Load credentials
load_dotenv()
API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
REGION = os.getenv("IBM_REGION", "us-south")  # default region

# Configure model
model_id = "ibm/granite-13b-chat-v2"   # Granite model for simplification
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 100,
    "min_new_tokens": 1
}

model = Model(
    model_id=model_id,
    params=parameters,
    project_id=PROJECT_ID,
    credentials={"apikey": API_KEY, "url": f"https://{REGION}.ml.cloud.ibm.com"}
)

# ---------- Simplify Text ----------
def simplify_text(text: str) -> str:
    try:
        prompt = f"Simplify the following medical explanation into patient-friendly language:\n{text}"
        response = model.generate_text(prompt=prompt)
        return response["results"][0]["generated_text"]
    except Exception as e:
        return f"Simplified (fallback): {text}"
