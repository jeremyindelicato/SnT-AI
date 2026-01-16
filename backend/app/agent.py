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
from .router import QueryRouter
from .knowledge_base import KnowledgeBase

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

        # Indices Boursiers Mondiaux
        "cac 40": "^FCHI",
        "cac40": "^FCHI",
        "cac": "^FCHI",
        "s&p 500 index": "^GSPC",
        "sp500 index": "^GSPC",
        "indice s&p": "^GSPC",
        "dow jones index": "^DJI",
        "dow jones industrial": "^DJI",
        "dow 30 index": "^DJI",
        "nasdaq composite": "^IXIC",
        "nasdaq index": "^IXIC",
        "dax": "^GDAXI",
        "dax 40": "^GDAXI",
        "ftse 100": "^FTSE",
        "ftse": "^FTSE",
        "nikkei": "^N225",
        "nikkei 225": "^N225",
        "euro stoxx 50": "^STOXX50E",
        "eurostoxx": "^STOXX50E",

        # Crypto-monnaies (Top 15 par capitalisation)
        "bitcoin": "BTC-USD",
        "btc": "BTC-USD",
        "ethereum": "ETH-USD",
        "eth": "ETH-USD",
        "ether": "ETH-USD",
        "binance coin": "BNB-USD",
        "bnb": "BNB-USD",
        "cardano": "ADA-USD",
        "ada": "ADA-USD",
        "solana": "SOL-USD",
        "sol": "SOL-USD",
        "xrp": "XRP-USD",
        "ripple": "XRP-USD",
        "polkadot": "DOT-USD",
        "dot": "DOT-USD",
        "dogecoin": "DOGE-USD",
        "doge": "DOGE-USD",
        "avalanche": "AVAX-USD",
        "avax": "AVAX-USD",
        "polygon": "MATIC-USD",
        "matic": "MATIC-USD",
        "chainlink": "LINK-USD",
        "link": "LINK-USD",
        "litecoin": "LTC-USD",
        "ltc": "LTC-USD",
    }

    def __init__(self):
        self.model = settings.ollama_model
        self.ollama_host = settings.ollama_host
        self.mcp_url = settings.mcp_server_url
        self.conversation_history: List[Dict] = []
        self.system_prompt = get_system_prompt()
        self.http_client = httpx.Client(timeout=30.0)

        # Initialize router and knowledge base
        self.router = QueryRouter()
        self.knowledge_base = KnowledgeBase()

        logger.info(
            f"FinancialAgent initialized with model: {self.model} at {self.ollama_host}"
        )
        logger.info(f"MCP Server URL: {self.mcp_url}")
        logger.info("Router and Knowledge Base initialized")

    def _initialize_conversation(self) -> None:
        """
        Initialize conversation with system prompt.
        Always ensures system prompt is at the beginning and up-to-date.

        CRITICAL FIX: Reinjects system prompt at every request to prevent
        identity hallucination when context accumulates over multiple turns.
        """
        # If conversation is empty, add system prompt
        if not self.conversation_history:
            self.conversation_history.append(
                {"role": "system", "content": self.system_prompt}
            )
            logger.debug("System prompt initialized (first message)")
        else:
            # CRITICAL: Always refresh system prompt to prevent identity drift
            # When knowledge base and scraping context accumulate, the initial
            # system prompt gets "buried" and the model forgets its identity
            if self.conversation_history[0]["role"] == "system":
                self.conversation_history[0]["content"] = self.system_prompt
                logger.debug("System prompt refreshed (identity reinforcement)")
            else:
                # Shouldn't happen, but insert if missing
                self.conversation_history.insert(0,
                    {"role": "system", "content": self.system_prompt}
                )
                logger.warning("System prompt was missing, reinserted")

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
        Uses intelligent routing to determine data sources (scraping/KB/LLM).

        Args:
            user_message: The user's input message

        Returns:
            Dict containing the assistant's response and metadata
        """
        try:
            self._initialize_conversation()

            # Step 1: Detect ticker
            ticker_detected = self._extract_ticker(user_message)

            # Step 2: Route query based on intent scoring
            route, scores = self.router.route_query(user_message, bool(ticker_detected))
            route_description = self.router.get_route_description(route)

            logger.info("="*60)
            logger.info(f"🎯 ROUTING DECISION: {route.upper()}")
            logger.info(f"📊 Description: {route_description}")
            logger.info(f"📈 Scores: {scores}")
            logger.info(f"🎫 Ticker detected: {ticker_detected if ticker_detected else 'None'}")
            logger.info("="*60)

            # Track data sources used for this response
            sources_used = []

            # Step 3: Handle routing based on strategy
            # CRITICAL FIX: Consolidate ALL context into a SINGLE system message
            # to avoid overwhelming the 7B model with multiple system messages
            additional_context = ""

            if route == "scraping":
                # Pure scraping: get real-time data only
                if ticker_detected:
                    sources_used.append("scraping")
                    tool_result = self.call_mcp_tool("get_market_data", {"ticker": ticker_detected})

                    if tool_result.get("success"):
                        result_data = tool_result.get("result", {})
                        context_data = result_data.get("context", "Données non disponibles")

                        additional_context = (
                            f"\n\n{'='*60}\n"
                            f"⚠️ INSTRUCTION CRITIQUE - UTILISE UNIQUEMENT CES DONNÉES ⚠️\n"
                            f"{'='*60}\n\n"
                            f"[DONNÉES FINANCIÈRES EN TEMPS RÉEL]\n"
                            f"{context_data}\n\n"
                            f"🚨 RÈGLE ABSOLUE : Tu DOIS utiliser EXACTEMENT les chiffres ci-dessus.\n"
                            f"❌ N'INVENTE AUCUN prix, variation, ou métrique.\n"
                            f"✅ Réponds en citant UNIQUEMENT les données fournies ci-dessus.\n"
                            f"{'='*60}"
                        )

                        logger.info(f"✅ Scraping: Données préparées pour {ticker_detected}")
                    else:
                        additional_context = (
                            f"\n\n[INFORMATION] Impossible de récupérer les données pour {ticker_detected}. "
                            f"Explique à l'utilisateur que les données ne sont pas disponibles actuellement."
                        )
                        logger.warning(f"❌ Scraping: Échec pour {ticker_detected}")

            elif route == "knowledge":
                # Pure knowledge base: educational content only
                sources_used.append("knowledge_base")
                kb_context = self.knowledge_base.build_context_message(user_message)

                if kb_context:
                    additional_context = f"\n\n{kb_context}"
                    logger.info(f"✅ Knowledge Base: {len(kb_context)} chars préparés")
                else:
                    logger.info("⚠️ Knowledge Base: Aucun contenu pertinent trouvé")

            elif route == "hybrid":
                # Hybrid: scraping + knowledge base
                sources_used.append("scraping")
                sources_used.append("knowledge_base")

                # 1. Get real-time data if ticker present
                if ticker_detected:
                    tool_result = self.call_mcp_tool("get_market_data", {"ticker": ticker_detected})

                    if tool_result.get("success"):
                        result_data = tool_result.get("result", {})
                        context_data = result_data.get("context", "Données non disponibles")

                        scraping_part = (
                            f"{'='*60}\n"
                            f"⚠️ INSTRUCTION CRITIQUE - UTILISE UNIQUEMENT CES DONNÉES ⚠️\n"
                            f"{'='*60}\n\n"
                            f"[DONNÉES FINANCIÈRES EN TEMPS RÉEL]\n"
                            f"{context_data}\n\n"
                            f"🚨 RÈGLE ABSOLUE : Tu DOIS utiliser EXACTEMENT les chiffres ci-dessus.\n"
                            f"❌ N'INVENTE AUCUN prix, variation, ou métrique.\n"
                            f"✅ Réponds en citant UNIQUEMENT les données fournies ci-dessus.\n"
                            f"{'='*60}"
                        )

                        additional_context += f"\n\n{scraping_part}"
                        logger.info(f"✅ Hybrid - Scraping: Données préparées pour {ticker_detected}")

                # 2. Add educational context from KB
                kb_context = self.knowledge_base.build_context_message(
                    user_message,
                    ticker=ticker_detected
                )

                if kb_context:
                    additional_context += f"\n\n{kb_context}"
                    logger.info(f"✅ Hybrid - Knowledge Base: {len(kb_context)} chars préparés")

            elif route == "conversational":
                # Pure LLM: no external data needed
                sources_used.append("llm_only")
                logger.info("💬 Conversational: Réponse LLM uniquement (pas de sources externes)")

                # CRITICAL FIX: Detect identity questions and add reminder to context
                identity_keywords = ["qui es-tu", "qui es tu", "c'est qui", "ton nom", "tu t'appelles",
                                    "ton identité", "qui t'a créé", "qui a créé", "qui ta créé"]
                if any(keyword in user_message.lower() for keyword in identity_keywords):
                    identity_reminder = (
                        "\n\n[RAPPEL IDENTITÉ]\n"
                        "Tu es Start&Trade, un assistant financier intelligent alimenté par Qwen2.5. "
                        "Tu accompagnes les jeunes investisseurs dans leur apprentissage des marchés financiers."
                    )
                    additional_context += identity_reminder
                    logger.info("🆔 Identity question detected → Identity reminder prepared")

            else:
                # Fallback to conversational
                sources_used.append("llm_only")
                logger.warning(f"⚠️ Route inconnue '{route}', fallback sur conversational")

            # CRITICAL FIX: Consolidate all additional context into the SINGLE system message
            # This prevents the 7B model from getting confused by multiple system messages

            # First, clean up any old system messages that might have accumulated (keep only [0])
            cleaned_history = [self.conversation_history[0]]  # Keep system prompt
            for msg in self.conversation_history[1:]:
                if msg['role'] != 'system':  # Remove all other system messages
                    cleaned_history.append(msg)

            if len(cleaned_history) < len(self.conversation_history):
                removed = len(self.conversation_history) - len(cleaned_history)
                logger.info(f"🧹 Cleaned up {removed} old system message(s)")
                self.conversation_history = cleaned_history

            # PERFORMANCE FIX: Prevent context from growing too large for 7B model
            # Keep: system prompt [0] + last N conversation turns (user + assistant pairs)
            MAX_CONVERSATION_PAIRS = 5  # Keep last 5 user-assistant pairs (10 messages)
            if len(self.conversation_history) > (1 + MAX_CONVERSATION_PAIRS * 2):
                # Keep system prompt + last N pairs
                old_count = len(self.conversation_history)
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-(MAX_CONVERSATION_PAIRS * 2):]
                logger.info(f"🗑️ Context pruning: removed {old_count - len(self.conversation_history)} old messages")

            # Now consolidate all context into the single system message
            if additional_context:
                # Append additional context to the system prompt at position [0]
                self.conversation_history[0]["content"] = self.system_prompt + additional_context
                logger.info(f"✅ Context consolidé: {len(additional_context)} chars ajoutés au system prompt")
            else:
                logger.info("ℹ️ Pas de contexte additionnel pour cette requête")

            # Add user message to conversation history
            self.conversation_history.append(
                {"role": "user", "content": user_message}
            )

            logger.info(f"Processing message: {user_message[:100]}...")

            # DEBUG: Afficher la taille de l'historique et la structure
            total_chars = sum(len(msg['content']) for msg in self.conversation_history)
            system_count = len([msg for msg in self.conversation_history if msg['role'] == 'system'])
            user_count = len([msg for msg in self.conversation_history if msg['role'] == 'user'])
            assistant_count = len([msg for msg in self.conversation_history if msg['role'] == 'assistant'])

            logger.info(f"📨 Sending to Ollama: {len(self.conversation_history)} messages (~{total_chars} chars)")
            logger.info(f"   Structure: {system_count} system, {user_count} user, {assistant_count} assistant")

            # DEBUG: Vérifier le contenu du message système consolidé
            if self.conversation_history[0]['role'] == 'system':
                system_msg = self.conversation_history[0]['content']
                logger.debug(f"🔍 SYSTEM MESSAGE CONSOLIDÉ ({len(system_msg)} chars)")
                logger.debug(f"   Preview (first 300): {system_msg[:300]}...")
                logger.debug(f"   Preview (last 300): ...{system_msg[-300:]}")

                # Vérifier si les données financières sont présentes
                if "DONNÉES FINANCIÈRES EN TEMPS RÉEL" in system_msg:
                    logger.info("✅ Données financières PRÉSENTES dans le system message consolidé")
                else:
                    logger.info("ℹ️ Pas de données financières dans cette requête")

            # Call Ollama avec contexte enrichi
            response = ollama.chat(
                model=self.model, messages=self.conversation_history
            )

            assistant_message = response["message"]["content"]

            # Add assistant response to conversation history
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            logger.info("="*60)
            logger.info("✅ RESPONSE GENERATED SUCCESSFULLY")
            logger.info(f"📋 Sources used: {', '.join(sources_used)}")
            logger.info(f"🎯 Route: {route}")
            logger.info(f"💬 Response length: {len(assistant_message)} chars")
            logger.info("="*60)

            return {
                "success": True,
                "response": assistant_message,
                "model": self.model,
                "conversation_length": len(self.conversation_history),
                "routing": {
                    "strategy": route,
                    "scores": scores,
                    "sources_used": sources_used,
                    "ticker_detected": ticker_detected
                }
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
