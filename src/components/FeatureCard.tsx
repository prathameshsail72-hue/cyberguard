import React from 'react';
import { 
  ShieldCheck, 
  Globe, 
  Fish, 
  KeyRound, 
  FileCheck2, 
  BarChart3, 
  Gamepad2, 
  ArrowRight, 
  ExternalLink,
  Sparkles,
  Zap,
  CheckCircle2,
  Lock
} from 'lucide-react';
import { FeatureItem } from '../types';

interface FeatureCardProps {
  feature: FeatureItem;
  onNavigate: (route: string) => void;
  variant?: 'compact' | 'expanded';
}

const iconMap: Record<string, React.ReactNode> = {
  ShieldCheck: <ShieldCheck className="w-7 h-7" />,
  Globe: <Globe className="w-7 h-7" />,
  Fish: <Fish className="w-7 h-7" />,
  KeyRound: <KeyRound className="w-7 h-7" />,
  FileCheck2: <FileCheck2 className="w-7 h-7" />,
  BarChart3: <BarChart3 className="w-7 h-7" />,
  Gamepad2: <Gamepad2 className="w-7 h-7" />,
  Zap: <Zap className="w-7 h-7" />,
  Lock: <Lock className="w-7 h-7" />
};

const badgeStyles = {
  cyan: {
    bg: 'bg-cyan-950/60 border-cyan-500/30 text-cyan-400 shadow-[0_0_12px_rgba(6,182,212,0.15)]',
    dot: 'bg-cyan-400 shadow-[0_0_8px_#22d3ee]'
  },
  violet: {
    bg: 'bg-indigo-950/60 border-indigo-500/30 text-indigo-300 shadow-[0_0_12px_rgba(99,102,241,0.15)]',
    dot: 'bg-indigo-400 shadow-[0_0_8px_#818cf8]'
  },
  emerald: {
    bg: 'bg-emerald-950/60 border-emerald-500/30 text-emerald-400 shadow-[0_0_12px_rgba(16,185,129,0.15)]',
    dot: 'bg-emerald-400 shadow-[0_0_8px_#34d399]'
  },
  amber: {
    bg: 'bg-amber-950/60 border-amber-500/30 text-amber-300 shadow-[0_0_12px_rgba(245,158,11,0.15)]',
    dot: 'bg-amber-400 shadow-[0_0_8px_#fbbf24]'
  }
};

const accentGradients = {
  cyan: 'from-cyan-500/20 via-sky-500/5 to-transparent group-hover:from-cyan-500/30',
  violet: 'from-indigo-500/20 via-purple-500/5 to-transparent group-hover:from-indigo-500/30',
  emerald: 'from-emerald-500/20 via-teal-500/5 to-transparent group-hover:from-emerald-500/30',
  amber: 'from-amber-500/20 via-orange-500/5 to-transparent group-hover:from-amber-500/30'
};

const iconContainers = {
  cyan: 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400 shadow-[0_0_20px_rgba(6,182,212,0.2)] group-hover:border-cyan-400 group-hover:bg-cyan-500/20',
  violet: 'bg-indigo-500/10 border-indigo-500/30 text-indigo-300 shadow-[0_0_20px_rgba(99,102,241,0.2)] group-hover:border-indigo-400 group-hover:bg-indigo-500/20',
  emerald: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400 shadow-[0_0_20px_rgba(16,185,129,0.2)] group-hover:border-emerald-400 group-hover:bg-emerald-500/20',
  amber: 'bg-amber-500/10 border-amber-500/30 text-amber-300 shadow-[0_0_20px_rgba(245,158,11,0.2)] group-hover:border-amber-400 group-hover:bg-amber-500/20'
};

export const FeatureCard: React.FC<FeatureCardProps> = ({
  feature,
  onNavigate
}) => {
  const badgeConfig = badgeStyles[feature.badgeVariant] || badgeStyles.cyan;
  const gradientConfig = accentGradients[feature.badgeVariant] || accentGradients.cyan;
  const iconContainerConfig = iconContainers[feature.badgeVariant] || iconContainers.cyan;

  return (
    <div
      onClick={() => onNavigate(feature.route)}
      className="group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-white/10 bg-slate-900/60 p-6 md:p-7 backdrop-blur-xl transition-all duration-300 hover:scale-[1.02] hover:border-cyan-500/40 hover:bg-slate-900/80 hover:shadow-[0_12px_40px_rgba(0,0,0,0.5),0_0_25px_rgba(56,189,248,0.12)] cursor-pointer"
    >
      {/* Background ambient corner gradient */}
      <div 
        className={`absolute -right-20 -top-20 h-56 w-56 rounded-full bg-gradient-to-br ${gradientConfig} blur-2xl transition-all duration-500 group-hover:scale-125`} 
      />

      {/* Top Bar: Icon + Badge */}
      <div className="relative z-10 flex items-start justify-between gap-4">
        <div className={`flex h-14 w-14 items-center justify-center rounded-xl border backdrop-blur-md transition-all duration-300 group-hover:rotate-2 ${iconContainerConfig}`}>
          {iconMap[feature.iconName] || <ShieldCheck className="w-7 h-7" />}
        </div>

        <div className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-[11px] font-bold tracking-wider uppercase transition-all duration-200 ${badgeConfig.bg}`}>
          <span className={`h-1.5 w-1.5 rounded-full animate-pulse ${badgeConfig.dot}`} />
          {feature.badge}
        </div>
      </div>

      {/* Title & Body Description */}
      <div className="relative z-10 mt-5 flex-1">
        <h3 className="text-xl font-bold tracking-tight text-white transition-colors duration-200 group-hover:text-cyan-300">
          {feature.title}
        </h3>
        <p className="mt-2.5 text-sm leading-relaxed text-slate-300/90 font-normal">
          {feature.description}
        </p>

        {/* Feature Highlights / Bullet Pills */}
        {feature.highlights && feature.highlights.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {feature.highlights.map((item, idx) => (
              <span
                key={idx}
                className="inline-flex items-center gap-1 rounded-md bg-white/[0.04] border border-white/5 px-2.5 py-0.5 text-xs text-slate-400 font-mono"
              >
                <CheckCircle2 className="w-3 h-3 text-cyan-400/80" />
                {item}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Footer CTA & Telemetry info */}
      <div className="relative z-10 mt-6 pt-4 border-t border-white/[0.08] flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
          {feature.statsLabel && (
            <span>
              {feature.statsLabel}: <strong className="text-slate-200">{feature.statsValue}</strong>
            </span>
          )}
        </div>

        {/* Interactive CTA Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onNavigate(feature.route);
          }}
          className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-sky-500/20 to-cyan-500/20 border border-sky-500/30 px-3.5 py-1.5 text-xs font-semibold text-cyan-300 transition-all duration-200 group-hover:border-cyan-400 group-hover:bg-cyan-500 group-hover:text-slate-950 group-hover:shadow-[0_0_15px_rgba(6,182,212,0.4)]"
        >
          <span>Launch Module</span>
          <ArrowRight className="w-3.5 h-3.5 transition-transform duration-200 group-hover:translate-x-1" />
        </button>
      </div>
    </div>
  );
};

export default FeatureCard;
