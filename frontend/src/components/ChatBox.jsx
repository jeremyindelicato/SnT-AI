import React, { useState, useEffect, useRef } from 'react';
import { Send, Activity, TrendingUp, Loader2, AlertCircle, RefreshCw } from 'lucide-react';
import GlassCard from './GlassCard';
import startAndTradeAPI from '../services/api';

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(false);
  const messagesEndRef = useRef(null);

  // Vérifier la connexion au backend au démarrage
  useEffect(() => {
    checkBackendHealth();
  }, []);

  // Auto-scroll vers le bas quand nouveaux messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const checkBackendHealth = async () => {
    try {
      const health = await startAndTradeAPI.checkHealth();
      setIsOnline(health.status === 'healthy' && health.ollama_connected);
    } catch (error) {
      setIsOnline(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');

    // Ajouter le message utilisateur
    const newUserMessage = {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      // Envoyer au backend
      const response = await startAndTradeAPI.sendMessage(userMessage);

      // Ajouter la réponse de l'assistant
      const assistantMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        model: response.model,
      };
      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      // Message d'erreur
      const errorMessage = {
        role: 'assistant',
        content: error.response || 'Une erreur est survenue. Assurez-vous que le backend est lancé sur le port 8000.',
        timestamp: new Date().toISOString(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      await startAndTradeAPI.resetConversation();
      setMessages([]);
    } catch (error) {
      console.error('Reset failed:', error);
    }
  };

  return (
    <GlassCard className="p-1 border-primary/20" hover={false}>
      <div className="bg-black/60 rounded-[1.7rem] overflow-hidden">

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-dark-border bg-white/[0.02]">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${isOnline ? 'bg-primary' : 'bg-red-500'} shadow-[0_0_15px] ${isOnline ? 'shadow-primary' : 'shadow-red-500'}`} />
            <span className="text-xs uppercase tracking-wider font-bold">
              Start&Trade Assistant
            </span>
            {!isOnline && (
              <span className="text-[10px] text-red-400">(Backend déconnecté)</span>
            )}
          </div>

          <div className="flex gap-4 items-center">
            <button
              onClick={checkBackendHealth}
              className="text-gray-500 hover:text-primary transition-colors"
              title="Vérifier la connexion"
            >
              <RefreshCw size={14} />
            </button>
            <Activity size={14} className="text-gray-500" />
            <TrendingUp size={14} className="text-primary" />
          </div>
        </div>

        {/* Messages */}
        <div className="h-[500px] overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-primary/20 scrollbar-track-transparent">

          {/* Message de bienvenue */}
          {messages.length === 0 && (
            <div className="flex justify-start">
              <div className="max-w-[80%] p-5 rounded-2xl rounded-tl-none bg-white/5 border border-dark-border text-sm leading-relaxed">
                <p className="mb-3">👋 Bonjour ! Je suis <span className="font-bold text-primary">Start&Trade Assistant</span>, ton conseiller financier pédagogique.</p>
                <p className="text-gray-400 text-xs">
                  Je suis là pour t'accompagner dans tes débuts en investissement. N'hésite pas à me poser des questions sur les actions, les ETF, la diversification ou toute autre notion financière !
                </p>
              </div>
            </div>
          )}

          {/* Liste des messages */}
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-5 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'rounded-tr-none bg-primary/10 border border-primary/30 text-primary-light'
                    : msg.isError
                    ? 'rounded-tl-none bg-red-500/10 border border-red-500/30 text-red-300'
                    : 'rounded-tl-none bg-white/5 border border-dark-border'
                }`}
              >
                {msg.isError && (
                  <div className="flex items-center gap-2 mb-2 text-red-400">
                    <AlertCircle size={16} />
                    <span className="text-xs font-bold">Erreur</span>
                  </div>
                )}
                <p className="whitespace-pre-wrap">{msg.content}</p>
                {msg.model && (
                  <p className="text-[10px] text-gray-500 mt-2">Modèle: {msg.model}</p>
                )}
              </div>
            </div>
          ))}

          {/* Indicateur de chargement */}
          {isLoading && (
            <div className="flex justify-start">
              <div className="p-5 rounded-2xl rounded-tl-none bg-white/5 border border-dark-border">
                <Loader2 className="animate-spin text-primary" size={20} />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 bg-white/[0.02] border-t border-dark-border">
          <form onSubmit={handleSendMessage} className="relative flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Pose-moi une question sur l'investissement..."
              disabled={isLoading || !isOnline}
              className="flex-1 bg-white/5 border border-dark-border rounded-2xl py-4 px-6 focus:outline-none focus:border-primary/50 transition-all text-sm font-light tracking-wide disabled:opacity-50 disabled:cursor-not-allowed"
            />

            <button
              type="button"
              onClick={handleReset}
              disabled={messages.length === 0 || isLoading}
              className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center hover:bg-white/10 transition-all disabled:opacity-30 disabled:cursor-not-allowed group"
              title="Réinitialiser la conversation"
            >
              <RefreshCw size={18} className="text-gray-400 group-hover:text-white transition-colors" />
            </button>

            <button
              type="submit"
              disabled={!input.trim() || isLoading || !isOnline}
              className="w-12 h-12 bg-primary rounded-xl flex items-center justify-center hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 group"
            >
              <Send size={18} className="text-black group-hover:-rotate-12 transition-transform" />
            </button>
          </form>
        </div>
      </div>
    </GlassCard>
  );
};

export default ChatBox;
