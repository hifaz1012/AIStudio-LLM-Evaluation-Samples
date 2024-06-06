#   This script demonstrates how to use the completeness evaluator in PromptFlow to evaluate the completeness of a response.
import os
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.client import load_flow
from datetime import datetime
from promptflow.evals.evaluate import evaluate

# with open("./sample_code_custom/completeness_evaluator.prompty") as fin:
#     print(fin.read())

# Initialize Azure OpenAI Connection with your environment variables
model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
)

# load completeness evaluator from prompty file using promptflow
completeness_eval = load_flow(source="./sample_code_custom/completeness_evaluator.prompty", model={"configuration": model_config})

result = completeness_eval(context="Patient: I have a headache. Doctor: Take 2 tablets of panadol", answer="Doctor said Take 2 tablets of Ibuprofen daily")
print("Completeness Evaluation: ", result)

print("\n")

result = completeness_eval(context="Patient: I have a headache. Doctor: Take 2 tablets of Asprin and 1 tablet of IbuProfen", answer="Doctor said Take 2 tablets of Aspirin and 1 tablet of IbuProfen")
print("Completeness Evaluation: ", result)

# run_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
# run_id = f"eval_custom_qa_{run_prefix}"   

# output_path = f"../results/{run_id}.json"

# result = evaluate(
#     evaluation_name=run_id,
#     data="../sample_data/sample_transcript.jsonl", # provide your data here
#     evaluators={
#         "prompty_eval": completeness_eval,
#     },
#     # column mapping
#     evaluator_config={
#         "default": {
#             "answer": "${data.answer}",
#             "context": "${data.context}"
#         }
#     },
#     # # Optionally provide your AI Studio project information to track your evaluation results in your Azure AI studio project
#     #azure_ai_project = azure_ai_project,
#     # Optionally provide an output path to dump a json of metric summary, row level data and metric and studio URL
#     output_path=output_path
# )

# print(result)

