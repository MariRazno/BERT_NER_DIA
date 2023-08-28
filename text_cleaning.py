import spacy
import re

# loading German language model
nlp = spacy.load("de_core_news_sm")

# clean reports
def text_preparation(text: str):

    """
    :param text: raw medical report text
    :return Str: clean report text
    """

    text = re.sub(r'\d{5,}', '', text)
    text = re.sub(r'[\n+\t+\f+]', ' ', text)
    text = re.sub(r'\d+\.\d+\.\d+', ' ', text)
    text = re.sub(r'\\m[0-9]+', '', text)
    text = re.sub(r'[\\"]', '', text)
    text = re.sub(r'f:', '', text)
    text = re.sub(r"^[\s\.:;,\(\)\-]+", '', text)
    text = re.sub('\s{2,}', ' ', text)
    return text


def get_sents(text: str):

    """
    :param text: raw medial report text
    :return List: liat of sentences from the report
    """
    # creating sents from report
    sentencized_data = []
    nlp_doc = nlp(text)
    for sent in nlp_doc.sents:
        if len(sent.text.split()) > 5:
            if sent.text not in sentencized_data:
                sentencized_data.append(sent.text)
    return sentencized_data

