import React from 'react';
import { Shield, Sparkles, Activity, Terminal, ArrowRight, Play, Cpu, Lock } from 'lucide-react';

interface HeroHeaderProps {
  onQuickStart: () => void;
  onOpenDocs?: () => void;
}

export const HeroHeader: React.FC<HeroHeaderProps> = ({
  onQuickStart,
  onOpenDocs
}) => {
  return (
    <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-b from-slate-900/80 via-slate-900/50 to-slate-950/90 p-8 md:p-12 backdrop-blur-2xl shadow-[0_20px_50px_rgba(0,0,0,0.6)]">
      {/* Background ambient light effects */}
      <div className="pointer-events-none absolute -top-40 -left-20 h-96 w-96 rounded-full bg-cyan-500/15 blur-3xl animate-pulse" />
      <div className="pointer-events-none absolute top-10 right-0 h-80 w-80 rounded-full bg-indigo-500/15 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-20 left-1/3 h-72 w-72 rounded-full bg-emerald-500/10 blur-3xl" />

      {/* Decorative Grid Overlay */}
      <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,#1e293b15_1px,transparent_1px),linear-gradient(to_bottom,#1e293b15_1px,transparent_1px)] bg-[size:32px_32px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />

      <div className="relative z-10 max-w-4xl">
        {/* Status Pill Badge */}
        <div className="inline-flex items-center gap-2.5 rounded-full border border-cyan-500/30 bg-cyan-950/50 px-4 py-1.5 text-xs font-semibold text-cyan-300 backdrop-blur-md shadow-[0_0_15px_rgba(6,182,212,0.25)]">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          <span className="tracking-wide uppercase font-mono text-[11px]">CyberGuard 3.0 Core Engine Active</span>
          <span className="text-cyan-500/50">|</span>
          <span className="text-slate-300 font-mono text-[11px]">v3.2.0-PRO</span>
        </div>

        {/* Dynamic Typography Hero Headline */}
        <h1 className="mt-6 text-4xl sm:text-5xl md:text-6xl font-black tracking-tight text-white leading-[1.1]">
          Intelligent Defense &{' '}
          <span className="bg-gradient-to-r from-sky-400 via-indigo-300 to-emerald-400 bg-clip-text text-transparent drop-shadow-[0_0_25px_rgba(56,189,248,0.3)]">
            Zero-Trust Cyber Operations
          </span>
        </h1>

        {/* Subtitle description */}
        <p className="mt-5 text-base sm:text-lg text-slate-300 font-normal leading-relaxed max-w-2xl">
          Comprehensive real-time threat intelligence, cryptographic password entropy analysis, AI-powered phishing defense, and forensic file integrity auditing wrapped in a unified glassmorphism dashboard.
        </p>

        {/* Action Buttons & Terminal Badge */}
        <div className="mt-8 flex flex-wrap items-center gap-4">
          <button
            onClick={onQuickStart}
            className="group relative inline-flex items-center gap-3 overflow-hidden rounded-xl bg-gradient-to-r from-sky-500 via-cyan-500 to-teal-400 p-[1px] font-semibold text-white shadow-[0_0_25px_rgba(56,189,248,0.35)] transition-all duration-300 hover:shadow-[0_0_35px_rgba(56,189,248,0.55)] hover:scale-[1.02] active:scale-[0.98]"
          >
            <span className="inline-flex h-full w-full items-center gap-2.5 rounded-xl bg-slate-950/80 px-6 py-3.5 backdrop-blur-md transition-colors duration-200 group-hover:bg-transparent group-hover:text-slate-950">
              <Sparkles className="w-4 h-4 text-cyan-400 group-hover:text-slate-950 transition-colors" />
              <span>Explore Security Suites</span>
              <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
            </span>
          </button>

          {/* Quick Terminal Command Snippet */}
          <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-slate-950/60 px-4 py-3 text-xs font-mono text-slate-300 backdrop-blur-md">
            <Terminal className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-slate-400">audit_engine</span>
            <span className="text-emerald-400">--deep-scan</span>
            <span className="text-cyan-400">--live</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroHeader;
