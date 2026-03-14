import { useApp } from '../../context/AppContext';
import { Copy, FileText, Download, Check } from 'lucide-react';
import { useState } from 'react';
import DyslexiaOutput from '../modes/DyslexiaOutput';
import ADHDFocusMode from '../modes/ADHDFocusMode';
import AutismOutput from '../modes/AutismOutput';

export default function OutputPanel() {
  const { outputText, isLoading, mode } = useApp();
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(outputText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col min-h-0 h-full overflow-hidden bg-[var(--color-surface)] relative">
      <div className="flex items-center justify-between px-4 py-3 border-b border-[var(--color-border)]">
        <h2 className="font-semibold text-[var(--color-text)] flex items-center gap-2">
          <FileText size={18} />
          Simplified Result
        </h2>
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            disabled={!outputText}
            className="flex items-center gap-1 p-1.5 text-[var(--color-muted)] hover:text-[var(--color-text)] hover:bg-[var(--color-bg)] rounded disabled:opacity-30 transition-colors"
            title="Copy to clipboard"
          >
            {copied ? <Check size={16} className="text-green-500" /> : <Copy size={16} />}
            {copied && <span className="text-xs text-green-500 font-medium">Copied!</span>}
          </button>
          <button
            onClick={() => window.print()}
            disabled={!outputText}
            className="p-1.5 text-[var(--color-muted)] hover:text-[var(--color-text)] hover:bg-[var(--color-bg)] rounded disabled:opacity-30 transition-colors"
            title="Save as PDF"
          >
            <Download size={16} />
          </button>
        </div>
      </div>

      <div
        className="flex-1 overflow-y-auto relative bg-[var(--color-surface)] outline-none"
        tabIndex={outputText && !isLoading ? 0 : -1}
      >
        {isLoading ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="border-2 border-dashed border-[var(--color-primary)] rounded-xl p-8 flex flex-col items-center gap-4 max-w-sm text-center">
              <div className="w-8 h-8 border-4 border-[var(--color-bg)] border-t-[var(--color-primary)] rounded-full animate-spin" />
              <div>
                <h3 className="font-bold text-lg mb-1">Neuro-Adjustments Active</h3>
                <p className="text-[var(--color-muted)] text-sm">Processing text with local T5 model...</p>
              </div>
            </div>
          </div>
        ) : !outputText ? (
          <div className="absolute inset-0 flex items-center justify-center text-[var(--color-muted)]">
            <p>Click "Simplify Text" to see results here.</p>
          </div>
        ) : (
          <div className="fade-in">
            <>
              {mode === 'dyslexia' && <DyslexiaOutput />}
              {mode === 'adhd' && <ADHDFocusMode />}
              {mode === 'autism' && <AutismOutput />}
            </>
          </div>
        )}
      </div>

      <div className="px-4 py-2 border-t border-[var(--color-border)] bg-[var(--color-bg)] flex items-center justify-center gap-2 text-xs font-semibold text-[var(--color-muted)]">
        <span className="w-2 h-2 rounded-full bg-[var(--color-badge-good)] animate-pulse" />
        PROCESSED LOCALLY ON YOUR DEVICE
      </div>
    </div>
  );
}
