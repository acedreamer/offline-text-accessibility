import { useApp } from '../../context/AppContext';
import { Settings, Sparkles, SpellCheck2, Brain, ActivitySquare, LayoutPanelLeft } from 'lucide-react';

export default function Header() {
  const { mode, setMode, handleSimplify, isLoading, setSettingsOpen } = useApp();

  return (
    <header className="flex items-center justify-between p-4 border-b border-[var(--color-border)] bg-[var(--color-surface)]">
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <div className="bg-[var(--color-primary)] text-white p-2 rounded-lg">
            <SpellCheck2 size={24} />
          </div>
          <span className="font-bold text-lg tracking-tight">SimplifyAI</span>
        </div>

        <div className="relative">
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="appearance-none bg-[var(--color-bg)] border border-[var(--color-border)] rounded-md py-2 pl-10 pr-10 font-medium focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]"
          >
            <option value="dyslexia">Dyslexia Friendly</option>
            <option value="adhd">ADHD Focus</option>
            <option value="autism">Literal Clarity</option>
          </select>
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-muted)]">
            {mode === 'dyslexia' && <LayoutPanelLeft size={16} />}
            {mode === 'adhd' && <ActivitySquare size={16} />}
            {mode === 'autism' && <Brain size={16} />}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={handleSimplify}
          disabled={isLoading}
          className="flex items-center gap-2 bg-[var(--color-primary)] text-white px-4 py-2 rounded-md font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          {isLoading ? (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <Sparkles size={18} />
          )}
          Simplify Text
        </button>
        <button
          onClick={() => setSettingsOpen(true)}
          className="p-2 text-[var(--color-text)] hover:bg-[var(--color-bg)] rounded-md transition-colors"
          aria-label="Settings"
        >
          <Settings size={20} />
        </button>
        <div className="w-8 h-8 rounded-full bg-[var(--color-bg)] border border-[var(--color-border)] flex items-center justify-center font-bold text-sm">
          JD
        </div>
      </div>
    </header>
  );
}
