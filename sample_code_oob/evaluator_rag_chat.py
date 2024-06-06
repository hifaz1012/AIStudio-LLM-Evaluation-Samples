# ChatEvaluator to evaluate the model on a sample conversation
import os
import json
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluators import ChatEvaluator

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
)

chat_evaluator = ChatEvaluator(
    model_config=model_config,
  )

## sample coversation
# conversation = [
#     {"role": "user", "content": "Compare northcare healthcare standard vs plus plan in 3 sentences?"},
#     {"role": "assistant", "content": "The Northwind Health Plus plan offers comprehensive coverage including emergency services, mental health and substance abuse coverage, and both in-network and out-of-network services, whereas the Northwind Standard plan does not cover these 1 . Northwind Health Plus also provides a wider range of prescription drug coverage compared to Northwind Standard, which only covers generic and brand-name drugs 1 . Both plans offer coverage for medical, vision, and dental services, but Northwind Health Plus offers additional benefits like coverage for glasses and contact lenses, which are not covered under the Standard plan 1", "context": {
#         "citations": [
#             {"id": "Benefit_Options.pdf - Part 1", "content": "Both plans offer coverage for routine physicals, well-child visits, immunizations, and other preventive care services. The plans also cover preventive care services such as mammograms, colonoscopies, and other cancer screenings. Northwind Health Plus offers more comprehensive coverage than Northwind Standard. This plan offers coverage for emergency services, both in-network and out-of-network, as well as mental health and substance abuse coverage. Northwind Standard does not offer coverage for emergency services, mental health and substance abuse coverage, or out-of-network services. Both plans offer coverage for prescription drugs. Northwind Health Plus offers a wider range of prescription drug coverage than Northwind Standard. Northwind Health Plus covers generic, brand- name, and specialty drugs, while Northwind Standard only covers generic and brand-name drugs. Both plans offer coverage for vision and dental services. Northwind Health Plus offers coverage for vision exams, glasses, and contact lenses, as well as dental exams, cleanings, and fillings. Northwind Standard only offers coverage for vision exams and glasses. Both plans offer coverage for medical services. Northwind Health Plus offers coverage for hospital stays, doctor visits, lab tests, and X-rays. Northwind Standard only offers coverage for doctor visits and lab tests. Northwind Health Plus is a comprehensive plan that offers more coverage than Northwind Standard. Northwind Health Plus offers coverage for emergency services, mental health and substance abuse coverage, and out-of-network services, while Northwind Standard does not. Northwind Health Plus also offers a wider range of prescription drug coverage than Northwind Standard. Both plans offer coverage for vision and dental services, as well as medical services"}
#         ]
#     }}
# ]
with open('./sample_data/conversation_health_insurance.json', 'r') as f:
    conversation = json.load(f)

print(conversation)

result = chat_evaluator(conversation=conversation)
print(result)