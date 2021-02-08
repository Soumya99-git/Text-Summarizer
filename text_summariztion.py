import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import os
import re



def summarization(path):
    
    os.chdir(r"c:\Users\Soumya Chatterjee\Desktop\INFRAMIND\PROJECT\uploads")
    text_obj = open(path,"r")
    text_l = text_obj.readlines()
    text = ""
    for i in text_l:
        text+=str(i)
    stops = list(STOP_WORDS)
    stops.append('\n')
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)

    #calculation of word frequency in text and storing it in a dict
    word_freq = {}

    for i in doc:
        if i.text.lower() not in stops:
            if i.text.lower() not in punctuation:
                if i.text.lower() not in word_freq.keys():
                    word_freq[i.text.lower()] = 1
                else:
                    word_freq[i.text.lower()]+= 1


    #normalised word frequencies of all words are being calculated
    max_freq = max(word_freq.values())
    norm_word_freq = {}
    for i in word_freq.keys():
        norm_word_freq[i] = word_freq[i]/max_freq

    #sentence tokenization
    sent_token=[]

    for i in doc.sents:
        sent_token.append(i)

    #calcualtion of sentence scores
    sent_score = {}
    for sent in sent_token:
        for i in sent:
            if i.text.lower() in norm_word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = norm_word_freq[i.text.lower()]
                else:
                    sent_score[sent]+= norm_word_freq[i.text.lower()]


    #summarization:-> taking 30% of the total number of sentences present in the text with heap queue 

    length_sent = int(len(sent_token)*0.3)

    summary = [sent_token[0]]
    summary_imp = nlargest(length_sent,sent_score,sent_score.get)
    summary.extend(summary_imp)


    final_summary = []

    for i in summary:
        final_summary.append(i.text)

    summary_disp = " ".join(final_summary)
    summary_disp.replace("\n"," ")
    
    new_path = path[:-4]+"_sum.txt"
    
    fp = open(new_path,"w")
    fp.write(summary_disp)
    
    return new_path

    