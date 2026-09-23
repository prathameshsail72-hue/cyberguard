import React from 'react';
import { ShieldCheck, Activity, AlertTriangle, CheckCircle2, Database, Gauge, Zap } from 'lucide-react';
import { SystemMetric } from '../types';

interface QuickStatsBarProps {
  metrics?: SystemMetric[];
}

const defaultMetrics: SystemMetric[] = [
  {
    id: 'total-audits',
    label: 'Total Security Audits',
    value: '24',
    subValue: 'Live DB Scans',
    change: '+18% this week',
    isPositive: true,
    statusColor: 'cyan',
    iconName: 'Activity'
  },
  {
    id: 'health-score',
    label: 'Avg Cyber Health Score',
    value: '84.6',
    subValue: '/ 100 benchmark',
    change: 'Optimal Posture',
    isPositive: true,
    statusColor: 'emerald',
    iconName: 'Gauge'
  },
  {
    id: 'high-threats',
    label: 'High Risk Mitigations',
    value: '3',
    subValue: 'Flagged & Neutralized',
    change: '100% Resolved',
    isPositive: true,
    statusColor: 'rose',
    iconName: 'AlertTriangle'
  },
  {
    id: 'engine-status',
    label: 'Engine Telemetry',
    value: '99.9%',
    subValue: 'Obsidian 3.0 Core',
    change: 'Operational',
    isPositive: true,
    statusColor: 'emerald',
    iconName: 'ShieldCheck'
  }
];

const colorMaps = {
  cyan: {
    border: 'border-cyan-500/20 hover:border-cyan-400/40',
    icon: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30',
    val: 'text-cyan-300',
    glow: 'group-hover:shadow-[0_0_20px_rgba(6,182,212,0.15)]'
  },
  emerald: {
    border: 'border-emerald-500/20 hover:border-emerald-400/40',
    icon: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
    val: 'text-emerald-300',
    glow: 'group-hover:shadow-[0_0_20px_rgba(16,185,129,0.15)]'
  },
  amber: {
    border: 'border-amber-500/20 hover:border-amber-400/40',
    icon: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
    val: 'text-amber-300',
    glow: 'group-hover:shadow-[0_0_20px_rgba(245,158,11,0.15)]'
  },
  rose: {
    border: 'border-rose-500/20 hover:border-rose-400/40',
    icon: 'text-rose-400 bg-rose-500/10 border-rose-500/30',
    val: 'text-rose-300',
    glow: 'group-hover:shadow-[0_0_20px_rgba(244,63,94,0.15)]'
  }
};

const iconRenderers: Record<string, React.ReactNode> = {
  Activity: <Activity className="w-5 h-5" />,
  Gauge: <Gauge className="w-5 h-5" />,
  AlertTriangle: <AlertTriangle className="w-5 h-5" />,
  ShieldCheck: <ShieldCheck className="w-5 h-5" />,
  Database: <Database className="w-5 h-5" />
};

export const QuickStatsBar: React.FC<QuickStatsBarProps> = ({
  metrics = defaultMetrics
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5">
      {metrics.map((m) => {
        const theme = colorMaps[m.statusColor] || colorMaps.cyan;

        return (
          <div
            key={m.id}
            className={`group relative overflow-hidden rounded-2xl border bg-slate-900/50 p-5 backdrop-blur-xl transition-all duration-300 hover:scale-[1.02] hover:bg-slate-900/80 ${theme.border} ${theme.glow}`}
          >
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 font-mono">
                  {m.label}
                </span>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className={`text-3xl font-extrabold tracking-tight font-mono ${theme.val}`}>
                    {m.value}
                  </span>
                  {m.subValue && (
                    <span className="text-xs text-slate-400 font-medium">
                      {m.subValue}
                    </span>
                  )}
                </div>
              </div>

              <div className={`flex h-10 w-10 items-center justify-center rounded-xl border backdrop-blur-md transition-transform duration-200 group-hover:scale-110 ${theme.icon}`}>
                {iconRenderers[m.iconName] || <Zap className="w-5 h-5" />}
              </div>
            </div>

            {m.change && (
              <div className="mt-4 flex items-center gap-1.5 text-xs font-medium">
                <span className={`inline-block h-1.5 w-1.5 rounded-full ${m.isPositive ? 'bg-emerald-400 shadow-[0_0_6px_#34d399]' : 'bg-rose-400'}`} />
                <span className={m.isPositive ? 'text-emerald-400' : 'text-rose-400'}>
                  {m.change}
                </span>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default QuickStatsBar;
