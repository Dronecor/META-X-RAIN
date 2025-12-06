import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv("backend/.env")

key = os.getenv("GROQ_API_KEY")
print(f"Key present: {bool(key)}")
# print(f"Key: {key}") # Don't print secret

try:
    llm = ChatGroq(groq_api_key=key, model_name="llama3-70b-8192")
    msg = HumanMessage(content="Hello")
    res = llm.invoke([msg])
    print("Success!")
    print(res.content)
except Exception as e:
    print("Error:")
    print(e)
