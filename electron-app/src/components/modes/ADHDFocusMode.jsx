import { useApp } from '../../context/AppContext';
import { ArrowLeft, ArrowRight, Focus } from 'lucide-react';
import { useEffect, useRef } from 'react';

export default function ADHDFocusMode() {
  const { sentences, focusSentenceIndex, setFocusSentenceIndex } = useApp();
  const containerRef = useRef(null);

  const prevSentence = () => {
    if (focusSentenceIndex > 0) {
      setFocusSentenceIndex(focusSentenceIndex - 1);
    }
  };

  const nextSentence = () => {
    if (focusSentenceIndex < sentences.length - 1) {
      setFocusSentenceIndex(focusSentenceIndex + 1);
    }
  };

  useEffect(() => {
    // Scroll active sentence into view
    if (containerRef.current) {
      const activeEl = containerRef.current.querySelector('.active-sentence');
      if (activeEl) {
        activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }, [focusSentenceIndex]);

  return (
    <div className="flex flex-col h-full bg-[var(--color-surface)] relative p-6">
      <div className="flex justify-between items-center bg-[var(--color-bg)] p-3 rounded-lg border border-[var(--color-border)] mb-4">
        <span className="font-semibold text-sm flex items-center gap-2">
          <Focus size={16} className="text-[var(--color-primary)]" />
          Focus Layer: Sentence {focusSentenceIndex + 1} of {sentences.length}
        </span>
        <div className="flex gap-2">
          <button
            onClick={prevSentence}
            disabled={focusSentenceIndex === 0}
            className="flex items-center gap-1 px-3 py-1 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-md hover:bg-[var(--color-bg)] disabled:opacity-50 transition-colors"
          >
            <ArrowLeft size={16} /> Prev
          </button>
          <button
            onClick={nextSentence}
            disabled={focusSentenceIndex === sentences.length - 1}
            className="flex items-center gap-1 px-3 py-1 bg-[var(--color-primary)] text-white rounded-md hover:opacity-90 disabled:opacity-50 transition-colors"
          >
            Next <ArrowRight size={16} />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pr-2" ref={containerRef}>
        {sentences.map((sentence, index) => {
          const isActive = index === focusSentenceIndex;
          return (
            <p
              key={index}
              className={`text-xl leading-relaxed transition-all duration-300 ${
                isActive
                  ? 'active-sentence font-medium text-[var(--color-text)] shadow-sm'
                  : 'dimmed-text hover:opacity-60 cursor-pointer'
              }`}
              onClick={() => setFocusSentenceIndex(index)}
            >
              {sentence}
            </p>
          );
        })}
      </div>
    </div>
  );
}
