import { useApp } from '../../context/AppContext';
import { Volume2, Focus } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';

export default function DyslexiaOutput() {
  const { outputText } = useApp();
  const [isPlaying, setIsPlaying] = useState(false);
  const [activePara, setActivePara] = useState(null);
  const paraRefs = useRef([]);

  // Handle case where speech synthesis is not available
  const speechSynthesisSupported = typeof window !== 'undefined' &&
                                  window.speechSynthesis !== undefined;

  const paragraphs = outputText.split('\n').filter(p => p.trim());

  // Build char-offset map: for each paragraph, its start index in the full spoken string.
  // Paragraphs are joined by '\n\n' in the output, so we replicate that join.
  const paraOffsets = [];
  let cursor = 0;
  const joined = paragraphs.join('\n\n');
  for (const para of paragraphs) {
    paraOffsets.push(cursor);
    cursor += para.length + 2; // +2 for the '\n\n' separator
  }

  const handleListen = () => {
    // Check if speech synthesis is supported
    if (!speechSynthesisSupported) {
      // Fallback: just show alert or do nothing silently
      return;
    }

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      setActivePara(null);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(joined);

    utterance.onboundary = (e) => {
      if (e.name !== 'word' && e.name !== 'sentence') return;
      const charIndex = e.charIndex;
      // Find which paragraph this charIndex falls in
      let active = 0;
      for (let i = 0; i < paraOffsets.length; i++) {
        if (charIndex >= paraOffsets[i]) active = i;
        else break;
      }
      setActivePara(active);
    };

    utterance.onend = () => {
      setIsPlaying(false);
      setActivePara(null);
    };

    utterance.onerror = () => {
      setIsPlaying(false);
      setActivePara(null);
    };

    window.speechSynthesis.speak(utterance);
    setIsPlaying(true);
    setActivePara(0);
  };

  // Scroll active paragraph into view
  useEffect(() => {
    if (activePara !== null && paraRefs.current[activePara]) {
      // Check if reduce motion is enabled
      const reduceMotion = document.body.classList.contains('reduce-motion');
      paraRefs.current[activePara].scrollIntoView({
        behavior: reduceMotion ? 'auto' : 'smooth',
        block: 'center'
      });
    }
  }, [activePara]);

  // Cancel speech if component unmounts or text changes
  useEffect(() => {
    return () => {
      if (speechSynthesisSupported) {
        window.speechSynthesis.cancel();
      }
    };
  }, [outputText]);

  return (
    <div className="flex flex-col bg-[var(--color-surface)] relative p-6 space-y-4">
      <div className="flex justify-between items-center bg-[var(--color-bg)] p-3 rounded-lg border border-[var(--color-border)] mb-4 sticky top-0 z-10">
        <span className="font-semibold text-sm flex items-center gap-2">
          <Focus size={16} className="text-[var(--color-primary)]" />
          Dyslexia Mode Active
        </span>
        <button
          onClick={handleListen}
          disabled={!speechSynthesisSupported}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
            isPlaying ? 'bg-red-100 text-red-600 border border-red-200' : 'bg-[var(--color-primary)] text-[var(--color-on-primary)] hover:opacity-90'
          }${!speechSynthesisSupported ? ' opacity-50 cursor-not-allowed' : ''}`}
        >
          <Volume2 size={16} />
          {isPlaying ? 'Stop' : 'Listen'}
        </button>
      </div>

      <div className="flex-1 space-y-6">
        {paragraphs.map((para, idx) => (
          <p
            key={idx}
            ref={el => paraRefs.current[idx] = el}
            className={`dyslexia-text text-[var(--color-text)] text-lg rounded-md transition-all duration-300 fade-in ${
              activePara === idx
                ? 'bg-[color-mix(in_srgb,var(--color-primary)_12%,transparent)] px-3 py-1 border-l-4 border-[var(--color-primary)] pulse-subtle'
                : 'px-3'
            }`}
          >
            {para}
          </p>
        ))}
      </div>
    </div>
  );
}
