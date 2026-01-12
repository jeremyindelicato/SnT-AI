import React, { useState, useEffect, useRef } from 'react';
import { Send, Activity, Sparkles, Loader2, AlertCircle, RefreshCw } from 'lucide-react';
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
    <GlassCard className="p-1 border-primary/20 shadow-[0_0_40px_rgba(212,175,55,0.08)]" hover={false}>
      <div className="bg-black/60 rounded-[1.7rem] overflow-hidden">

        {/* Header Premium */}
        <div className="relative flex items-center justify-between px-6 py-5 border-b border-primary/10 bg-gradient-to-r from-white/[0.02] to-white/[0.01]">
          <div className="flex items-center gap-3">
            <div className={`relative w-3 h-3 rounded-full ${isOnline ? 'bg-primary' : 'bg-red-500'} shadow-[0_0_15px] ${isOnline ? 'shadow-primary' : 'shadow-red-500'}`}>
              {isOnline && <div className="absolute inset-0 bg-primary rounded-full animate-ping opacity-75" />}
            </div>
            <span className="text-[10px] uppercase tracking-[0.15em] font-bold bg-gradient-to-r from-accent-light to-primary bg-clip-text text-transparent">
              Start&Trade Assistant
            </span>
            {!isOnline && (
              <span className="text-[9px] text-red-400/70 uppercase tracking-wider">(Backend déconnecté)</span>
            )}
          </div>

          <div className="flex gap-4 items-center">
            <button
              onClick={checkBackendHealth}
              className="text-gray-600 hover:text-primary transition-all duration-300 hover:scale-110"
              title="Vérifier la connexion"
            >
              <RefreshCw size={13} />
            </button>
            <Activity size={13} className="text-gray-600" />
            <Sparkles size={13} className="text-primary animate-pulse" />
          </div>
        </div>

        {/* Messages */}
        <div className="h-[500px] overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-primary/20 scrollbar-track-transparent">

          {/* Message de bienvenue Premium */}
          {messages.length === 0 && (
            <div className="flex justify-start animate-slide-up">
              <div className="max-w-[85%] p-6 rounded-2xl rounded-tl-none bg-gradient-to-br from-white/5 to-white/[0.02] border border-primary/10 backdrop-blur-sm text-sm leading-relaxed">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles size={16} className="text-primary" />
                  <p className="font-bold text-accent-light">Bienvenue chez Start&Trade</p>
                </div>
                <p className="text-gray-400 mb-3">
                  Je suis votre <span className="text-primary font-semibold">conseiller financier pédagogique</span>,
                  propulsé par l'intelligence artificielle.
                </p>
                <p className="text-gray-500 text-xs">
                  Posez-moi des questions sur les actions, les ETF, la diversification ou toute autre notion d'investissement.
                  Je suis là pour vous accompagner dans votre apprentissage.
                </p>
              </div>
            </div>
          )}

          {/* Liste des messages */}
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
            >
              <div
                className={`max-w-[85%] p-5 rounded-2xl text-sm leading-relaxed backdrop-blur-sm transition-all duration-300 hover:scale-[1.02] ${
                  msg.role === 'user'
                    ? 'rounded-tr-none bg-gradient-to-br from-primary/15 to-primary/5 border border-primary/30 text-accent-light shadow-[0_0_20px_rgba(212,175,55,0.1)]'
                    : msg.isError
                    ? 'rounded-tl-none bg-gradient-to-br from-red-500/10 to-red-500/5 border border-red-500/30 text-red-300'
                    : 'rounded-tl-none bg-gradient-to-br from-white/5 to-white/[0.02] border border-accent/10 text-gray-300'
                }`}
              >
                {msg.isError && (
                  <div className="flex items-center gap-2 mb-2 text-red-400">
                    <AlertCircle size={16} />
                    <span className="text-xs font-bold uppercase tracking-wider">Erreur</span>
                  </div>
                )}
                <p className="whitespace-pre-wrap">{msg.content}</p>
                {msg.model && (
                  <p className="text-[9px] text-gray-600 mt-3 uppercase tracking-wider">Modèle: {msg.model}</p>
                )}
              </div>
            </div>
          ))}

          {/* Indicateur de chargement Premium */}
          {isLoading && (
            <div className="flex justify-start animate-slide-up">
              <div className="p-5 rounded-2xl rounded-tl-none bg-gradient-to-br from-white/5 to-white/[0.02] border border-accent/10 backdrop-blur-sm">
                <div className="flex items-center gap-3">
                  <Loader2 className="animate-spin text-primary" size={20} />
                  <span className="text-xs text-gray-500 uppercase tracking-wider">Réflexion en cours...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Premium */}
        <div className="p-5 bg-gradient-to-r from-white/[0.01] to-white/[0.02] border-t border-primary/10 backdrop-blur-sm">
          <form onSubmit={handleSendMessage} className="relative flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Posez votre question sur l'investissement..."
              disabled={isLoading || !isOnline}
              className="flex-1 bg-white/5 border border-primary/20 rounded-2xl py-4 px-6
                focus:outline-none focus:border-primary/50 focus:shadow-[0_0_20px_rgba(212,175,55,0.1)]
                transition-all duration-300 text-sm font-light tracking-wide
                placeholder:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed
                text-accent-light"
            />

            <button
              type="button"
              onClick={handleReset}
              disabled={messages.length === 0 || isLoading}
              className="w-12 h-12 bg-white/5 border border-accent/20 rounded-xl flex items-center justify-center
                hover:bg-white/10 hover:border-accent/40 hover:scale-105
                transition-all duration-300 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:scale-100 group"
              title="Réinitialiser la conversation"
            >
              <RefreshCw size={18} className="text-gray-500 group-hover:text-accent transition-colors" />
            </button>

            <button
              type="submit"
              disabled={!input.trim() || isLoading || !isOnline}
              className="relative w-12 h-12 rounded-xl flex items-center justify-center
                overflow-hidden group
                hover:scale-105 active:scale-95
                transition-all duration-300
                disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-primary via-primary-dark to-accent opacity-90 group-hover:opacity-100 transition-opacity" />
              <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
              <Send size={18} className="relative z-10 text-black group-hover:-rotate-12 transition-transform duration-300" />
            </button>
          </form>
        </div>
      </div>
    </GlassCard>
  );
};

export default ChatBox;
