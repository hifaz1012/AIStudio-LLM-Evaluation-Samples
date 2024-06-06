# This script is used to dump a conversation into a JSON file.

import json

conversation = [
    {"role": "user", "content": "Compare northcare healthcare standard vs plus plan in 3 sentences?"},
    {"role": "assistant", "content": "The Northwind Health Plus plan offers comprehensive coverage including emergency services, mental health and substance abuse coverage, and both in-network and out-of-network services, whereas the Northwind Standard plan does not cover these 1 . Northwind Health Plus also provides a wider range of prescription drug coverage compared to Northwind Standard, which only covers generic and brand-name drugs 1 . Both plans offer coverage for medical, vision, and dental services, but Northwind Health Plus offers additional benefits like coverage for glasses and contact lenses, which are not covered under the Standard plan 1", "context": {
        "citations": [
            {"id": "Benefit_Options.pdf - Part 1", "content": "Both plans offer coverage for routine physicals, well-child visits"}
        ]
    }}
]

with open('conversation_health_insurance1.json', 'w') as f:
    json.dump(conversation, f)
