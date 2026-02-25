import { useApp } from '../../context/AppContext';
import { Activity } from 'lucide-react';

export default function MetricsBar() {
  const { metrics, outputText } = useApp();

  const { before, after } = metrics;
  const hasData = !!outputText;

  const renderBadge = (label, beforeVal, afterVal, inverse = false) => {
    if (!hasData) {
      return (
        <div className="flex flex-col">
          <span className="text-[10px] font-bold text-[var(--color-muted)] tracking-wider">{label}</span>
          <span className="text-sm font-mono font-medium text-[var(--color-text)]">0 → 0 (0%)</span>
        </div>
      );
    }

    const diff = afterVal - beforeVal;
    let pct = beforeVal ? Math.round((diff / beforeVal) * 100) : 0;
    const isGood = inverse ? diff > 0 : diff < 0;

    return (
      <div className="flex flex-col">
        <span className="text-[10px] font-bold text-[var(--color-muted)] tracking-wider">{label}</span>
        <div className="flex items-center gap-2">
          <span className="text-sm font-mono font-medium text-[var(--color-text)]">
            {beforeVal} → {afterVal}
          </span>
          <span className={`text-xs px-1.5 rounded font-bold ${
            isGood ? 'bg-[var(--color-badge-good)]/10 text-[var(--color-badge-good)]' : 'bg-red-500/10 text-red-600'
          }`}>
            {diff > 0 ? '+' : ''}{pct}%
          </span>
        </div>
      </div>
    );
  };

  return (
    <div className="h-16 flex items-center justify-between px-6 bg-[var(--color-bg)] border-t border-[var(--color-border)] shrink-0">
      <div className="flex items-center gap-12">
        {renderBadge('WORD COUNT', before.word_count, after.word_count, false)}
        {renderBadge('SENTENCE LENGTH', before.avg_sentence_length, after.avg_sentence_length, false)}
        {renderBadge('READABILITY (FLESCH)', Math.round(before.flesch_reading_ease), Math.round(after.flesch_reading_ease), true)}
      </div>

      <div className="flex items-center gap-3 bg-[var(--color-surface)] px-4 py-1.5 rounded-full border border-[var(--color-border)] shadow-sm">
        <span className="relative flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--color-badge-good)] opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-[var(--color-badge-good)]"></span>
        </span>
        <span className="text-sm font-medium text-[var(--color-text)] flex items-center gap-2">
          <Activity size={16} className="text-[var(--color-muted)]" />
          T5-Simplifier Ready
        </span>
      </div>
    </div>
  );
}
