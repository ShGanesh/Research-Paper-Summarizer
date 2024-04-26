import streamlit as st
import PyPDF2
import google.generativeai as genai
import time

genai_API_KEY = st.secrets["genai_API"]

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
    Process the instructions step by step and summarize according to the level. The word count of your answer SHOULD EXCEED 300 words.
    """
    completion = model.generate_content(
        prompt,
        generation_config={
            'temperature': 0,
            'max_output_tokens': 1500
        }
    )

    return completion.text

def level_manual():
    with st.sidebar:
        with st.container(border=True):
            st.header("About this project")
            st.markdown("""
                This Streamlit app leverages the power of Natural Language Processing (NLP) to summarize text documents based on nine distinct levels of abstraction. 

                **What does it do?**

                * It takes your text input and analyzes its content.
                * It extracts key sentences and concepts at different levels of detail, from high-level overviews to granular specifics.
                * It presents you with a concise summary tailored to your desired level of abstraction.

                **Why is it useful?**

                * Quickly grasp the main points of lengthy documents.
                * Identify key information relevant to your specific needs.
                * Enhance your understanding of complex topics.
                * Save time and effort when reading and processing information.

            """)
    
    levels_expander = st.expander("Levels of Abstraction")

    levels_expander.markdown("""
        **Abstraction Level** | **Description**
        ---|---
        Level 1 | **Key Sentences (Sentence Extraction)**: Identifies the most important sentences from each section, representing the main points without additional explanations.
        Level 2 | **Section Overviews (Brief Summaries)**: Generates concise summaries for each section, capturing the main points and supporting details in a few sentences.
        Level 3 | **Argument/Finding Identification (Focus on Content)**: Identifies and summarize the main arguments, findings, or conclusions within each section, omitting irrelevant details.
        Level 4 | **Textual Overview (Holistic Summary)**: Creates a concise summary of the entire text, highlighting key themes, relationships between sections, and the overall message.
        Level 5 | **Keyword Extraction and Analysis (Deep Content Exploration)**: Identifies and analyzes key keywords and phrases throughout the text, revealing hidden connections and deeper meanings.
        Level 6 | **Causal Inference and Relationship Mapping (Advanced Analysis)**: Infers causal relationships between events or concepts, and map the connections between different sections of the text.
        Level 7 | **Contextual Awareness and Fact-Checking (Enhanced Accuracy)**: Integrates external knowledge and fact-checking mechanisms to verify information and provide contextually relevant summaries.
        Level 8 | **Multiple Perspectives and Counterarguments (Critical Analysis)**: Identifies and summarize potential counterarguments or alternative viewpoints presented in the text, fostering critical thinking.
        Level 9 | **Abstract Conceptualization and Synthesis (Highest Abstraction)**: Extracts the core concepts, themes, and implications of the text, presenting a high-level understanding without losing critical details.
        
        """)

def level_explain(level):
    level_details = {
        "Level 1": "Key Sentences (Sentence Extraction): Identifies the most important sentences from each section, representing the main points without additional explanations.",
        "Level 2": "Section Overviews (Brief Summaries): Generates concise summaries for each section, capturing the main points and supporting details in a few sentences.",
        "Level 3": "Argument/Finding Identification (Focus on Content): Identifies and summarize the main arguments, findings, or conclusions within each section, omitting irrelevant details.",
        "Level 4": "Textual Overview (Holistic Summary): Creates a concise summary of the entire text, highlighting key themes, relationships between sections, and the overall message.",
        "Level 5": "Keyword Extraction and Analysis (Deep Content Exploration): Identifies and analyze key keywords and phrases throughout the text, revealing hidden connections and deeper meanings.",
        "Level 6": "Causal Inference and Relationship Mapping (Advanced Analysis): Infers causal relationships between events or concepts, and map the connections between different sections of the text.",
        "Level 7": "Contextual Awareness and Fact-Checking (Enhanced Accuracy): Integrates external knowledge and fact-checking mechanisms to verify information and provide contextually relevant summaries.",
        "Level 8": "Multiple Perspectives and Counterarguments (Critical Analysis): Identifies and summarize potential counterarguments or alternative viewpoints presented in the text, fostering critical thinking.",
        "Level 9": "Abstract Conceptualization and Synthesis (Highest Abstraction): Extracts the core concepts, themes, and implications of the text, presenting a high-level understanding without losing critical details."
    }
    lvl = f"Level {level}"
    head, bod = level_details[lvl].split(":")
    container = st.container(border=True)
    container.subheader(f"{lvl}: {head}")
    container.caption(bod)

progress_text = "Operation in progress. Please wait."
                    
# Streamlit app start (need to make this more beautiful)
st.title("Research Paper Summarizer")
uploaded_file = st.file_uploader("Upload your research paper PDF")
remove_all = st.checkbox("Remove all content after (and including) 'References'", value=True)

st.divider()    
level_manual()

st.divider()    

if uploaded_file:
    text = extract_text(uploaded_file)
    n = len(text)
    section_boundaries = find_section_boundaries(text, sections)
    split_sections = split_text(text, section_boundaries)

    #st.subheader("Sections:")
    #list_titles = title_disp(fin_sections)
    #st.write(list_titles)

    level = st.slider("Which level of summarization do you need?", 1, 9, 4)
    level_explain(level)

    # Button to summarize
    
    if (remove_all == True):
        fin_sections = remove_after_references(split_sections)
    elif remove_all == False:
        fin_sections = split_sections

    ## Now starts the ML Part
    # Combine split sections with <section/> tag for easy usage with genAI.
    spliced_text = combine(fin_sections)
    if level:
        isTrue = False
        if st.button("Generate Text"):
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1, text=progress_text)
            st.write(generate_summary(spliced_text, level))
            my_bar.empty()
    ignore = '''
    if level:
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1, text=progress_text)
        st.write(generate_summary(spliced_text, level))
    '''

# Footer
st.divider()
st.markdown(f"Copyright © 2023 ShGanesh")
#. All rights reserved. Visit [shganesh.streamlit.app](%shganesh.streamlit.app) to see my other projects :smile:")
