import React from 'react';

export default function ColorBends({ color = '#FFD700' }) {
  return (
    <>
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        {/* Animated gradient blobs */}
        <div
          className="absolute top-[-10%] left-[-5%] w-[60%] h-[60%] rounded-full opacity-40 blur-[120px] animate-blob"
          style={{
            background: `radial-gradient(circle, ${color} 0%, transparent 70%)`
          }}
        />
        <div
          className="absolute top-[20%] right-[-10%] w-[50%] h-[50%] rounded-full opacity-35 blur-[100px] animate-blob"
          style={{
            background: `radial-gradient(circle, ${color} 0%, transparent 70%)`,
            animationDelay: '2s'
          }}
        />
        <div
          className="absolute bottom-[-5%] left-[30%] w-[45%] h-[45%] rounded-full opacity-38 blur-[110px] animate-blob"
          style={{
            background: `radial-gradient(circle, ${color} 0%, transparent 70%)`,
            animationDelay: '4s'
          }}
        />
        <div
          className="absolute top-[50%] left-[40%] w-[40%] h-[40%] rounded-full opacity-30 blur-[90px] animate-glow"
          style={{
            background: `radial-gradient(circle, ${color} 0%, transparent 70%)`
          }}
        />
      </div>

      <style>{`
        @keyframes blob {
          0%, 100% {
            transform: translate(0px, 0px) scale(1);
          }
          33% {
            transform: translate(50px, -80px) scale(1.15);
          }
          66% {
            transform: translate(-40px, 40px) scale(0.85);
          }
        }
      `}</style>
    </>
  );
}
