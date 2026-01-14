"""
FinancialAgent - Core agent for Start&Trade using Ollama
"""
import logging
import re
from typing import Dict, List, Optional
import ollama
import httpx
from .config import settings
from .prompts import get_system_prompt

logger = logging.getLogger(__name__)


class FinancialAgent:
    """
    Financial Agent that communicates with Ollama (Phi 3.5) and manages
    tool calling for market data retrieval.
    """

    # Mapping entreprises → tickers (noms français et anglais)
    TICKER_MAPPINGS = {
        # US Tech Giants
        "apple": "AAPL",
        "microsoft": "MSFT",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "amazon": "AMZN",
        "tesla": "TSLA",
        "meta": "META",
        "facebook": "META",
        "nvidia": "NVDA",
        "amd": "AMD",
        "intel": "INTC",
        "netflix": "NFLX",
        "adobe": "ADBE",

        # Marché français (Paris - .PA)
        "air liquide": "AI.PA",
        "airbus": "AIR.PA",
        "bnp": "BNP.PA",
        "bnp paribas": "BNP.PA",
        "lvmh": "MC.PA",
        "louis vuitton": "MC.PA",
        "total": "TTE.PA",
        "totalenergies": "TTE.PA",
        "sanofi": "SAN.PA",
        "l'oréal": "OR.PA",
        "loreal": "OR.PA",
        "oréal": "OR.PA",
        "orange": "ORA.PA",
        "renault": "RNO.PA",
        "peugeot": "UG.PA",
        "stellantis": "STLAM.PA",
        "vinci": "DG.PA",
        "danone": "BN.PA",
        "saint-gobain": "SGO.PA",
        "saint gobain": "SGO.PA",
        "schneider": "SU.PA",
        "schneider electric": "SU.PA",
        "safran": "SAF.PA",
        "bouygues": "EN.PA",
        "carrefour": "CA.PA",
        "legrand": "LR.PA",
        "michelin": "ML.PA",
        "veolia": "VIE.PA",
        "thales": "HO.PA",
        "stmicroelectronics": "STM.PA",
        "st micro": "STM.PA",
        "stm": "STM.PA",
        "publicis": "PUB.PA",
        "hermes": "RMS.PA",
        "hermès": "RMS.PA",
        "kering": "KER.PA",
        "essilorluxottica": "EL.PA",
        "essilor": "EL.PA",
        "accor": "AC.PA",
        "axa": "CS.PA",
        "société générale": "GLE.PA",
        "societe generale": "GLE.PA",
        "sg": "GLE.PA",
        "crédit agricole": "ACA.PA",
        "credit agricole": "ACA.PA",
        "engie": "ENGI.PA",
        "alstom": "ALO.PA",

        # ETF US populaires
        "spy": "SPY",
        "s&p 500": "SPY",
        "sp 500": "SPY",
        "sp500": "SPY",
        "s&p500": "SPY",
        "spdr s&p": "SPY",
        "qqq": "QQQ",
        "nasdaq 100": "QQQ",
        "nasdaq100": "QQQ",
        "invesco nasdaq": "QQQ",
        "vti": "VTI",
        "vanguard total": "VTI",
        "vanguard total market": "VTI",
        "voo": "VOO",
        "vanguard s&p": "VOO",
        "vanguard s&p 500": "VOO",
        "dia": "DIA",
        "dow jones": "DIA",
        "dow 30": "DIA",
        "iwm": "IWM",
        "russell 2000": "IWM",
        "vea": "VEA",
        "vanguard developed": "VEA",
        "vwo": "VWO",
        "vanguard emerging": "VWO",
        "emergent": "VWO",

        # ETF Européens (UCITS) - Euronext Amsterdam
        "iwda": "IWDA.AS",
        "ishares world": "IWDA.AS",
        "msci world": "IWDA.AS",
        "ishares msci world": "IWDA.AS",
        "vwce": "VWCE.DE",
        "vanguard all world": "VWCE.DE",
        "vanguard ftse all": "VWCE.DE",
        "all world": "VWCE.DE",

        # ETF Européens - Euronext Paris
        "cw8": "CW8.PA",
        "amundi msci world": "CW8.PA",
        "lyxor msci world": "EWLD.PA",
        "ewld": "EWLD.PA",
        "lyxor sp500": "SP5.PA",
        "sp5": "SP5.PA",
    }

    def __init__(self):
        self.model = settings.ollama_model
        self.ollama_host = settings.ollama_host
        self.mcp_url = settings.mcp_server_url
        self.conversation_history: List[Dict] = []
        self.system_prompt = get_system_prompt()
        self.http_client = httpx.Client(timeout=30.0)

        logger.info(
            f"FinancialAgent initialized with model: {self.model} at {self.ollama_host}"
        )
        logger.info(f"MCP Server URL: {self.mcp_url}")

    def _initialize_conversation(self) -> None:
        """Initialize conversation with system prompt"""
        if not self.conversation_history:
            self.conversation_history.append(
                {"role": "system", "content": self.system_prompt}
            )

    def _extract_ticker(self, message: str) -> Optional[str]:
        """
        Extrait un ticker du message utilisateur avec mapping intelligent.
        Détecte les noms d'entreprises (Apple → AAPL) et les tickers directs.

        Args:
            message: Message utilisateur

        Returns:
            Ticker trouvé ou None
        """
        message_lower = message.lower()

        # 1. Chercher mapping nom → ticker (PRIORITAIRE)
        # On cherche les noms les plus longs d'abord pour éviter les faux positifs
        sorted_mappings = sorted(
            self.TICKER_MAPPINGS.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        for name, ticker in sorted_mappings:
            if name in message_lower:
                logger.info(f"Ticker détecté via mapping: '{name}' → {ticker}")
                return ticker

        # 2. Fallback : chercher pattern ticker direct (AAPL, MSFT.PA, etc.)
        pattern = r'\b([A-Z]{1,5}(?:\.[A-Z]{1,2})?)\b'
        matches = re.findall(message, pattern)

        # Filtrer les faux positifs courants
        excluded = {"USA", "EUR", "USD", "ETF", "AI", "IA", "CEO", "CFO", "IPO", "NYSE", "API", "PDF"}
        valid_tickers = [m for m in matches if m not in excluded]

        if valid_tickers:
            ticker = valid_tickers[0]
            logger.info(f"Ticker détecté via regex: {ticker}")
            return ticker

        return None

    def call_mcp_tool(self, tool_name: str, parameters: dict) -> dict:
        """
        Appelle un tool via le MCP server.

        Args:
            tool_name: Nom du tool à appeler
            parameters: Paramètres du tool

        Returns:
            Résultat du tool
        """
        try:
            logger.info(f"Calling MCP tool: {tool_name} with parameters: {parameters}")

            response = self.http_client.post(
                f"{self.mcp_url}/tools/execute",
                json={"tool_name": tool_name, "parameters": parameters}
            )
            response.raise_for_status()
            result = response.json()

            logger.info(f"MCP tool result: success={result.get('success')}")
            return result

        except httpx.ConnectError:
            logger.error("MCP server is offline")
            return {
                "success": False,
                "context": "Le serveur MCP n'est pas disponible. Assurez-vous qu'il est lancé sur le port 8001."
            }
        except httpx.HTTPStatusError as e:
            logger.error(f"MCP HTTP error: {e.response.status_code}")
            return {
                "success": False,
                "context": f"Erreur HTTP du serveur MCP: {e.response.status_code}"
            }
        except Exception as e:
            logger.error(f"MCP tool call failed: {str(e)}")
            return {
                "success": False,
                "context": f"Erreur lors de l'appel du tool MCP: {str(e)}"
            }

    async def chat(self, user_message: str) -> Dict:
        """
        Process user message and generate response using Ollama.
        Détecte automatiquement les demandes de données financières et appelle le MCP.

        Args:
            user_message: The user's input message

        Returns:
            Dict containing the assistant's response and metadata
        """
        try:
            self._initialize_conversation()

            # Détection de ticker via regex simple (Phase 2)
            # Sera amélioré en Phase 3 avec mapping intelligent
            ticker_detected = self._extract_ticker(user_message)

            if ticker_detected:
                logger.info(f"Ticker détecté dans le message: {ticker_detected}")

                # Appel du MCP tool
                tool_result = self.call_mcp_tool("get_market_data", {"ticker": ticker_detected})
                logger.info(f"Résultat MCP brut: {tool_result}")

                # Injection des données dans le contexte système
                if tool_result.get("success"):
                    # Le contexte est dans tool_result['result']['context']
                    result_data = tool_result.get("result", {})
                    context_data = result_data.get("context", "Données non disponibles")

                    context_message = (
                        f"[DONNÉES FINANCIÈRES EN TEMPS RÉEL]\n"
                        f"{context_data}\n\n"
                        f"Utilise ces informations pour répondre à la question de l'utilisateur "
                        f"de manière pédagogique et contextuelle."
                    )

                    self.conversation_history.append({
                        "role": "system",
                        "content": context_message
                    })
                    logger.info(f"Contexte financier injecté pour {ticker_detected}")
                    logger.debug(f"Contexte injecté:\n{context_message}")
                else:
                    # En cas d'erreur, on informe le modèle
                    error_context = (
                        f"[INFORMATION] Impossible de récupérer les données pour {ticker_detected}. "
                        f"Explique à l'utilisateur que les données ne sont pas disponibles actuellement."
                    )
                    self.conversation_history.append({
                        "role": "system",
                        "content": error_context
                    })
                    logger.warning(f"Échec récupération données pour {ticker_detected}")

            # Add user message to conversation history
            self.conversation_history.append(
                {"role": "user", "content": user_message}
            )

            logger.info(f"Processing message: {user_message[:100]}...")

            # DEBUG: Afficher la taille de l'historique
            total_chars = sum(len(msg['content']) for msg in self.conversation_history)
            logger.info(f"Sending {len(self.conversation_history)} messages to Ollama (~{total_chars} chars)")

            # Afficher le dernier message système (avec données financières) si présent
            system_messages = [msg for msg in self.conversation_history if msg['role'] == 'system']
            if len(system_messages) > 1:  # Plus que le system prompt initial
                last_system = system_messages[-1]
                logger.info(f"Latest system message (financial data): {last_system['content'][:300]}...")

            # Call Ollama avec contexte enrichi
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
