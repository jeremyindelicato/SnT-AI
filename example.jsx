import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Zap, 
  ChevronRight, 
  Menu, 
  X, 
  Globe, 
  Sparkles,
  ArrowUpRight,
  Send,
  Lock,
  PieChart,
  Activity
} from 'lucide-react';

const App = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [chatInput, setChatInput] = useState("");
  const [activeTab, setActiveTab] = useState('ia');

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Composant Liquid Glass Premium
  const PremiumGlass = ({ children, className = "", hover = true }) => (
    <div className={`
      relative overflow-hidden
      bg-[#0a0a0a]/40 backdrop-blur-2xl 
      border border-white/10 rounded-[2rem]
      shadow-[0_20px_50px_rgba(0,0,0,0.5)]
      transition-all duration-500
      ${hover ? 'hover:border-[#C5A059]/40 hover:shadow-[#C5A059]/5' : ''}
      ${className}
    `}>
      {/* Reflet de lumière balayant */}
      <div className="absolute inset-0 bg-gradient-to-tr from-white/5 via-transparent to-transparent pointer-events-none" />
      {children}
    </div>
  );

  return (
    <div className="min-h-screen bg-[#020202] text-[#e5e5e5] selection:bg-[#C5A059]/30 font-sans antialiased overflow-x-hidden">
      
      {/* Background : Liquid Smoke & Gold Dust */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-20%] right-[-10%] w-[70%] h-[70%] bg-[#C5A059]/10 blur-[150px] rounded-full animate-pulse" />
        <div className="absolute bottom-[-10%] left-[-5%] w-[50%] h-[50%] bg-white/5 blur-[120px] rounded-full" />
      </div>

      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-500 ${isScrolled ? 'py-4 bg-black/80 backdrop-blur-xl border-b border-white/5' : 'py-8 bg-transparent'}`}>
        <div className="max-w-7xl mx-auto px-8 flex justify-between items-center">
          <div className="flex items-center gap-3 group cursor-pointer">
            <svg width="40" height="40" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="group-hover:rotate-[180deg] transition-transform duration-700">
              <path d="M50 5L95 50L50 95L5 50L50 5Z" stroke="#C5A059" strokeWidth="2" />
              <circle cx="50" cy="50" r="15" stroke="white" strokeWidth="1" strokeDasharray="4 4" />
              <path d="M50 25V75M25 50H75" stroke="#C5A059" strokeWidth="1" opacity="0.5" />
            </svg>
            <span className="text-2xl font-light tracking-[0.3em] uppercase">Vantage<span className="font-bold text-[#C5A059]">.AI</span></span>
          </div>

          <div className="hidden md:flex items-center gap-12 text-[11px] uppercase tracking-[0.2em] font-medium text-gray-400">
            <a href="#" className="hover:text-[#C5A059] transition-colors">Vision</a>
            <a href="#" className="hover:text-[#C5A059] transition-colors">Terminal</a>
            <a href="#" className="hover:text-[#C5A059] transition-colors">Privilège</a>
          </div>

          <button className="px-8 py-3 rounded-full border border-[#C5A059]/30 text-[#C5A059] text-xs uppercase tracking-widest font-bold hover:bg-[#C5A059] hover:text-black transition-all duration-500">
            Accès Exclusif
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-52 pb-20 px-6 z-10">
        <div className="max-w-7xl mx-auto flex flex-col items-center">
          <div className="inline-flex items-center gap-3 px-5 py-2 rounded-full bg-white/5 border border-white/10 text-[#C5A059] text-[10px] font-bold uppercase tracking-[0.3em] mb-10">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#C5A059] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#C5A059]"></span>
            </span>
            Intelligence de marché en temps réel
          </div>
          
          <h1 className="text-6xl md:text-9xl font-extralight tracking-tighter text-center mb-10 leading-[0.9]">
            L'élite de l'investissement <br />
            <span className="italic font-serif text-[#C5A059]">dirigée par l'IA.</span>
          </h1>
          
          <p className="max-w-2xl mx-auto text-gray-400 text-lg md:text-xl text-center mb-16 font-light leading-relaxed">
            Oubliez la spéculation. Accédez à une IA prédictive qui analyse 15 ans de cycles financiers par seconde pour optimiser votre patrimoine.
          </p>

          {/* CENTRE DU PROJET : LE CHATBOT IA IMMERSIF */}
          <div className="w-full max-w-5xl mx-auto mt-10 perspective-1000">
            <PremiumGlass className="p-1 group border-[#C5A059]/20" hover={false}>
              <div className="bg-black/60 rounded-[1.8rem] overflow-hidden">
                {/* Chat Header */}
                <div className="flex items-center justify-between px-8 py-6 border-b border-white/5 bg-white/[0.02]">
                  <div className="flex items-center gap-4">
                    <div className="w-3 h-3 rounded-full bg-[#C5A059] shadow-[0_0_15px_#C5A059]" />
                    <span className="text-xs uppercase tracking-widest font-bold">Vantage Oracle V.4</span>
                  </div>
                  <div className="flex gap-6">
                    <Activity size={16} className="text-gray-500" />
                    <Globe size={16} className="text-gray-500" />
                  </div>
                </div>

                {/* Chat Body */}
                <div className="h-[500px] flex flex-col p-8 overflow-y-auto space-y-8 scrollbar-hide">
                  <div className="flex justify-start">
                    <div className="max-w-[70%] p-6 rounded-2xl rounded-tl-none bg-white/5 border border-white/10 text-sm leading-relaxed">
                      Bonjour Arthur. Les marchés asiatiques viennent de clôturer. J'ai détecté une anomalie sur le secteur des semi-conducteurs. Souhaitez-vous une analyse de réallocation ?
                    </div>
                  </div>

                  <div className="flex justify-end">
                    <div className="max-w-[70%] p-6 rounded-2xl rounded-tr-none bg-[#C5A059]/10 border border-[#C5A059]/30 text-sm leading-relaxed text-[#C5A059]">
                      Oui, montre-moi l'impact sur mon rendement annuel.
                    </div>
                  </div>

                  <div className="flex justify-start">
                    <div className="max-w-[85%] p-1 rounded-3xl bg-gradient-to-br from-[#C5A059]/20 to-transparent">
                      <div className="bg-[#0a0a0a] p-6 rounded-[calc(1.5rem-1px)]">
                        <div className="flex items-center gap-4 mb-6">
                          <PieChart className="text-[#C5A059]" />
                          <span className="text-xs font-bold uppercase tracking-widest">Projection Optimisée</span>
                        </div>
                        <div className="grid grid-cols-2 gap-8">
                          <div>
                            <p className="text-[10px] text-gray-500 uppercase mb-1">Rendement Estimé</p>
                            <p className="text-2xl font-light text-white">+18.4% <span className="text-[10px] text-[#C5A059]">vs 12.1%</span></p>
                          </div>
                          <div>
                            <p className="text-[10px] text-gray-500 uppercase mb-1">Indice de Risque</p>
                            <p className="text-2xl font-light text-white italic underline decoration-[#C5A059]">Modéré</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Chat Input Area */}
                <div className="p-6 bg-white/[0.02] border-t border-white/5">
                  <div className="relative flex items-center">
                    <input 
                      type="text" 
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      placeholder="Demandez une analyse de marché..."
                      className="w-full bg-white/5 border border-white/10 rounded-2xl py-5 pl-8 pr-16 focus:outline-none focus:border-[#C5A059]/50 transition-all text-sm font-light tracking-wide"
                    />
                    <button className="absolute right-3 w-12 h-12 bg-[#C5A059] rounded-xl flex items-center justify-center hover:scale-105 transition-transform group">
                      <Send size={18} className="text-black group-hover:-rotate-12 transition-transform" />
                    </button>
                  </div>
                </div>
              </div>
            </PremiumGlass>
          </div>
        </div>
      </section>

      {/* Trust Bar */}
      <section className="py-20 border-y border-white/5">
        <div className="max-w-7xl mx-auto px-8 flex flex-wrap justify-between items-center opacity-40 grayscale hover:grayscale-0 transition-all duration-1000">
          <span className="text-xl font-serif italic tracking-widest">BLOOMBERG</span>
          <span className="text-xl font-sans font-black tracking-tighter">REUTERS</span>
          <span className="text-xl font-serif tracking-widest uppercase">Financial Times</span>
          <span className="text-xl font-sans font-bold italic">NASDAQ</span>
        </div>
      </section>

      {/* Features : L'Architecture Premium */}
      <section className="py-32 px-6">
        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-20 items-center">
          <div>
            <h2 className="text-4xl md:text-6xl font-extralight mb-8 leading-tight">
              Une technologie <br />
              <span className="text-[#C5A059] italic font-serif">invisible mais absolue.</span>
            </h2>
            <div className="space-y-10 mt-16">
              {[
                { icon: <Lock />, title: "Sécurité de grade Institutionnel", desc: "Chiffrement AES-256 et isolation des actifs sur serveurs privés." },
                { icon: <Zap />, title: "Latence Zéro", desc: "Exécution des ordres en millisecondes via nos nœuds directs." },
                { icon: <Sparkles />, title: "IA Générative", desc: "L'Oracle apprend vos habitudes pour devenir votre double financier." }
              ].map((item, i) => (
                <div key={i} className="flex gap-6 group">
                  <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-[#C5A059] border border-white/10 group-hover:bg-[#C5A059] group-hover:text-black transition-all duration-500 shrink-0">
                    {item.icon}
                  </div>
                  <div>
                    <h4 className="text-lg font-bold mb-2 uppercase tracking-widest text-sm">{item.title}</h4>
                    <p className="text-gray-500 font-light leading-relaxed">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="relative">
            <PremiumGlass className="aspect-square flex items-center justify-center">
               <div className="relative w-64 h-64">
                  {/* Animation de cercle de données */}
                  <div className="absolute inset-0 rounded-full border-2 border-[#C5A059]/20 animate-[spin_10s_linear_infinite]" />
                  <div className="absolute inset-4 rounded-full border border-white/10 animate-[spin_15s_linear_infinite_reverse]" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Globe size={80} className="text-[#C5A059] animate-pulse" />
                  </div>
               </div>
            </PremiumGlass>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-20 border-t border-white/5 px-8">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-12">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 border border-[#C5A059] rotate-45 flex items-center justify-center">
              <div className="w-4 h-4 bg-[#C5A059]" />
            </div>
            <span className="text-lg font-light tracking-[0.4em] uppercase">Vantage</span>
          </div>
          
          <div className="flex gap-12 text-[10px] uppercase tracking-[0.2em] font-medium text-gray-500">
            <a href="#" className="hover:text-white transition-colors">Termes</a>
            <a href="#" className="hover:text-white transition-colors">Confidentialité</a>
            <a href="#" className="hover:text-white transition-colors">Conciergerie</a>
          </div>

          <div className="text-[10px] text-gray-600 uppercase tracking-widest">
            © 2026 Vantage AI - Luxury Financial Intelligence
          </div>
        </div>
      </footer>

      <style dangerouslySetInnerHTML={{ __html: `
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:italic@0,400;1,400&family=Inter:wght@100;300;500;700&display=swap');
        
        body { font-family: 'Inter', sans-serif; }
        .font-serif { font-family: 'Playfair Display', serif; }
        
        .scrollbar-hide::-webkit-scrollbar { display: none; }
        .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
        
        .perspective-1000 { perspective: 1500px; }
        
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}} />
    </div>
  );
};

export default App;