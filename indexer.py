import os
import chromadb
from sentence_transformers import SentenceTransformer 
from pathlib import Path
import hashlib 

class DocIndexer:
    def __init__(self, db_path="./chroma_db"):
        #needs a client, a collecton aand a model to initialize indexer
        self.client = chromadb.PersistentClient(path = db_path) 
        
        self.collection = self.client.get_or_create_collection(
                name = "documents" , 
                metadata = {"description": "personal document search"}
                )

        print("loading embedding model")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    
    def chunkText(self, text,  chunkSize = 500, overlap = 50): 
        stringArr = text.split() 
        chunks = []
        
        for i in range(0, len(stringArr), chunkSize - overlap): 

            mystr = " ".join(stringArr[i: i + chunkSize])

            if len(mystr.strip() ) > 0: 
                chunks.append(mystr)
        return chunks

    def extractText(self, filePath):
        #extract text from different fileTypes
        try:
            if filePath.suffix.lower() == '.txt' or filePath.suffix.lower() == '.md': 
                with open(filePath, 'r', encoding = 'utf-8') as f: 
                    return f.read()
            else: 
                return None
        except Exception as e: 
            print(f"error parsing document {filePath}: {e}")
            
    def IndexDocs(self, folderPath): 
        """index all documents in a folder""" 
        folderPath = Path(folderPath)

        documents = []
        metadatas = []
        ids = []

        for filePath in folderPath.rglob("*"): 

            if filePath.is_file() and filePath.suffix.lower() in ['.txt', '.md']: 
                text = self.extractText(filePath) 

                if text:
                    chunks = self.chunkText(text) 
    
                    for i, chunk in enumerate(chunks):
                        #after enumerating chunk 
                        chunkId = hashlib.md5(f"{filePath}_{i}".encode()).hexdigest()
                        documents.append(chunk)
                        metadatas.append({
                            "filePath": str(filePath),
                            "id": chunkId,
                            "filename": filePath.name})
                        ids.append(chunkId)
        if documents:
            print(f"adding {len(documents)} to db")
            self.collection.add(
                    documents = documents,
                    metadatas = metadatas,
                    ids = ids)
            print("indexing complete") 
        else: 
            print("problem with indexing")


            
                
if __name__ == "__main__": 
    
    indexer = DocIndexer()
    documentFolder = input("enter path to folder")
    indexer.IndexDocs(documentFolder)

    




