import { useApp } from '../../context/AppContext';
import { useTheme } from '../../context/ThemeContext';
import { X, Monitor, Moon, Sun, Type, LayoutTemplate } from 'lucide-react';
import { useEffect, useRef } from 'react';

export default function SettingsPanel() {
  const { settingsOpen, setSettingsOpen, settings, setSettings } = useApp();
  const { theme, setTheme } = useTheme();
  const panelRef = useRef(null);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && settingsOpen) {
        setSettingsOpen(false);
      }
    };
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [settingsOpen, setSettingsOpen]);

  // Handle clicking outside
  const handleBackdropClick = (e) => {
    if (panelRef.current && !panelRef.current.contains(e.target)) {
      setSettingsOpen(false);
    }
  };

  const updateSetting = (key, value) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
    // Apply specific CSS variables based on settings
    if (key === 'fontSize') {
      document.documentElement.style.setProperty('--font-size-body', `${value}px`);
    } else if (key === 'fontFamily') {
      document.body.className = `${value}-font`;
    }
  };

  if (!settingsOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex justify-end"
      onClick={handleBackdropClick}
    >
      <div
        ref={panelRef}
        className="w-[400px] bg-[var(--color-surface)] h-full shadow-2xl border-l border-[var(--color-border)] flex flex-col transform transition-transform duration-300 translate-x-0 overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-6 border-b border-[var(--color-border)] sticky top-0 bg-[var(--color-surface)] z-10">
          <h2 className="text-xl font-bold text-[var(--color-text)]">Accessibility Settings</h2>
          <button
            onClick={() => setSettingsOpen(false)}
            className="p-2 text-[var(--color-muted)] hover:bg-[var(--color-bg)] rounded-full transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        <div className="flex-1 p-6 space-y-8">
          {/* Section 1: Display & Theme */}
          <section className="space-y-4">
            <h3 className="text-sm font-semibold text-[var(--color-muted)] uppercase tracking-wider flex items-center gap-2">
              <Monitor size={16} />
              Display & Theme
            </h3>
            <div className="grid grid-cols-3 gap-3">
              <button
                onClick={() => setTheme('light')}
                className={`flex flex-col items-center gap-2 p-3 rounded-lg border-2 transition-all ${
                  theme === 'light' ? 'border-[var(--color-primary)] bg-[var(--color-primary)]/5' : 'border-[var(--color-border)] hover:border-gray-400'
                }`}
              >
                <div className="w-12 h-8 bg-[#f6f6f8] rounded border border-gray-200 flex items-center justify-center">
                  <Sun size={14} className="text-gray-500" />
                </div>
                <span className="text-xs font-medium text-[var(--color-text)]">Light</span>
              </button>
              <button
                onClick={() => setTheme('dark')}
                className={`flex flex-col items-center gap-2 p-3 rounded-lg border-2 transition-all ${
                  theme === 'dark' ? 'border-[var(--color-primary)] bg-[var(--color-primary)]/5' : 'border-[var(--color-border)] hover:border-gray-400'
                }`}
              >
                <div className="w-12 h-8 bg-[#101622] rounded border border-gray-700 flex items-center justify-center">
                  <Moon size={14} className="text-gray-400" />
                </div>
                <span className="text-xs font-medium text-[var(--color-text)]">Dark</span>
              </button>
              <button
                onClick={() => setTheme('high-contrast')}
                className={`flex flex-col items-center gap-2 p-3 rounded-lg border-2 transition-all ${
                  theme === 'high-contrast' ? 'border-[var(--color-primary)] bg-[var(--color-primary)]/10' : 'border-[var(--color-border)] hover:border-gray-400'
                }`}
              >
                <div className="w-12 h-8 bg-black rounded border-2 border-yellow-400 flex items-center justify-center">
                  <span className="text-yellow-400 font-bold text-xs">AAA</span>
                </div>
                <span className="text-xs font-medium text-[var(--color-text)]">High Contrast</span>
              </button>
            </div>
          </section>

          {/* Section 2: Typography */}
          <section className="space-y-4">
            <h3 className="text-sm font-semibold text-[var(--color-muted)] uppercase tracking-wider flex items-center gap-2">
              <Type size={16} />
              Typography
            </h3>

            <div className="space-y-3">
              <label className="text-sm font-medium text-[var(--color-text)]">Font Family</label>
              <select
                value={settings.fontFamily}
                onChange={(e) => updateSetting('fontFamily', e.target.value)}
                className="w-full p-2 border border-[var(--color-border)] rounded-md bg-[var(--color-bg)] text-[var(--color-text)] focus:ring-2 focus:ring-[var(--color-primary)] outline-none"
              >
                <option value="lexend">Lexend (Default)</option>
                <option value="opendyslexic">OpenDyslexic</option>
                <option value="merriweather">Merriweather (Serif)</option>
                <option value="mono">Monospace</option>
              </select>
            </div>

            <div className="space-y-3 pt-2">
              <div className="flex justify-between items-center text-sm font-medium text-[var(--color-text)]">
                <label>Font Size</label>
                <span className="text-[var(--color-muted)]">{settings.fontSize}px</span>
              </div>
              <input
                type="range"
                min="14"
                max="28"
                step="1"
                value={settings.fontSize}
                onChange={(e) => updateSetting('fontSize', parseInt(e.target.value))}
                className="w-full accent-[var(--color-primary)]"
              />
              <div className="flex justify-between text-xs text-[var(--color-muted)]">
                <span>A (Small)</span>
                <span>A (Large)</span>
              </div>
            </div>

            <div className="space-y-3 pt-2">
              <div className="flex justify-between items-center text-sm font-medium text-[var(--color-text)]">
                <label>Hyphenation</label>
                <span className="text-[var(--color-muted)]">
                  {settings.useHyphenation ? 'On' : 'Off'}
                </span>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  className="sr-only peer"
                  checked={settings.useHyphenation}
                  onChange={(e) => updateSetting('useHyphenation', e.target.checked)}
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[var(--color-primary)]/30 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--color-primary)]"></div>
              </label>
              <div className="flex justify-between text-xs text-[var(--color-muted)]">
                <span>Off</span>
                <span>On</span>
              </div>
              <p className="text-xs text-[var(--color-muted)] mt-1">
                Note: Hyphenation may reduce readability for some dyslexic users per BDA guidelines
              </p>
            </div>
          </section>

          {/* Section 3: Reading Assistance */}
          <section className="space-y-4">
            <h3 className="text-sm font-semibold text-[var(--color-muted)] uppercase tracking-wider flex items-center gap-2">
              <LayoutTemplate size={16} />
              Reading Assistance
            </h3>

            <div className="space-y-3">
              <label className="text-sm font-medium text-[var(--color-text)]">Line Spacing</label>
              <select
                value={settings.lineSpacing}
                onChange={(e) => updateSetting('lineSpacing', e.target.value)}
                className="w-full p-2 border border-[var(--color-border)] rounded-md bg-[var(--color-bg)] text-[var(--color-text)] focus:ring-2 focus:ring-[var(--color-primary)] outline-none"
              >
                <option value="standard">Standard (1.5)</option>
                <option value="relaxed">Relaxed (1.8)</option>
                <option value="wide">Wide (2.0)</option>
              </select>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-[var(--color-border)]">
              <div>
                <span className="block text-sm font-medium text-[var(--color-text)]">Reduce Motion</span>
                <span className="text-xs text-[var(--color-muted)]">Disable animations and transitions</span>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  className="sr-only peer"
                  checked={settings.reduceMotion}
                  onChange={(e) => updateSetting('reduceMotion', e.target.checked)}
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[var(--color-primary)]/30 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--color-primary)]"></div>
              </label>
            </div>
          </section>
        </div>

        <div className="p-6 border-t border-[var(--color-border)] bg-[var(--color-bg)] sticky bottom-0">
          <button
            onClick={() => setSettingsOpen(false)}
            className="w-full py-3 bg-[var(--color-primary)] text-[var(--color-on-primary)] rounded-lg font-semibold hover:opacity-90 transition-opacity shadow-sm"
          >
            Save and Apply Settings
          </button>
        </div>
      </div>
    </div>
  );
}