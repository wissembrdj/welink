from input_preprocessing.input_treatement import Input_treatement
from candidate_generation.string_match import StringMatch
from models.similarities import Similarities 
from candidate_ranking.candidate_similarities import Candidate_similarities
import json
import csv
from results.result import Result


def main():
    
    writer = csv.writer(open("final_results.csv", 'w', newline=''))
     
    with open('LCQuAD.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read()) 
 
        for distro in data:
            input_query=Input_treatement(distro['question'])
            treated_query=input_query.input_treatement()
            entities_sim=[]
            named_e=[]
            for ne in treated_query: 
                named_e.append(ne.name)
                candidates=StringMatch(str(ne.name))
                candidates_ec=candidates.string_match()   
                contexts=[ne.context]
                type_m=str(ne.e_type)
                if type_m=="None": 
                    type_m="" 
                types=[type_m]
                t=0
                cosine_sim_type=[]
                if len(candidates_ec)>0:
                    for i in candidates_ec:                             
                        contexts.append(i.ec_context)
                        type_c=str(i.ec_types)                
                        if (len(i.ec_types)==1 and i.ec_types[0]=='') :
                            type_c=""    
                        types.append(type_c)
                    sim_c=Candidate_similarities(contexts)
                    cosine_sim_context=sim_c.moy_cosine()
                    sim_t=Candidate_similarities(types)
                    cosine_sim_types=sim_t.moy_cosine()
    #                 for i in candidates_ec:
    #                     context_m=str(ne.context)
    #                     print(ne.context)
    #                     context_c=str(i.ec_context)
    #                     sim_c=Candidate_similarities(context_m, context_c)
    #                     cosine_sim_context=sim_c.moy_cosine() 
    #                     type_m=str(ne.e_type)
    #                     type_c=str(i.ec_types)
    #                     sim_t=Candidate_similarities(type_m, type_c)                  
    #                     cosine_sim_types=sim_t.moy_cosine()
    #                     types_supp_moyenne.append(cosine_sim_types)  
                    a=1
                    for i in candidates_ec:
                        total= cosine_sim_context[a]+cosine_sim_types[a]
                        similarities_e=Similarities(ne, i, cosine_sim_context[a], cosine_sim_types[a], total)
                        entities_sim.append(similarities_e)
                        a=a+1
                            
            entities_sim.sort(key=lambda x: x.total_sim, reverse=True)
             
             
            best_candidate = sorted(entities_sim, key=lambda x: x.total_sim, reverse=True)
#             for b in best_candidate:
#                 print(b.em.name, b.ec.ec_name,b.ec.ec_context, b.ec.ec_uri, b.sim_context)
#                          
#         #             for nels in named_e:
#         #                 max_sim=0
#         #                 min_sim=0
#         #                 for emm in entities_sim:   
#         #                     if(emm.em.name==nels): 
#         #                         if float(emm.total_sim) > max_sim:
#         #                             max_sim=float(emm.total_sim)
#         #                             nem_best=emm    
#         #                         else:
#         #                             for bc in best_candidate:
#         #                                 if bc.total_sim < min_sim:
#         #                                     min_sim= bc.total_sim 
#         #                                     best_candidate.remove(bc)
#         #                                     nem_best=emm  
#         #                             
#         #                         if nem_best not in best_candidate:   
#         #                             best_candidate.append(nem_best)    
#             
            nbem=0
            n=1    
            entity_mentions=0 
            correctly_linked=0  
            result=[]  
            nsm=0
            detected_entity=len(named_e)  
            print(detected_entity)
            if detected_entity==0:
                #No detected named entity:
                system_result=0    
                entity_precision=0 
                entity_recall=0 
                for em in distro["entity mapping"]:
                    nbem=nbem+1
                myData=[[distro['SerialNumber'],distro['question'],nbem,detected_entity,system_result,correctly_linked, entity_precision,entity_recall,"0", "1", "0"] ]                
                print("____________________________________")    
                myFile = open('final_results.csv', 'a')
                with myFile:
                    writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                    writer.writerows(myData)  
                     
            else:          
                if best_candidate:
                    for em in distro["entity mapping"]:
                        entity_mentions=entity_mentions+1
                        for b in best_candidate:
                            #print("id question: ", distro['SerialNumber'], "result n: ",  n, b.em.name, b.ec.ec_name, b.ec.ec_uri, b.sim_context)  
                            if b.ec.ec_uri==em["uri"]:
                                system_result=n
                                correctly_linked=correctly_linked+1     
                                result.append(b)  
                                                   
                            n=n+1      
                    #print(correctly_linked, system_result, entity_mentions)
                    res= Result(correctly_linked, system_result, entity_mentions)
                    if system_result!=0:
                        entity_precision=res.precision()
                    else:
                        entity_precision=0   
                    entity_recall=res.recall()  
                    if entity_recall!=0 and entity_precision!=0:
                        fmeasure= (2*entity_precision*entity_recall)/(entity_precision + entity_recall)   
                    else:
                        fmeasure=0       
                    for i in result:
                        print("id question: ", distro['SerialNumber'], "result n: ",  system_result, i.em.name, i.ec.ec_name, i.ec.ec_uri, i.sim_context)  
                    print("Precision:", entity_precision," Recall:", entity_recall )          
                    print("____________________________________")
                    myData=[[distro['SerialNumber'],distro['question'],entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, fmeasure, "0", "0"] ]               
                    myFile = open('final_results.csv', 'a')
                    with myFile:
                        writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                        writer.writerows(myData) 
                     
                else:
                    #No string match
                    system_result=0    
                    entity_precision=0 
                    entity_recall=0 
                    nsm=nsm+1
                    myData=[[distro['SerialNumber'],distro['question'],entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, "0", "0",nsm] ]                
                    print("____________________________________")    
                    myFile = open('final_results.csv', 'a')
                    with myFile:
                        writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                        writer.writerows(myData)    
             
        
             
            #resultats= Results(best_candidate)
            #resultats_classified=resultats.message()
            #print(resultats_classified)
    print("process completed")         
if __name__ == '__main__':
    main()