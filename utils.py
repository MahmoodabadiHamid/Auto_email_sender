from groq import Groq
import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup


def html_to_raw_text(html_text):
    return BeautifulSoup(html_text, "lxml").text


def extract_json(input_string):
    try:
        match = re.search(r'\{.*?\}', input_string, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except json.JSONDecodeError:
        pass
    return False

 


def get_email_text(text, experiences):
    api_key = "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"
    client = Groq(api_key=api_key)
    prompt = f"""
                Based on the information provided from a professor's personal webpage defined in thriple ' qoutation: '''{text}''', please distill the relevant details and compose a short, polished, formal email to the professor. Emphasize at most two of the professor's research interests that are very close and related to the sender's experiece, and draw connections to the sender's professional experience. If any projects or publications are particularly pertinent to the sender’s background, express a strong desire to engage with those initiatives.
                The email should state, "I am reaching out to you through your personal webpage," and note that the sender's CV is attached for their review. Additionally, inquire about the availability of Ph.D. positions.
                Make sure the email is impeccably drafted, containing multiple paragraphs splitted by "\\n", and ready for immediate sending.
                The sender’s background is detailed as follows: '''{experiences}'''. The sender's full name, XXXX YYY, should be mentioned at the end of the email.
                Mention "Professor's Name" in the first line of the email and use common phrases like Dear "Professor's Name",.
                Write the email as simple as possible; use simple human written grammar and simple words. Turn the email as a non-native human written text.
                **Important:** Only extract the exact, legitimate email address provided on the professor’s personal webpage, and **Do not** generate or use placeholder addresses such as "firstname.lastname@university.edu" or similar. 
                Provide the output in JSON format with the following structure:
                {{
                  "name": "Professor's Name",
                  "email": "Email Address",
                  "email_title": "Generated Email title"
                  "email_body": "Generated Email body"
                }}
                
                    """
    for attempt in range(1):
        try:
            chat_completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}],model="mixtral-8x7b-32768",)# "llama3-70b-8192", "llama3-8b-8192"
            response_text = chat_completion.choices[0].message.content
            #print(response_text)
            output = extract_json(response_text)
            if output:
                return output
            prompt += "The output have to contain JSON with defined format."
        except Exception as e:
            print(f"Attempt {attempt} failed with exception: {e}")
            continue
    
    print("ERROR EXTRACTING JSON")
    return False
def fetch_and_process_webpages(url):
    experiences = """I am an experienced machine learning engineer with a strong background in artificial intelligence, natural language processing (NLP), computer vision, and deep learning. I have expertise in model evaluation, hyperparameter tuning, feature engineering, and data preprocessing, using tools such as Python, PyTorch, TensorFlow, and Scikit-Learn. I have a solid foundation in data manipulation (Pandas, NumPy), big data tools (Spark), and data visualization (Matplotlib, Seaborn, Plotly, Dash). My experience spans various domains, including developing NLP solutions, time series forecasting, image processing, and building high-performance web-based dashboards. I hold a Master’s degree in Computer Science with a focus on artificial intelligence and have worked on sentiment analysis using deep learning approaches. My work includes research and development of Persian NLP tools and datasets, real-time social media monitoring, and creating advanced AI solutions for financial applications. In addition to technical skills, I have strong project management experience, and a proven track record in cross-functional collaboration. I have authored and contributed to multiple research papers and publications in machine learning and AI, demonstrating my commitment to staying at the forefront of industry trends and contributing to data-driven decision-making."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        raw_text = html_to_raw_text(text)
        result = get_email_text(raw_text, experiences)
        if result:
            if isinstance(result['email_body'], list):
                result['email_body'] = "\n".join(i for i in result['email_body'])
            result['email_body'] = result['email_body'].replace("XXXX YYY", "Hamid Mahmoodabadi")
            print("*" * 50)
            return result
    except requests.RequestException as e:
        print(f"Failed to retrieve or process {url} with exception: {e}")
        return False
    




#df = pd.read_excel("excel.xlsx")
##websites = ["http://michaelryoo.com/"]
#a = fetch_and_process_webpages(websites[0])



