import openai
import google.generativeai as genai

def query_llm(provider, api_key, prompt):
    try:
        if provider == "OpenAI":
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        
        elif provider == "Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            response = model.generate_content(prompt)
            return response.text
            
    except Exception as e:
        return f"Error with {provider}: {str(e)}"
