import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import HomePage from './HomePage';
import BreadcrumbNav from './BreadcrumbNav';
import { BreadcrumbItem } from '../types';

// Mock sub-views for demonstration and zero-reload SPA navigation
const URLAnalyzerView: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [url, setUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleScan = () => {
    if (!url.trim()) return;
    setIsScanning(true);
    setTimeout(() => {
      setIsScanning(false);
      setResult({
        score: 95,
        risk: 'Low Risk',
        ssl: 'Valid TLS 1.3 Certificate (Let\'s Encrypt Authority)',
        headers: ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options: DENY']
      });
    }, 900);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <BreadcrumbNav 
        items={[{ label: 'Website Security & SSL', path: '/url-analyzer', active: true }]} 
        onNavigate={onNavigate} 
      />

      <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-8 backdrop-blur-2xl">
        <h2 className="text-2xl font-bold text-white">🌐 Website Security & SSL Audit Inspector</h2>
        <p className="mt-2 text-sm text-slate-300">
          Probe SSL/TLS handshake latency, DNS nameserver propagation, security response headers, and domain entropy.
        </p>

        <div className="mt-6 flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="flex-1 rounded-xl border border-white/10 bg-slate-950/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-cyan-400 focus:outline-none"
          />
          <button
            onClick={handleScan}
            disabled={isScanning}
            className="rounded-xl bg-cyan-500 px-6 py-3 text-sm font-bold text-slate-950 hover:bg-cyan-400 transition-all duration-200 disabled:opacity-50"
          >
            {isScanning ? 'Analyzing Domain...' : 'Audit Target'}
          </button>
        </div>

        {result && (
          <div className="mt-6 rounded-2xl border border-cyan-500/30 bg-cyan-950/20 p-6 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-mono text-cyan-400 font-bold">SAFETY SCORE: {result.score}/100</span>
              <span className="rounded-full bg-emerald-950 border border-emerald-500/40 px-3 py-1 text-xs font-bold text-emerald-400">
                {result.risk}
              </span>
            </div>
            <div className="text-xs font-mono text-slate-300 space-y-1">
              <div>🔒 <strong>SSL Status:</strong> {result.ssl}</div>
              <div>🛡️ <strong>Security Headers:</strong> {result.headers.join(', ')}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const PhishingView: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <BreadcrumbNav 
        items={[{ label: 'Phishing Detector', path: '/phishing-scan', active: true }]} 
        onNavigate={onNavigate} 
      />
      <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-8 backdrop-blur-2xl">
        <h2 className="text-2xl font-bold text-white">🎣 AI Phishing & Social Engineering Shield</h2>
        <p className="mt-2 text-sm text-slate-300">
          Paste suspicious email text, SMS bodies, or prompt injections to detect deceptive patterns.
        </p>
        <textarea
          rows={5}
          placeholder="Paste message body here..."
          className="mt-6 w-full rounded-xl border border-white/10 bg-slate-950/80 p-4 text-sm text-white placeholder-slate-500 focus:border-indigo-400 focus:outline-none font-mono"
        />
        <button className="mt-4 rounded-xl bg-indigo-500 px-6 py-3 text-sm font-bold text-white hover:bg-indigo-400 transition-all">
          Inspect Payload
        </button>
      </div>
    </div>
  );
};

const PasswordView: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <BreadcrumbNav 
        items={[{ label: 'Password Entropy', path: '/password-checker', active: true }]} 
        onNavigate={onNavigate} 
      />
      <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-8 backdrop-blur-2xl">
        <h2 className="text-2xl font-bold text-white">🔑 Mathematical Password Entropy Analyzer</h2>
        <p className="mt-2 text-sm text-slate-300">
          Calculate Shannon entropy, character diversity, and GPU cluster brute-force resistance.
        </p>
        <input
          type="password"
          placeholder="Enter password to evaluate..."
          className="mt-6 w-full rounded-xl border border-white/10 bg-slate-950/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-emerald-400 focus:outline-none"
        />
        <button className="mt-4 rounded-xl bg-emerald-500 px-6 py-3 text-sm font-bold text-slate-950 hover:bg-emerald-400 transition-all">
          Calculate Entropy
        </button>
      </div>
    </div>
  );
};

const FileIntegrityView: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <BreadcrumbNav 
        items={[{ label: 'File Integrity', path: '/file-security', active: true }]} 
        onNavigate={onNavigate} 
      />
      <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-8 backdrop-blur-2xl">
        <h2 className="text-2xl font-bold text-white">📁 File Integrity & Magic Byte Verifier</h2>
        <p className="mt-2 text-sm text-slate-300">
          Verify SHA-256 digests and detect double-extension spoofing using binary magic signatures.
        </p>
        <div className="mt-6 rounded-2xl border-2 border-dashed border-white/20 p-8 text-center bg-slate-950/40">
          <p className="text-sm text-slate-400">Drag and drop file here or browse files</p>
        </div>
      </div>
    </div>
  );
};

export const AppRouter: React.FC = () => {
  const [currentPath, setCurrentPath] = useState<string>(() => {
    return window.location.pathname || '/';
  });

  // Client-side routing with browser history push state
  const handleNavigate = (path: string) => {
    setCurrentPath(path);
    window.history.pushState({}, '', path);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  useEffect(() => {
    const handlePopState = () => {
      setCurrentPath(window.location.pathname || '/');
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const renderActiveView = () => {
    switch (currentPath) {
      case '/url-analyzer':
        return <URLAnalyzerView onNavigate={handleNavigate} />;
      case '/phishing-scan':
        return <PhishingView onNavigate={handleNavigate} />;
      case '/password-checker':
        return <PasswordView onNavigate={handleNavigate} />;
      case '/file-security':
        return <FileIntegrityView onNavigate={handleNavigate} />;
      case '/':
      default:
        return <HomePage onNavigate={handleNavigate} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#030712] text-slate-100 font-sans selection:bg-cyan-500 selection:text-slate-950">
      {/* Background ambient gradient glow */}
      <div className="fixed inset-0 pointer-events-none bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(14,165,233,0.15),rgba(255,255,255,0))]" />
      
      {/* Persistent Navigation Bar */}
      <Navbar currentPath={currentPath} onNavigate={handleNavigate} />

      {/* Main Content Area */}
      <main className="relative z-10 px-4 sm:px-6 lg:px-8 py-6">
        {renderActiveView()}
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/[0.08] bg-slate-950/80 py-8 text-center text-xs text-slate-500 font-mono">
        <p>© 2026 CYBERGUARD PRO | Next-Gen AI Security Operations & Threat Telemetry</p>
      </footer>
    </div>
  );
};

export default AppRouter;
