import React from 'react';

/**
 * Composant GlassCard - Effet glassmorphism premium
 */
const GlassCard = ({ children, className = "", hover = true }) => {
  return (
    <div
      className={`
        relative overflow-hidden
        bg-dark-card/40 backdrop-blur-2xl
        border border-dark-border rounded-3xl
        shadow-[0_20px_50px_rgba(0,0,0,0.5)]
        transition-all duration-500
        ${hover ? 'hover:border-primary/40 hover:shadow-primary/10' : ''}
        ${className}
      `}
    >
      {/* Reflet de lumière */}
      <div className="absolute inset-0 bg-gradient-to-tr from-white/5 via-transparent to-transparent pointer-events-none" />
      {children}
    </div>
  );
};

export default GlassCard;
