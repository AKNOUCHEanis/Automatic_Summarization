# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 12:52:57 2021

@author: DELL VOSTRO
"""

import bs4 as BeautifulSoup
import urllib.request  
from nltk.tokenize import sent_tokenize



from DataPreparation import DataPreparation


if __name__ == '__main__':

    """ Chargement des données """
    # Fetching the content from the URL
    fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/20th_century')
    
    article_read = fetched_data.read()
    
    # Parsing the URL content and storing in a variable
    article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')
    
    # Returning <p> tags
    paragraphs = article_parsed.find_all('p')
    
    article_content = ''
    
    # Looping through the paragraphs and adding them to the variable
    for p in paragraphs:  
        article_content += p.text
        
    """ Data Preparation """
    dataPreparation = DataPreparation()
    frequency_table = dataPreparation._create_dictionary_table(article_content)     
    
    #print(frequency_table.keys())
    #print(len(frequency_table.keys()))
    
    

    sentences = sent_tokenize(article_content)
    
    sentences_weighted = dataPreparation._calculate_sentence_scores(sentences, frequency_table)
    avg_score = dataPreparation._calculate_average_score(sentences_weighted)
    
    article_summary, nb_sentences = dataPreparation._get_article_summary(sentences, sentences_weighted, 1.5*avg_score)
    print("Summary :\n",article_summary)
    print("\n Number of sentences of the article : ", len(sentences))
    print("\n Number of sentences of the summary : ",nb_sentences)
    
    
    