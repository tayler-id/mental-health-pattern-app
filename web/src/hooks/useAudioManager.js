import { useState, useEffect, useCallback } from 'react';
import { Howl } from 'howler';

// Hook for managing audio playback in the application
export const useAudioManager = () => {
  const [sounds, setSounds] = useState({});
  const [muted, setMuted] = useState(
    localStorage.getItem('audio_muted') === 'true'
  );
  
  // Initialize sound sources
  const soundSources = {
    click: '/assets/sounds/click.mp3',
    success: '/assets/sounds/success.mp3',
    achievement: '/assets/sounds/achievement.mp3',
    error: '/assets/sounds/error.mp3',
    streak: '/assets/sounds/streak.mp3',
    levelUp: '/assets/sounds/level-up.mp3',
    notification: '/assets/sounds/notification.mp3',
    typing: '/assets/sounds/typing.mp3',
    sliderMove: '/assets/sounds/slider-move.mp3',
  };
  
  // Preload all sounds
  const preloadSounds = useCallback(() => {
    const loadedSounds = {};
    
    Object.entries(soundSources).forEach(([name, src]) => {
      loadedSounds[name] = new Howl({
        src: [src],
        volume: 0.5,
        preload: true,
        onloaderror: (id, error) => console.error(`Error loading sound ${name}:`, error),
      });
    });
    
    setSounds(loadedSounds);
  }, []);
  
  // Play a sound by name
  const playSound = useCallback((soundName, volume = 0.5) => {
    if (muted || !sounds[soundName]) return;
    
    try {
      const sound = sounds[soundName];
      sound.volume(volume);
      sound.play();
    } catch (error) {
      console.error(`Error playing sound ${soundName}:`, error);
    }
  }, [sounds, muted]);
  
  // Toggle mute state
  const toggleMute = useCallback(() => {
    const newMuted = !muted;
    setMuted(newMuted);
    localStorage.setItem('audio_muted', newMuted.toString());
    
    // Play a test sound when unmuting
    if (!newMuted) {
      setTimeout(() => playSound('click', 0.3), 100);
    }
  }, [muted, playSound]);
  
  // Check if audio is muted
  const isMuted = useCallback(() => muted, [muted]);
  
  // Load user preference on component mount
  useEffect(() => {
    const userPreference = localStorage.getItem('audio_muted');
    if (userPreference !== null) {
      setMuted(userPreference === 'true');
    }
  }, []);
  
  // Create a sound sprite for continuous UI feedback
  const createUISoundSprite = useCallback(() => {
    return new Howl({
      src: ['/assets/sounds/ui-sounds.mp3'],
      sprite: {
        hover: [0, 100],
        click: [200, 150],
        toggle: [400, 200]
      }
    });
  }, []);
  
  // Speech synthesis for announcements
  const speak = useCallback((text, rate = 1, pitch = 1) => {
    if (muted || !window.speechSynthesis) return;
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = rate;
    utterance.pitch = pitch;
    utterance.volume = 0.8;
    
    window.speechSynthesis.speak(utterance);
  }, [muted]);
  
  // Play a sequence of sounds with delays
  const playSoundSequence = useCallback((soundNames, delay = 200) => {
    if (muted) return;
    
    soundNames.forEach((sound, index) => {
      setTimeout(() => {
        playSound(sound);
      }, index * delay);
    });
  }, [muted, playSound]);
  
  // Special achievement sound with fanfare
  const playAchievementSound = useCallback(() => {
    if (muted) return;
    
    // Play a sequence for more dramatic effect
    playSoundSequence(['notification', 'achievement', 'success'], 300);
    
    // Announce achievement if speech synthesis is available
    setTimeout(() => {
      speak('Achievement unlocked!');
    }, 1000);
  }, [muted, playSoundSequence, speak]);
  
  return {
    preloadSounds,
    playSound,
    toggleMute,
    isMuted,
    createUISoundSprite,
    speak,
    playSoundSequence,
    playAchievementSound
  };
};
