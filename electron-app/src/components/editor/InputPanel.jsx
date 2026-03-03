import { useApp } from '../../context/AppContext';
import { Type, AlignLeft, Bold, Italic, Trash2 } from 'lucide-react';

export default function InputPanel() {
  const { inputText, setInputText, mode } = useApp();

  const handleClear = () => setInputText('');

  // Apply dyslexia class specifically when in that mode
  const textClass = mode === 'dyslexia' ? 'dyslexia-text' : '';

  return (
    <div className="flex flex-col min-h-0 h-full overflow-hidden bg-[var(--color-bg)] border-r border-[var(--color-border)] relative">
      <div className="flex items-center justify-between px-4 py-3 bg-[var(--color-surface)] border-b border-[var(--color-border)]">
        <h2 className="font-semibold text-[var(--color-text)] flex items-center gap-2">
          <Type size={18} />
          Original Text
        </h2>
        <button
          onClick={handleClear}
          className="text-[var(--color-muted)] hover:text-red-500 transition-colors p-1"
          aria-label="Clear all"
        >
          <Trash2 size={16} />
        </button>
      </div>

      <div className="flex-1 p-4 relative">
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste or type text here that you want to simplify..."
          className={`w-full h-full resize-none outline-none bg-transparent text-[var(--color-text)] ${textClass}`}
          spellCheck="false"
        />
      </div>

      <div className="flex items-center justify-between px-4 py-2 bg-[var(--color-surface)] border-t border-[var(--color-border)] text-[var(--color-muted)] text-sm">
        <div className="flex gap-2">
          <button className="p-1.5 hover:bg-[var(--color-bg)] rounded"><Bold size={16} /></button>
          <button className="p-1.5 hover:bg-[var(--color-bg)] rounded"><Italic size={16} /></button>
          <button className="p-1.5 hover:bg-[var(--color-bg)] rounded"><AlignLeft size={16} /></button>
        </div>
        <div className="font-mono">
          {inputText.length} chars | {inputText.split(/\s+/).filter(Boolean).length} words
        </div>
      </div>
    </div>
  );
}
