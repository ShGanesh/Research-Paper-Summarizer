#!pip install google.generativeai

import google.generativeai as genai
import os

genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel(model_name='gemini-pro')

def generate_summary(text, level):
    prompt = f"""
    I am developing a text summarization application for students and researchers to efficiently grasp the key points of complex documents.
    The input text is already divided into sections using delimiters. The text given will have sections demarcated by the tag <section/>, where the first sentence of that section will generally be the title of that section.
    Each section has to be represented in the summary.
    You can summarize anything according to 9 levels. The specific details are given as such-
    Level 1: Key Sentences (Sentence Extraction): Identify the most important sentences from each section, representing the main points without additional explanations.
    Level 2: Section Overviews (Brief Summaries): Generate concise summaries for each section, capturing the main points and supporting details in a few sentences.
    Level 3: Argument/Finding Identification (Focus on Content): Identify and summarize the main arguments, findings, or conclusions within each section, omitting irrelevant details.
    Level 4: Textual Overview (Holistic Summary): Create a concise summary of the entire text, highlighting key themes, relationships between sections, and the overall message.
    Level 5: Keyword Extraction and Analysis (Deep Content Exploration): Identify and analyze key keywords and phrases throughout the text, revealing hidden connections and deeper meanings.
    Level 6: Causal Inference and Relationship Mapping (Advanced Analysis): Infer causal relationships between events or concepts, and map the connections between different sections of the text.
    Level 7: Contextual Awareness and Fact-Checking (Enhanced Accuracy): Integrate external knowledge and fact-checking mechanisms to verify information and provide contextually relevant summaries.
    Level 8: Multiple Perspectives and Counterarguments (Critical Analysis): Identify and summarize potential counterarguments or alternative viewpoints presented in the text, fostering critical thinking.
    Level 9: Abstract Conceptualization and Synthesis (Highest Abstraction): Extract the core concepts, themes, and implications of the text, presenting a high-level understanding without losing critical details.
    
    The text is given below, enclosed within triple backticks. This text is to be summarized according to level {level}.
    ```
    {text}
    ```
    Process the instructions step by step and summarize according to the level.
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