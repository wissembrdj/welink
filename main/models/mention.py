'''
Created on 19 fvr. 2019

@author: Breneer Jacinto PC
'''

class Mention:
    '''
    classdocs
    '''
    def __init__(self, name, context, e_type, sentence_words):
        '''
        Constructor
        '''
        self.name= name
        self.context= context
        self.e_type= e_type
        self.sentence_words= sentence_words
        