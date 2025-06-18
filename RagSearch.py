import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from datetime import datetime
from search import DocumentSearcher
from dotenv import load_dotenv

class RagSearcher(DocumentSearcher):

    load_dotenv()

    
    def __init__(self, db_path = "./chroma_db", openai_api_key =None): 
        super().__init__(db_path)
        
        if openai_api_key: 
            OpenAI.api_key = openai_api_key
        else: 
            pass
        
    
    def answerQuestion(self, question, context_chunks = 5, model = "gpt-3.5-turbo"): 
        
        try: 
            print("searching for relevant documents")
            search_results = self.search(question, context_chunks)
            
            if not search_results['documents'][0]: 
                return{
                    "answer": "I couldnt find any relevant answers", 
                    "sources": [],
                    "confidence": "low"
                }     
                
            content_docs = search_results['documents'][0]
            source_files = [meta['filename'] for meta in search_results['metadatas'] [0]]
            
            context = ""
            for i, doc in enumerate(content_docs):
                context += f"Doument {i + 1} ({source_files[i]}): \n{doc}\n \n"
                
            system_prompt = """You are a helpful assistant that answers questions based on provided document context. 
            
            Rules:
            1. Only answer based on the provided context
            2. If the context doesn't contain enough information, say so
            3. Cite which documents you're referencing
            4. Be concise but thorough
            5. If you're uncertain, express that uncertainty"""

            user_prompt = f"""Based on the following documents, please answer this question:

Question: {question}

Context from documents:
{context}

Please provide a clear answer based on the information in these documents."""

            print("Generating answer using ChatGPT...")
            client = OpenAI(api_key = OpenAI.api_key)
            response = client.chat.completions.create(
                model = model, 
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens = 500, 
                temperature = 0.3
            )
            
            answer = response.choices[0].message.content            
            return {
                "answer": answer, 
                "sources": source_files,
                "context_chunks": len(content_docs),
                "confidence": "high" if len(content_docs) >= 3 else "medium",
                "timestamp": datetime.now().isoformat()
            }
            
            
            
        except Exception as e: 
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": [],
                "confidence": "error"
            }
        
    def display_answer(self, answer_result):
        """Display the Q&A result in a nice format"""
        print("\n" + "="*80)
        print("ANSWER:")
        print("="*80)
        print(answer_result["answer"])
        print("\n" + "-"*80)
        print("SOURCES:")
        print("-"*80)
        
        if answer_result["sources"]:
            for i, source in enumerate(answer_result["sources"], 1):
                print(f"{i}. {source}")
        else:
            print("No sources found")
            
        print(f"\nConfidence: {answer_result['confidence']}")
        print(f"Context chunks used: {answer_result.get('context_chunks', 0)}")
        print("="*80 + "\n")
                 
                 
if __name__ == "__main__": 
    
    import os
     
    api_key = os.getenv('OPENAI_API_KEY')   
    
    if not api_key: 
        api_key = input("enter apikey").strip()
    
    print("qna document system") 
    searcher = RagSearcher(openai_api_key=api_key)
    
    while True: 
        question = input("ask a question or quit").strip()
        
        if question: 
            answerResult = searcher.answerQuestion(question)
            searcher.display_answer(answerResult) 

    
        
        

