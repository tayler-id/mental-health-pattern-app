import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { gsap } from 'gsap';

const MainMenu = ({ onNavigate, audioManager }) => {
  // Reference for animation
  const menuRef = useRef(null);
  
  // Menu options
  const menuOptions = [
    { id: 'mood-entry', label: '1. Data Entry', desc: 'Record your mood and emotions' },
    { id: 'view-data', label: '2. View Data', desc: 'Browse your recorded data' },
    { id: 'analysis', label: '3. Analysis', desc: 'See patterns in your data' },
    { id: 'visualizations', label: '4. Visualizations', desc: 'View graphical reports' },
    { id: 'insights', label: '5. Insights', desc: 'Get personalized insights' },
    { id: 'settings', label: '6. Settings', desc: 'Configure application options' },
    { id: 'exit', label: '7. Exit', desc: 'Close the application' }
  ];
  
  // Stagger animation for menu items on component mount
  useEffect(() => {
    if (menuRef.current) {
      const menuItems = menuRef.current.children;
      
      gsap.fromTo(
        menuItems,
        { 
          y: 20, 
          opacity: 0 
        },
        { 
          y: 0, 
          opacity: 1, 
          stagger: 0.1, 
          duration: 0.5,
          ease: 'power2.out',
          onStart: () => {
            // Play a subtle sound when menu appears
            audioManager.playSound('notification', 0.2);
          }
        }
      );
    }
  }, [audioManager]);
  
  // Handle menu item hover
  const handleHover = () => {
    audioManager.playSound('sliderMove', 0.1);
  };
  
  // Handle menu item click with sound
  const handleMenuClick = (optionId) => {
    // Play click sound
    audioManager.playSound('click');
    
    // Handle special cases
    if (optionId === 'exit') {
      alert('App closed (not really)');
      return;
    }
    
    // For options that are not yet implemented
    const notImplemented = ['view-data', 'analysis', 'visualizations', 'insights'];
    if (notImplemented.includes(optionId)) {
      setTimeout(() => {
        audioManager.playSound('error', 0.3);
        alert(`${optionId.replace('-', ' ')} feature coming soon!`);
      }, 100);
      return;
    }
    
    // Navigate to selected screen
    onNavigate(optionId);
  };
  
  // Handle keyboard navigation
  const handleKeyDown = (e, index) => {
    const option = menuOptions[index];
    
    // Enter or Space key activates the menu item
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleMenuClick(option.id);
    }
    
    // Number keys (1-7) for quick navigation
    const num = parseInt(e.key, 10);
    if (num >= 1 && num <= menuOptions.length) {
      e.preventDefault();
      handleMenuClick(menuOptions[num - 1].id);
      audioManager.playSound('click');
    }
  };
  
  // Animation variants for menu items
  const itemVariants = {
    hover: { 
      scale: 1.05, 
      y: -5,
      boxShadow: '0 10px 20px rgba(0,0,0,0.1)',
      transition: { type: 'spring', stiffness: 400, damping: 10 }
    },
    tap: { 
      scale: 0.95,
      boxShadow: '0 5px 10px rgba(0,0,0,0.1)',
      transition: { duration: 0.1 }
    }
  };
  
  return (
    <div className="main-menu animate-fade-in">
      <h2 className="main-menu-title">Main Menu</h2>
      
      <p className="menu-instruction">
        Select an option below or press the corresponding number key:
      </p>
      
      <div className="menu-items" ref={menuRef}>
        {menuOptions.map((option, index) => (
          <motion.div
            key={option.id}
            className="menu-item"
            onClick={() => handleMenuClick(option.id)}
            onMouseEnter={handleHover}
            onKeyDown={(e) => handleKeyDown(e, index)}
            tabIndex={0}
            role="button"
            aria-label={option.label}
            whileHover="hover"
            whileTap="tap"
            variants={itemVariants}
          >
            <span className="menu-item-label">{option.label}</span>
            <span className="menu-item-description">{option.desc}</span>
          </motion.div>
        ))}
      </div>
      
      <div className="menu-footer">
        <p className="menu-tip">
          TIP: Log your mood daily to maintain your streak and earn points!
        </p>
      </div>
    </div>
  );
};

export default MainMenu;
