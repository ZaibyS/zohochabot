# tools.py

add_visitor_tool = {
    "type": "function",
    "name": "add_visitor",
    "description": "Adds a new visitor to the database with the provided details. After collecting both email and phone number, visitor will be marked for onboarding.",
    "strict": True,
    "parameters": {
        "type": "object",
        "required": [
            "name",
            "email",
            "phone",
            "consent"
        ],
        "properties": {
            "name": {
                "type": "string",
                "description": "Full name of the visitor"
            },
            "email": {
                "type": "string",
                "description": "Email address of the visitor"
            },
            "phone": {
                "type": "string",
                "description": "Phone number of the visitor with country code (e.g., +92...)"
            },
            "consent": {
                "type": "boolean",
                "description": "Whether the visitor has agreed to share their information for expert consultation"
            }
        },
        "additionalProperties": False
    }
}

retrieve_expert_tool = {
    "type": "function",
    "name": "retrieve_experts",
    "description": "Retrieves a list of available experts based on the client's project needs.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
}
