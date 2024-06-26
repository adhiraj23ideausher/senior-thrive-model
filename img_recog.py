from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import openai
import requests
from dotenv import load_dotenv, dotenv_values
load_dotenv()
import os
#from getpass import getpass
openai.api_key = os.getenv('OPENAI_API_KEY')

import base64

# Function to encode the image
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')
def encode_image(image_path):
    if image_path.startswith('http://') or image_path.startswith('https://'):
        response = requests.get(image_path)
        response.raise_for_status()  
        image_data = response.content
    else:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()    
    return base64.b64encode(image_data).decode('utf-8')


def calculate_cosine_similarity(text1, texts):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1] + texts)
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:])
    return np.max(cosine_similarities)


def caption_image(image_path):
  encoded_image = encode_image(image_path)

  result = openai.chat.completions.create(
    model = "gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text",
                "text": "Analyze the image of a room carefully, focusing on elements that could pose risks or dangers to elderly individuals. Consider common safety hazards for older people, such as poor lighting, slippery floors, clutter that could cause tripping, and furniture that is not senior-friendly. For each identified potential danger, suggest appropriate products from Amazon that could mitigate these risks. Your suggestions should include product tags relevant to elder safety, such as 'non-slip mats', 'motion-sensor night lights', 'corner protectors', and 'grab bars'. If the room appears to be safe and you identify no dangers, confirm that the room is fine. Additionally, provide a tag or keyword for a DIY video that addresses the safety improvements or installations recommended. This DIY tag should help in finding instructional content to make the room safer for older individuals, emphasizing simplicity and effectiveness for those who may not be highly skilled in home improvements.avoid saying elderly or old"},
                {"type": "image_url",
                "image_url": f"data:image/jpeg;base64,{encoded_image}"},
            ]
        },
    ],
    max_tokens=1000,
    )
    
  personalized_result = result.choices[0].message.content
  #.replace('elderly individuals', 'you').replace('older person', 'you').replace('elderly person', 'you')   
  known_error_messages = [
        "I'm sorry, I can't provide assistance with that request.",
        "I'm sorry, but I cannot assist with this request.",
        "I'm sorry, but I cannot provide an analysis of the image based on your request.",
        "I'm sorry, I can't assist with that request."
   ]
    
    # Calculate the maximum cosine similarity between personalized_result and known error messages
  max_similarity = calculate_cosine_similarity(personalized_result, known_error_messages)
    
    # Assuming a threshold for similarity. This might need adjustment based on testing.
  similarity_threshold = 0.5
  if max_similarity > similarity_threshold:
     return "Please take the photo again."
  else:
     return personalized_result   



# from IPython.display import Image

# print(os.getenv('NAME'))

# image_path = r"https://seniorthrive.s3.us-east-1.amazonaws.com/public/scanImages/f6bcf060-cad6-4ac3-be14-2a4cbb595f18-bedroom.jpg"
# text = caption_image(image_path)
# print(text)
