
class Result(object):


    def __init__(self, corrected_entity, system_result, entity_mentions ):
        '''
        Constructor
        '''
        self.corrected_entity=corrected_entity
        self.system_result= system_result
        self.entity_mentions= entity_mentions
        
        
    def precision(self):
        if self.system_result==0:
            precision=0
        else:
            precision= self.corrected_entity/self.system_result
                
        return precision     
    
    def recall(self):
        if self.entity_mentions==0:
            recall=0
        else:    
            recall= self.corrected_entity/self.entity_mentions
        return recall
    
        