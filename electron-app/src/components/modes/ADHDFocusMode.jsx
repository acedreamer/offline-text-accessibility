import { useApp } from '../../context/AppContext';
import { ArrowLeft, ArrowRight, Focus } from 'lucide-react';
import { useEffect, useRef } from 'react';

function parseLine(line) {
  const markerMatch = line.match(/^\[(\d+)\/(\d+)\]\s*-\s*/);
  const marker = markerMatch ? { current: markerMatch[1], total: markerMatch[2] } : null;
  const text = markerMatch ? line.slice(markerMatch[0].length) : line;

  const parts = text.split(/(\*\*.*?\*\*)/g);
  const rendered = parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} className="text-[var(--color-primary)] font-bold">{part.slice(2, -2)}</strong>;
    }
    return part;
  });

  return { marker, rendered };
}

export default function ADHDFocusMode() {
  const { sentences, focusSentenceIndex, setFocusSentenceIndex } = useApp();
  const containerRef = useRef(null);

  const prevSentence = () => {
    if (focusSentenceIndex > 0) setFocusSentenceIndex(focusSentenceIndex - 1);
  };

  const nextSentence = () => {
    if (focusSentenceIndex < sentences.length - 1) setFocusSentenceIndex(focusSentenceIndex + 1);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
      e.preventDefault();
      nextSentence();
    } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
      e.preventDefault();
      prevSentence();
    }
  };

  useEffect(() => {
    if (containerRef.current) {
      const activeEl = containerRef.current.querySelector('.active-sentence');
      if (activeEl) {
        // Check if reduce motion is enabled
        const reduceMotion = document.body.classList.contains('reduce-motion');
        activeEl.scrollIntoView({
          behavior: reduceMotion ? 'auto' : 'smooth',
          block: 'center'
        });
      }
    }
  }, [focusSentenceIndex]);

  return (
    <div
      className="flex flex-col bg-[var(--color-surface)] relative p-6 min-h-full outline-none"
      tabIndex={0}
      onKeyDown={handleKeyDown}
    >
      <div className="flex justify-between items-center bg-[var(--color-bg)] p-3 rounded-lg border border-[var(--color-border)] mb-4 sticky top-0 z-10">
        <span className="font-semibold text-sm flex items-center gap-2">
          <Focus size={16} className="text-[var(--color-primary)]" />
          {sentences.length > 0 ? (
            `Focus Layer: Sentence ${focusSentenceIndex + 1} of ${sentences.length}`
          ) : (
            <span className="text-[var(--color-muted)]">No content to display</span>
          )}
        </span>
        <div className="flex items-center gap-3">
          <span className="text-xs text-[var(--color-muted)] hidden sm:inline">↑↓ arrow keys</span>
          <div className="flex gap-2">
            <button
              onClick={prevSentence}
              disabled={focusSentenceIndex === 0 || sentences.length === 0}
              className="flex items-center gap-1 px-3 py-1 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-md hover:bg-[var(--color-bg)] disabled:opacity-50 transition-colors"
            >
              <ArrowLeft size={16} /> Prev
            </button>
            <button
              onClick={nextSentence}
              disabled={focusSentenceIndex === sentences.length - 1 || sentences.length === 0}
              className="flex items-center gap-1 px-3 py-1 bg-[var(--color-primary)] text-[var(--color-on-primary)] rounded-md hover:opacity-90 disabled:opacity-50 transition-colors"
            >
              Next <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </div>

      <div className="space-y-4 pr-2" ref={containerRef}>
        {sentences.length > 0 ? (
          sentences.map((sentence, index) => {
            const isActive = index === focusSentenceIndex;
            const { marker, rendered } = parseLine(sentence);
            return (
              <div
                key={index}
                className={`transition-all duration-300 ${
                  isActive
                    ? 'active-sentence shadow-sm pulse-subtle'
                    : 'dimmed-text hover:opacity-60 cursor-pointer'
                }`}
                onClick={() => setFocusSentenceIndex(index)}
              >
                {marker && (
                  <span className="inline-block text-xs font-bold px-2 py-0.5 rounded-full bg-[var(--color-primary)] text-[var(--color-on-primary)] mr-2 align-middle">
                    {marker.current}/{marker.total}
                  </span>
                )}
                <span className="text-xl leading-relaxed font-medium text-[var(--color-text)]">
                  {rendered}
                </span>
              </div>
            );
          })
        ) : (
          <div className="text-[var(--color-text)] text-center py-8">
            No content to display
          </div>
        )}
      </div>
    </div>
  );
}
