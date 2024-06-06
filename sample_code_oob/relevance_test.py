import os
from promptflow.core import AzureOpenAIModelConfiguration

# Initialize Azure OpenAI Connection with your environment variables
model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
)

from promptflow.evals.evaluators import RelevanceEvaluator

# Initialzing Relevance Evaluator
relevance_eval = RelevanceEvaluator(model_config)
# Running Relevance Evaluator on single input row
relevance_score = relevance_eval(
    answer="The Alpine Explorer Tent is the most waterproof.",
    context="From the our product list,"
    " the alpine explorer tent is the most waterproof."
    " The Adventure Dining Table has higher weight.",
    question="Which tent is the most waterproof?",
)
print(relevance_score)