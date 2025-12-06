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

    async def run(self, user_input: str, user_id: str = "guest", user_details: Dict[str, Any] = None, context: Dict[str, Any] = None) -> str:
        """
        Main execution method for the agent.
        """
        from backend.services.chat_history import chat_history
        
        # 1. Retrieve Memory (Summary + Recent)
        full_name = user_details.get("full_name") if user_details else None
        email = user_details.get("email") if user_details else None
        
        memory_ctx = chat_history.get_context(user_id, full_name=full_name, email=email)
        
        # 2. Construct Prompt
        messages = [
            SystemMessage(content=self.system_prompt)
        ]
        
        # Inject Memory Summary
        if memory_ctx.get("summary"):
            messages.append(SystemMessage(content=f"MEMORY SUMMARY (Previous Context):\n{memory_ctx['summary']}"))
            
        # Inject Recent History (Last 10 turns)
        for msg in memory_ctx.get("history", []):
            if msg["sender"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["sender"] == "agent":
                messages.append(AIMessage(content=msg["content"]))

        # Add generic context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            messages.append(SystemMessage(content=f"Current Context:\n{context_str}"))

        # Add current user input
        messages.append(HumanMessage(content=user_input))

        # 3. Invoke LLM
        response = self.llm.invoke(messages)
        agent_resp = response.content
        
        # 4. Save Interaction (and trigger async summarization)
        chat_history.save_interaction(user_id, user_input, agent_resp)
        
        return agent_resp
