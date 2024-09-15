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
        text += f"Here is my description or biography: {author_dict['description']}.\n"
    if author_dict["keywords"]:
        text += f"Here are my key words and phrases: {author_dict['keywords']}.\n"
    if author_dict["articles_topic"]:
        text += f"This is the topic of articles that I want to create: {author_dict['articles_topic']}.\n"
    if author_dict["text_tone"]:
        text += f"I use {author_dict['text_tone']} style of speech.\n"
    if author_dict["text_style"]:
        text += f"I want the text to be in a {author_dict['text_style']} style.\n"
    if author_dict["articles"]:
        previous_topics = [art["topic"] for art in author_dict["articles"]]
        text += f"I already have articles on the following topics: {', '.join(previous_topics)}. I need new topics.\n"

    text += "Write 3 ideas for my new article separated by commas. I just need ideas separated by commas without additional text. Even without text `Here are three article ideas for you...`"
    resp = get_response(prompt=text)
    print("FINISHED")
    try:
        topics = resp.split(",")
        topics = list(map(lambda x: x.strip(), topics))
        return topics[:3]
    except Exception:
        return []


def generate_article(author_dict, topic):
    print("Start generating article...")
    text = f"I am an author who wants to generate an article on a specific topic: {topic}.\n"
    if author_dict["description"]:
        text += f"Here is my description or biography: {author_dict['description']}.\n"
    if author_dict["keywords"]:
        text += f"Here are my key words and phrases: {author_dict['keywords']}.\n"
    if author_dict["articles_topic"]:
        text += f"This is the topic of articles that I want to create: {author_dict['articles_topic']}.\n"
    if author_dict["text_tone"]:
        text += f"I use {author_dict['text_tone']} style of speech.\n"
    if author_dict["text_style"]:
        text += f"I want the text to be in a {author_dict['text_style']} style.\n"
    text += "Write me a new article. I just need article without additional text. Even without text `Here is an article for you...` or something like this."
    resp = get_response(prompt=text)
    print("FINISHED")
    # Replace * ** with "\n – "
    formatted_text = re.sub(r"\*\ \*\*", "\n – ", resp)
    # Replace **: with :\n
    formatted_text = re.sub(r"\*\*\:", ":\n", formatted_text)
    # Replace ** with new lines
    formatted_text = re.sub(r"\*\*", "\n", formatted_text)
    # Replace * with a dash and space
    formatted_text = re.sub(r"\*", " – ", formatted_text)
    # Replace ### with \n
    formatted_text = re.sub(r"\#\#\#", "\n", formatted_text)
    # Replace ## with \n
    formatted_text = re.sub(r"\#\#", "\n", formatted_text)
    # Replace # with \n
    formatted_text = re.sub(r"\#", "\n", formatted_text)
    # Remove lines with only `=` characters
    formatted_text = re.sub(r"^=+$", "\n", formatted_text, flags=re.MULTILINE)
    # Remove lines with only `-` characters
    formatted_text = re.sub(r"^-+$", "\n", formatted_text, flags=re.MULTILINE)
    return formatted_text


def edit_article(article_text, changes):
    print("Start editing article...")
    text = f"I have an article. I want make these changes to this article: {changes}. Write me edited article. I just need article text without additional text from you. Even without text `Here is the edited article...` or something like this.\n"
    text += f"Here is article text: {article_text}"
    resp = get_response(prompt=text)
    print("FINISHED")
    # Replace * ** with "\n – "
    formatted_text = re.sub(r"\*\ \*\*", "\n – ", resp)
    # Replace **: with :\n
    formatted_text = re.sub(r"\*\*\:", ":\n", formatted_text)
    # Replace ** with new lines
    formatted_text = re.sub(r"\*\*", "\n", formatted_text)
    # Replace * with a dash and space
    formatted_text = re.sub(r"\*", " – ", formatted_text)
    # Replace ### with \n
    formatted_text = re.sub(r"\#\#\#", "\n", formatted_text)
    # Replace ## with \n
    formatted_text = re.sub(r"\#\#", "\n", formatted_text)
    # Replace # with \n
    formatted_text = re.sub(r"\#", "\n", formatted_text)
    # Remove lines with only `=` characters
    formatted_text = re.sub(r"^=+$", "\n", formatted_text, flags=re.MULTILINE)
    # Remove lines with only `-` characters
    formatted_text = re.sub(r"^-+$", "\n", formatted_text, flags=re.MULTILINE)
    return formatted_text
