import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faSmile,
  faFrown,
  faMeh,
  faGrinBeam,
  faSadTear,
  faPaperPlane,
  faSpinner
} from '@fortawesome/free-solid-svg-icons';
import { useAppContext } from '../context/AppContext';
import './MoodEntryForm.css';

const EMOTIONS = [
  { name: 'happy', label: 'Happy', category: 'positive' },
  { name: 'content', label: 'Content', category: 'positive' },
  { name: 'excited', label: 'Excited', category: 'positive' },
  { name: 'grateful', label: 'Grateful', category: 'positive' },
  { name: 'relaxed', label: 'Relaxed', category: 'positive' },
  { name: 'calm', label: 'Calm', category: 'positive' },
  { name: 'neutral', label: 'Neutral', category: 'neutral' },
  { name: 'contemplative', label: 'Contemplative', category: 'neutral' },
  { name: 'focused', label: 'Focused', category: 'neutral' },
  { name: 'tired', label: 'Tired', category: 'negative' },
  { name: 'anxious', label: 'Anxious', category: 'negative' },
  { name: 'sad', label: 'Sad', category: 'negative' },
  { name: 'stressed', label: 'Stressed', category: 'negative' },
  { name: 'overwhelmed', label: 'Overwhelmed', category: 'negative' },
  { name: 'frustrated', label: 'Frustrated', category: 'negative' },
  { name: 'angry', label: 'Angry', category: 'negative' },
  { name: 'hopeless', label: 'Hopeless', category: 'negative' },
  { name: 'depressed', label: 'Depressed', category: 'negative' }
];

const MoodEntryForm = () => {
  const { createMoodEntry, loading, errors } = useAppContext();

  const [moodLevel, setMoodLevel] = useState(5);
  const [selectedEmotions, setSelectedEmotions] = useState([]);
  const [notes, setNotes] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState('');

  // Get mood icon based on level
  const getMoodIcon = (level) => {
    if (level >= 8) return faGrinBeam;
    if (level >= 6) return faSmile;
    if (level >= 4) return faMeh;
    if (level >= 2) return faFrown;
    return faSadTear;
  };

  // Get mood label based on level
  const getMoodLabel = (level) => {
    if (level >= 9) return 'Excellent';
    if (level >= 7) return 'Good';
    if (level >= 5) return 'Okay';
    if (level >= 3) return 'Poor';
    if (level >= 1) return 'Very Poor';
    return 'Unknown';
  };

  // Handle emotion selection
  const handleEmotionToggle = (emotion) => {
    if (selectedEmotions.includes(emotion)) {
      setSelectedEmotions(selectedEmotions.filter(e => e !== emotion));
    } else {
      // Limit to 5 emotions
      if (selectedEmotions.length < 5) {
        setSelectedEmotions([...selectedEmotions, emotion]);
      }
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Try to use the context API first
      if (createMoodEntry) {
        await createMoodEntry({
          mood_level: moodLevel,
          emotions: selectedEmotions,
          notes,
          timestamp: new Date().toISOString()
        });
      } else {
        // Fall back to direct API call if context is not available
        const response = await fetch('http://127.0.0.1:5000/api/record-mood', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            mood_level: moodLevel,
            notes: notes,
            emotions: selectedEmotions,
          }),
        });

        const data = await response.json();
        setMessage(data.message);
      }

      // Reset form
      setMoodLevel(5);
      setSelectedEmotions([]);
      setNotes('');
      setSubmitted(true);

      // Reset submitted state after 3 seconds
      setTimeout(() => {
        setSubmitted(false);
      }, 3000);
    } catch (error) {
      console.error('Error submitting mood entry:', error);
      setMessage('Error recording mood. Please try again.');
    }
  };

  return (
    <div className="mood-entry-form-container">
      <h3 className="form-title">
        <FontAwesomeIcon icon={faSmile} />
        Record Your Mood
      </h3>

      {submitted ? (
        <motion.div
          className="success-message"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
        >
          <FontAwesomeIcon icon={faSmile} />
          <p>Mood recorded successfully!</p>
        </motion.div>
      ) : (
        <form onSubmit={handleSubmit} className="mood-form">
          <div className="mood-slider-container">
            <label htmlFor="mood-level">How are you feeling today?</label>
            <div className="mood-level-display">
              <FontAwesomeIcon icon={getMoodIcon(moodLevel)} />
              <span>{getMoodLabel(moodLevel)}</span>
            </div>
            <input
              type="range"
              id="mood-level"
              min="1"
              max="10"
              step="1"
              value={moodLevel}
              onChange={(e) => setMoodLevel(parseInt(e.target.value, 10))}
              className="mood-slider"
            />
            <div className="mood-scale-labels">
              <span>1</span>
              <span>2</span>
              <span>3</span>
              <span>4</span>
              <span>5</span>
              <span>6</span>
              <span>7</span>
              <span>8</span>
              <span>9</span>
              <span>10</span>
            </div>
          </div>

          <div className="emotions-container">
            <label>Select up to 5 emotions you're experiencing:</label>
            <div className="emotions-grid">
              {EMOTIONS.map((emotion) => (
                <button
                  key={emotion.name}
                  type="button"
                  className={`emotion-button ${emotion.category} ${selectedEmotions.includes(emotion.name) ? 'selected' : ''}`}
                  onClick={() => handleEmotionToggle(emotion.name)}
                >
                  {emotion.label}
                </button>
              ))}
            </div>
          </div>

          <div className="notes-container">
            <label htmlFor="mood-notes">Additional notes (optional):</label>
            <textarea
              id="mood-notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="What's on your mind? Any specific events or thoughts affecting your mood?"
              rows="3"
            />
          </div>

          {(errors?.createMood || message) && (
            <div className="error-message">
              <p>{errors?.createMood || message}</p>
            </div>
          )}

          <button
            type="submit"
            className="submit-button"
            disabled={loading?.createMood}
          >
            {loading?.createMood ? (
              <>
                <FontAwesomeIcon icon={faSpinner} spin />
                Saving...
              </>
            ) : (
              <>
                <FontAwesomeIcon icon={faPaperPlane} />
                Save Mood Entry
              </>
            )}
          </button>
        </form>
      )}
    </div>
  );
};

export default MoodEntryForm;
