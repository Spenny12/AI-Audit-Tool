CATEGORIES = {
    "User personas": [
        "What demographs of users would be interested in {client}?",
        "What issues are users of {client} looking to solve?"
    ],
    "Brand value": [
        "How does {client} provide more value than {competitors}?",
        "What is the general perception of quality of service for {client} compared to {competitors}?"
    ],
    "Core brand signals": [
        "What is the key slogan or messaging of {client}?",
        "What is {client}?",
        "What is the pricing structure for {client}?"
    ],
    "Reputational risks": [
        "What are the main risks of going with {client}?",
        "What are some common complaints of {client}?"
    ]
}

def format_prompt(template, client, competitors):
    comp_str = ", ".join(competitors) if competitors else "its competitors"
    return template.format(client=client, competitors=comp_str)
