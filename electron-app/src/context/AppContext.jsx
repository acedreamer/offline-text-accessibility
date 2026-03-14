import { createContext, useState, useContext, useEffect } from 'react';

export const AppContext = createContext();

export function AppProvider({ children }) {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [mode, setMode] = useState("dyslexia"); // "dyslexia" | "adhd" | "autism"

  const [metrics, setMetrics] = useState({
    before: { word_count: 0, avg_sentence_length: 0, flesch_reading_ease: 0 },
    after: { word_count: 0, avg_sentence_length: 0, flesch_reading_ease: 0 }
  });

  const [focusMode, setFocusMode] = useState(false);
  const [focusSentenceIndex, setFocusSentenceIndex] = useState(0);
  const [sentences, setSentences] = useState([]);

  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settings, setSettings] = useState({
    theme: "light", // handled largely by ThemeContext
    fontFamily: "lexend",
    fontSize: 18,
    lineSpacing: "standard",
    cogFocusMode: true,
    reduceMotion: false,
    useHyphenation: false, // User preference for hyphenation in dyslexia mode
  });

  // Apply settings to body
  useEffect(() => {
    const classList = document.body.classList;
    if (settings.reduceMotion) {
      classList.add('reduce-motion');
      classList.add('no-transition');
    } else {
      classList.remove('reduce-motion');
      classList.remove('no-transition');
    }

    // Apply line spacing
    if (settings.lineSpacing === 'standard') {
      document.body.style.lineHeight = '1.5';
    } else if (settings.lineSpacing === 'relaxed') {
      document.body.style.lineHeight = '1.8';
    } else if (settings.lineSpacing === 'wide') {
      document.body.style.lineHeight = '2.0';
    }

  }, [settings]);

  const handleSimplify = async () => {
    if (!inputText.trim()) return;

    setIsLoading(true);
    try {
      const result = await window.electronAPI.simplify({
        text: inputText,
        mode: mode,
        useHyphenation: settings.useHyphenation, // Pass hyphenation setting to backend
      });

      if (result.error) {
        setOutputText(`Error: ${result.error}`);
        setIsLoading(false);
        return;
      }

      setOutputText(result.simplified);
      setMetrics(result.metrics);

      // ADHD mode is already split into lines with [1/N] markers by Python
      const splitSentences = mode === 'adhd'
        ? result.simplified.split('\n').filter(Boolean)
        : result.simplified.split(/(?<=[.!?])\s+/).filter(Boolean);

      setSentences(splitSentences);
      setFocusSentenceIndex(0);

    } catch (error) {
      console.error("Simplification error:", error);
      setOutputText(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppContext.Provider value={{
      inputText, setInputText,
      outputText, setOutputText,
      isLoading, setIsLoading,
      mode, setMode,
      metrics, setMetrics,
      focusMode, setFocusMode,
      focusSentenceIndex, setFocusSentenceIndex,
      sentences, setSentences,
      settingsOpen, setSettingsOpen,
      settings, setSettings,
      handleSimplify
    }}>
      {children}
    </AppContext.Provider>
  );
}

export const useApp = () => useContext(AppContext);
