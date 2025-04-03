import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { gsap } from 'gsap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import BridgeService from '../services/BridgeService';
import {
  faRunning,
  faDumbbell,
  faBookReader,
  faLaptopCode,
  faUsers,
  faBriefcase,
  faUtensils,
  faMusic,
  faGamepad,
  faPlus,
  faPeace,
  faMinus,
  faSave,
  faTimes,
  faExclamationTriangle,
  faClock,
  faHeartbeat,
  faBrain,
  faSmile,
  faSadTear
} from '@fortawesome/free-solid-svg-icons';

const ActivityTracker = ({ onCancel, onSuccess, audioManager }) => {
  // Activity types with icons
  const activityTypes = [
    { id: 'exercise', label: 'Exercise', icon: faRunning, color: 'var(--success)' },
    { id: 'work', label: 'Work', icon: faBriefcase, color: 'var(--primary-dark)' },
    { id: 'study', label: 'Study', icon: faBookReader, color: 'var(--info)' },
    { id: 'coding', label: 'Coding', icon: faLaptopCode, color: 'var(--primary)' },
    { id: 'social', label: 'Social', icon: faUsers, color: 'var(--accent)' },
    { id: 'meditation', label: 'Meditation', icon: faPeace, color: 'var(--secondary)' },
    { id: 'strength', label: 'Strength', icon: faDumbbell, color: 'var(--warning)' },
    { id: 'eating', label: 'Eating', icon: faUtensils, color: 'var(--neutral-600)' },
    { id: 'music', label: 'Music', icon: faMusic, color: 'var(--accent-light)' },
    { id: 'gaming', label: 'Gaming', icon: faGamepad, color: 'var(--primary-light)' }
  ];
  
  // State for activity data
  const [selectedType, setSelectedType] = useState(null);
  const [customType, setCustomType] = useState('');
  const [duration, setDuration] = useState(30);
  const [intensity, setIntensity] = useState(3);
  const [moodImpact, setMoodImpact] = useState(0);
  const [notes, setNotes] = useState('');
  const [showCustomType, setShowCustomType] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  // Refs for animations
  const formRef = useRef(null);
  const submitButtonRef = useRef(null);
  
  // Format duration for display
  const formatDuration = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    
    return `${mins}m`;
  };
  
  // Format data for API
  const formatRequestData = () => {
    const activityType = showCustomType ? customType : selectedType;
    
    return {
      activity_type: activityType,
      duration_minutes: duration,
      intensity: intensity,
      mood_impact: moodImpact,
      notes: notes.trim(),
      timestamp: new Date().toISOString()
    };
  };
  
  // Handle activity type selection
  const handleTypeSelect = (typeId) => {
    audioManager.playSound('click', 0.2);
    setSelectedType(typeId);
    setShowCustomType(false);
  };
  
  // Toggle custom type input
  const toggleCustomType = () => {
    audioManager.playSound('click', 0.2);
    setShowCustomType(prev => !prev);
    if (!showCustomType) {
      setSelectedType(null);
    }
  };
  
  // Adjust duration
  const adjustDuration = (amount) => {
    audioManager.playSound('click', 0.2);
    setDuration(prev => Math.max(5, prev + amount));
  };
  
  // Handle intensity change
  const handleIntensityChange = (newIntensity) => {
    audioManager.playSound('click', 0.2);
    setIntensity(newIntensity);
  };
  
  // Handle mood impact change
  const handleMoodImpactChange = (newImpact) => {
    audioManager.playSound('click', 0.2);
    setMoodImpact(newImpact);
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (isSubmitting) return;
    
    // Validate form
    if (!selectedType && !showCustomType) {
      setError('Please select an activity type');
      audioManager.playSound('error', 0.3);
      return;
    }
    
    if (showCustomType && !customType.trim()) {
      setError('Please enter a custom activity type');
      audioManager.playSound('error', 0.3);
      return;
    }
    
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
      const responseData = await BridgeService.recordActivity(requestData);
      
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
      console.error('Error submitting activity data:', err);
      
      // Get error message
      const errorMessage = err.data?.message || err.message || 'Failed to save activity data. Please try again.';
      
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
  
  // Get color based on intensity level
  const getIntensityColor = (level) => {
    const colors = {
      1: 'var(--neutral-500)',  // Very Low
      2: 'var(--info)',         // Low
      3: 'var(--primary)',      // Moderate
      4: 'var(--warning)',      // High
      5: 'var(--accent)'        // Very High
    };
    
    return colors[level] || 'var(--primary)';
  };
  
  // Get label for intensity level
  const getIntensityLabel = (level) => {
    const labels = {
      1: 'Very Low',
      2: 'Low',
      3: 'Moderate',
      4: 'High',
      5: 'Very High'
    };
    
    return labels[level] || 'Moderate';
  };
  
  // Get color based on mood impact
  const getMoodImpactColor = (impact) => {
    if (impact > 0) return 'var(--success)';
    if (impact < 0) return 'var(--error)';
    return 'var(--neutral-500)';
  };
  
  // Get label for mood impact
  const getMoodImpactLabel = (impact) => {
    if (impact === 2) return 'Very Positive';
    if (impact === 1) return 'Positive';
    if (impact === 0) return 'Neutral';
    if (impact === -1) return 'Negative';
    if (impact === -2) return 'Very Negative';
    return 'Neutral';
  };
  
  // Create intensity rating buttons
  const renderIntensityButtons = () => {
    return Array.from({ length: 5 }, (_, i) => i + 1).map(level => (
      <button
        key={level}
        type="button"
        className={`rating-button ${level === intensity ? 'active' : ''}`}
        onClick={() => handleIntensityChange(level)}
        style={{ 
          '--active-color': getIntensityColor(level) 
        }}
      >
        {level}
      </button>
    ));
  };
  
  // Create mood impact rating buttons
  const renderMoodImpactButtons = () => {
    return Array.from({ length: 5 }, (_, i) => i - 2).map(impact => (
      <button
        key={impact}
        type="button"
        className={`rating-button ${impact === moodImpact ? 'active' : ''}`}
        onClick={() => handleMoodImpactChange(impact)}
        style={{ 
          '--active-color': getMoodImpactColor(impact) 
        }}
      >
        {impact === -2 && <FontAwesomeIcon icon={faSadTear} />}
        {impact === -1 && '−'}
        {impact === 0 && '○'}
        {impact === 1 && '+'}
        {impact === 2 && <FontAwesomeIcon icon={faSmile} />}
      </button>
    ));
  };
  
  // Render activity type buttons
  const renderActivityTypeButtons = () => {
    return activityTypes.map(type => (
      <motion.button
        key={type.id}
        type="button"
        className={`activity-type-button ${selectedType === type.id ? 'selected' : ''}`}
        onClick={() => handleTypeSelect(type.id)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <div className="activity-icon" style={{ color: type.color }}>
          <FontAwesomeIcon icon={type.icon} />
        </div>
        <span>{type.label}</span>
      </motion.button>
    ));
  };
  
  return (
    <div className="activity-tracker-container" ref={formRef}>
      <form onSubmit={handleSubmit}>
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">
              <FontAwesomeIcon icon={faRunning} className="mr-2" /> Track Your Activity
            </h2>
            <p className="card-subtitle">Record activities to discover how they influence your mood and well-being</p>
          </div>
          
          <div className="card-body">
            {/* Activity Type Section */}
            <div className="form-group">
              <label className="form-label">Activity Type</label>
              <div className="activity-types-grid">
                {renderActivityTypeButtons()}
                
                <motion.button
                  type="button"
                  className={`activity-type-button custom-type ${showCustomType ? 'selected' : ''}`}
                  onClick={toggleCustomType}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <div className="activity-icon" style={{ color: 'var(--secondary)' }}>
                    <FontAwesomeIcon icon={faPlus} />
                  </div>
                  <span>Custom</span>
                </motion.button>
              </div>
              
              {showCustomType && (
                <div className="custom-type-input">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Enter activity type"
                    value={customType}
                    onChange={(e) => setCustomType(e.target.value)}
                    autoFocus
                  />
                </div>
              )}
            </div>
            
            {/* Duration Section */}
            <div className="form-group">
              <label className="form-label">
                <FontAwesomeIcon icon={faClock} className="mr-2" /> Duration
              </label>
              <div className="duration-control">
                <button 
                  type="button" 
                  className="btn btn-outline btn-icon"
                  onClick={() => adjustDuration(-5)}
                  disabled={duration <= 5}
                >
                  <FontAwesomeIcon icon={faMinus} />
                </button>
                
                <div className="duration-value">
                  {formatDuration(duration)}
                </div>
                
                <button 
                  type="button" 
                  className="btn btn-outline btn-icon"
                  onClick={() => adjustDuration(5)}
                >
                  <FontAwesomeIcon icon={faPlus} />
                </button>
              </div>
              
              <div className="duration-presets">
                <button 
                  type="button" 
                  className="btn btn-sm btn-outline"
                  onClick={() => setDuration(15)}
                >
                  15m
                </button>
                <button 
                  type="button" 
                  className="btn btn-sm btn-outline"
                  onClick={() => setDuration(30)}
                >
                  30m
                </button>
                <button 
                  type="button" 
                  className="btn btn-sm btn-outline"
                  onClick={() => setDuration(45)}
                >
                  45m
                </button>
                <button 
                  type="button" 
                  className="btn btn-sm btn-outline"
                  onClick={() => setDuration(60)}
                >
                  1h
                </button>
                <button 
                  type="button" 
                  className="btn btn-sm btn-outline"
                  onClick={() => setDuration(90)}
                >
                  1.5h
                </button>
              </div>
            </div>
            
            {/* Intensity Section */}
            <div className="form-group">
              <label className="form-label">
                <FontAwesomeIcon icon={faHeartbeat} className="mr-2" /> Intensity
              </label>
              <div className="rating-control">
                {renderIntensityButtons()}
                <span className="rating-label" style={{ color: getIntensityColor(intensity) }}>
                  {getIntensityLabel(intensity)}
                </span>
              </div>
            </div>
            
            {/* Mood Impact Section */}
            <div className="form-group">
              <label className="form-label">
                <FontAwesomeIcon icon={faBrain} className="mr-2" /> Mood Impact
              </label>
              <div className="rating-control mood-impact">
                {renderMoodImpactButtons()}
                <span className="rating-label" style={{ color: getMoodImpactColor(moodImpact) }}>
                  {getMoodImpactLabel(moodImpact)}
                </span>
              </div>
            </div>
            
            {/* Notes Section */}
            <div className="form-group">
              <label className="form-label" htmlFor="activity-notes">
                Notes (optional)
              </label>
              <textarea
                id="activity-notes"
                className="form-control"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Any additional details about this activity?"
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
                Activity recorded successfully!
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
                    <FontAwesomeIcon icon={faSave} className="mr-2" /> Save Activity
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

export default ActivityTracker;
