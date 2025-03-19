import React, { useState, useEffect } from 'react';
import { useAudioManager } from './hooks/useAudioManager';
import MainMenu from './components/MainMenu';
import MoodEntry from './components/MoodEntry';
import Header from './components/Header';
import Footer from './components/Footer';

const App = () => {
  // State for user data and application state
  const [currentScreen, setCurrentScreen] = useState('main-menu');
  const [points, setPoints] = useState(0);
  const [streak, setStreak] = useState(0);
  const [serverUrl, setServerUrl] = useState('http://localhost:3001/record-mood');
  
  // Initialize audio manager
  const audioManager = useAudioManager();
  
  // Preload sounds on component mount
  useEffect(() => {
    audioManager.preloadSounds();
  }, []);
  
  // Calculate streak bar width as a percentage (max 7 days)
  const streakPercentage = Math.min((streak / 7) * 100, 100);
  
  // Handle menu navigation with sound effects
  const navigateTo = (screen) => {
    audioManager.playSound('click');
    setCurrentScreen(screen);
  };
  
  // Handle successful record completion
  const handleRecordSuccess = (data) => {
    // Update points (10 points per entry)
    setPoints(prevPoints => prevPoints + 10);
    
    // Update streak
    setStreak(data.streak);
    
    // Play success sound
    audioManager.playSound('success');
    
    // Return to menu
    setTimeout(() => navigateTo('main-menu'), 1500);
  };
  
  // Render appropriate screen based on current state
  const renderScreen = () => {
    switch (currentScreen) {
      case 'mood-entry':
        return (
          <MoodEntry 
            onCancel={() => navigateTo('main-menu')}
            onSuccess={handleRecordSuccess}
            audioManager={audioManager}
            serverUrl={serverUrl}
            currentStreak={streak}
          />
        );
      
      case 'settings':
        return (
          <div className="card animate-fade-in">
            <h2>Settings</h2>
            <div className="form-group">
              <label className="form-label" htmlFor="server-url">Server URL</label>
              <input
                id="server-url"
                type="text"
                className="form-control"
                value={serverUrl}
                onChange={(e) => setServerUrl(e.target.value)}
                placeholder="http://localhost:3001/record-mood"
              />
            </div>
            <div className="form-group">
              <label className="form-label">
                <input
                  type="checkbox"
                  checked={!audioManager.isMuted()}
                  onChange={() => audioManager.toggleMute()}
                /> 
                Enable Sound Effects
              </label>
            </div>
            <button className="btn btn-primary" onClick={() => navigateTo('main-menu')}>Save and Close</button>
          </div>
        );
      
      case 'main-menu':
      default:
        return (
          <MainMenu 
            onNavigate={navigateTo} 
            audioManager={audioManager}
          />
        );
    }
  };
  
  return (
    <div className="container">
      <Header 
        points={points} 
        streak={streak} 
        streakPercentage={streakPercentage} 
      />
      <main className="app-content">
        {renderScreen()}
      </main>
      <Footer />
    </div>
  );
};

export default App;
