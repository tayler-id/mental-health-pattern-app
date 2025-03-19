import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { gsap } from 'gsap';
import Confetti from 'react-confetti';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faSmile, 
  faSadTear, 
  faMeh, 
  faAngry, 
  faGrinBeam, 
  faGrinStars, 
  faTired, 
  faGrimace,
  faPaperPlane
} from '@fortawesome/free-solid-svg-icons';

const MoodEntry = ({ onCancel, onSuccess, audioManager, serverUrl, currentStreak }) => {
  // State for form values
  const [moodLevel, setMoodLevel] = useState(5);
  const [notes, setNotes] = useState('');
  const [selectedEmotions, setSelectedEmotions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  
  // Refs for animations
  const sliderRef = useRef(null);
  const formRef = useRef(null);
  const moodValueRef = useRef(null);
  
  // Define available emotions with icons
  const emotions = [
    { id: 'happy', label: 'Happy', icon: faSmile },
    { id: 'sad', label: 'Sad', icon: faSadTear },
    { id: 'calm', label: 'Calm', icon: faMeh },
    { id: 'angry', label: 'Angry', icon: faAngry },
    { id: 'excited', label: 'Excited', icon: faGrinBeam },
    { id: 'grateful', label: 'Grateful', icon: faGrinStars },
    { id: 'tired', label: 'Tired', icon: faTired },
    { id: 'stressed', label: 'Stressed', icon: faGrimace }
  ];
  
  // Animate form elements on mount
  useEffect(() => {
    if (formRef.current) {
      const formElements = formRef.current.children;
      
      gsap.fromTo(
        formElements,
        { y: 30, opacity: 0 },
        { 
          y: 0, 
          opacity: 1, 
          stagger: 0.1, 
          duration: 0.5,
          ease: 'power2.out'
        }
      );
    }
  }, []);
  
  // Animate mood value and update color when mood level changes
  useEffect(() => {
    if (moodValueRef.current) {
      // Scale animation
      gsap.fromTo(
        moodValueRef.current,
        { scale: 1.3 },
        { scale: 1, duration: 0.3, ease: 'back.out(1.7)' }
      );
      
      // Play slider sound
      audioManager.playSound('sliderMove', 0.1);
    }
  }, [moodLevel, audioManager]);
  
  // Handle mood level change
  const handleMoodChange = (e) => {
    setMoodLevel(parseInt(e.target.value, 10));
  };
  
  // Handle emotion selection
  const toggleEmotion = (emotionId) => {
    setSelectedEmotions(prev => {
      const isSelected = prev.includes(emotionId);
      
      // Play appropriate sound
      audioManager.playSound(isSelected ? 'click' : 'success', 0.2);
      
      // Toggle the emotion in the array
      return isSelected
        ? prev.filter(e => e !== emotionId)
        : [...prev, emotionId];
    });
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic validation
    if (selectedEmotions.length === 0) {
      setError('Please select at least one emotion');
      audioManager.playSound('error');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      // Play typing sound effect
      audioManager.playSound('typing', 0.3);
      
      // Submit data to server
      const response = await fetch(serverUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mood_level: moodLevel,
          notes: notes,
          emotions: selectedEmotions,
          streak: currentStreak
        }),
        signal: AbortSignal.timeout(8000) // 8s timeout
      });
      
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Server failed to process request');
      }
      
      // Show success state with animations
      setSuccess(true);
      
      // Show confetti for streaks of 3 or more
      if (data.streak >= 3) {
        setShowConfetti(true);
        
        // Play achievement sound for notable streaks
        if (data.streak >= 5) {
          audioManager.playAchievementSound();
          
          // Announce achievement with speech synthesis
          if (data.streak === 7) {
            setTimeout(() => {
              audioManager.speak("Amazing! You've reached a full week streak!");
            }, 1000);
          }
        }
      }
      
      // Call the success handler with server data
      setTimeout(() => {
        onSuccess(data);
      }, 1500);
      
    } catch (err) {
      console.error('Fetch error:', err);
      
      // Play error sound
      audioManager.playSound('error');
      
      // Set appropriate error message
      let errorMessage = 'An unexpected error occurred';
      
      if (err.name === 'AbortError') {
        errorMessage = 'Request timed out. Please try again.';
      } else if (err.message.includes('Network request failed')) {
        errorMessage = `Network connection failed. Make sure the server is running at ${serverUrl}`;
      } else {
        errorMessage = `Error: ${err.message}`;
      }
      
      setError(errorMessage);
      
    } finally {
      setLoading(false);
    }
  };
  
  // Handle typing in notes field with typing sound
  const handleNotesChange = (e) => {
    setNotes(e.target.value);
    
    // Occasionally play typing sound (not on every keystroke)
    if (Math.random() > 0.7) {
      audioManager.playSound('typing', 0.05);
    }
  };
  
  // Calculate mood color based on mood level
  const getMoodColor = () => {
    const colors = {
      1: 'var(--mood-1)',
      2: 'var(--mood-2)',
      3: 'var(--mood-3)',
      4: 'var(--mood-4)',
      5: 'var(--mood-5)',
      6: 'var(--mood-6)',
      7: 'var(--mood-7)',
      8: 'var(--mood-8)',
      9: 'var(--mood-9)',
      10: 'var(--mood-10)'
    };
    
    return colors[moodLevel] || colors[5];
  };
  
  // Get mood description based on level
  const getMoodDescription = () => {
    const descriptions = {
      1: 'Very Low',
      2: 'Low',
      3: 'Somewhat Low',
      4: 'Slightly Low',
      5: 'Neutral',
      6: 'Slightly Elevated',
      7: 'Moderately Good',
      8: 'Good',
      9: 'Very Good',
      10: 'Excellent'
    };
    
    return descriptions[moodLevel] || 'Neutral';
  };
  
  // Animation variants for emotion buttons
  const emotionVariants = {
    selected: { 
      backgroundColor: 'var(--color-secondary)',
      color: 'white',
      scale: 1.05,
      y: -2
    },
    unselected: { 
      backgroundColor: 'white',
      color: 'var(--text-primary)',
      scale: 1,
      y: 0
    }
  };
  
  return (
    <div className="mood-entry-container animate-fade-in">
      {/* Success confetti effect */}
      {showConfetti && (
        <Confetti
          width={window.innerWidth}
          height={window.innerHeight}
          recycle={false}
          numberOfPieces={500}
          gravity={0.2}
          onConfettiComplete={() => setShowConfetti(false)}
        />
      )}
      
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Record Your Mood</h2>
        </div>
        
        <form ref={formRef} onSubmit={handleSubmit}>
          {/* Mood Level Slider */}
          <div className="form-group mood-slider-container">
            <label className="form-label">
              Mood Level: 
              <span 
                ref={moodValueRef}
                className="mood-value" 
                style={{ color: getMoodColor() }}
              >
                {moodLevel} - {getMoodDescription()}
              </span>
            </label>
            
            <div className="slider-track">
              <input
                ref={sliderRef}
                type="range"
                min="1"
                max="10"
                value={moodLevel}
                onChange={handleMoodChange}
                className="mood-slider"
              />
              
              <div 
                className="mood-color-indicator"
                style={{ 
                  background: `linear-gradient(90deg, var(--mood-1) 0%, var(--mood-10) 100%)`,
                  height: '10px',
                  borderRadius: '5px',
                  marginTop: '5px'
                }}
              />
            </div>
          </div>
          
          {/* Emotions Selection */}
          <div className="form-group">
            <label className="form-label">How are you feeling? (Select all that apply)</label>
            
            <div className="emotions-grid">
              {emotions.map(emotion => (
                <motion.div
                  key={emotion.id}
                  className="emotion-button"
                  onClick={() => toggleEmotion(emotion.id)}
                  variants={emotionVariants}
                  animate={selectedEmotions.includes(emotion.id) ? 'selected' : 'unselected'}
                  transition={{ type: 'spring', stiffness: 300, damping: 15 }}
                >
                  <FontAwesomeIcon icon={emotion.icon} className="emotion-icon" />
                  <span>{emotion.label}</span>
                </motion.div>
              ))}
            </div>
          </div>
          
          {/* Notes */}
          <div className="form-group">
            <label className="form-label">
              Notes (optional)
              <span className="char-counter">{notes.length}/200</span>
            </label>
            <textarea
              className="form-control"
              value={notes}
              onChange={handleNotesChange}
              placeholder="Add any additional thoughts or context..."
              maxLength={200}
              rows={3}
            />
          </div>
          
          {/* Error Message */}
          <AnimatePresence>
            {error && (
              <motion.div 
                className="error-message"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
              >
                {error}
              </motion.div>
            )}
          </AnimatePresence>
          
          {/* Success Message */}
          <AnimatePresence>
            {success && (
              <motion.div 
                className="success-message"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
              >
                Mood recorded successfully! Updating your streak...
              </motion.div>
            )}
          </AnimatePresence>
          
          {/* Action Buttons */}
          <div className="form-actions">
            <button 
              type="button" 
              className="btn btn-outline"
              onClick={onCancel}
              disabled={loading || success}
            >
              Cancel
            </button>
            
            <motion.button
              type="submit"
              className="btn btn-primary"
              disabled={loading || success}
              whileHover={{ scale: loading ? 1 : 1.05 }}
              whileTap={{ scale: loading ? 1 : 0.95 }}
            >
              {loading ? (
                <span className="loading-text">Submitting...</span>
              ) : (
                <>
                  <FontAwesomeIcon icon={faPaperPlane} className="submit-icon" />
                  <span>Record Mood</span>
                </>
              )}
            </motion.button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MoodEntry;
