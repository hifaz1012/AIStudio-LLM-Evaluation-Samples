# We will demonstrate how to use Content Safety Evaluator and Content Safety Chat Evaluator to evaluate content safety of a single input row and a conversation respectively.

azure_ai_project = {
    "subscription_id": "[subscription id]",
    "resource_group_name": "[resource group name]",
    "project_name": "[AI Hub Project Name]"
}



from promptflow.evals.evaluators import ContentSafetyEvaluator, ContentSafetyChatEvaluator

# Initialzing Content Safety QA Evaluator with project information
content_safety_eval = ContentSafetyEvaluator(azure_ai_project)

# Running Content Safety Evaluator on single input row
content_safety_score = content_safety_eval(question="What is the capital of France?", answer="Paris.")
print("Conntent Safety Score: #####\n")
print(content_safety_score)
print("\n##############################################\n")

# Initialzing ontent Safety Chat Evaluator with project information
content_safety_chat_eval = ContentSafetyChatEvaluator(azure_ai_project)
# Running Violence Evaluator on single input message

conversation = [
                {"role": "user", "content": "What is the value of 2 + 2?"},
                {"role": "assistant", "content": "2 + 2 = 4", "context": {
                    "citations": [
                            {"id": "math_doc.md", "content": "Information about additions: 1 + 2 = 3, 2 + 2 = 4"}
                            ]
                    }
                }
            ]

content_safety_chat_score = content_safety_chat_eval(conversation=conversation)
print("Conntent Safety Chat Score: #####\n")
print(content_safety_chat_score)
print("\n##############################################\n")


