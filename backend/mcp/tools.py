"""
MCP Tools Definition - Financial data retrieval tools
"""
import logging
import sys
import os
from typing import Dict, Optional
from datetime import datetime

# Ajouter le répertoire parent au path pour importer scraping_yfinance
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraping.scraping_yfinance import get_market_data as scrape_market_data

logger = logging.getLogger(__name__)


def format_market_data_for_context(data: dict) -> str:
    """
    Formate les données pour injection dans le contexte du modèle (style conversationnel).

    Args:
        data: Données brutes du scraper

    Returns:
        Texte formaté pour le modèle LLM
    """
    if data.get("error"):
        return f"Erreur : {data['error']}"

    # Format SIMPLE et FACTUEL pour que le modèle puisse l'utiliser naturellement
    symbol = data.get("symbol", "N/A")
    name = data.get("name", "N/A")
    price = data.get("price", "N/A")
    change = data.get("change", "N/A")
    percent = data.get("percent_change", "N/A")

    # En-tête avec informations principales
    response = f"{name} ({symbol})\n"
    response += f"Prix actuel : {price}\n"
    response += f"Variation du jour : {change} ({percent})\n\n"

    # Ajouter toutes les métriques pertinentes si disponibles
    if "details" in data:
        details = data["details"]

        # Organisation par catégories pour un contexte structuré
        categories = {
            "📊 Marché aujourd'hui": [
                "Ouverture", "Plus haut du jour", "Plus bas du jour",
                "Plage du jour", "Clôture précédente", "Volume", "Volume moyen"
            ],
            "📈 Performance": [
                "Plage sur 52 semaines", "Plus haut 52 semaines", "Plus bas 52 semaines",
                "Bêta (volatilité)", "Prix cible moyen"
            ],
            "💰 Valorisation": [
                "Capitalisation boursière", "Ratio C/B (P/E)", "Ratio C/B prévisionnel",
                "Ratio prix/valeur comptable", "Valeur d'entreprise"
            ],
            "💵 Dividendes": [
                "Rendement du dividende", "Dividende annuel", "Date ex-dividende",
                "Taux de distribution"
            ],
            "📉 Bénéfices": [
                "BPA (12 derniers mois)", "BPA prévisionnel", "Revenu par action",
                "Marge bénéficiaire", "Marge opérationnelle"
            ],
            "🏦 Santé financière": [
                "Retour sur actifs (ROA)", "Retour sur capitaux propres (ROE)",
                "Ratio dette/capitaux propres", "Ratio de liquidité"
            ]
        }

        for category, keys in categories.items():
            category_data = []
            for key in keys:
                if key in details and details[key]:
                    category_data.append(f"  • {key} : {details[key]}")

            if category_data:
                response += f"{category}\n"
                response += "\n".join(category_data) + "\n\n"

    return response.strip()


class MarketDataTool:
    """
    Tool for retrieving market data from Yahoo Finance via Python scraper.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize the MarketDataTool

        Args:
            webhook_url: (Deprecated) Not used anymore, kept for compatibility
        """
        logger.info("MarketDataTool initialized with Python scraper")

    def get_market_data(self, ticker: str) -> Dict:
        """
        Retrieve market data for a given stock ticker from Yahoo Finance.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT', 'AI.PA')

        Returns:
            Dict containing:
                - success (bool): Whether the scraping succeeded
                - context (str): Formatted data for LLM context
                - raw_data (dict): Raw scraped data for reference
        """
        logger.info(f"[MCP TOOL CALL] get_market_data invoked for ticker: {ticker}")

        # Validate ticker format
        if not ticker or not isinstance(ticker, str):
            logger.error("Invalid ticker provided")
            return {
                "success": False,
                "context": "Format de ticker invalide.",
            }

        try:
            # Appel du scraper Python
            logger.info(f"Scraping Yahoo Finance for {ticker}...")
            raw_data = scrape_market_data(ticker)

            # Vérifier si le scraping a retourné une erreur
            if raw_data.get("error"):
                error_msg = raw_data["error"]
                logger.warning(f"Scraping error for {ticker}: {error_msg}")

                # Messages d'erreur plus explicites
                if "not found" in error_msg.lower() or "404" in error_msg.lower():
                    context = f"Le ticker '{ticker}' est introuvable sur Yahoo Finance. Vérifiez l'orthographe ou ajoutez le suffixe de marché (ex: .PA pour Paris, .L pour Londres)."
                else:
                    context = f"Impossible de récupérer les données pour {ticker}. Erreur : {error_msg}"

                return {
                    "success": False,
                    "context": context,
                }

            # Formatage simple pour injection dans le contexte du modèle
            formatted_context = format_market_data_for_context(raw_data)

            logger.info(f"Successfully scraped data for {ticker}")

            # Le modèle recevra ces données et les intégrera naturellement
            return {
                "success": True,
                "context": formatted_context,  # Données pour le modèle
                "raw_data": raw_data,          # Données brutes pour référence
            }

        except Exception as e:
            logger.error(f"Unexpected error scraping {ticker}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "context": f"Erreur inattendue lors de la récupération des données pour {ticker}. Veuillez réessayer.",
            }

    def get_tool_definition(self) -> Dict:
        """
        Return the tool definition in MCP format.

        Returns:
            Dict describing the tool for LLM integration
        """
        return {
            "type": "function",
            "function": {
                "name": "get_market_data",
                "description": "Retrieve real-time market data for a stock ticker from Yahoo Finance. Use this when the user asks about current stock prices, market trends, or financial data for a specific company.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock ticker symbol (e.g., 'AAPL' for Apple, 'TSLA' for Tesla, 'MSFT' for Microsoft, 'AI.PA' for Air Liquide Paris)",
                        }
                    },
                    "required": ["ticker"],
                },
            },
        }


# Global tool instance
market_data_tool = MarketDataTool()
