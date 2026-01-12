import React, { useState, useEffect } from 'react';
import {
  Shield,
  Zap,
  BookOpen,
  Target,
  Sparkles,
  ChevronRight,
  Github,
  Brain,
  Lock,
  TrendingUp
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

      {/* Background Effects Premium */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        {/* Gradient Orbs */}
        <div className="absolute top-[-20%] right-[-10%] w-[70%] h-[70%] bg-primary/8 blur-[150px] rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[-10%] left-[-5%] w-[60%] h-[60%] bg-accent/5 blur-[140px] rounded-full animate-float" />
        <div className="absolute top-[40%] left-[50%] w-[40%] h-[40%] bg-primary/5 blur-[100px] rounded-full animate-glow" />

        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:100px_100px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000,transparent)]" />
      </div>

      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-700 ${
        isScrolled ? 'py-3 bg-black/90 backdrop-blur-2xl border-b border-primary/10 shadow-[0_0_30px_rgba(212,175,55,0.1)]' : 'py-6 bg-transparent'
      }`}>
        <div className="max-w-7xl mx-auto px-6 md:px-8 flex justify-between items-center">

          {/* Logo avec SVG */}
          <div className="flex items-center gap-3 group cursor-pointer animate-fade-in">
            <div className="relative w-10 h-10 transition-transform duration-500 group-hover:scale-110 group-hover:rotate-6">
              <img
                src="/LogoSnT.svg"
                alt="Start&Trade Logo"
                className="w-full h-full object-contain"
              />
              <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            </div>
            <span className="text-xl md:text-2xl font-bold tracking-tight bg-gradient-to-r from-accent-light via-primary to-accent-light bg-clip-text text-transparent animate-shimmer bg-[length:200%_auto]">
              Start<span className="text-primary">&</span>Trade
            </span>
          </div>

          {/* Nav Links */}
          <div className="hidden md:flex items-center gap-8 text-[10px] uppercase tracking-[0.15em] font-bold text-gray-500">
            <a href="#assistant" className="hover:text-primary transition-all duration-300 relative group">
              <span>Assistant</span>
              <span className="absolute -bottom-1 left-0 w-0 h-[1px] bg-primary transition-all duration-300 group-hover:w-full"></span>
            </a>
            <a href="#features" className="hover:text-primary transition-all duration-300 relative group">
              <span>Fonctionnalités</span>
              <span className="absolute -bottom-1 left-0 w-0 h-[1px] bg-primary transition-all duration-300 group-hover:w-full"></span>
            </a>
            <a href="#about" className="hover:text-primary transition-all duration-300 relative group">
              <span>À propos</span>
              <span className="absolute -bottom-1 left-0 w-0 h-[1px] bg-primary transition-all duration-300 group-hover:w-full"></span>
            </a>
          </div>

          {/* CTA Button Premium */}
          <a
            href="https://github.com/jeremyindelicato/SnT-AI"
            target="_blank"
            rel="noopener noreferrer"
            className="group relative flex items-center gap-2 px-6 py-2.5 rounded-full overflow-hidden text-[10px] uppercase tracking-[0.15em] font-bold transition-all duration-500 hover:scale-105"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-primary/20 via-primary/10 to-accent/20 group-hover:from-primary/30 group-hover:via-primary/20 group-hover:to-accent/30 transition-all duration-500" />
            <div className="absolute inset-0 border border-primary/30 rounded-full group-hover:border-primary/50 transition-all duration-500" />
            <Github size={14} className="relative z-10 text-primary" />
            <span className="relative z-10 text-accent-light hidden md:inline">GitHub</span>
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-36 md:pt-48 pb-20 px-6 z-10">
        <div className="max-w-7xl mx-auto flex flex-col items-center">

          {/* Badge Premium */}
          <div className="inline-flex items-center gap-3 px-5 py-2.5 rounded-full bg-white/5 border border-primary/20 backdrop-blur-sm text-primary text-[9px] font-bold uppercase tracking-[0.2em] mb-12 animate-slide-up shadow-[0_0_20px_rgba(212,175,55,0.1)]">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary shadow-[0_0_10px_rgba(212,175,55,0.5)]"></span>
            </span>
            Intelligence Financière Locale
          </div>

          {/* Hero Title Premium avec animation */}
          <h1 className="text-5xl md:text-8xl lg:text-9xl font-extralight tracking-tighter text-center mb-8 leading-[0.95] animate-fade-in">
            L'élite de
            <br />
            <span className="relative inline-block">
              <span className="bg-gradient-to-r from-accent-light via-primary to-accent-light bg-clip-text text-transparent animate-shimmer bg-[length:200%_auto] font-light italic">
                l'investissement intelligent.
              </span>
              <div className="absolute -bottom-2 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-primary to-transparent opacity-50" />
            </span>
          </h1>

          {/* Hero Subtitle */}
          <p className="max-w-2xl mx-auto text-gray-400 text-base md:text-xl text-center mb-16 font-light leading-relaxed animate-slide-up [animation-delay:200ms]">
            Start&Trade Assistant, votre conseiller financier personnel propulsé par l'IA.
            <br />
            <span className="text-accent">Apprenez, explorez et investissez avec confiance.</span>
          </p>

          {/* Scroll Indicator Premium */}
          <a href="#assistant" className="group flex flex-col items-center gap-3 text-sm text-gray-600 hover:text-primary transition-all duration-500 animate-slide-up [animation-delay:400ms]">
            <span className="text-[10px] uppercase tracking-[0.2em] font-bold">Découvrir l'assistant</span>
            <div className="w-6 h-10 rounded-full border-2 border-gray-700 group-hover:border-primary flex items-start justify-center p-2 transition-all duration-500">
              <div className="w-1 h-2 bg-primary rounded-full animate-pulse" />
            </div>
          </a>
        </div>
      </section>

      {/* Chat Section Premium */}
      <section id="assistant" className="relative py-20 px-6 z-10">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16 animate-slide-up">
            <div className="inline-flex items-center gap-2 mb-4">
              <div className="h-[1px] w-12 bg-gradient-to-r from-transparent to-primary" />
              <Brain className="w-5 h-5 text-primary" />
              <div className="h-[1px] w-12 bg-gradient-to-l from-transparent to-primary" />
            </div>
            <h2 className="text-4xl md:text-6xl font-extralight mb-6 tracking-tight">
              Votre <span className="bg-gradient-to-r from-primary via-accent-light to-primary bg-clip-text text-transparent font-light italic">assistant personnel</span>
            </h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-sm md:text-base leading-relaxed">
              Posez vos questions sur les actions, ETF, diversification ou toute notion financière.
              <br />
              <span className="text-accent-dark">Propulsé par Phi 3.5 Mini en local via Ollama.</span>
            </p>
          </div>

          <div className="animate-slide-up [animation-delay:200ms]">
            <ChatBox />
          </div>
        </div>
      </section>

      {/* Features Section Premium */}
      <section id="features" className="relative py-32 px-6 z-10">
        <div className="max-w-7xl mx-auto">

          <div className="text-center mb-20 animate-fade-in">
            <div className="inline-flex items-center gap-2 mb-4">
              <div className="h-[1px] w-12 bg-gradient-to-r from-transparent to-primary" />
              <Sparkles className="w-5 h-5 text-primary" />
              <div className="h-[1px] w-12 bg-gradient-to-l from-transparent to-primary" />
            </div>
            <h2 className="text-4xl md:text-6xl font-extralight mb-6 tracking-tight">
              Une expérience <span className="bg-gradient-to-r from-primary via-accent-light to-primary bg-clip-text text-transparent font-light italic">d'exception</span>
            </h2>
            <p className="text-gray-500 max-w-2xl mx-auto leading-relaxed">
              Architecture modulaire et technologie de pointe au service de votre apprentissage.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">

            {/* Feature 1 */}
            <div className="animate-slide-up [animation-delay:100ms]">
              <GlassCard className="p-8 group hover:scale-105 transition-all duration-500">
                <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/10 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-500">
                  <BookOpen size={28} className="text-primary" />
                  <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                </div>
                <h3 className="text-lg font-bold mb-4 uppercase tracking-[0.15em] text-[11px] text-accent-light">
                  Pédagogie Premium
                </h3>
                <p className="text-gray-500 leading-relaxed text-sm">
                  Une approche unique qui vulgarise les concepts les plus complexes avec élégance et précision.
                </p>
              </GlassCard>
            </div>

            {/* Feature 2 */}
            <div className="animate-slide-up [animation-delay:200ms]">
              <GlassCard className="p-8 group hover:scale-105 transition-all duration-500">
                <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/10 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-500">
                  <Lock size={28} className="text-primary" />
                  <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                </div>
                <h3 className="text-lg font-bold mb-4 uppercase tracking-[0.15em] text-[11px] text-accent-light">
                  Confidentialité Absolue
                </h3>
                <p className="text-gray-500 leading-relaxed text-sm">
                  Vos données restent strictement privées. Architecture 100% locale, zéro tracking.
                </p>
              </GlassCard>
            </div>

            {/* Feature 3 */}
            <div className="animate-slide-up [animation-delay:300ms]">
              <GlassCard className="p-8 group hover:scale-105 transition-all duration-500">
                <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/10 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-500">
                  <Zap size={28} className="text-primary" />
                  <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                </div>
                <h3 className="text-lg font-bold mb-4 uppercase tracking-[0.15em] text-[11px] text-accent-light">
                  Données Temps Réel
                </h3>
                <p className="text-gray-500 leading-relaxed text-sm">
                  Intégration MCP pour récupérer les données financières en direct depuis Yahoo Finance.
                </p>
              </GlassCard>
            </div>

            {/* Feature 4 */}
            <div className="animate-slide-up [animation-delay:400ms]">
              <GlassCard className="p-8 group hover:scale-105 transition-all duration-500">
                <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/10 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-500">
                  <Shield size={28} className="text-primary" />
                  <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                </div>
                <h3 className="text-lg font-bold mb-4 uppercase tracking-[0.15em] text-[11px] text-accent-light">
                  Éthique & Transparence
                </h3>
                <p className="text-gray-500 leading-relaxed text-sm">
                  Aucune promesse irréaliste. Seule une analyse prudente et responsable.
                </p>
              </GlassCard>
            </div>

            {/* Feature 5 */}
            <div className="animate-slide-up [animation-delay:500ms]">
              <GlassCard className="p-8 group hover:scale-105 transition-all duration-500">
                <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/10 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-500">
                  <Brain size={28} className="text-primary" />
                  <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                </div>
                <h3 className="text-lg font-bold mb-4 uppercase tracking-[0.15em] text-[11px] text-accent-light">
                  Architecture HEPHAESTUS
                </h3>
                <p className="text-gray-500 leading-relaxed text-sm">
                  Système modulaire avancé : Frontend React, Backend Python, MCP et LLM local.
                </p>
              </GlassCard>
            </div>

            {/* Feature 6 */}
            <div className="animate-slide-up [animation-delay:600ms]">
              <GlassCard className="p-8 group hover:scale-105 transition-all duration-500">
                <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/10 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-500">
                  <TrendingUp size={28} className="text-primary" />
                  <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                </div>
                <h3 className="text-lg font-bold mb-4 uppercase tracking-[0.15em] text-[11px] text-accent-light">
                  Open Source
                </h3>
                <p className="text-gray-500 leading-relaxed text-sm">
                  Code ouvert et documenté. Étudiez, modifiez et adaptez selon vos besoins.
                </p>
              </GlassCard>
            </div>

          </div>
        </div>
      </section>

      {/* About Section Premium */}
      <section id="about" className="relative py-32 px-6 z-10 border-t border-primary/10">
        <div className="max-w-4xl mx-auto text-center animate-fade-in">
          <div className="inline-flex items-center gap-2 mb-6">
            <div className="h-[1px] w-12 bg-gradient-to-r from-transparent to-primary" />
            <Target className="w-5 h-5 text-primary" />
            <div className="h-[1px] w-12 bg-gradient-to-l from-transparent to-primary" />
          </div>
          <h2 className="text-4xl md:text-6xl font-extralight mb-8 tracking-tight">
            Projet <span className="bg-gradient-to-r from-primary via-accent-light to-primary bg-clip-text text-transparent font-light italic">HEPHAESTUS</span>
          </h2>
          <p className="text-gray-500 leading-relaxed mb-12 text-sm md:text-base">
            Start&Trade est un agent conversationnel intelligent développé dans le cadre du projet HEPHAESTUS.
            Notre mission : créer un assistant financier pédagogique pour jeunes investisseurs,
            <br />
            <span className="text-accent">entièrement local, sans dépendance aux APIs payantes.</span>
          </p>

          <div className="flex flex-wrap justify-center gap-4 text-xs">
            {[
              { label: 'Frontend', value: 'React + Vite', delay: '0ms' },
              { label: 'Backend', value: 'Python + FastAPI', delay: '100ms' },
              { label: 'LLM', value: 'Phi 3.5 (Ollama)', delay: '200ms' },
              { label: 'Tooling', value: 'MCP + n8n', delay: '300ms' },
            ].map((tech, i) => (
              <div
                key={i}
                className={`group px-5 py-3 rounded-full bg-white/5 border border-primary/20 backdrop-blur-sm hover:border-primary/40 transition-all duration-500 hover:scale-105 animate-slide-up`}
                style={{ animationDelay: tech.delay }}
              >
                <span className="text-gray-600 uppercase tracking-wider font-bold text-[9px]">{tech.label}:</span>{' '}
                <span className="text-primary font-bold text-[10px] uppercase tracking-wider">{tech.value}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer Premium */}
      <footer className="relative py-16 border-t border-primary/10 px-6 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">

          <div className="flex items-center gap-3 opacity-60 hover:opacity-100 transition-opacity duration-500">
            <img src="/LogoSnT.svg" alt="S&T" className="w-8 h-8" />
            <span className="text-sm font-light tracking-[0.3em] uppercase text-accent-light">Start&Trade</span>
          </div>

          <div className="flex gap-10 text-[9px] uppercase tracking-[0.2em] font-bold text-gray-600">
            <a href="#" className="hover:text-primary transition-colors duration-300">Documentation</a>
            <a href="https://github.com/jeremyindelicato/SnT-AI" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors duration-300">GitHub</a>
            <a href="#" className="hover:text-primary transition-colors duration-300">Contact</a>
          </div>

          <div className="text-[9px] text-gray-700 uppercase tracking-[0.2em] font-medium">
            © 2026 HEPHAESTUS
          </div>
        </div>
      </footer>

    </div>
  );
}

export default App;
