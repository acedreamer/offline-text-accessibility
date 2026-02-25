import { ThemeProvider } from './context/ThemeContext';
import { AppProvider } from './context/AppContext';
import Header from './components/layout/Header';
import MetricsBar from './components/layout/MetricsBar';
import SettingsPanel from './components/layout/SettingsPanel';
import InputPanel from './components/editor/InputPanel';
import OutputPanel from './components/editor/OutputPanel';

function AppContent() {
  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <Header />

      <main className="flex-1 overflow-hidden grid grid-cols-1 md:grid-cols-2">
        <InputPanel />
        <OutputPanel />
      </main>

      <MetricsBar />
      <SettingsPanel />
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AppProvider>
        <AppContent />
      </AppProvider>
    </ThemeProvider>
  );
}

export default App;
