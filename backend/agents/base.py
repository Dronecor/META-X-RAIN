from typing import List, Dict, Any, Optional
from backend.llm.groq_client import get_groq_client
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.llm = get_groq_client()
        self.memory = [] # Simple in-memory list for now, should use DB in prod

    async def run(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """
        Main execution method for the agent.
        """
        # Construct messages
        messages = [
            SystemMessage(content=self.system_prompt)
        ]
        
        # Add context if provided (simplified)
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            messages.append(SystemMessage(content=f"Context:\n{context_str}"))

        # Add specific history (omitted for brevity, would load from DB)
        
        # Add user input
        messages.append(HumanMessage(content=user_input))

        # Invoke LLM
        response = self.llm.invoke(messages)
        
        return response.content
