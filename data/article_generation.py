import re
import requests

url = "https://g4f-api-u0fr.onrender.com/response"


def get_response(prompt):
    # Send the GET request
    params = {"prompt": prompt}
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON
    else:
        return f"Request failed with status code {response.status_code}"


def generate_topics(author_dict):
    print("Start generating topics...")
    text = "I am an author who wants to create an article on a specific topic.\n"
    if author_dict["description"]:
        text += f"Here is my description or biography: {author_dict["description"]}.\n"
    if author_dict["keywords"]:
        text += f"Here are my key words and phrases: {author_dict["keywords"]}.\n"
    if author_dict["articles_topic"]:
        text += f"This is the topic of articles that I want to create: {author_dict["articles_topic"]}.\n"
    if author_dict["text_tone"]:
        text += f"I use {author_dict["text_tone"]} style of speech.\n"
    if author_dict["text_style"]:
        text += f"I want the text to be in a {author_dict["text_style"]} style.\n"
    text += "Write 3 ideas for my new article separated by commas. I just need ideas separated by commas without additional text. Even without text `Here are three article ideas for you...`"
    resp = get_response(prompt=text)
    print("FINISHED")
    try:
        topics = resp.split(",")
        topics = list(map(lambda x: x.strip(), topics))
        return topics
    except Exception:
        return []


def generate_article(author_dict, topic):
    print("Start generating article...")
    text = f"I am an author who wants to generate an article on a specific topic: {topic}.\n"
    if author_dict["description"]:
        text += f"Here is my description or biography: {author_dict["description"]}.\n"
    if author_dict["keywords"]:
        text += f"Here are my key words and phrases: {author_dict["keywords"]}.\n"
    if author_dict["articles_topic"]:
        text += f"This is the topic of articles that I want to create: {author_dict["articles_topic"]}.\n"
    if author_dict["text_tone"]:
        text += f"I use {author_dict["text_tone"]} style of speech.\n"
    if author_dict["text_style"]:
        text += f"I want the text to be in a {author_dict["text_style"]} style.\n"
    text += "Write me a new article. I just need article without additional text. Even without text `Here is an article for you...` or something like this."
    resp = get_response(prompt=text)
    print("FINISHED")
    cleaned_text = re.sub(r"(\*\*|\*)", "", resp)
    return cleaned_text


d = {
    "description": "I like space",
    "keywords": "",
    "articles_topic": "our galaxy",
    "text_tone": "",
    "text_style": "",
    "articles": [],
}
