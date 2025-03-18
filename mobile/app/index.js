import React, { useState } from 'react';
import { AppRegistry, View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';

const App = () => {
  const [points, setPoints] = useState(0);
  const [streak, setStreak] = useState(0);
  const streakWidth = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => {
    console.log('Animating streak to:', streakWidth.value); // Debug log
    return { width: `${streakWidth.value}%` };
  });

  const recordMood = async () => {
    try {
      console.log('Attempting to record mood...');
      const response = await fetch('http://10.0.0.100:3000/record-mood', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood: 'positive' }) // Example payload
      });
      if (!response.ok) throw new Error(`Server error: ${response.status}`);
      console.log('Mood recorded successfully');
      setPoints(points + 10);
      const newStreak = Math.min(streak + 1, 7);
      setStreak(newStreak);
      streakWidth.value = withSpring((newStreak / 7) * 100);
      setTimeout(() => alert('Mood recorded successfully!'), 500);
    } catch (err) {
      console.error('Record mood failed:', err);
      alert('Failed to record mood: ' + err.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Mental Health Tracker</Text>
      <Text style={styles.points}>Points: {points}</Text>
      <View style={styles.streakBar}>
        <Animated.View style={[styles.streakFill, animatedStyle]} />
      </View>
      <TouchableOpacity onPress={recordMood} style={styles.button}>
        <Text style={styles.buttonText}>Record Mood</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#f0f0f0' },
  title: { fontSize: 24, color: '#2c3e50', marginBottom: 20 },
  points: { fontSize: 18, color: '#3498db', marginBottom: 10 },
  streakBar: { width: 300, height: 20, backgroundColor: '#ddd', marginBottom: 20 },
  streakFill: { height: '100%', backgroundColor: '#2ecc71' },
  button: { padding: 10, backgroundColor: '#3498db', borderRadius: 5 },
  buttonText: { color: 'white', fontSize: 16 },
});

AppRegistry.registerComponent('main', () => App);

export default App;