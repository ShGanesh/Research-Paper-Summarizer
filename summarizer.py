import streamlit as st
import PyPDF2
import google.generativeai as genai
import os

genai_API_KEY = "hehe"

genai.configure(api_key=genai_API_KEY)
model = genai.GenerativeModel(model_name='gemini-pro')

def upload_pdf():
  uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
  if uploaded_file is not None:
    return PyPDF2.PdfReader(uploaded_file)
  else:
    return None

# Define section titles
sections = ["Abstract\n", "Introduction\n", "Background\n", "Motivation\n", "Model Architecture\n", "Objective\n", "Literature Review\n", "Related Work\n", "Previous Studies\n", "Methodology\n", "Methods\n", "Training\n", "Data Collection\n", "Data Analysis\n", "Results\n", "Findings\n", "Analysis\n", "Observations\n", "Discussion\n", "Interpretation\n", "Implications\n", "Limitations\n", "Conclusion\n", "Conclusions\n" "Future work\n", "Recommendations\n", "Summary\n", "References\n"]

# Function to extract text from PDF
def extract_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to find section boundaries
def find_section_boundaries(text, section_keywords):
    boundaries = []
    for keyword in section_keywords:
        index = text.find(keyword)
        if index != -1:
            boundaries.append((keyword, index))
    return sorted(boundaries, key=lambda x: x[1])

# Function to split text based on section boundraies
def split_text(text, boundries):
    op = []
    lim = 0
    for i in boundries:
        str = text[lim: i[1]]
        lim = i[1]
        op.append(str)
    op.append(text[lim:])
    ret = "\n<section/>\n".join(op)
    return op

# Function to remove 'References' and beyond
def remove_after_references(data_list):
    for i, para in enumerate(data_list):
       title = para[:para.find('\n')]
       if title == "References":
           del data_list[i]
    return data_list

def combine(split_sections):
    # Joins all sections with "<section\n>"" as delimiter, for easy usage of GenAI.
    return "\n<section/>\n".join(split_sections)

def title_disp(sections):
    #  'sections' == final fin_section. This returns a list of just the titles
    titles = []
    for i, para in enumerate(sections):
        title = para[:para.find("\n")]
        titles.append(title)
    return titles

def generate_summary(text, level):
    prompt = f"""
    I am developing a text summarization application for students and researchers to efficiently grasp the key points of complex documents.
    The input text is already divided into sections using delimiters. The text given will have sections demarcated by the tag <section/>, where the first sentence of that section will generally be the title of that section.
    Each section has to be represented in the summary.
    You can summarize anything according to 10 levels. The specific details are given as such-
    Level 1: No Summarization (Original Text): Return the entire text without any modifications, preserving all original sentences and details
    Level 2: Key Sentences (Sentence Extraction): Identify the most important sentences from each section, representing the main points without additional explanations.
    Level 3: Section Overviews (Brief Summaries): Generate concise summaries for each section, capturing the main points and supporting details in a few sentences.
    Level 4: Argument/Finding Identification (Focus on Content): Identify and summarize the main arguments, findings, or conclusions within each section, omitting irrelevant details.
    Level 5: Textual Overview (Holistic Summary): Create a concise summary of the entire text, highlighting key themes, relationships between sections, and the overall message.
    Level 6: Keyword Extraction and Analysis (Deep Content Exploration): Identify and analyze key keywords and phrases throughout the text, revealing hidden connections and deeper meanings.
    Level 7: Causal Inference and Relationship Mapping (Advanced Analysis): Infer causal relationships between events or concepts, and map the connections between different sections of the text.
    Level 8: Contextual Awareness and Fact-Checking (Enhanced Accuracy): Integrate external knowledge and fact-checking mechanisms to verify information and provide contextually relevant summaries.
    Level 9: Multiple Perspectives and Counterarguments (Critical Analysis): Identify and summarize potential counterarguments or alternative viewpoints presented in the text, fostering critical thinking.
    Level 10: Abstract Conceptualization and Synthesis (Highest Abstraction): Extract the core concepts, themes, and implications of the text, presenting a high-level understanding without losing critical details.
    
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
            'max_output_tokens': 2000
        }
    )

    return completion.text

# Streamlit app start (need to make this more beautiful)
st.title("Research Paper Section Dividerr")
remove_all = st.checkbox("Remove all content after (and including) 'References'", value=True)

uploaded_file = st.file_uploader("Upload your research paper PDF")

if uploaded_file:
    text = extract_text(uploaded_file)
    n = len(text)
    section_boundaries = find_section_boundaries(text, sections)
    split_sections = split_text(text, section_boundaries)

    if (remove_all == True):
        fin_sections = remove_after_references(split_sections)
    elif remove_all == False:
        fin_sections = split_sections

    st.subheader("Sections:")
    list_titles = title_disp(fin_sections)
    st.write(list_titles)

    ## ow starts the ML Part
    # Combine split sections with <section/> tag for easy usage with genAI.
    spliced_text = combine(fin_sections)

    level = st.radio("Which level of summarization do you need?", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], captions=["No summaization at all", "", "", "", "", "", "", "", "", "Full summarization"])
    if level:
        st.write(generate_summary(spliced_text, level))

st.write()