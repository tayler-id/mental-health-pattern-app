import React, { useRef, useEffect } from 'react';
import { gsap } from 'gsap';

const Header = ({ points, streak, streakPercentage }) => {
  // Refs for GSAP animations
  const streakBarRef = useRef(null);
  const streakTextRef = useRef(null);
  const pointsRef = useRef(null);
  
  // Animate streak bar when streak changes
  useEffect(() => {
    if (streakBarRef.current) {
      gsap.to(streakBarRef.current, {
        width: `${streakPercentage}%`,
        duration: 0.8,
        ease: 'power2.out'
      });
    }
  }, [streakPercentage]);
  
  // Animate points and streak text when they change
  useEffect(() => {
    if (pointsRef.current) {
      gsap.from(pointsRef.current, {
        scale: 1.3,
        duration: 0.5,
        ease: 'elastic.out(1, 0.3)',
        clearProps: 'scale'
      });
    }
  }, [points]);
  
  useEffect(() => {
    if (streakTextRef.current) {
      gsap.from(streakTextRef.current, {
        scale: 1.3,
        color: '#2ecc71',
        duration: 0.5,
        ease: 'elastic.out(1, 0.3)',
        clearProps: 'all'
      });
    }
  }, [streak]);
  
  return (
    <header className="app-header">
      <div className="app-header-content">
        <h1 className="app-title">Mental Health Tracker</h1>
        
        <div className="app-stats">
          <div className="points-display">
            <span>Points:</span>
            <span ref={pointsRef} className="points-value">{points}</span>
          </div>
          
          <div className="streak-container">
            <div className="streak-info">
              <span>Streak:</span>
              <span ref={streakTextRef} className="streak-value">{streak} day{streak !== 1 ? 's' : ''}</span>
            </div>
            
            <div className="streak-bar-container">
              <div 
                ref={streakBarRef} 
                className="streak-bar" 
                style={{ width: `${streakPercentage}%` }}
              />
              
              {Array(7).fill(0).map((_, index) => (
                <div 
                  key={index} 
                  className={`streak-marker ${index < streak ? 'active' : ''}`} 
                  style={{ left: `${(index / 6) * 100}%` }}
                  title={`Day ${index + 1}`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
