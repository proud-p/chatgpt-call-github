from openai import AzureOpenAI
import os
from dotenv import load_dotenv

os.chdir("../")

# Get Authentications
load_dotenv()


AZURE_CLIENT = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version="2023-10-01-preview"
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")



