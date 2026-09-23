import React from 'react';
import { Home, ChevronRight, ArrowLeft } from 'lucide-react';
import { BreadcrumbItem } from '../types';

interface BreadcrumbNavProps {
  items: BreadcrumbItem[];
  onNavigate: (path: string) => void;
  showBackButton?: boolean;
}

export const BreadcrumbNav: React.FC<BreadcrumbNavProps> = ({
  items,
  onNavigate,
  showBackButton = true
}) => {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 py-3 border-b border-white/[0.08] mb-6">
      <div className="flex items-center gap-2 text-sm">
        {/* Home Base Link */}
        <button
          onClick={() => onNavigate('/')}
          className="flex items-center gap-1.5 text-slate-400 hover:text-cyan-300 transition-colors duration-150 font-medium"
        >
          <Home className="w-4 h-4 text-cyan-400" />
          <span>Hub</span>
        </button>

        {items.map((item, index) => (
          <React.Fragment key={index}>
            <ChevronRight className="w-3.5 h-3.5 text-slate-600 flex-shrink-0" />
            {item.active ? (
              <span className="font-semibold text-cyan-300 font-mono text-xs uppercase tracking-wider bg-cyan-950/60 border border-cyan-500/30 px-2.5 py-1 rounded-md">
                {item.label}
              </span>
            ) : (
              <button
                onClick={() => onNavigate(item.path)}
                className="text-slate-400 hover:text-slate-200 transition-colors duration-150"
              >
                {item.label}
              </button>
            )}
          </React.Fragment>
        ))}
      </div>

      {showBackButton && (
        <button
          onClick={() => onNavigate('/')}
          className="inline-flex items-center gap-2 rounded-lg border border-white/10 bg-slate-900/60 px-3 py-1.5 text-xs font-semibold text-slate-300 hover:border-cyan-500/40 hover:text-cyan-300 hover:bg-slate-900 transition-all duration-200"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Return to Directory</span>
        </button>
      )}
    </div>
  );
};

export default BreadcrumbNav;
