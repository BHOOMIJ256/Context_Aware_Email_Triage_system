import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="AIzaSyB0jdGkJ7lV1u66baGbKnFVf_O6hoenYDI")  # or use environment variable

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

def call_llm(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text  # this is safe for text-only output
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return "Error"

