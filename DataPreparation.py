# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

import string
import re

class DataPreparation():
    
    def _create_dictionary_table(self,text_string) -> dict:
    
        # Remove numbers
        #text = re.sub(r'\d+', '', text)
        
        # Remove references [number]
        text_string = re.sub(r'\[\d+\]', '',text_string)
        
        # Mettre le texte en Minuscule
        text_string = text_string.lower()      
    
        # Every punctuation symbol will be replaced by a space
        punct = string.punctuation
        trantab = str.maketrans(punct, len(punct)*' ') 
        text_string = text_string.translate(trantab)     
   
        # Removing stop words
        stop_words = set(stopwords.words("english"))
        
        words = word_tokenize(text_string)
        
        # Reducing words to their root form
        stem = PorterStemmer()
        
        # Creating dictionary for the word frequency table
        frequency_table = dict()
        for wd in words:
            wd = stem.stem(wd)
            if wd in stop_words:
                continue
            if wd in frequency_table:
                frequency_table[wd] += 1
            else:
                frequency_table[wd] = 1
    
        return frequency_table

    def _calculate_sentence_scores(self, sentences, frequency_table) -> dict:
        
        sentence_weight = dict()
        max_freq = max(frequency_table.values())
        
        for sentence in sentences:
            #max_freq = len(word_tokenize(sentence.lower()))
            sentence_weight[sentence] = 0
            
            for word in word_tokenize(sentence.lower()):
                
                if word in frequency_table.keys():
                    
                    sentence_weight[sentence] += frequency_table[word]/max_freq
           
        
            
        return sentence_weight
    
    def _calculate_average_score(self, sentence_weight) -> int:
   
        # Calculating the average score for the sentences
        sum_values = 0
        for entry in sentence_weight:
            
            sum_values += sentence_weight[entry]
    
        # Getting sentence average value from source text
        average_score = (sum_values / len(sentence_weight))
    
        return average_score

    
    def _get_article_summary(self, sentences, sentence_weight, threshold):
        sentence_counter = 0
        article_summary = ''
    
        for sentence in sentences:
            if sentence in sentence_weight and sentence_weight[sentence] >= (threshold):
                article_summary += " " + sentence
                sentence_counter += 1
    
        return article_summary, sentence_counter