# WeLink
WeLink is a Named Entity Disambiguation system for queries within Question Answering systems. WeLink exploits syntactic and semantic features of an entity to proceed to its disambiguation. 

You can try [WeLink](http://193.194.84.136:8000/)

## API
The REST API of WeLink is accessible as follows:

```bash
curl -X POST -H "Content-Type: application/json" 
-d '{"query": "What are the books written by Jack London? " }' 
http://193.194.84.136:8000/api/ 
```
## Usage
After installing all the requirements, use the next command inside the WeLink application folder:
```bash
python manage.py runserver 
```
and open the application in your browser at 120.0.0.1:8000



