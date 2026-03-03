import { useApp } from '../../context/AppContext';
import { Volume2, Focus } from 'lucide-react';
import { useState } from 'react';

export default function DyslexiaOutput() {
  const { outputText } = useApp();
  const [isPlaying, setIsPlaying] = useState(false);

  // For this simple version, we'll split by newlines for paragraphs
  const paragraphs = outputText.split('\n').filter(p => p.trim());

  const handleListen = () => {
    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(outputText);
    utterance.onend = () => setIsPlaying(false);
    window.speechSynthesis.speak(utterance);
    setIsPlaying(true);
  };

  return (
    <div className="flex flex-col bg-[var(--color-surface)] relative p-6 space-y-4">
      <div className="flex justify-between items-center bg-[var(--color-bg)] p-3 rounded-lg border border-[var(--color-border)] mb-4 sticky top-0 z-10">
        <span className="font-semibold text-sm flex items-center gap-2">
          <Focus size={16} className="text-[var(--color-primary)]" />
          Dyslexia Mode Active
        </span>
        <button
          onClick={handleListen}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
            isPlaying ? 'bg-red-100 text-red-600 border border-red-200' : 'bg-[var(--color-primary)] text-[var(--color-on-primary)] hover:opacity-90'
          }`}
        >
          <Volume2 size={16} />
          {isPlaying ? 'Stop Listening' : 'Listen'}
        </button>
      </div>

      <div className="flex-1 space-y-6">
        {paragraphs.map((para, idx) => (
          <p key={idx} className="dyslexia-text text-[var(--color-text)] text-lg">
            {/* Very simple highlighting - real impl might need to match sentences exactly */}
            {para}
          </p>
        ))}
      </div>
    </div>
  );
}
