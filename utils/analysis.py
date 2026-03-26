from utils.llm_handler import query_llm

def analyze_response(p_name, p_key, response_text, client_name, country):
    """
    Performs multi-dimensional analysis on an LLM response.
    """
    prompt = f"""
    Analyze the following LLM response about '{client_name}' in the context of the {country} market.
    
    Response Text: "{response_text}"
    
    Provide the following in a structured format (JSON-like, but just the values):
    1. Sentiment: [Positive, Neutral, Negative]
    2. GEO Score: [1-10] (How well-optimised and authoritative the brand appears)
    3. Hallucination Risk: [Low, Medium, High] (Does it state facts that seem unverified or overly generic?)
    4. Primary Entities: [List 2-3 key topics or brands mentioned]

    Return your answer in exactly this format:
    Sentiment: <value>
    GEO Score: <value>
    Hallucination Risk: <value>
    Entities: <value>
    """
    
    analysis = query_llm(p_name, p_key, prompt)
    
    # Simple parsing logic
    results = {
        "Sentiment": "Neutral",
        "GEO Score": "5",
        "Hallucination Risk": "Low",
        "Entities": ""
    }
    
    try:
        lines = analysis.strip().split('\n')
        for line in lines:
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                if key in results:
                    results[key] = val.strip()
    except:
        pass
        
    return results

def calculate_sov(response_text, client_name, competitors):
    """
    Calculates simple Share of Voice based on mentions.
    """
    mentions = {client_name: 0}
    for comp in competitors:
        mentions[comp] = 0
        
    text_lower = response_text.lower()
    
    if client_name.lower() in text_lower:
        mentions[client_name] = 1
        
    for comp in competitors:
        if comp.lower() in text_lower:
            mentions[comp] = 1
            
    return mentions
