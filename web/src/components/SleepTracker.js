import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { gsap } from 'gsap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import BridgeService from '../services/BridgeService';
import {
  faMoon,
  faSun,
  faBed,
  faClock,
  faChevronUp,
  faChevronDown,
  faStar,
  faSave,
  faTimes,
  faExclamationTriangle
} from '@fortawesome/free-solid-svg-icons';

const SleepTracker = ({ onCancel, onSuccess, audioManager }) => {
  // State for sleep data
  const [sleepTime, setSleepTime] = useState('22:00');
  const [wakeTime, setWakeTime] = useState('07:00');
  const [quality, setQuality] = useState(3);
  const [interruptions, setInterruptions] = useState(0);
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  // Calculate sleep duration
  const calculateSleepDuration = () => {
    // Parse times
    const [sleepHours, sleepMinutes] = sleepTime.split(':').map(Number);
    const [wakeHours, wakeMinutes] = wakeTime.split(':').map(Number);
    
    // Create date objects for calculation
    const sleepDate = new Date();
    sleepDate.setHours(sleepHours, sleepMinutes, 0);
    
    const wakeDate = new Date();
    wakeDate.setHours(wakeHours, wakeMinutes, 0);
    
    // If wake time is earlier, it's the next day
    if (wakeDate < sleepDate) {
      wakeDate.setDate(wakeDate.getDate() + 1);
    }
    
    // Calculate difference in hours
    const diffMs = wakeDate - sleepDate;
    const diffHrs = diffMs / (1000 * 60 * 60);
    
    return diffHrs;
  };
  
  // Format duration as hours and minutes
  const formatDuration = (hours) => {
    const wholeHours = Math.floor(hours);
    const minutes = Math.round((hours - wholeHours) * 60);
    
    return `${wholeHours}h ${minutes}m`;
  };
  
  // Refs for animations
  const formRef = useRef(null);
  const submitButtonRef = useRef(null);
  
  // Format data for API
  const formatRequestData = () => {
    return {
      sleep_time: sleepTime,
      wake_time: wakeTime,
      quality: quality,
      duration: calculateSleepDuration(),
      interruptions: interruptions,
      notes: notes.trim(),
      timestamp: new Date().toISOString()
    };
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (isSubmitting) return;
    
    // Play submit sound
    audioManager.playSound('click');
    
    // Show loading state
    setIsSubmitting(true);
    setError(null);
    
    // Animate submit button
    if (submitButtonRef.current) {
      gsap.to(submitButtonRef.current, {
        scale: 0.95,
        duration: 0.1,
        yoyo: true,
        repeat: 1
      });
    }
    
    try {
      // Prepare data
      const requestData = formatRequestData();
      
      // Use BridgeService to submit data
      // Note: This endpoint needs to be implemented in the server-stub
      const responseData = await BridgeService.recordSleep(requestData);
      
      // Show success state
      setSuccess(true);
      audioManager.playSound('success');
      
      // Animate success
      gsap.fromTo(
        formRef.current,
        { opacity: 1, y: 0 },
        { 
          opacity: 0, 
          y: -20,
          duration: 0.4,
          delay: 0.8,
          onComplete: () => {
            // Call success callback
            onSuccess(responseData);
          }
        }
      );
      
    } catch (err) {
      console.error('Error submitting sleep data:', err);
      
      // Get error message
      const errorMessage = err.data?.message || err.message || 'Failed to save sleep data. Please try again.';
      
      setError(errorMessage);
      setIsSubmitting(false);
      audioManager.playSound('error', 0.3);
    }
  };
  
  // Animate form on mount
  useEffect(() => {
    if (formRef.current) {
      gsap.fromTo(
        formRef.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }
      );
    }
  }, []);
  
  // Handle cancel
  const handleCancel = () => {
    audioManager.playSound('click');
    
    // Animate out
    gsap.to(formRef.current, {
      opacity: 0,
      y: 20,
      duration: 0.3,
      onComplete: onCancel
    });
  };
  
  // Increment/decrement interruptions
  const adjustInterruptions = (amount) => {
    audioManager.playSound('click', 0.2);
    setInterruptions(prev => Math.max(0, prev + amount));
  };
  
  // Change quality rating
  const handleQualityChange = (newQuality) => {
    audioManager.playSound('click', 0.2);
    setQuality(newQuality);
  };
  
  // Get color based on sleep quality
  const getQualityColor = (level) => {
    const colors = {
      1: 'var(--error)',    // Very Poor
      2: 'var(--warning)',  // Poor
      3: 'var(--primary)',  // Fair
      4: 'var(--info)',     // Good
      5: 'var(--success)'   // Excellent
    };
    
    return colors[level] || 'var(--primary)';
  };
  
  // Get label for sleep quality
  const getQualityLabel = (level) => {
    const labels = {
      1: 'Very Poor',
      2: 'Poor',
      3: 'Fair',
      4: 'Good',
      5: 'Excellent'
    };
    
    return labels[level] || 'Fair';
  };
  
  // Calculate sleep health score
  const calculateSleepScore = () => {
    const duration = calculateSleepDuration();
    
    // Duration factor (ideal is 7-9 hours)
    let durationScore = 0;
    if (duration >= 7 && duration <= 9) {
      durationScore = 50;
    } else if (duration >= 6 && duration < 7) {
      durationScore = 40;
    } else if (duration > 9 && duration <= 10) {
      durationScore = 40;
    } else if (duration >= 5 && duration < 6) {
      durationScore = 30;
    } else if (duration > 10 && duration <= 11) {
      durationScore = 30;
    } else {
      durationScore = 20;
    }
    
    // Quality factor
    const qualityScore = quality * 10;
    
    // Interruptions factor
    const interruptionsScore = Math.max(0, 10 - interruptions * 2);
    
    // Total score (normalized to 100)
    return Math.min(100, durationScore + qualityScore + interruptionsScore);
  };
  
  // Get color for sleep score
  const getSleepScoreColor = (score) => {
    if (score >= 80) return 'var(--success)';
    if (score >= 60) return 'var(--info)';
    if (score >= 40) return 'var(--warning)';
    return 'var(--error)';
  };
  
  // Create quality rating buttons
  const renderQualityButtons = () => {
    return Array.from({ length: 5 }, (_, i) => i + 1).map(level => (
      <button
        key={level}
        type="button"
        className={`quality-button ${level <= quality ? 'active' : ''}`}
        onClick={() => handleQualityChange(level)}
        style={{ 
          '--active-color': getQualityColor(level) 
        }}
      >
        <FontAwesomeIcon icon={faStar} />
      </button>
    ));
  };
  
  // Score variants for animations
  const scoreVariants = {
    hover: { 
      scale: 1.05,
      transition: { duration: 0.2 } 
    }
  };
  
  return (
    <div className="sleep-tracker-container" ref={formRef}>
      <form onSubmit={handleSubmit}>
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">
              <FontAwesomeIcon icon={faMoon} className="mr-2" /> Track Your Sleep
            </h2>
            <p className="card-subtitle">Record your sleep details to identify patterns and improve your rest</p>
          </div>
          
          <div className="card-body">
            {/* Sleep Duration Section */}
            <div className="sleep-time-container">
              <div className="form-group">
                <label className="form-label">
                  <FontAwesomeIcon icon={faBed} className="mr-2" /> Bedtime
                </label>
                <input
                  type="time"
                  className="form-control"
                  value={sleepTime}
                  onChange={(e) => setSleepTime(e.target.value)}
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">
                  <FontAwesomeIcon icon={faSun} className="mr-2" /> Wake Time
                </label>
                <input
                  type="time"
                  className="form-control"
                  value={wakeTime}
                  onChange={(e) => setWakeTime(e.target.value)}
                />
              </div>
              
              <div className="sleep-duration">
                <div className="sleep-duration-label">
                  <FontAwesomeIcon icon={faClock} className="mr-2" /> Duration
                </div>
                <div className="sleep-duration-value">
                  {formatDuration(calculateSleepDuration())}
                </div>
              </div>
            </div>
            
            {/* Sleep Score */}
            <motion.div 
              className="sleep-score-container"
              variants={scoreVariants}
              whileHover="hover"
            >
              <div className="sleep-score" style={{ 
                background: `conic-gradient(
                  ${getSleepScoreColor(calculateSleepScore())} 
                  ${calculateSleepScore() * 3.6}deg, 
                  var(--neutral-200) 0deg
                )`
              }}>
                <div className="sleep-score-inner">
                  <div className="sleep-score-value">
                    {calculateSleepScore()}
                  </div>
                  <div className="sleep-score-label">
                    Sleep Score
                  </div>
                </div>
              </div>
              
              <div className="sleep-score-insights">
                {calculateSleepScore() >= 80 && (
                  <p>Excellent sleep pattern! Your current schedule promotes optimal rest.</p>
                )}
                {calculateSleepScore() >= 60 && calculateSleepScore() < 80 && (
                  <p>Good sleep pattern. Minor adjustments could improve your rest quality.</p>
                )}
                {calculateSleepScore() >= 40 && calculateSleepScore() < 60 && (
                  <p>Fair sleep pattern. Consider adjusting your sleep schedule for better rest.</p>
                )}
                {calculateSleepScore() < 40 && (
                  <p>Your sleep pattern may be affecting your well-being. Consider consulting a healthcare professional.</p>
                )}
              </div>
            </motion.div>
            
            {/* Sleep Quality Section */}
            <div className="form-group">
              <label className="form-label">Sleep Quality</label>
              <div className="quality-rating">
                {renderQualityButtons()}
                <span className="quality-label" style={{ color: getQualityColor(quality) }}>
                  {getQualityLabel(quality)}
                </span>
              </div>
            </div>
            
            {/* Interruptions Section */}
            <div className="form-group">
              <label className="form-label">Sleep Interruptions</label>
              <div className="interruptions-control">
                <button 
                  type="button" 
                  className="btn btn-outline btn-icon"
                  onClick={() => adjustInterruptions(-1)}
                  disabled={interruptions <= 0}
                >
                  <FontAwesomeIcon icon={faChevronDown} />
                </button>
                
                <div className="interruptions-value">
                  {interruptions}
                </div>
                
                <button 
                  type="button" 
                  className="btn btn-outline btn-icon"
                  onClick={() => adjustInterruptions(1)}
                >
                  <FontAwesomeIcon icon={faChevronUp} />
                </button>
              </div>
            </div>
            
            {/* Notes Section */}
            <div className="form-group">
              <label className="form-label" htmlFor="sleep-notes">
                Notes (optional)
              </label>
              <textarea
                id="sleep-notes"
                className="form-control"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Any factors that affected your sleep? (stress, caffeine, exercise, etc.)"
                rows={3}
              />
            </div>
            
            {/* Error Message */}
            {error && (
              <div className="error-message">
                <FontAwesomeIcon icon={faExclamationTriangle} className="mr-2" />
                {error}
              </div>
            )}
            
            {/* Success Message */}
            {success && (
              <div className="success-message">
                Sleep data recorded successfully!
              </div>
            )}
          </div>
          
          <div className="card-footer">
            <div className="form-actions">
              <button
                type="button"
                className="btn btn-outline"
                onClick={handleCancel}
                disabled={isSubmitting}
              >
                <FontAwesomeIcon icon={faTimes} className="mr-2" /> Cancel
              </button>
              
              <button
                ref={submitButtonRef}
                type="submit"
                className="btn btn-primary"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <span>Saving...</span>
                ) : (
                  <>
                    <FontAwesomeIcon icon={faSave} className="mr-2" /> Save Sleep Data
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};

export default SleepTracker;
