#!/usr/bin/env python3
"""
Quick start script for personal document search
"""
import os
import sys
from pathlib import Path

def main():
    print("=== Personal Document Search Engine ===\n")
    
    # Check if database exists
    if not Path("./chroma_db").exists():
        print("No search database found. Let's create one!")
        
        from indexer import DocIndexer
        
        while True:
            folder_path = input("Enter the path to your documents folder: ").strip()
            if Path(folder_path).exists():
                break
            print("Folder not found. Please try again.")
        
        print("\nIndexing documents...")
        indexer = DocIndexer()
        indexer.IndexDocs(folder_path)
        print("Done!\n")
    
    # Start search interface
    from search import DocumentSearcher
    
    searcher = DocumentSearcher()
    
    print("Search your documents! Type 'quit' to exit.\n")
    
    while True:
        try:
            query = input("Search: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if query:
                results = searcher.search(query)
                searcher.displayResults(results)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print("here")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()