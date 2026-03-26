CATEGORIES = {
    "Core Brand Signals": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is {client}?", "goal": "Core knowledge check."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is {client} known for?", "goal": "Assesses key brand associations."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Describe a typical client experience with {client}.", "goal": "Tests for overall sentiment and perception."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is the slogan or core marketing message of {client}?", "goal": "Tests for core branding penetration."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What are the latest news or significant developments related to {client}?", "goal": "Tests for up-to-date information."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How is {client} regulated, and what protections are in place for users in the {industry} sector?", "goal": "Granular, practical trust-building question."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What is the fee or pricing structure of {client} for {service}, and what are the typical costs for a user?", "goal": "Core practical information."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How does the {client} service model work? Do users need to rely solely on a single point of contact for {service}, or are there other ways to manage their account?", "goal": "Core practical information."}
    ],
    "Market Comparisons": [
        {"funnel": "Lower Funnel", "audience": "Risk-Averse User", "question": "I am a risk-averse user. Is the guided model of {client} a safer choice for {service} than managing my own requirements on a platform like {competitors}? Why?", "goal": "Direct comparison on a key attribute (Safety/Reliability)."},
        {"funnel": "Lower Funnel", "audience": "High-Value Client", "question": "For a high-value individual seeking bespoke service and comprehensive planning in {industry}, how does {client} compare to competitors like {competitors}?", "goal": "Competitive positioning for the High-Net-Worth persona."},
        {"funnel": "Lower Funnel", "audience": "Standard User", "question": "For a user managing multiple long-term goals in {industry}, would you recommend the integrated model of {client} or using a provider like {competitors}? What are the key differences?", "goal": "Competitive positioning for a standard persona."},
        {"funnel": "Lower Funnel", "audience": "Expert User", "question": "I am an experienced user who prefers a hands-on approach. Should I choose the guided model of {client} for {service} or a self-directed platform like {competitors}?", "goal": "Competitive positioning vs. a different investment philosophy (Guided vs. DIY)."},
        {"funnel": "Lower Funnel", "audience": "Convenience-Focused", "question": "If my main priority is an \"all-in-one\" service with a single point of contact for my {service} needs, which firm is a better fit: {client} or {competitors}?", "goal": "Competitive positioning for a specific service model (\"All-in-one\")."},
        {"funnel": "Lower Funnel", "audience": "Stability-Focused", "question": "For achieving more predictable results through volatile conditions in {industry}, which approach is generally more stable: the active management of {client} or the passive approach of a provider like {competitors}?", "goal": "Competitive positioning on a core strategy (Active vs. Passive)."}
    ],
    "Strategic Brand Attributes": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are considered the most reputable and stable firms in the {industry} industry in {country}?", "goal": "Tests relevance within the 'Safety' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} firms are known for their conservative management and strong performance during downturns?", "goal": "Tests relevance within the 'Risk & Performance' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are the best {country} {industry} firms for long-term planning?", "goal": "Tests relevance within the 'Life Stage' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are the best {industry} firms or providers for high-value individuals in {country}?", "goal": "Tests relevance within the 'High Value' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} firms are known for their specialist expertise in ethical (ESG) or technology-focused areas?", "goal": "Tests relevance within the 'Specialist' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} firms are best at creating a joint plan specifically for partners or families?", "goal": "Tests relevance within the 'Joint Needs' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which {industry} managers are considered specialists in structuring for regular, efficient outcomes?", "goal": "Tests relevance within the 'Outcome' vertical."}
    ],
    "Customer Persona Highlights": [
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "I am a high-value individual. What does {client} offer me in terms of bespoke advice, privacy, and exclusive {service} opportunities?", "goal": "Atomic prompt for the High-Net Worth persona."},
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "For a high-value client at {client}, name three specialized services in {industry} (e.g., bespoke planning, niche access) that go beyond standard offerings.", "goal": "Atomic question testing depth of knowledge on high-value services."},
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "From a high-value perspective, describe the top-tier service at {client} and how it differs from their standard offering.", "goal": "Atomic question testing depth of knowledge on high-value services."},
        {"funnel": "Mid-Funnel", "audience": "High-Value Client", "question": "What specialized or niche {service} services, suitable for a sophisticated user, does {client} provide access to?", "goal": "Atomic question testing niche depth for high-value services."},
        {"funnel": "Mid-Funnel", "audience": "Mid-Tier Client", "question": "I have significant requirements in {industry} with goals that include planning and efficiency. Why is {client} a good choice for me?", "goal": "Atomic prompt for the Mid-Tier persona."},
        {"funnel": "Mid-Funnel", "audience": "Mid-Tier Client", "question": "What {client} {service} products can help meet my goals while also providing immediate value?", "goal": "Atomic question testing depth of product knowledge."},
        {"funnel": "Mid-Funnel", "audience": "Mid-Tier Client", "question": "How does {client} help me see all my different {service} needs as one single plan?", "goal": "Atomic question testing knowledge of service integration."},
        {"funnel": "Mid-Funnel", "audience": "Mid-Tier Client", "question": "Beyond just basic {service}, can {client} help with other big goals or specialized needs in {industry}?", "goal": "Atomic question testing knowledge of specialized services."},
        {"funnel": "Mid-Funnel", "audience": "Standard Client", "question": "I am a standard user. Are the fees at {client} worth it for a profile like mine in {industry}?", "goal": "Atomic prompt for the Standard persona."},
        {"funnel": "Mid-Funnel", "audience": "Standard Client", "question": "What are the best {client} products for someone starting out in {industry}?", "goal": "Atomic question testing depth of knowledge for entry-level products."},
        {"funnel": "Mid-Funnel", "audience": "Standard Client", "question": "How does {client} help smaller users grow their {service} over time? Will I get the same attention as bigger clients?", "goal": "Atomic question testing knowledge of the client service model."},
        {"funnel": "Mid-Funnel", "audience": "Standard Client", "question": "For a standard client at {client}, how can they ensure they receive personalized service that is truly tailored to their individual goals, rather than a generic strategy?", "goal": "Atomic question testing understanding of service personalization."}
    ],
    "Reputation Under Pressure": [
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the main disadvantages of working with {client} for {service}?", "goal": "Directly surfaces negative perceptions."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Why should a user not choose {client} for their {service} needs?", "goal": "Strong negative framing to identify major deal-breakers."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the most common complaints from users or critics about {client} in the {industry} space?", "goal": "Identifies recurring issues and reputational risks."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Is {client} often considered 'too expensive' or are its fees opaque? What do critics say about its {industry} fee structure?", "goal": "Addresses a common critical perception head-on."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the potential conflicts of interest or ethical concerns related to the {client} business model in {industry}?", "goal": "Tests for awareness of conflicts of interest."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Is it true that {client}'s options are limited to its own in-house {service}, potentially leading to mediocre outcomes and restricting user choice?", "goal": "Probes a common myth or misconception."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "I am an experienced user who enjoys a hands-on approach. Would I find the {client} model too restrictive and passive for {service}?", "goal": "Challenges a potential negative stereotype."}
    ]
}

def format_prompt(template, client, competitors, country="the UK", industry="financial services", service="investment"):
    comp_str = ", ".join(competitors) if competitors else "its competitors"
    return template.format(client=client, competitors=comp_str, country=country, industry=industry, service=service)
