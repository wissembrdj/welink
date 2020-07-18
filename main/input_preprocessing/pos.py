import nltk


class Pos:
    '''
    classdocs
    '''
    def __init__(self, words):
        '''
        Constructor
        '''
        self.words = words
        
    def pos(self):
        pos = nltk.pos_tag(self.words)
        return pos  
    
    def pos_filter(self):
        pos = nltk.pos_tag(self.words)
        wordpos = []
        tags=["NNS", "NN", "VB", "VBD", "VBG", "VBP", "VBZ", "CD", "JJR", "JJR", "RBR", "RBS"]
        for t in pos: 
            if t[1] in tags:
                wordpos.append(t[0])
#         all_tags = {tag: [t for t in pos if t[1] == tag] for tag in ["NNS", "NN", "VB", "VBD", "VBG", "VBP", "VBZ", "CD", "JJR", "JJR", "RBR", "RBS"]}
#  
#         for v in all_tags:
#             releases = all_tags[v]
#             if releases:
#                 wordpos.append(releases[0]);
        return wordpos     
    
    def truecasing_by_pos(text):
        # tokenize the text into words
        words = nltk.word_tokenize(text)
        print(text)
        # apply POS-tagging on words
        tagged_words = nltk.pos_tag([word.lower() for word in words])
        # apply capitalization based on POS tags
        capitalized_words = [w.capitalize() if t in ["NN","NNS"] else w for (w,t) in tagged_words]
        # capitalize first word in sentence
        capitalized_words[0] = capitalized_words[0].capitalize()
        # join capitalized words
        text_truecase = re.sub(" (?=[\.,'!?:;])", "", ' '.join(capitalized_words))
        return text_truecase
#         
# pos= Pos(['Name', 'leaders', 'parent', 'organisation', 'Gestapo'])
# pos= pos.pos_filter()
# print(pos)
