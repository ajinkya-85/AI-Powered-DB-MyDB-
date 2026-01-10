import google.generativeai as genai
import os

class QueryGenerator:
    def __init__(self, model_name='gemini-2.5-flash'):
        api_key = os.environ.get("key")
        if not api_key:
            raise ValueError("API Key is not set. Please configure it in the 'API Key' settings.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.user_input = ""
        self.prompt = """
        Act as a SQL expert. Generate SQL queries based on the following requirements.
        Only return the SQL query without any explanation.
        Make sure the query is valid SQLite syntax.(raw SQL, no markdown format)
        """

    def set_user_input(self, user_input):
        self.user_input = user_input

    def get_response(self):
        try:
            response = self.model.generate_content(self.user_input + self.prompt)
            return response.text
        except Exception as e:
            return f"Error generating query: {str(e)}"