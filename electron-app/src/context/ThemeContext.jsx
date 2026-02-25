import { createContext, useState, useEffect, useContext } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light'); // 'light' | 'dark' | 'high-contrast'

  useEffect(() => {
    // Apply theme to document element
    const html = document.documentElement;
    html.classList.remove('light', 'dark', 'high-contrast');

    if (theme !== 'light') {
      html.classList.add(theme);
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
