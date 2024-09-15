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


art = """

The Effects of Climate Change on Global Food Production

Climate change is one of the most pressing issues of our time, with far-reaching consequences for the environment, human health, and the economy. One of the most significant impacts of climate change is on global food production, which is essential for human survival. Rising temperatures, changing precipitation patterns, and increased frequency of extreme weather events are altering the conditions necessary for growing crops, raising livestock, and producing food.

Impacts on Crop Yields


 – Temperature Increase:
 Rising temperatures are altering the growing seasons, leading to changes in the timing of planting and harvesting. This can result in reduced crop yields, lower quality crops, and decreased food security.

 – Water Scarcity:
 Changes in precipitation patterns are leading to droughts in some areas and floods in others, affecting crop growth and food production.

 – Shift in Growing Seasons:
 Warmer temperatures are causing plants to bloom earlier, making them more vulnerable to frost and other extreme weather events.

Consequences for Food Security


 – Reduced Crop Yields:
 Climate change is projected to reduce global crop yields by up to 2% per decade, leading to food shortages and price increases.

 – Food Price Volatility:
 Climate-related shocks to food systems can lead to price volatility, making food less accessible to vulnerable populations.

 – Malnutrition:
 Climate change is expected to increase the number of people suffering from malnutrition, particularly in developing countries.

Regional Impacts


 – Sub-Saharan Africa:
 Climate change is projected to reduce crop yields by up to 22% by 2050, exacerbating existing food security challenges.

 – South Asia:
 Rising temperatures and changing precipitation patterns are affecting rice and wheat production, threatening food security for millions of people.

 – Latin America:
 Climate change is altering the distribution of crops, leading to losses in agricultural productivity and food security.

Adaptation and Mitigation Strategies


 – Sustainable Agriculture:
 Practices such as agroforestry, conservation agriculture, and organic farming can help farmers adapt to climate change.

 – Climate-Smart Agriculture:
 This approach involves using climate information and agricultural practices to enhance resilience and productivity.

 – Reducing Greenhouse Gas Emissions:
 Mitigating climate change through reduced greenhouse gas emissions can help minimize its impacts on global food production.

Conclusion

Climate change poses significant challenges to global food production, threatening food security and the livelihoods of millions of people. Understanding the impacts of climate change on food production is crucial for developing effective adaptation and mitigation strategies. By adopting sustainable agriculture practices, reducing greenhouse gas emissions, and supporting climate-resilient agriculture, we can help ensure a food-secure future for all.
"""


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
