import os
import google.genai as genai
from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

client = None
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file!")
else:
    client = genai.Client(api_key=api_key)

def research_topic(topic):
    if client is None:
        return "API key not found."
    
    models_to_try = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-2.0-flash-lite', 'gemini-2.5-pro']
    
    for model in models_to_try:
        try:
            response = client.models.generate_content(
                model=model,
                contents=f"Research the topic '{topic}' and provide a summary of the best and most important parts, especially useful for homework."
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            if "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
                print(f"Model {model} quota limit exceeded, trying another model...")
                continue
            else:
                return f"Error occurred: {e}"
    
    return "All models' quota limits exceeded. Please try again later or check your API quota."

def main():
    print("--- Homework Helper AI Agent (Stable Mode) ---")
    topic = input("Enter a topic to research: ")
    
    if topic.strip():
        print(f"\n'{topic}' is being researched, please wait...\n")
        summary = research_topic(topic)
        print("Summary:\n", summary)
    else:
        print("Please enter a topic title.")

if __name__ == "__main__":
    main()