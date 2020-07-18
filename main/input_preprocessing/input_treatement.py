from main.input_preprocessing import *
from main.input_preprocessing.contractions import Contractions
from main.input_preprocessing.ner import Ner
from main.input_preprocessing.ngram import Word_grams
from main.input_preprocessing.pos import Pos
from main.input_preprocessing.punctuations_removal import Punctuations_removal
from main.input_preprocessing.stopwords import Stopwords
from main.input_preprocessing.synonyms import Synonyms
from main.input_preprocessing.tokenization import Tokenization
from main.models.mention import Mention
from main.models.pretreated_query import PretreatedQuery
from main.input_preprocessing.convert import convert
from main.input_preprocessing.ngram import Word_grams
from nltk.corpus import wordnet
from textblob import TextBlob
import time


class Input_treatement:
    def __init__(self, sentence):
        '''
        Constructor
        '''
        self.sentence= sentence
    

                
        
    def input_treatement(self): 
        query_input= self.sentence
        query=Contractions(query_input)
        sentence=query.contractions()
        tokens=Tokenization(sentence)
        token=tokens.tokenization()
#         token=[]
#         t=0
#         while t<len(tokens):
#             if t+1<len(tokens):
#                 if tokens[t+1]=="'s":
#                     word_n=tokens[t]+tokens[t+1]
#                     token.append(word_n)
#                     t=t+2
#                 elif (t+1!=len(tokens)-1) and tokens[t+1]==".":
#                     word_n=tokens[t]+tokens[t+1]
#                     token.append(word_n)
#                     t=t+2
#                 else:
#                     if tokens[t]!='"' or '>' or '<':
#                         token.append(tokens[t])
#                     t=t+1        
#             else:
#                 if tokens[t]!='"' or '>' or '<':    
#                     token.append(tokens[t])
#                 t=t+1                
                    
        punctuation=Punctuations_removal(token)
        punctuation_removal=punctuation.punctuations_removal()
        stopwords= Stopwords(punctuation_removal)
        sentence_without_stopword=stopwords.stop_words()
        pos_sentence= Pos(token)
        pos= pos_sentence.pos()
        pos_filter=pos_sentence.pos_filter()
        named_entities=[]    
        text= Ner(pos)
        named_entities=text.ner_welink()
        conform_ne=[]
        conform_ne=text.ner_welink()


            #--------------------TEXTBLOB
#         blobedquery=TextBlob(query_input)  
#         nementions=blobedquery.noun_phrases
#         sentence=[]
#         for i in nementions:
#             word=""
#             phrase_split= i.split(" ")
#             for p in phrase_split:
#                 sentence.append(p)
#                 word=word+" "+p.capitalize()
#             word=word.strip()
#             if word not in conform_ne:
#                 conform_ne.append(i)
#----------------------------NGRAM
#         if not named_entities:
        text= Word_grams(token)
        nes=text.word_grams()
        for ne in nes:
            if ne not in named_entities:
                named_entities.append(ne)
                

#         print(named_entities)
        list_mentions=[]
        if named_entities:    
            for ne in named_entities:
                ne_tag=ne
                types_ne=""
                ne_definition=Synonyms(ne)
                ne_def=ne_definition.definition()  
                syno=Synonyms(pos_filter)
                synonymes=syno.synonyms()
                synosentence=Synonyms(sentence_without_stopword)
                synonymes_sentence_words=syno.synonyms() 
                synonymes_sentence_words= synonymes_sentence_words.replace('_', ' ')
                synonymes_s_words=synonymes_sentence_words.split(" ")
                context_m= ne_def+synonymes
                mentions= Mention(ne_tag, context_m ,types_ne, synonymes_s_words)
                list_mentions.append(mentions)
                
        pretreated_query=PretreatedQuery(list_mentions, conform_ne)       
        
                     
        return pretreated_query         
                            
 
