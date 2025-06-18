import chromadb
from sentence_transformers import SentenceTransformer

class DocumentSearcher: 
    def __init__(self, dbPath = "./chroma_db"):
        self.client = chromadb.PersistentClient(path = dbPath)
        self.collection = self.client.get_collection(name="documents")
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded!")
    
    
    def search(self, query, n_results=5): 
        results = self.collection.query(
            query_texts =[query], 
            n_results = n_results
        )
        
        return results

    def displayResults(self, results): 
        #query outputs in batches and returns the first batch
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results ['distances'][0]
        
        print(f"\nFound {len(documents)} results:\n")
        for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
            
            print(f"DEBUG - Available metadata keys: {list(metadata.keys())}")    
            print(f"Result {i+1} (similarity: {1-distance:.3f})")
            print(f"File: {metadata['filename']}")
            print(f"Path: {metadata['filePath']}")
            print(f"Preview: {doc[:200]}...")
            print("-" * 80)

if __name__ == "__main__": 
    documentSearcher = DocumentSearcher()
    print("personal search engine")
    while myInput != "quit":
        myInput = input("search something or quit") 
        results =  documentSearcher.search(myInput)
        documentSearcher.displayResults(results)
    

   
    
