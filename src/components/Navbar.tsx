import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Search, 
  Command, 
  Menu, 
  X, 
  Globe, 
  Fish, 
  KeyRound, 
  FileCheck2, 
  BarChart3, 
  Gamepad2,
  Terminal,
  ExternalLink
} from 'lucide-react';
import { NavRouteItem } from '../types';

interface NavbarProps {
  currentPath: string;
  onNavigate: (path: string) => void;
  onSearchOpen?: () => void;
}

const navLinks: NavRouteItem[] = [
  { id: 'home', label: 'Directory Hub', path: '/', iconName: 'ShieldCheck' },
  { id: 'dashboard', label: 'Threat Analytics', path: '/dashboard', iconName: 'BarChart3' },
  { id: 'url-analyzer', label: 'Website Security', path: '/url-analyzer', iconName: 'Globe' },
  { id: 'phishing-detector', label: 'Phishing Shield', path: '/phishing-scan', iconName: 'Fish' },
  { id: 'password-entropy', label: 'Password Entropy', path: '/password-checker', iconName: 'KeyRound' },
  { id: 'file-integrity', label: 'File Integrity', path: '/file-security', iconName: 'FileCheck2' },
  { id: 'cyber-quiz', label: 'Cyber Quiz', path: '/cyber-quiz', iconName: 'Gamepad2', badge: 'LIVE' }
];

export const Navbar: React.FC<NavbarProps> = ({
  currentPath,
  onNavigate,
  onSearchOpen
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/[0.08] bg-slate-950/70 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Brand Logo & Core Identifier */}
        <div 
          onClick={() => onNavigate('/')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500/20 to-cyan-500/10 border border-cyan-500/30 text-cyan-400 shadow-[0_0_20px_rgba(6,182,212,0.25)] transition-all duration-300 group-hover:scale-105 group-hover:border-cyan-400">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
            <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-cyan-500"></span>
            </span>
          </div>

          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-lg font-black tracking-tight text-white group-hover:text-cyan-300 transition-colors">
                CYBERGUARD
              </span>
              <span className="rounded-full bg-cyan-500/10 border border-cyan-500/30 px-1.5 py-0.2 text-[10px] font-bold font-mono text-cyan-400">
                PRO 3.0
              </span>
            </div>
            <p className="text-[10px] font-mono text-slate-400 -mt-0.5">
              AI Operations & Threat Telemetry
            </p>
          </div>
        </div>

        {/* Desktop Navigation Links */}
        <nav className="hidden lg:flex items-center gap-1">
          {navLinks.slice(0, 6).map((item) => {
            const isActive = currentPath === item.path || (item.path !== '/' && currentPath.startsWith(item.path));
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.path)}
                className={`relative px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? 'text-cyan-300 bg-cyan-950/60 border border-cyan-500/30 shadow-[0_0_12px_rgba(6,182,212,0.15)]'
                    : 'text-slate-300 hover:text-white hover:bg-white/[0.04]'
                }`}
              >
                {item.label}
              </button>
            );
          })}
        </nav>

        {/* Right Action Bar */}
        <div className="flex items-center gap-3">
          {/* Quick Search Shortcut */}
          <button
            onClick={onSearchOpen}
            className="hidden sm:flex items-center gap-2 rounded-xl border border-white/10 bg-slate-900/60 px-3 py-1.5 text-xs text-slate-400 hover:border-cyan-500/40 hover:text-slate-200 transition-all duration-200"
          >
            <Search className="w-3.5 h-3.5 text-slate-400" />
            <span className="font-sans">Search suites...</span>
            <kbd className="inline-flex items-center gap-0.5 rounded border border-white/10 bg-white/5 px-1.5 py-0.5 font-mono text-[10px] text-slate-400">
              <Command className="w-2.5 h-2.5" /> K
            </kbd>
          </button>

          {/* Engine Status Beacon */}
          <div className="hidden sm:inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-950/40 px-3 py-1 text-[11px] font-mono font-semibold text-emerald-400">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>SEC-ENGINE ONLINE</span>
          </div>

          {/* Mobile Menu Toggle Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="flex lg:hidden h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-slate-900/60 text-slate-300 hover:text-white"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-white/[0.08] bg-slate-950/95 p-4 backdrop-blur-2xl">
          <div className="flex flex-col gap-1.5">
            {navLinks.map((item) => {
              const isActive = currentPath === item.path;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onNavigate(item.path);
                    setMobileMenuOpen(false);
                  }}
                  className={`flex items-center justify-between rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-150 ${
                    isActive
                      ? 'bg-cyan-950/80 border border-cyan-500/30 text-cyan-300'
                      : 'text-slate-300 hover:bg-white/[0.04]'
                  }`}
                >
                  <span>{item.label}</span>
                  {item.badge && (
                    <span className="rounded-full bg-cyan-500/20 px-2 py-0.5 text-[10px] font-mono text-cyan-300">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
