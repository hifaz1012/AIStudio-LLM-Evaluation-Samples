import os
import json
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_prompty import create_chat_prompt
from pathlib import Path
from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential

# pip install openai langchain-core langchain-prompty langchain-azure-openai azure-identity
# Load environment variables from .env file
load_dotenv()

# Obtain an access token using DefaultAzureCredential
credential = DefaultAzureCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default")

# Load prompty as langchain ChatPromptTemplate
folder = Path(__file__).parent.absolute().as_posix()
path_to_prompty = folder + "/completeness_evaluator.prompty"
#path_to_prompty = "C:\\Users\\hifazhassan\\workspace\\SingHealth\\test-evaluation-mi\\completeness_evaluator.prompty"
prompt = create_chat_prompt(path_to_prompty)
os.environ["AZURE_OPENAI_ENDPOINT"] = os.environ["AZURE_OPENAI_ENDPOINT"]
os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"]

# Initialize AzureChatOpenAI with access token
model = AzureChatOpenAI(
    #api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    #default_headers={"Ocp-Apim-Subscription-Key": os.environ["SUBSCRIPTION_KEY"]},
    azure_ad_token=token.token,
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    temperature=0
)

output_parser = StrOutputParser()

chain = prompt | model | output_parser

result = chain.invoke({"context": "Patient: I have a headache. Doctor: Take 2 tablets of panadol", "answer": "Doctor said Take 2 tablets of Ibuprofen daily"})

print("Completeness Evaluation: ", result)

print("\n")

result = chain.invoke({"context": "Patient: I have a headache. Doctor: Take 2 tablets of Asprin and 1 tablet of IbuProfen", "answer": "Doctor said Take 2 tablets of Aspirin and 1 tablet of IbuProfen"})
print("Completeness Evaluation: ", result)
