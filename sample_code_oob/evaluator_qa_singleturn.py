# We will evaluate a QA datset using the following metrics: Relevance, Groundedness, Coherence and Fluency
from datetime import datetime
import os

from promptflow.evals.evaluate import evaluate
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluators import RelevanceEvaluator, GroundednessEvaluator, CoherenceEvaluator, FluencyEvaluator
import pandas as pd

# Initialize Azure OpenAI Connection with your environment variables
model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
)

# Optionally provide your Azure AI studio project information to track your evaluation results in your Azure AI studio project
# azure_ai_project = {
#     "subscription_id": "[subscription id]",
#     "resource_group_name": "[resource group name]",
#     "project_name": "[AI Hub Project Name]"
# }

# Initialzing Relevance Evaluator
relevance_eval = RelevanceEvaluator(model_config)
# Initialzing Groundedness Evaluator
groundedness_eval = GroundednessEvaluator(model_config)
# # Initialzing Coherence Evaluator
# coherence_eval = CoherenceEvaluator(model_config)
# # Initialzing Fluency Evaluator
# fluency_eval = FluencyEvaluator(model_config)

run_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
run_id = f"eval_qa_{run_prefix}"   

# Output path to dump a json of metric summary, row level data and metric and studio URL
output_path = f"./results/{run_id}.json"

result = evaluate(
    evaluation_name=run_id,
    data="./sample_data/sample_transcript.jsonl", # provide your data here
    evaluators={
        "relevance": relevance_eval,
        "groundedness": groundedness_eval,
        # "coherence": coherence_eval,
        # "fluency": fluency_eval
    },
    # column mapping
    evaluator_config={
        "default": {
            "question": "${data.question}",
            "context": "${data.context}",
            "answer": "${data.answer}",
            "ground_truth": "${data.ground_truth}",
        }
    },
    # # Optionally provide your AI Studio project information to track your evaluation results in your Azure AI studio project
    azure_ai_project = azure_ai_project,
    # Optionally provide an output path to dump a json of metric summary, row level data and metric and studio URL
    output_path=output_path
)

print(result)