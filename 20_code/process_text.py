# import required packages
import pandas as pd
import numpy as np
import multiprocessing
import re

filename = "../10_cleaned_data/generic_sentiment_dataset_50k_cleaned.csv"
data = pd.read_csv(filename)

# source clean data code:
''' 
These functions were sourced from another author. Contains basic functions to clean raw text data for tokenization using regex.
See original code here: https://www.kaggle.com/code/akgeni/logistic-regression-with-countvectorizer
'''


def remove_unwanted_text(text):
    if text.startswith("Re: "):
        text = text.replace("Re:", "")
    new_text = text.replace("\n", ". ")
    new_text = remove_mentions(new_text)
    new_text = new_text.lower()
    new_text = remove_html(new_text)
    new_text = remove_link(new_text)
    new_text = re.sub(r"[^\w\s]+", " ", new_text)
    return new_text


def remove_link(text):
    new_text = re.sub(r"http\S+", " ", text)
    new_text = re.sub(r"www.\S+", " ", new_text)
    return new_text


def remove_mentions(text):
    new_text = re.sub(r"@\S+", " ", text)
    new_text = re.sub(r"RT[\s]+", " ", new_text)
    return new_text


def remove_html(text):
    return re.sub(r"<[^<>]+>", " ", text)


def clean_text(data):
    pool = multiprocessing.Pool(processes=4)
    data["clean_text"] = pool.map(remove_unwanted_text, data["text"])
    return data


clean_data = clean_text(data)
clean_data.to_csv("../10_cleaned_data/processed_text.csv")
