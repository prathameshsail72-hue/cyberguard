import React, { useState, useMemo } from 'react';
import { 
  ShieldCheck, 
  Search, 
  Layers, 
  Shield, 
  KeyRound, 
  Fish, 
  Globe, 
  FileCheck2, 
  Gamepad2, 
  BarChart3,
  SlidersHorizontal,
  Sparkles,
  Zap,
  Terminal,
  Clock,
  ArrowUpRight
} from 'lucide-react';
import HeroHeader from './HeroHeader';
import QuickStatsBar from './QuickStatsBar';
import FeatureCard from './FeatureCard';
import { FeatureItem } from '../types';

interface HomePageProps {
  onNavigate: (route: string) => void;
}

const ALL_FEATURES: FeatureItem[] = [
  {
    id: 'dashboard',
    title: 'Threat Intelligence & Analytics',
    category: 'audit',
    badge: 'REAL-TIME',
    badgeVariant: 'cyan',
    iconName: 'BarChart3',
    description: 'Centralized live telemetry dashboard tracking global scan volumes, health score distributions, and vulnerability resolution queues.',
    highlights: ['Multi-Engine Metrics', 'Risk Gauge Telemetry', 'SQLite Audit Trail'],
    route: '/dashboard',
    endpoint: '/api/stats',
    status: 'operational',
    statsLabel: 'Scans Logged',
    statsValue: '24'
  },
  {
    id: 'url-analyzer',
    title: 'Website Security & SSL Inspector',
    category: 'threat-defense',
    badge: 'ACTIVE',
    badgeVariant: 'cyan',
    iconName: 'Globe',
    description: 'Deep-probe target domains for SSL/TLS handshakes, certificate expirations, DNS records, missing security headers, and IP anomalies.',
    highlights: ['TLS Handshake Audit', 'HSTS & CSP Checks', 'DNS Resolution'],
    route: '/url-analyzer',
    endpoint: '/api/analyze-url',
    status: 'operational',
    statsLabel: 'Safety Score',
    statsValue: '95/100'
  },
  {
    id: 'phishing-detector',
    title: 'AI Phishing & Social Engineering Shield',
    category: 'threat-defense',
    badge: 'AI-POWERED',
    badgeVariant: 'violet',
    iconName: 'Fish',
    description: 'Natural language heuristic scanner that detects psychological urgency triggers, credential harvesting traps, and deceptive hyperlink cloaks.',
    highlights: ['Urgency Cue Parsing', 'Deceptive Link Extraction', 'Heuristic Threat Score'],
    route: '/phishing-scan',
    endpoint: '/api/analyze-phishing',
    status: 'operational',
    statsLabel: 'Detection Rate',
    statsValue: '99.4%'
  },
  {
    id: 'password-entropy',
    title: 'Password Entropy & Crypto Hardening',
    category: 'cryptography',
    badge: 'REAL-TIME',
    badgeVariant: 'emerald',
    iconName: 'KeyRound',
    description: 'Mathematical Shannon entropy calculator measuring character pool diversity, dictionary collision checks, and multi-threaded GPU crack times.',
    highlights: ['Shannon Entropy (Bits)', 'GPU Cluster Crack Calc', 'Weak List Crosscheck'],
    route: '/password-checker',
    endpoint: '/api/check-password',
    status: 'operational',
    statsLabel: 'Pool Space',
    statsValue: '94 chars'
  },
  {
    id: 'file-integrity',
    title: 'File Integrity & Header Magic Verifier',
    category: 'audit',
    badge: 'ACTIVE',
    badgeVariant: 'amber',
    iconName: 'FileCheck2',
    description: 'Forensic file inspector validating magic hex byte signatures against reported extensions to expose double-extension spoofing and malware disguise.',
    highlights: ['SHA-256 & MD5 Hash', 'Magic Byte Signatures', 'Extension Mask Detector'],
    route: '/file-security',
    endpoint: '/api/check-file',
    status: 'operational',
    statsLabel: 'Verification',
    statsValue: 'Instant'
  },
  {
    id: 'cyber-quiz',
    title: 'Cyber Security Challenge & Quiz Hub',
    category: 'education',
    badge: 'INTERACTIVE',
    badgeVariant: 'violet',
    iconName: 'Gamepad2',
    description: 'Interactive gamified cyber ethics and threat defense arena designed to test practitioner awareness against modern attack vectors.',
    highlights: ['Scenario Simulators', 'Real-Time Scoring', 'Community Benchmarking'],
    route: '/cyber-quiz',
    endpoint: '/api/quiz',
    status: 'active',
    statsLabel: 'Scenarios',
    statsValue: '10 Modules'
  }
];

type CategoryFilter = 'all' | 'threat-defense' | 'cryptography' | 'audit' | 'education';

export const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<CategoryFilter>('all');

  // Filtered features list based on search and category
  const filteredFeatures = useMemo(() => {
    return ALL_FEATURES.filter((feature) => {
      const matchesCategory = selectedCategory === 'all' || feature.category === selectedCategory;
      const matchesSearch = 
        feature.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        feature.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        feature.highlights.some(h => h.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchesCategory && matchesSearch;
    });
  }, [searchQuery, selectedCategory]);

  return (
    <div className="min-h-screen pb-20 pt-6">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-10">
        
        {/* Top Hero Section */}
        <HeroHeader 
          onQuickStart={() => {
            const el = document.getElementById('feature-directory');
            el?.scrollIntoView({ behavior: 'smooth' });
          }} 
        />

        {/* Real-Time Telemetry Metrics Ribbon */}
        <section aria-label="System Metrics">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400 font-mono">
                Real-Time Security Posture & Telemetry
              </h2>
            </div>
            <span className="text-xs font-mono text-slate-500">Live Auto-Sync</span>
          </div>
          <QuickStatsBar />
        </section>

        {/* Feature Directory Section */}
        <section id="feature-directory" className="space-y-6 pt-4">
          
          {/* Section Header with Dynamic Controls */}
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/[0.08] pb-6">
            <div>
              <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-cyan-400 font-mono">
                <Layers className="w-3.5 h-3.5" />
                <span>Modular Defense Suites</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white mt-1">
                Security Capabilities & Tools
              </h2>
              <p className="text-sm text-slate-400 mt-1 max-w-xl">
                Select an operational suite below to launch targeted threat scans, inspect cryptosystems, or analyze data payloads.
              </p>
            </div>

            {/* Filter Pills & Search Input */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
              {/* Search Bar */}
              <div className="relative">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Filter security modules..."
                  className="w-full sm:w-64 rounded-xl border border-white/10 bg-slate-900/80 pl-10 pr-4 py-2 text-xs text-white placeholder-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-1 focus:ring-cyan-400/50 backdrop-blur-md transition-all font-sans"
                />
              </div>

              {/* Category Dropdown/Selector */}
              <div className="flex items-center gap-1.5 p-1 rounded-xl border border-white/10 bg-slate-900/60 backdrop-blur-md overflow-x-auto">
                {(['all', 'threat-defense', 'cryptography', 'audit', 'education'] as CategoryFilter[]).map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`rounded-lg px-2.5 py-1 text-xs font-semibold whitespace-nowrap transition-all duration-150 ${
                      selectedCategory === cat
                        ? 'bg-cyan-500 text-slate-950 font-bold shadow-[0_0_12px_rgba(6,182,212,0.3)]'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                    }`}
                  >
                    {cat === 'all' ? 'All Modules' : cat.replace('-', ' ')}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Feature Grid */}
          {filteredFeatures.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredFeatures.map((feature) => (
                <FeatureCard
                  key={feature.id}
                  feature={feature}
                  onNavigate={onNavigate}
                />
              ))}
            </div>
          ) : (
            <div className="rounded-2xl border border-white/10 bg-slate-900/40 p-12 text-center backdrop-blur-xl">
              <Shield className="w-12 h-12 text-slate-500 mx-auto mb-3 opacity-50" />
              <h3 className="text-lg font-bold text-slate-300">No matching security modules found</h3>
              <p className="text-xs text-slate-500 mt-1">Try clearing your search query or selecting a different category filter.</p>
              <button
                onClick={() => { setSearchQuery(''); setSelectedCategory('all'); }}
                className="mt-4 inline-flex items-center gap-1.5 rounded-lg border border-cyan-500/30 bg-cyan-950/60 px-4 py-1.5 text-xs font-semibold text-cyan-300 hover:bg-cyan-900/60"
              >
                Reset All Filters
              </button>
            </div>
          )}
        </section>

        {/* Quick Launchpad Terminal Banner */}
        <section className="rounded-2xl border border-white/10 bg-gradient-to-r from-slate-900/90 via-slate-900/60 to-slate-950/90 p-6 backdrop-blur-xl">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
                <Terminal className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Direct CLI & API Integration</h3>
                <p className="text-xs text-slate-400 mt-0.5 font-mono">
                  cyberguard-cli --scan-all --format=json --output=./reports/audit.json
                </p>
              </div>
            </div>

            <button
              onClick={() => onNavigate('/dashboard')}
              className="inline-flex items-center gap-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-white/10 px-4 py-2.5 text-xs font-semibold text-white transition-all duration-200"
            >
              <span>View Audit Logs</span>
              <ArrowUpRight className="w-4 h-4 text-cyan-400" />
            </button>
          </div>
        </section>

      </div>
    </div>
  );
};

export default HomePage;
