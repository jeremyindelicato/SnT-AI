"""
FinancialAgent - Core agent for Start&Trade using Ollama
"""
import logging
from typing import Dict, List, Optional
import ollama
from .config import settings
from .prompts import get_system_prompt

logger = logging.getLogger(__name__)


class FinancialAgent:
    """
    Financial Agent that communicates with Ollama (Phi 3.5) and manages
    tool calling for market data retrieval.
    """

    def __init__(self):
        self.model = settings.ollama_model
        self.ollama_host = settings.ollama_host
        self.conversation_history: List[Dict] = []
        self.system_prompt = get_system_prompt()

        logger.info(
            f"FinancialAgent initialized with model: {self.model} at {self.ollama_host}"
        )

    def _initialize_conversation(self) -> None:
        """Initialize conversation with system prompt"""
        if not self.conversation_history:
            self.conversation_history.append(
                {"role": "system", "content": self.system_prompt}
            )

    async def chat(self, user_message: str) -> Dict:
        """
        Process user message and generate response using Ollama.

        Args:
            user_message: The user's input message

        Returns:
            Dict containing the assistant's response and metadata
        """
        try:
            self._initialize_conversation()

            # Add user message to conversation history
            self.conversation_history.append(
                {"role": "user", "content": user_message}
            )

            logger.info(f"Processing message: {user_message[:100]}...")

            # Call Ollama
            response = ollama.chat(
                model=self.model, messages=self.conversation_history
            )

            assistant_message = response["message"]["content"]

            # Add assistant response to conversation history
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            logger.info("Response generated successfully")

            return {
                "success": True,
                "response": assistant_message,
                "model": self.model,
                "conversation_length": len(self.conversation_history),
            }

        except ollama.ResponseError as e:
            logger.error(f"Ollama API error: {str(e)}")
            return {
                "success": False,
                "error": f"Ollama API error: {str(e)}",
                "response": "Désolé, je rencontre un problème technique. Assurez-vous qu'Ollama est lancé avec le modèle phi3.5.",
            }

        except Exception as e:
            logger.error(f"Unexpected error in chat: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": "Désolé, une erreur inattendue s'est produite.",
            }

    def reset_conversation(self) -> None:
        """Reset conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history reset")

    def get_conversation_history(self) -> List[Dict]:
        """Get current conversation history"""
        return self.conversation_history.copy()
