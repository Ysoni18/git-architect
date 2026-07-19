from langchain_ollama import OllamaLLM

# Initialize using the modern LangChain-Ollama integration class
llm = OllamaLLM(model="llama3")

print("Sending a test ping to local Llama 3...")
response = llm.invoke("Say the word 'Systems Operational' and nothing else.")
print(f"Response: {response}")