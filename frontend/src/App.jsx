import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Shield,
  Zap,
  BookOpen,
  Target,
  Sparkles,
  ChevronRight,
  Github
} from 'lucide-react';
import ChatBox from './components/ChatBox';
import GlassCard from './components/GlassCard';

function App() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-dark-bg text-gray-100 selection:bg-primary/30 font-sans antialiased overflow-x-hidden">

      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-20%] right-[-10%] w-[70%] h-[70%] bg-primary/10 blur-[150px] rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[-10%] left-[-5%] w-[50%] h-[50%] bg-blue-500/5 blur-[120px] rounded-full" />
      </div>

      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-500 ${
        isScrolled ? 'py-3 bg-black/80 backdrop-blur-xl border-b border-dark-border' : 'py-6 bg-transparent'
      }`}>
        <div className="max-w-7xl mx-auto px-6 md:px-8 flex justify-between items-center">

          {/* Logo */}
          <div className="flex items-center gap-3 group cursor-pointer">
            <div className="relative">
              <TrendingUp className="w-8 h-8 text-primary group-hover:scale-110 transition-transform" />
              <div className="absolute inset-0 bg-primary/20 blur-xl group-hover:bg-primary/40 transition-all" />
            </div>
            <span className="text-xl md:text-2xl font-bold tracking-tight">
              Start<span className="text-primary">&</span>Trade
            </span>
          </div>

          {/* Nav Links */}
          <div className="hidden md:flex items-center gap-8 text-xs uppercase tracking-wider font-medium text-gray-400">
            <a href="#assistant" className="hover:text-primary transition-colors">Assistant</a>
            <a href="#features" className="hover:text-primary transition-colors">Fonctionnalités</a>
            <a href="#about" className="hover:text-primary transition-colors">À propos</a>
          </div>

          {/* CTA Button */}
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-5 py-2.5 rounded-full border border-primary/30 text-primary text-xs uppercase tracking-wider font-bold hover:bg-primary hover:text-black transition-all duration-500"
          >
            <Github size={16} />
            <span className="hidden md:inline">GitHub</span>
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 md:pt-40 pb-16 px-6 z-10">
        <div className="max-w-7xl mx-auto flex flex-col items-center">

          {/* Badge */}
          <div className="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-white/5 border border-dark-border text-primary text-[10px] font-bold uppercase tracking-wider mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
            Projet HEPHAESTUS - IA Locale
          </div>

          {/* Hero Title */}
          <h1 className="text-5xl md:text-8xl font-bold tracking-tight text-center mb-6 leading-[1.1]">
            Investis intelligemment
            <br />
            <span className="text-primary">avec confiance.</span>
          </h1>

          {/* Hero Subtitle */}
          <p className="max-w-2xl mx-auto text-gray-400 text-base md:text-lg text-center mb-12 font-light leading-relaxed">
            Start&Trade est ton assistant financier personnel propulsé par l'IA.
            Apprends, explore et découvre le monde de l'investissement avec un conseiller pédagogique disponible 24/7.
          </p>

          {/* Scroll Indicator */}
          <a href="#assistant" className="flex items-center gap-2 text-sm text-gray-500 hover:text-primary transition-colors group">
            <span>Essayer l'assistant</span>
            <ChevronRight className="group-hover:translate-x-1 transition-transform" size={16} />
          </a>
        </div>
      </section>

      {/* Chat Section */}
      <section id="assistant" className="relative py-16 px-6 z-10">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">
              Discute avec <span className="text-primary">Start&Trade Assistant</span>
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Pose tes questions sur les actions, les ETF, la diversification ou toute autre notion financière.
              L'assistant utilise le modèle Phi 3.5 en local via Ollama.
            </p>
          </div>

          <ChatBox />
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative py-24 px-6 z-10">
        <div className="max-w-7xl mx-auto">

          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">
              Pourquoi <span className="text-primary">Start&Trade</span> ?
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Une architecture moderne et modulaire pour une expérience d'apprentissage optimale.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">

            {/* Feature 1 */}
            <GlassCard className="p-8 group">
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20 mb-6 group-hover:scale-110 transition-transform">
                <BookOpen size={24} />
              </div>
              <h3 className="text-xl font-bold mb-3 uppercase tracking-wide text-sm">
                Pédagogie d'abord
              </h3>
              <p className="text-gray-400 leading-relaxed text-sm">
                Conçu pour les débutants, l'assistant vulgarise les concepts financiers complexes sans jamais être condescendant.
              </p>
            </GlassCard>

            {/* Feature 2 */}
            <GlassCard className="p-8 group">
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20 mb-6 group-hover:scale-110 transition-transform">
                <Shield size={24} />
              </div>
              <h3 className="text-xl font-bold mb-3 uppercase tracking-wide text-sm">
                100% Local & Privé
              </h3>
              <p className="text-gray-400 leading-relaxed text-sm">
                Tes données restent chez toi. Le modèle Phi 3.5 tourne localement via Ollama, aucune donnée n'est envoyée à des serveurs tiers.
              </p>
            </GlassCard>

            {/* Feature 3 */}
            <GlassCard className="p-8 group">
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20 mb-6 group-hover:scale-110 transition-transform">
                <Zap size={24} />
              </div>
              <h3 className="text-xl font-bold mb-3 uppercase tracking-wide text-sm">
                Données en temps réel
              </h3>
              <p className="text-gray-400 leading-relaxed text-sm">
                Grâce au serveur MCP et à n8n, l'assistant peut récupérer des données financières en direct depuis Yahoo Finance.
              </p>
            </GlassCard>

            {/* Feature 4 */}
            <GlassCard className="p-8 group">
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20 mb-6 group-hover:scale-110 transition-transform">
                <Target size={24} />
              </div>
              <h3 className="text-xl font-bold mb-3 uppercase tracking-wide text-sm">
                Éthique & Prudence
              </h3>
              <p className="text-gray-400 leading-relaxed text-sm">
                L'assistant ne donne jamais de conseils garantis et rappelle toujours que tout investissement comporte des risques.
              </p>
            </GlassCard>

            {/* Feature 5 */}
            <GlassCard className="p-8 group">
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20 mb-6 group-hover:scale-110 transition-transform">
                <Sparkles size={24} />
              </div>
              <h3 className="text-xl font-bold mb-3 uppercase tracking-wide text-sm">
                Architecture Modulaire
              </h3>
              <p className="text-gray-400 leading-relaxed text-sm">
                Frontend React, Backend Python, MCP server et LLM local : chaque composant est isolé et facilement extensible.
              </p>
            </GlassCard>

            {/* Feature 6 */}
            <GlassCard className="p-8 group">
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20 mb-6 group-hover:scale-110 transition-transform">
                <TrendingUp size={24} />
              </div>
              <h3 className="text-xl font-bold mb-3 uppercase tracking-wide text-sm">
                Open Source
              </h3>
              <p className="text-gray-400 leading-relaxed text-sm">
                Le code est ouvert et documenté. Tu peux l'étudier, le modifier et l'adapter à tes besoins.
              </p>
            </GlassCard>

          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="relative py-24 px-6 z-10 border-t border-dark-border">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-6">
            Le projet <span className="text-primary">HEPHAESTUS</span>
          </h2>
          <p className="text-gray-400 leading-relaxed mb-8">
            Start&Trade est un projet d'agent conversationnel intelligent développé dans le cadre du projet HEPHAESTUS.
            L'objectif est de créer un assistant financier pédagogique pour jeunes investisseurs, entièrement local et sans dépendance à des APIs payantes.
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <div className="px-4 py-2 rounded-full bg-white/5 border border-dark-border">
              <span className="text-gray-500">Frontend:</span> <span className="text-primary font-bold">React + Vite</span>
            </div>
            <div className="px-4 py-2 rounded-full bg-white/5 border border-dark-border">
              <span className="text-gray-500">Backend:</span> <span className="text-primary font-bold">Python + FastAPI</span>
            </div>
            <div className="px-4 py-2 rounded-full bg-white/5 border border-dark-border">
              <span className="text-gray-500">LLM:</span> <span className="text-primary font-bold">Phi 3.5 (Ollama)</span>
            </div>
            <div className="px-4 py-2 rounded-full bg-white/5 border border-dark-border">
              <span className="text-gray-500">Tooling:</span> <span className="text-primary font-bold">MCP + n8n</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-dark-border px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">

          <div className="flex items-center gap-3">
            <TrendingUp className="w-6 h-6 text-primary" />
            <span className="text-sm font-light tracking-wider uppercase">Start&Trade</span>
          </div>

          <div className="flex gap-8 text-[10px] uppercase tracking-wider font-medium text-gray-500">
            <a href="#" className="hover:text-white transition-colors">Documentation</a>
            <a href="#" className="hover:text-white transition-colors">GitHub</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>

          <div className="text-[10px] text-gray-600 uppercase tracking-wider">
            © 2026 Start&Trade - Projet HEPHAESTUS
          </div>
        </div>
      </footer>

    </div>
  );
}

export default App;
