import json
import sys
import os

# Add the current directory to the path so it can find ai_agent.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_agent import process_prompt

def run_test():
    print("\n==================================================")
    print("🤖 Interactive AI Backend Tester")
    print("Type 'exit' or 'quit' to stop.")
    print("==================================================\n")
    
    current_data = {}
    
    while True:
        test_text = input("Enter your custom complaint prompt: ")
        
        if test_text.strip().lower() in ['exit', 'quit']:
            print("Exiting test...")
            break
            
        if not test_text.strip():
            continue
        
        print("\nWaiting for AI response... (this may take a few seconds)")
    
        try:
            result = process_prompt(test_text, current_data)
            current_data = result["data"]  # Save the state for the next turn!
            
            print("\n✅ AI processing complete!\n")
            print("--- AI Chat Reply ---")
            print(result["reply"])
            
            print("\n--- Extracted Complaint Data (Ready for Database) ---")
            # Print the extracted structured data beautifully
            print(json.dumps(result["data"], indent=4))
            print("\n" + "="*50 + "\n")
            
        except Exception as e:

            print(f"\n❌ Error occurred: {e}")
            print("Make sure your GROQ_API_KEY is correctly set in the .env file!")
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    run_test()
