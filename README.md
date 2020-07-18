# welink
WeLink is a Named Entity Disambiguation system for queries within Question Answering systems. WeLink exploits syntactic and semantic features of an entity to proceed to its disambiguation. 

You can try <a href="http://193.194.84.136:8000/">WeLink</a>

To use the WeLink API as follows:

```bash
curl -X POST -H "Content-Type: application/json" 
-d '{"query": "What are the books written by Jack London? " }' 
http://193.194.84.136:8000/api 
```
