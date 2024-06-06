# Azure AI Studio Evaluation
Azure AI Studio provides 3 types of LLM Evaluations.

1. **Manual Evaluation**: Manual review of LLM Responses by human reviewers and domain experts. Please refer to https://learn.microsoft.com/en-us/azure/ai-studio/how-to/evaluate-prompts-playground for detailed steps.

2. **AI Assisted Evaluation**: Large language models (LLM) such as GPT-4 can be used to evaluate the output of generative AI language systems. Please refer to https://learn.microsoft.com/en-us/azure/ai-studio/how-to/evaluate-generative-ai-app for detailed steps.

AI Assisted Evaluation Metrics supports Generation Quality Metrics like Groundedness, Relevance and Risk and Safety Metrics https://learn.microsoft.com/en-us/azure/ai-studio/how-to/evaluate-generative-ai-app 
Defintion of Generation Quality Metics and Score (1 -5) is described here https://learn.microsoft.com/en-us/azure/ai-studio/how-to/evaluate-generative-ai-app

3. **Prompt Flow SDK**: Use Prompt Flow SDK to generate AI Assisted Metrics in in python code and also build your own custom metrics. https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/flow-evaluate-sdk 
Code Samples and Description are provided below.  

## Setup
1. Create a Python Venv ```python -m venv dev_env```
2. Activate venv and install requirements.txt
```
dev_env\Scripts\activate
pip install -r requirements.txt
```
3. Setup Env Variables to Azure OpenAI Connection.
Region: Currently AI-assisted risk and safety metrics are only available in the following regions: East US 2, France Central, UK South, Sweden Central. Groundedness measurement leveraging Azure AI Content Safety Groundedness Detection is only supported following regions: East US 2 and Sweden Central. So Create AI Studio and Azure OpenAI instance in either Sweden Central or East US 2.
Model: Use the best GPT Models like GPT-4-o or GPT-4-2024-04-09

Rename `env_template` to `.env`
Set Azure OpenAI Endpoint, API Key and Deployment Parameters

## Code Samples

### I. Question Answering Evaluation
Evaluation of completion tasks lime Summarization and NER

Evaluation Data Set should be in JSONL format.

```
{"question":"[Input/Prompt to LLM]","context":"[Context from Data Source]","answer":"[Response from LLM]", ground_truth:"[Ground Truth]"}
```

`context` and `ground_truth` are optional.
Please refer to `sample_data/sample_qa.jsonl` and `sample_data/sample_transcript.jsonl` for examples

1. Groundedness Evaluator : `python sample_code_oob\groundedness_test.py`

2. Relevance Evaluator: `python sample_code_oob\relevance_test.py`

3. Composite Evaluator using evaluate function to generate Groundedness and Relevance metrics on sample JSONL dataset : `python sample_code_oob\evaluator_qa_singleturn.py`
The results will stored as JSON under results folder with unique run id. "rows" will contain the metrics such as groundedness for each question and answer and "metrics" will contain the mean results for the run.

### II. Chat Conversation Evaluation

Chat Evaluator: `python sample_code_oob\evaluator_rag_chat.py`
Input format for conversation between user and AI assistant
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
To build your own custom evaluator, prepare prompty file similar to `sample_code_custom\completeness_evaluator.prompty`.
The prompty file contains model parameters, inputs, outputs, system message and few shot examples. Prepare similar propmpt file and Change configuration as per your use.
Then execute `python sample_code_custom\evaluator_custom_completeness.py`. The evaluation score and reason will be output.

## Issues during testing
1. The composite "evaluate" function returns coherence and fluency values as NAN

2. The composite "evaluate" function when used with custom evaluator or chat evaluator throws error. I have reported this to PG team.
```
  columns=[col for col in evaluator_result_df.columns if col.startswith(Prefixes._INPUTS)]
AttributeError: 'int' object has no attribute 'startswith'
```

