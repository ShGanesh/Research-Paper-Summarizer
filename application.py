#!pip install google.generativeai

import google.generativeai as genai
import os

genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel(model_name='gemini-pro')

def generate_summary(text, level):
    prompt = f"""
    You are an expert who can succintly summarize any text while retaining all the necessary information.
    The text given will have sections demarcated by the tag <section/>, where the first sentence of that section will generally be the title of that section.
    Each section has to be represented in the summary.
    You can summarize anything according to 10 levels, where "level 1" means that you do not summarize the text at all, and level 10 means that any section of text will be summarized in three or less lines.

    The text is given below, enclosed within triple backticks. This text is to be summarized according to level {level}.
    ```
    {text}
    ```
    """
    completion = model.generate_content(
        prompt,
        generation_config={
            'temperature': 0,
            'max_output_tokens': 800
        }
    )

    return completion.text
       
comments = '''
Add option to retain references
'''

text = "paper"
level = 5
print(generate_summary(text, level))