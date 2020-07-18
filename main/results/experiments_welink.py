import json
import csv
from result import Result
import requests
import time
import re
import io
from extract_entities import entities

   
writer = csv.writer(open("welink_results_qald7.csv", 'a',  newline=''))
url = 'http://127.0.0.1:8000/api/'
headers = {'Content-type': 'application/json'} 
with open('qald-7.json', encoding='UTF-8') as data_file:
    data = json.loads(data_file.read()) 
    nb=0
    for distro in data['questions']:
#         print(distro['query']['sparql'])
        entities_dataset=entities(distro['query']['sparql'])
        print(entities_dataset)
        entity_mentions=0
        correctly_linked=0
        n=1
        system_result=0
        result=[]
        tmp=time.time()
        for d in distro['question']:
            if d["language"]=='en':
                question_en=d["string"]
                print(question_en)
        query = {'query': str(question_en)}
        data_json = json.dumps(query)
        response = requests.post(url, data=data_json, headers=headers)
        execution_time=time.time()-tmp
        print(execution_time)
        if response: 
            response_json=response.json()
            if 'mentions' in response_json:
                detected_entity= len(response_json['mentions'])
                system_result=detected_entity
                if 'results' in response_json:
#                     system_result=len(response_json['results']) 
                    entity_mentions=len(entities_dataset)
                    for em in entities_dataset:
                        for i in range(len(response_json["mentions"])):
                            j=response_json["results"][str(i)][0][1] 
                            if j==em:
                                if j not in result:
#                                             system_result=system_result+n
                                    correctly_linked=correctly_linked+1     
                                    result.append(j)                                                    
                            n=n+1      
                    #print(correctly_linked, system_result, entity_mentions)
                    res= Result(correctly_linked, system_result, entity_mentions)
                    fmeasure=0
                    if system_result!=0:
                        entity_precision=res.precision()
                    else:
                        entity_precision=0   
                    if entity_mentions!=0:    
                        entity_recall=res.recall()  
                    else:
                        entity_recall=0   
                    if entity_recall!=0 and entity_precision!=0:
                        fmeasure= (2*entity_precision*entity_recall)/(entity_precision + entity_recall)   
                      
                    for i in result:
                        print("id question: ", distro['id'], "result n: ",  system_result, detected_entity, result)  
                    print("Precision:", entity_precision," Recall:", entity_recall )          
                    print("____________________________________")
                    myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, fmeasure, "0", "0", execution_time] ]               
                    myFile = open('welink_results_qald7.csv', 'a', encoding='utf-8')
                    with myFile:
                        writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                        writer.writerows(myData) 
                     
                else:
                    #No string match
                    nsm=0
                    system_result=0    
                    entity_precision=0 
                    entity_recall=0  
                    nsm=nsm+1
                    myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, "0", "0",nsm, execution_time] ]                
                    print("____________________________________No string match")    
                    myFile = open('welink_results_qald7.csv', 'a', encoding='utf-8')
                    with myFile:
                        writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                        writer.writerows(myData)    
            else:          
                #No detected named entity:
                if entities_dataset:
                    nbem=0
                    system_result=0    
                    entity_precision=0 
                    entity_recall=0 
                    correctly_linked=0
                    detected_entity=0
                    if 'entity mapping' in distro:
                        for em in distro["entity mapping"]:
                            nbem=nbem+1
                    myData=[[distro['id'],question_en,nbem,detected_entity,system_result,correctly_linked, entity_precision,entity_recall,"0", "1", "0", execution_time] ]                
                    print("____________________________________No detected named entity")    
                    
                else:  
                    nbem=0
                    system_result=1    
                    entity_precision=1 
                    entity_recall=1 
                    correctly_linked=1
                    detected_entity=0
                    fmeasure=1
                    if 'entity mapping' in distro:
                        for em in distro["entity mapping"]:
                            nbem=nbem+1
                    myData=[[distro['id'],question_en,nbem,detected_entity,system_result,correctly_linked, entity_precision,entity_recall,fmeasure, "3", "3", execution_time] ]                
                    print("____________________________________No mention + No results")  
                myFile = open('welink_results_qald7.csv', 'a', encoding='utf-8')
                with myFile:
                    writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                    writer.writerows(myData)  
        else:         
            #Unknown error from the web service
            execution_time=time.time()-tmp
            system_result=0    
            entity_precision=0 
            entity_recall=0 
            fmeasure= 0          
            entity_mentions=0
            detected_entity=0
            correctly_linked=0
            print("____________________________________Unknown error from the web service")
            myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, fmeasure, "2", "2", execution_time] ]               
            myFile = open('welink_results_qald7.csv', 'a', encoding='utf-8')
            with myFile:
                writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                writer.writerows(myData)  
        

 
        #resultats= Results(best_candidate)
        #resultats_classified=resultats.message()
        #print(resultats_classified)
print("process completed")         



# import json
# import csv
# from result import Result
# import requests
# import time
# import re
# import io
# 
# def extract_entities(query):
#     pattern="http://dbpedia.org/resource/[^>]+"
#     return re.findall(pattern,query)
# def extract_entities_QALD7(query):
#     firstModified=[]
#     #print (query)
#     if query=="OUT OF SCOPE":
#         return firstModified
#     whereString = query[query.index('{')+1:query.rfind('}')-1]
#     if "no_query" in whereString:
#         return firstModified
#     whereString=whereString.replace("\n","")
#     whereString=whereString.replace("\t"," ")
#     query=whereString
#     pattern="res:[^\s]+"
#     first=re.findall(pattern,query)
#     
#     for entity in first:
#         firstModified.append(entity.replace("res:","http://dbpedia.org/resource/"))
#         
#     pattern="http://dbpedia.org/resource/[^>]+"
#     second=re.findall(pattern,query)
#     #print(firstModified+second)
#     return firstModified+second   
#    
# writer = csv.writer(open("final_results_qald8_tt.csv", 'a',  newline=''))
# url = 'http://127.0.0.1:8000/api/'
# headers = {'Content-type': 'application/json'} 
# with open('qald-8-train-multilingual.json', encoding='UTF-8') as data_file:
#     data = json.loads(data_file.read()) 
#     nb=0
#     for distro in data['questions']:
#         print(distro['query']['sparql'])
#         entities_dataset=extract_entities_QALD7(distro['query']['sparql'])
#         print(entities_dataset)
#         entity_mentions=0
#         correctly_linked=0
#         n=1
#         system_result=0
#         result=[]
#         tmp=time.time()
#         if distro['question'][nb]['language']=='en':
#             question_en=distro['question'][nb]['string']
#         query = {'query': str(question_en)}
#         data_json = json.dumps(query)
#         response = requests.post(url, data=data_json, headers=headers)
#         if response:
#             execution_time=time.time()-tmp
#             response_json=response.json()
#             if 'mentions' in response_json:
#                 detected_entity= len(response_json['mentions'])
#                 if response_json['results']:
# #                     system_result=len(response_json['results'])
#                     if entities_dataset:
#                         for em in entities_dataset:
#                             entity_mentions=entity_mentions+1
#                             for b in response_json['results']: 
#                                 n=1
#                                 for j in response_json['results'][str(b)]: 
#                                     if j[1]==em:
#                                         if j[1] not in result:
#                                             system_result=system_result+n
#                                             correctly_linked=correctly_linked+1     
#                                             result.append(j[1])                                                    
#                                     n=n+1      
#                     else:
#                         system_result=1
#                         correctly_linked=1
#                         entity_mentions=1
#                     #print(correctly_linked, system_result, entity_mentions)
#                     res= Result(correctly_linked, system_result, entity_mentions)
#                     fmeasure=0
#                     if system_result!=0:
#                         entity_precision=res.precision()
#                     else:
#                         entity_precision=0   
#                     if entity_mentions!=0:    
#                         entity_recall=res.recall()  
#                     else:
#                         entity_recall=0   
#                     if entity_recall!=0 and entity_precision!=0:
#                         fmeasure= (2*entity_precision*entity_recall)/(entity_precision + entity_recall)   
#                       
#                     for i in result:
#                         print("id question: ", distro['id'], "result n: ",  system_result, detected_entity, result)  
#                     print("Precision:", entity_precision," Recall:", entity_recall )          
#                     print("____________________________________")
#                     myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, fmeasure, "0", "0", execution_time] ]               
#                     myFile = open('final_results_qald8_tt.csv', 'a', encoding='utf-8')
#                     with myFile:
#                         writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
#                         writer.writerows(myData) 
#                      
#                 else:
#                     #No string match
#                     system_result=0    
#                     entity_precision=0 
#                     entity_recall=0 
#                     nsm=nsm+1
#                     myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, "0", "0",nsm, execution_time] ]                
#                     print("____________________________________No string match")    
#                     myFile = open('final_results_qald8_tt.csv', 'a', encoding='utf-8')
#                     with myFile:
#                         writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
#                         writer.writerows(myData)    
#             else:          
#                 #No detected named entity:
#                 nbem=0
#                 system_result=0    
#                 entity_precision=0 
#                 entity_recall=0 
#                 correctly_linked=0
#                 detected_entity=0
#                 if 'entity mapping' in distro:
#                     for em in distro["entity mapping"]:
#                         nbem=nbem+1
#                 myData=[[distro['id'],question_en,nbem,detected_entity,system_result,correctly_linked, entity_precision,entity_recall,"0", "1", "0", execution_time] ]                
#                 print("____________________________________No detected named entity")    
#                 myFile = open('final_results_qald8_tt.csv', 'a', encoding='utf-8')
#                 with myFile:
#                     writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
#                     writer.writerows(myData)  
#         else:         
#             #Unknown error from the web service
#             execution_time=time.time()-tmp
#             system_result=0    
#             entity_precision=0 
#             entity_recall=0 
#             fmeasure= 0          
#             entity_mentions=0
#             detected_entity=0
#             correctly_linked=0
#             print("____________________________________Unknown error from the web service")
#             myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, fmeasure, "2", "2", execution_time] ]               
#             myFile = open('final_results_qald8_tt.csv', 'a', encoding='utf-8')
#             with myFile:
#                 writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
#                 writer.writerows(myData)  
#         
#          
#         #resultats= Results(best_candidate)
#         #resultats_classified=resultats.message()
#         #print(resultats_classified)
# print("process completed")         

