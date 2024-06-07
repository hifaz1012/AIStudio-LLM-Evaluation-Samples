# Azure AI Studio Evaluation
Azure AI Studio offers 3 types of Large Language Model (LLM) Evaluations.

1. **Manual Evaluation**: Manual review of LLM Responses by human reviewers and domain experts. Please refer to https://learn.microsoft.com/en-us/azure/ai-studio/how-to/evaluate-prompts-playground for detailed steps.

2. **AI Assisted Evaluation**: Large language models (LLM) such as GPT-4 can be used to evaluate the output of generative AI language systems. Please refer to https://learn.microsoft.com/en-us/azure/ai-studio/how-to/evaluate-generative-ai-app for detailed steps.

    AI Assisted Evaluation Metrics supports Generation Quality Metrics like Groundedness, Relevance and Risk and Safety Metrics https://learn.microsoft.com/en-us/azure/ai-studio/how-to/evaluate-generative-ai-app 
    Defintion of Generation Quality Metrics and Score (1 -5) is described here https://learn.microsoft.com/en-us/azure/ai-studio/concepts/evaluation-metrics-built-in?tabs=warning#generation-quality-metrics

3. **Prompt Flow SDK**: Use the Prompt Flow SDK to generate AI Assisted Metrics in in python code and also build your own custom metrics. For more info refer https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/flow-evaluate-sdk 

| Metric    | Description |
|----------|----------|
|   Groundedness  |  Measures how well the model's generated answers align with information from the source data (user-defined context). |
|   Relevance  |   The relevance metric measures the extent to which the model's generated responses are pertinent and directly related to the given questions. |

**Code Samples and Description are provided below.** 

*Please note that AI Assisted Evaluation and Prompt Flow SDK Evualator Library is in Public Preview

## Setup
1. Git clone the project : `https://github.com/hifaz1012/AIStudio-Evaluation-Samples`
2. Create a Python Venv ```python -m venv dev_env```
2. Activate venv and install requirements.txt
```
dev_env\Scripts\activate
pip install -r requirements.txt
```
3. Setup Env Variables to Azure OpenAI Connection.

**Region Selection for AI Studio**: At present, AI-assisted risk and safety metrics are available only in the following regions: East US 2, France Central, UK South, and Sweden Central. The Groundedness measurement, which leverages Azure AI Content Safety Groundedness Detection, is supported only in the following regions: East US 2 and Sweden Central.

Therefore, it is recommended to create an AI Studio and Azure OpenAI instance in either Sweden Central or East US 2 for evaluation purposes.

**Model Selection**: For optimal performance, it is suggested to use the best-performing GPT Models, such as GPT-4-o or GPT-4-2024-04-09.

Rename `env_template` to `.env`
Set Azure OpenAI Endpoint, API Key and Deployment Name

## Code Samples

### I. Question Answering Evaluation
This is used for evaluation of completion tasks lime Summarization and NER

The evaluation Data Set should be in JSONL format.

```
{"question":"[Input/Prompt to LLM]","context":"[Context from Data Source]","answer":"[Response from LLM]", ground_truth:"[Ground Truth]"}
```

`context` and `ground_truth` are optional.
Please refer to `sample_data/sample_qa.jsonl` and `sample_data/sample_transcript.jsonl` for examples

1. Groundedness Evaluator : Execute `python sample_code_oob\groundedness_test.py`

2. Relevance Evaluator: Execute `python sample_code_oob\relevance_test.py`

3. Composite Evaluator (Multiple Evaluations) using `evaluate` function to generate Groundedness and Relevance metrics on sample JSONL dataset : Execute `python sample_code_oob\evaluator_qa_singleturn.py`

The results will stored as JSON under results folder with unique run id. "rows" will contain the metrics such as groundedness for each question and answer pair and "metrics" will contain the mean results of the run.

If you want to log the results into AI Studio, comment out the following lines in code
```
# Optionally provide your Azure AI studio project information to track your evaluation results in your Azure AI studio project
# azure_ai_project = {
#     "subscription_id": "[subscription id]",
#     "resource_group_name": "[resource group name]",
#     "project_name": "[AI Hub Project Name]"
# }
```

resource_group_name : resource group name where AI studio is setup

project_name: AI Hub Project name (Please enter Project Name and not AI Hub Name)

Run `az login` before executing the python code. After successful run, the AI Studio Evaluation Tab will display run id.

### II. Chat Conversation Evaluation

Chat Evaluator: Execute `python sample_code_oob\evaluator_rag_chat.py`

Eval Data Set Input format for chat conversation
```
conversation = [
    {"role": "user", "content": "Compare northcare healthcare standard vs plus plan in 3 sentences?"},
    {"role": "assistant", "content": "The Northwind Health Plus plan offers comprehensive coverage including emergency services, mental health and substance abuse coverage, and both in-network and out-of-network services, whereas the Northwind Standard plan does not cover these 1", "context": {
        "citations": [
            {"id": "Benefit_Options.pdf - Part 1", "content": "Both plans offer coverage for routine physicals, well-child visits, immunizations, and other preventive care services. The plans also cover preventive care services such as mammograms, colonoscopies, and other cancer screenings. Northwind Health Plus offers more comprehensive coverage than Northwind Standard."}
        ]
    }}
]
```
The conversation can contain series of messages between user and AI assistant. The "citations" contains chunk_id and content retrieved from AI Search or any other data sources.

The results will produce various metrics like groundedness, relevance and retrieval scores.

### III. Content Safety Evaluation
Content Safety Evaluator: `python sample_code_oob\content_safety_eval.py`
Content Safety needs connection to AI Studio, provide it in the format
```
azure_ai_project = {
    "subscription_id": "[subscription id]",
    "resource_group_name": "[resource group name]",
    "project_name": "[AI Hub Project Name]",
}
```
The results will contain content saftey metrics like violence, hate and self harm.

### IV. Custom Evaluator
To build your own custom evaluator, prepare `prompty` file similar to `sample_code_custom\completeness_evaluator.prompty`. Learn more about prompty https://microsoft.github.io/promptflow/how-to-guides/develop-a-prompty/use-prompty-in-flow.html

The prompty file contains model parameters, inputs, outputs, system message and few shot examples. Prepare similar prompty file and change configuration as per your use.

Ensure the Eval data set columns matches the inputs variables

Then execute `python sample_code_custom\evaluator_custom_completeness.py`. 

The evaluation score and reason will be output.

The results are amazing : )

```
Input: context="Patient: I have a headache. Doctor: Take 2 tablets of panadol", answer="Doctor said Take 2 tablets of Ibuprofen daily")

Completeness Evaluation Score:  0

Reason: The medication prescribed in the context is "panadol," but the answer mentions "Ibuprofen," which is not the medication prescribed by the doctor in the context.
```

```
Input: context="Patient: I have a headache. Doctor: Take 2 tablets of Asprin and 1 tablet of IbuProfen", answer="Doctor said Take 2 tablets of Aspirin and 1 tablet of IbuProfen"

Completeness Evaluation Score:  1

Reason: The answer contains all the medications prescribed in the context, which are 2 tablets of Aspirin and 1 tablet of Ibuprofen, despite minor spelling differences in the context ("Asprin" and "IbuProfen").
```

## Issues during testing
1. The composite "evaluate" function sometimes returns coherence and fluency values as NAN

2. The composite "evaluate" function when used with custom evaluator or chat evaluator throws error. I have reported this to PG team.
```
  columns=[col for col in evaluator_result_df.columns if col.startswith(Prefixes._INPUTS)]
AttributeError: 'int' object has no attribute 'startswith'
```
## Legal Disclaimer
This Prototype/Proof of Concept (POC) sample template code can be utilized by customer and adapted according to their specific use cases and testing requirements. Microsoft or the author does not hold responsibility for the maintenance of customer code, production issues, or security vulnerabilities.

