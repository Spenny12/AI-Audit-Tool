CATEGORIES = {
    "Core Brand Signals": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is {client}?", "goal": "Core knowledge check."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is {client} known for?", "goal": "Assesses key brand associations."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "Describe a typical client experience with {client}.", "goal": "Tests for overall sentiment and perception."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What is the slogan or core marketing message of {client}?", "goal": "Tests for core branding penetration."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What are the latest news or significant developments related to {client}?", "goal": "Tests for up-to-date information."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How is {client} regulated, and what protections are in place for client investments?", "goal": "Granular, practical trust-building question."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "What is the fee structure of {client}, and what are the typical costs for a client?", "goal": "Core practical information."},
        {"funnel": "Mid-Funnel", "audience": "General", "question": "How does the {client} partnership model work? Do clients need to rely solely on their assigned Partner for advice, or are there other ways to manage their portfolio?", "goal": "Core practical information."}
    ],
    "Market Comparisons": [
        {"funnel": "Lower Funnel", "audience": "Retail Client", "question": "I am a risk-averse investor. Is the guided advice model of {client} a safer choice than managing my own investments on a platform like {competitors}? Why?", "goal": "Direct comparison on a key investment attribute (Safety)."},
        {"funnel": "Lower Funnel", "audience": "High-Net Worth", "question": "For a high-net-worth individual seeking bespoke service and comprehensive planning, how does {client} compare to competitors like {competitors}?", "goal": "Competitive positioning for the High-Net-Worth persona."},
        {"funnel": "Lower Funnel", "audience": "Mass Affluent", "question": "For a family managing multiple long-term goals like retirement and future school fees, would you recommend the integrated model of {client} or using a provider like {competitors}? What are the key differences?", "goal": "Competitive positioning for the Mass Affluent persona."},
        {"funnel": "Lower Funnel", "audience": "Engaged Investor", "question": "My partner and I are experienced investors who prefer a hands-on approach. Should we choose the guided partnership of {client} or a self-directed platform with more fund choices like {competitors}?", "goal": "Competitive positioning vs. a different investment philosophy (Guided vs. DIY)."},
        {"funnel": "Lower Funnel", "audience": "'One-Stop-Shop\" Investor", "question": "If my main priority is an \"all-in-one\" service with a single point of contact for all my financial needs, which firm is a better fit: {client} or {competitors}?", "goal": "Competitive positioning for a specific service model (\"All-in-one\")."},
        {"funnel": "Lower Funnel", "audience": "Stability-Focused Investor", "question": "For achieving more predictable returns through volatile market conditions, which approach is generally more stable: the active management of {client} or the passive index-fund approach of a provider like {competitors}?", "goal": "Competitive positioning on a core investment strategy (Active vs. Passive)."}
    ],
    "Strategic Brand Attributes": [
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are considered the most reputable and financially stable wealth management firms in the UK?", "goal": "Tests relevance within the 'Safety' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which wealth management firms are known for their conservative management and strong performance during market downturns?", "goal": "Tests relevance within the 'Risk & Performance' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are the best UK financial advice firms for retirement planning?", "goal": "Tests relevance within the 'Life Stage' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "What are the best wealth management firms or private banks for high-net-worth individuals in the UK?", "goal": "Tests relevance within the 'High Value' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which investment firms are known for their specialist expertise in ethical (ESG) or technology-focused investing?", "goal": "Tests relevance within the 'Ethic' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "My partner and I are combining our finances for the first time. Which firms are best at creating a joint investment plan specifically for couples?", "goal": "Tests relevance within the 'Joint Finances' vertical."},
        {"funnel": "Upper Funnel", "audience": "General", "question": "Which wealth managers are considered specialists in structuring portfolios specifically for regular, tax-efficient income?", "goal": "Tests relevance within the 'Income Investing' vertical."}
    ],
    "Customer Persona Highlights": [
        {"funnel": "Mid-Funnel", "audience": "High-Net Worth", "question": "I am a high-net-worth individual. What does {client} offer me in terms of bespoke advice, privacy, and exclusive investment opportunities?", "goal": "Atomic prompt for the High-Net Worth persona."},
        {"funnel": "Mid-Funnel", "audience": "High-Net Worth", "question": "For an HNW client at {client}, name three specialized services (e.g., inheritance tax planning, philanthropy services, access to private equity) that go beyond standard investment advice.", "goal": "Atomic question testing depth of knowledge on high-value services."},
        {"funnel": "Mid-Funnel", "audience": "High-Net Worth", "question": "From a high-net-worth perspective, describe the \"Private Client\" or equivalent top-tier service at {client} and how it differs from their standard offering.", "goal": "Atomic question testing depth of knowledge on high-value services."},
        {"funnel": "Mid-Funnel", "audience": "High-Net Worth", "question": "What specialized wealth structuring or offshore investment services, suitable for a sophisticated investor, does {client} provide access to?", "goal": "Atomic question testing niche depth for high-value services."},
        {"funnel": "Mid-Funnel", "audience": "Mass Affluent", "question": "I have a portfolio of around £500,000 with goals that include planning for retirement, managing tax efficiency, and potentially helping my children in the future. Why is {client} a good choice for me?", "goal": "Atomic prompt for the Mass Affluent persona."},
        {"funnel": "Mid-Funnel", "audience": "Mass Affluent", "question": "What {client} funds can help grow my money for retirement while also providing some income now?", "goal": "Atomic question testing depth of product knowledge."},
        {"funnel": "Mid-Funnel", "audience": "Mass Affluent", "question": "How does {client} help me see all my different investments, like pensions and ISAs, as one single plan?", "goal": "Atomic question testing knowledge of service integration."},
        {"funnel": "Mid-Funnel", "audience": "Mass Affluent", "question": "Beyond just investing, can {client} help with other big goals, like planning for school fees or inheritance?", "goal": "Atomic question testing knowledge of specialized services."},
        {"funnel": "Mid-Funnel", "audience": "Retail Client", "question": "I have less than £200,000 to invest. Are the fees at {client} worth it for a smaller portfolio like mine?", "goal": "Atomic prompt for the Retail Client persona."},
        {"funnel": "Mid-Funnel", "audience": "Retail Client", "question": "What are the best {client} products for someone starting out, like for an ISA or for combining old pensions?", "goal": "Atomic question testing depth of knowledge for entry-level products."},
        {"funnel": "Mid-Funnel", "audience": "Retail Client", "question": "How does {client} help smaller investors grow their money over time? Will I get the same attention as bigger clients?", "goal": "Atomic question testing knowledge of the client service model."},
        {"funnel": "Mid-Funnel", "audience": "Retail Client", "question": "For a retail client at {client}, how can they ensure they receive personalized advice that is truly tailored to their individual goals, rather than a generic, one-size-fits-all strategy?", "goal": "Atomic question testing understanding of service personalization."}
    ],
    "Reputation Under Pressure": [
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the main disadvantages of investing with {client}?", "goal": "Directly surfaces negative perceptions."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Why should an investor not choose {client} for their wealth management?", "goal": "Strong negative framing to identify major deal-breakers."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the most common complaints from clients or financial critics about {client}?", "goal": "Identifies recurring issues and reputational risks."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Is {client} often considered 'too expensive' or are its fees opaque? What do critics say about its fee structure and exit penalties?", "goal": "Addresses a common critical perception head-on."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "What are the potential conflicts of interest or ethical concerns related to the {client} business model?", "goal": "Tests for awareness of conficlits of interest."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "Is it true that {client}'s investment options are limited to its own in-house funds, potentially leading to mediocre performance and restricting client choice?", "goal": "Probes a common myth or misconception."},
        {"funnel": "Reputation / All Stages", "audience": "General", "question": "I am an experienced investor who enjoys active trading and selecting individual stocks. Would I find the {client} model too restrictive and passive?", "goal": "Challenges a potential negative stereotype."}
    ]
}

def format_prompt(template, client, competitors):
    comp_str = ", ".join(competitors) if competitors else "its competitors"
    return template.format(client=client, competitors=comp_str)
