from main.input_preprocessing.input_treatement import Input_treatement
from main.candidate_generation.string_match import StringMatch
from main.models.similarities import Similarities 
from main.candidate_ranking.candidate_similarities import Candidate_similarities
from main.candidate_ranking.coherence import Coherence
from main.candidate_ranking.edit_distance import Edit_distance
import json
import time


class Welink():
    
    def __init__(self, query):
        self.query=query   
    
    def userquerymodel(self):
        start_time = time.time()
        input_query=Input_treatement(self.query)
        treated_query_p=input_query.input_treatement()
        treated_query=treated_query_p.mentions_list
        deteted_entities=treated_query_p.detected_ne
        print(deteted_entities)
        
        nbr_ne=len(deteted_entities)

        print('pre traitement de la requete', time.time() - start_time)
        entities_sim=[]
        named_e=[]
        ne_nb=len(treated_query)
        results_disambiguation=[]
        entities_mentions=[]
        r=0
        if treated_query:
            for ne in treated_query: 
                named_entity=ne.name 
                mention=len(named_entity)/10
                named_entity_type=""
                best_candidate=[]
                entities_sim=[]
                candidates=StringMatch(ne)
                candidates_ec=candidates.string_match()
                print('string match:', time.time() - start_time)  
                if candidates_ec:                  
                    sim_c=Candidate_similarities(ne, candidates_ec)
                    cosine_sim_context=sim_c.cosine()
                    a=1
                    total_sim=0
                    for i in candidates_ec:
                        candidate=i.ec_name
                        candidates_relations= i.properties + i.objects
                        sim_proprieties= Coherence(ne.sentence_words, candidates_relations)
                        jaccard_sim_properties= sim_proprieties.jaccard_variation()
                        edit_distance_name=Edit_distance(named_entity,candidate)
                        edit_distance=edit_distance_name.minimumEditDistance()   
                        max_name_len=edit_distance_name.compare_strings_len()
                        if edit_distance!=0:  
                            edit_distance=(edit_distance/max_name_len)
                        
    
                        if ne_nb>1 :
                            sim_entities= Coherence(ne.sentence_words,i.objects)
                            jaccard_sim_entities= sim_entities.jaccard_variation()
                        else:
                            jaccard_sim_entities=0 
#                         print("CANDIDATE", candidate, "contexte", cosine_sim_context[a], "prop", jaccard_sim_properties, "obj", jaccard_sim_entities, "edit", edit_distance)
                        total_sim= jaccard_sim_properties + jaccard_sim_entities - edit_distance
                        if named_entity in deteted_entities:
#                         cap=0
#                         if named_entity[0].isupper():
#                             cap=1
                            total_sim=total_sim+0.5

   
#                         candidate_length=len(candidate)/10
#                         total_sim=total_sim*candidate_length
#                         candidate_length=len(candidate)/10
                        total_sim=total_sim+mention
#                                         print("contexte", cosine_sim_context[a], "prop", jaccard_sim_properties, "objects", jaccard_sim_entities)
#                         total_sim= cosine_sim_context[a] +jaccard_sim_properties+jaccard_sim_entities+cap
                        
                        similarities_e=Similarities(ne, i, cosine_sim_context[a], jaccard_sim_properties, jaccard_sim_entities,total_sim)
                        entities_sim.append(similarities_e)
                        a=a+1  
                        
           
                    print('candidate ranking:', time.time() - start_time)       
                    best_candidate = sorted(entities_sim, key=lambda x: x.total_sim, reverse=True)
                    print('tri', time.time()- start_time)
                    results_disambiguation.append(best_candidate)
                    print("--- %s seconds ---" % (time.time() - start_time))

        
        final = sorted(results_disambiguation, key=lambda x: x[0].total_sim, reverse=True)            
 
 
 #-----------threshold with ner numner       
        threshold=nbr_ne
        n=0
        filtred_entities_sim=[]
        if final:
            if len(final)==1:
                if final[0][0].total_sim>0.6:    
                    filtred_entities_sim=final
            else:
                if threshold>0:
                    if len(final)<threshold:
                        for rd in final:
                            if rd[0].total_sim>0.6:
                                filtred_entities_sim.append(rd)
                    else:    
                        while n<threshold:    
                            if final[n][0].total_sim>0.6:
                                filtred_entities_sim.append(final[n])    
                            n=n+1 
                else:
                    if final[0][0].total_sim>0.6:
                        filtred_entities_sim.append(final[0])          
                        
                          
#---------------lengeur question                    
#         rd=0
#         filtred_entities_sim=[]
#         if len(results_disambiguation)>1:    
#             if len(self.query)<=8.2:
#                 max=1
#             elif len(self.query)>=8.2 and len(self.query)<10:
#                 max=2
#             else:
#                 max=3    
#             while rd<max:    
#                 filtred_entities_sim.append(results_disambiguation[rd])
#                 rd=rd+1            
#         else:
#             filtred_entities_sim=results_disambiguation                
#-----------Threshold without mise à l'echelle 
#         threshold=0
#         filtred_entities_sim=[]
#         for rd in results_disambiguation:
#             ml=rd[0].total_sim
#             if ml>threshold:
#                 if rd not in filtred_entities_sim:    
#                     filtred_entities_sim.append(rd)  
#----------threshold with mise à l'echelle
#         threshold=0
#         max=0
#         for rd in results_disambiguation:
#             for bc in rd:
#                 if bc.total_sim>max:
#                     max=bc.total_sim
#         filtred_entities_sim=[]
#         for rd in results_disambiguation:
#             ml=rd[0].total_sim/max
#             if ml>threshold:
#                 if rd not in filtred_entities_sim:    
#                     filtred_entities_sim.append(rd)      
                    
               
#--------------filtring with names        
#         filtred_entities_sim=[]
#         for rd in results_disambiguation:
#             if filtred_entities_sim:
#                 entity=rd[0].em.name
#                 score=rd[0].total_sim
#                 uri=rd[0].ec.ec_uri
#                 for fe in filtred_entities_sim:
#                     if entity in fe[0].em.name: 
#                         if len(entity)>len(fe[0].em.name):
#                             filtred_entities_sim.pop(filtred_entities_sim.index(fe))
#                         if (rd not in filtred_entities_sim) and (uri not in fe[0].ec.ec_uri) and (score>-1):
#                             filtred_entities_sim.append(rd)
#                     else:
#                         if (rd not in filtred_entities_sim) and (uri not in fe[0].ec.ec_uri) and (score>-1):
#                             filtred_entities_sim.append(rd)                        
#             else:
#                 filtred_entities_sim.append(rd)    
        
   
    
        
                    #------------------
#         print(entities_mentions)
#         final_entities_sim=[]
#         i=0
#         j=0
#         max=len(entities_mentions)
#         filtred_entities_sim=[]
#         if max>1:
#             while i<max:
#                 j=i+1
#                 if j<max:
#                     while j<max:
#                         if entities_mentions[i] in entities_mentions[j]:
#                             if len(entities_mentions[i]) < len(entities_mentions[j]):
#                                 if entities_mentions[i] in final_entities_sim:
#                                     final_entities_sim.pop(final_entities_sim.index(entities_mentions[i]))
#                                 if entities_mentions[j] not in final_entities_sim: 
#                                     final_entities_sim.append(entities_mentions[j]) 
#                             else: 
#                                 if entities_mentions[i] not in final_entities_sim:     
#                                     final_entities_sim.append(entities_mentions[i])        
#                         else:
#                             if entities_mentions[i] not in final_entities_sim:    
#                                 final_entities_sim.append(entities_mentions[i]) 
#                         j=j+1
#                 else:
#                     if entities_mentions[i] not in final_entities_sim:    
#                         final_entities_sim.append(entities_mentions[i])                           
#                 i=i+1        
#             for n in results_disambiguation: 
#                 for f in n:
#                     if f.em.name in final_entities_sim:
#                         if n not in filtred_entities_sim:
#                             filtred_entities_sim.append(n) 
#         else:
#             filtred_entities_sim=results_disambiguation       
#--------------------------                               
#--------------------------                                  
        return filtred_entities_sim
        
        
    
