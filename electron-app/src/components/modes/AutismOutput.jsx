import { useApp } from '../../context/AppContext';
import { AlignLeft, LayoutList } from 'lucide-react';

export default function AutismOutput() {
  const { outputText } = useApp();

  // Format the output by splitting into distinct, clear paragraphs
  const paragraphs = outputText.split('\n').filter(p => p.trim());

  return (
    <div className="flex flex-col h-full bg-[var(--color-surface)] relative p-8 overflow-y-auto font-sans">
      <div className="flex justify-between items-center bg-[var(--color-bg)] p-3 rounded-lg border border-[var(--color-border)] mb-8">
        <span className="font-semibold text-sm flex items-center gap-2">
          <AlignLeft size={16} className="text-[var(--color-primary)]" />
          Literal Clarity Mode
        </span>
        <span className="text-xs text-[var(--color-muted)] font-medium uppercase tracking-wider bg-white px-2 py-1 rounded shadow-sm border border-[var(--color-border)]">
          Direct Context
        </span>
      </div>

      <div className="flex-1 space-y-8 max-w-2xl mx-auto w-full">
        {paragraphs.map((para, idx) => (
          <div key={idx} className="flex gap-4">
            <div className="text-[var(--color-muted)] mt-1">
              <LayoutList size={20} />
            </div>
            <p className="text-[var(--color-text)] text-[1.1rem] leading-loose">
              {para}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
