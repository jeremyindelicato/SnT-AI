/**
 * API Service - Communication avec le backend Start&Trade
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 secondes pour les requêtes longues
});

/**
 * Service API pour Start&Trade
 */
export const startAndTradeAPI = {
  /**
   * Envoyer un message au chatbot
   * @param {string} message - Message de l'utilisateur
   * @param {string} sessionId - ID de session optionnel
   * @returns {Promise} Réponse de l'IA
   */
  sendMessage: async (message, sessionId = null) => {
    try {
      const response = await api.post('/chat', {
        message,
        session_id: sessionId,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw {
        success: false,
        error: error.response?.data?.detail || error.message || 'Erreur de connexion',
        response: 'Désolé, je ne peux pas répondre pour le moment. Vérifiez que le backend est lancé.',
      };
    }
  },

  /**
   * Vérifier l'état de santé du backend
   * @returns {Promise} Statut du système
   */
  checkHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      return {
        status: 'offline',
        ollama_connected: false,
      };
    }
  },

  /**
   * Réinitialiser la conversation
   * @returns {Promise} Confirmation de réinitialisation
   */
  resetConversation: async () => {
    try {
      const response = await api.post('/chat/reset');
      return response.data;
    } catch (error) {
      console.error('Error resetting conversation:', error);
      throw error;
    }
  },

  /**
   * Obtenir l'historique de conversation
   * @returns {Promise} Historique des messages
   */
  getHistory: async () => {
    try {
      const response = await api.get('/chat/history');
      return response.data;
    } catch (error) {
      console.error('Error fetching history:', error);
      throw error;
    }
  },
};

export default startAndTradeAPI;
