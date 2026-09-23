export interface FeatureItem {
  id: string;
  title: string;
  category: 'threat-defense' | 'cryptography' | 'audit' | 'education';
  badge: 'ACTIVE' | 'AI-POWERED' | 'REAL-TIME' | 'INTERACTIVE';
  badgeVariant: 'cyan' | 'violet' | 'emerald' | 'amber';
  iconName: string;
  description: string;
  highlights: string[];
  route: string;
  endpoint: string;
  status: 'operational' | 'monitoring' | 'active';
  statsLabel?: string;
  statsValue?: string;
}

export interface SystemMetric {
  id: string;
  label: string;
  value: string | number;
  subValue?: string;
  change?: string;
  isPositive?: boolean;
  statusColor: 'cyan' | 'emerald' | 'amber' | 'rose';
  iconName: string;
}

export interface NavRouteItem {
  id: string;
  label: string;
  path: string;
  iconName: string;
  badge?: string;
}
