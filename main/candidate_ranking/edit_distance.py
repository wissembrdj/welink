'''
Code from https://rosettacode.org/wiki/Levenshtein_distance#Python
'''
class Edit_distance:
    def __init__(self, word1, word2):
        self.word1=word1
        self.word2=word2
        
    def minimumEditDistance(self):
        word1=str(self.word1)
        word2=str(self.word2)
        if len(word1) > len(word2):
            word1,word2 = word2,word1
        distances = range(len(word1) + 1)
        for index2,char2 in enumerate(word2):
            newDistances = [index2+1]
            for index1,char1 in enumerate(word1):
                if char1 == char2:
                    newDistances.append(distances[index1])
                else:
                    newDistances.append(1 + min((distances[index1],
                                                 distances[index1+1],
                                                 newDistances[-1])))
            distances = newDistances
        return distances[-1]     

    def compare_strings_len(self):
        s1=str(self.word1)
        s2=str(self.word2)
        if len(s1) > len(s2):
            max=len(s1)
        elif len(s1) < len(s2):
            max=len(s2)
        else:
            max=len(s1)
        return max   
 
# distance=Edit_distance("New York", "Q-York")
# distance=distance.minimumEditDistance()
# print(distance)
# print(1-(distance/10))           