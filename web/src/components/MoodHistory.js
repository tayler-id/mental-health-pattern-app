import React, { useState, useEffect } from 'react';

const MoodHistory = () => {
  const [moodEntries, setMoodEntries] = useState([]);

  useEffect(() => {
    const fetchMoodHistory = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/get-mood-history');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setMoodEntries(data);
      } catch (error) {
        console.error('Error fetching mood history:', error);
      }
    };

    fetchMoodHistory();
  }, []);

  return (
    <div>
      <h3>Mood History</h3>
      {moodEntries.length > 0 ? (
        <ul>
          {moodEntries.map(entry => (
            <li key={entry.timestamp}>
              {new Date(entry.timestamp).toLocaleString()}: Mood Level - {entry.mood_level}
            </li>
          ))}
        </ul>
      ) : (
        <p>No mood entries found.</p>
      )}
    </div>
  );
};

export default MoodHistory;
