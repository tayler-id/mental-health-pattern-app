import React, { useState, useEffect } from 'react';
import { AppRegistry, View, Text, TouchableOpacity, StyleSheet, Modal, Slider, TextInput, Alert, ActivityIndicator } from 'react-native';
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';
import Sound from 'react-native-sound';
import NetInfo from '@react-native-community/netinfo';
import { 
  saveOfflineEntry, 
  getPendingEntryCount, 
  syncOfflineEntries,
  scheduleBackgroundSync,
  getLastSyncTime
} from '../offline-storage';

const App = () => {
  const [points, setPoints] = useState(0);
  const [streak, setStreak] = useState(0);
  const [modalVisible, setModalVisible] = useState(false);
  const [moodLevel, setMoodLevel] = useState(5);
  const [notes, setNotes] = useState('');
  const [emotions, setEmotions] = useState([]);
  const streakWidth = useSharedValue(0);
  const sound = new Sound('ding.mp3', Sound.MAIN_BUNDLE, (error) => {
    if (error) console.log('Failed to load sound', error);
  });
  const animatedStyle = useAnimatedStyle(() => ({
    width: `${Math.min(streakWidth.value, 100)}%`
  }));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [serverUrl, setServerUrl] = useState('');
  const [serverModalVisible, setServerModalVisible] = useState(false);
  
  // New offline state variables
  const [isConnected, setIsConnected] = useState(true);
  const [pendingEntries, setPendingEntries] = useState(0);
  const [syncModalVisible, setSyncModalVisible] = useState(false);
  const [syncStatus, setSyncStatus] = useState(null);
  const [isSyncing, setIsSyncing] = useState(false);
  const [lastSyncTime, setLastSyncTime] = useState(null);
  
  // Network connectivity monitoring
  useEffect(() => {
    // Subscribe to network state updates
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsConnected(state.isConnected && state.isInternetReachable);
      console.log("Connection status:", state.isConnected, state.isInternetReachable);
      
      // If connection is restored, show sync option
      if (state.isConnected && pendingEntries > 0) {
        Alert.alert(
          'Internet Connection Restored',
          `You have ${pendingEntries} entries saved offline. Would you like to sync them now?`,
          [
            { text: 'Sync Later', style: 'cancel' },
            { 
              text: 'Sync Now', 
              onPress: () => synchronizeOfflineEntries() 
            }
          ]
        );
      }
    });
    
    // Set up background sync
    const cancelBackgroundSync = scheduleBackgroundSync(serverUrl, 15); // Try sync every 15 min
    
    // Load initial offline entry count and last sync time
    const loadOfflineData = async () => {
      const count = await getPendingEntryCount();
      setPendingEntries(count);
      
      const syncTime = await getLastSyncTime();
      if (syncTime) {
        setLastSyncTime(new Date(parseInt(syncTime)).toLocaleString());
      }
    };
    loadOfflineData();
    
    // Clean up on unmount
    return () => {
      unsubscribe();
      cancelBackgroundSync();
    };
  }, [serverUrl, pendingEntries]);
  
  // Check for stored server URL in local storage on component mount
  useEffect(() => {
    // In a real app, we would use AsyncStorage here
    // For now, prompt user to enter the server URL
    setTimeout(() => {
      setServerModalVisible(true);
    }, 500);
  }, []);
  
  // Refreshes the pending entries count
  const refreshPendingCount = async () => {
    const count = await getPendingEntryCount();
    setPendingEntries(count);
  };
  
  // Synchronize offline entries
  const synchronizeOfflineEntries = async () => {
    if (!serverUrl) {
      Alert.alert('Error', 'Server URL not configured. Please go to Settings first.');
      return;
    }
    
    setIsSyncing(true);
    setSyncStatus('Syncing offline entries...');
    setSyncModalVisible(true);
    
    try {
      const result = await syncOfflineEntries(serverUrl);
      
      if (result.success) {
        setSyncStatus(`Sync complete! ${result.synced} entries synchronized.`);
      } else {
        if (result.synced > 0) {
          setSyncStatus(`Partial sync: ${result.synced} entries synced, ${result.failed} failed. Error: ${result.error || 'Unknown error'}`);
        } else {
          setSyncStatus(`Sync failed: ${result.error || 'Unknown error'}`);
        }
      }
      
      // Refresh pending count
      await refreshPendingCount();
      
      // Update last sync time
      const now = Date.now().toString();
      setLastSyncTime(new Date(parseInt(now)).toLocaleString());
      
    } catch (error) {
      setSyncStatus(`Sync error: ${error.message}`);
    } finally {
      setIsSyncing(false);
      setTimeout(() => {
        setSyncModalVisible(false);
      }, 3000); // Hide sync modal after 3 seconds
    }
  };
  
  const recordMood = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (!serverUrl) {
        throw new Error('Server URL not configured. Please go to Settings to configure it.');
      }
      
      // Create entry object
      const entry = { 
        mood_level: moodLevel, 
        notes, 
        emotions, 
        streak,
        timestamp: new Date().toISOString()
      };
      
      console.log('Starting mood record:', entry);
      
      // Check if we're online or offline
      if (!isConnected) {
        console.log('Device is offline, saving entry locally');
        
        // Save entry to local storage
        const saveResult = await saveOfflineEntry(entry);
        
        if (saveResult) {
          // Update UI state (locally)
          setPoints(points + 5); // Less points for offline entry
          const newStreak = Math.min((streak || 0) + 1, 7);
          setStreak(newStreak);
          streakWidth.value = withSpring((newStreak / 7) * 100);
          
          // Reset form
          setModalVisible(false);
          setMoodLevel(5);
          setNotes('');
          setEmotions([]);
          
          // Update pending count
          await refreshPendingCount();
          
          // Show success message
          Alert.alert(
            'Saved Offline', 
            'Your mood entry has been saved offline. It will be synchronized when an internet connection is available.'
          );
          
          // Try to play sound if available
          try {
            sound.play((success) => {
              if (!success) console.log('Sound playback failed');
            });
          } catch (soundErr) {
            console.log('Sound error:', soundErr);
          }
          
          return; // Exit early after offline save
        } else {
          throw new Error('Failed to save entry offline');
        }
      }
      
      // If we're online, proceed with server submission
      const response = await fetch(serverUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry),
        signal: AbortSignal.timeout(8000) // 8s timeout - giving more time for Python execution
      });
      
      console.log('Fetch response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Server response data:', data);
      
      if (!data.success) {
        throw new Error(data.error || 'Server failed to process request');
      }
      
      // Update UI state
      setPoints(points + 10);
      setStreak(data.streak);
      streakWidth.value = withSpring((data.streak / 7) * 100);
      
      // Try to play sound if available
      try {
        sound.play((success) => {
          if (!success) {
            console.log('Sound playback failed');
          }
        });
      } catch (soundErr) {
        console.log('Sound error:', soundErr);
      }
      
      // Reset form
      setModalVisible(false);
      setMoodLevel(5);
      setNotes('');
      setEmotions([]);
      
      Alert.alert('Success', 'Your mood has been recorded successfully!');
      
    } catch (err) {
      console.error('Fetch error details:', { 
        message: err.message, 
        name: err.name, 
        stack: err.stack 
      });
      
      // Set error message based on error type
      let errorMessage = 'An unexpected error occurred';
      
      if (err.name === 'AbortError') {
        errorMessage = 'Request timed out. Please try again.';
      } else if (err.message.includes('Network request failed')) {
        // For network errors, offer to save offline
        Alert.alert(
          'Network Error',
          'Cannot connect to server. Would you like to save this entry offline?',
          [
            { 
              text: 'Cancel', 
              style: 'cancel',
              onPress: () => {
                setError('Network request failed. Entry was not saved.');
              }
            },
            { 
              text: 'Save Offline', 
              onPress: async () => {
                setIsConnected(false); // Force offline mode
                await recordMood(); // Call record again (will use offline path)
              }
            }
          ]
        );
        return; // Exit early to prevent setting error message
      } else {
        errorMessage = `Error: ${err.message}`;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };
  
  const toggleEmotion = (emotion) => {
    setEmotions(emotions.includes(emotion) 
      ? emotions.filter(e => e !== emotion) 
      : [...emotions, emotion]);
  };
  
  const saveServerUrl = () => {
    // In a real app, we would save to AsyncStorage here
    setServerModalVisible(false);
    Alert.alert('Server URL Saved', `Server URL set to: ${serverUrl}`);
  };
  
  const menuOptions = [
    { label: '1. Data Entry', action: () => setModalVisible(true) },
    { label: '2. View Data', action: () => alert('View Data TBD') },
    { label: '3. Analysis', action: () => alert('Analysis TBD') },
    { label: '4. Visualizations', action: () => alert('Visualizations TBD') },
    { label: '5. Insights', action: () => alert('Insights TBD') },
    { label: '6. Settings', action: () => setServerModalVisible(true) },
    { label: '7. Exit', action: () => alert('App closed (not really)') }
  ];
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Mental Health Tracker</Text>
      
      {/* Status Bar */}
      <View style={styles.statusBar}>
        <Text style={styles.points}>Points: {points}</Text>
        {!isConnected && (
          <Text style={styles.offlineText}>OFFLINE</Text>
        )}
        {pendingEntries > 0 && (
          <TouchableOpacity 
            onPress={synchronizeOfflineEntries}
            style={styles.syncButton}
          >
            <Text style={styles.syncButtonText}>
              Sync ({pendingEntries})
            </Text>
          </TouchableOpacity>
        )}
      </View>
      
      <View style={styles.streakBar}>
        <Animated.View style={[styles.streakFill, animatedStyle]} />
      </View>
      
      {/* Last Sync Time */}
      {lastSyncTime && (
        <Text style={styles.syncTime}>Last sync: {lastSyncTime}</Text>
      )}
      
      <Text style={styles.menuTitle}>Main Menu:</Text>
      {menuOptions.map((option, index) => (
        <TouchableOpacity key={index} onPress={option.action} style={styles.button}>
          <Text style={styles.buttonText}>{option.label}</Text>
        </TouchableOpacity>
      ))}
      
      {/* Server URL Configuration Modal */}
      <Modal visible={serverModalVisible} animationType="slide">
        <View style={styles.modal}>
          <Text style={styles.modalTitle}>Server Configuration</Text>
          <Text style={styles.modalText}>
            Enter your server URL. If running on the same network as your computer, 
            use your computer's local IP address with port 3000.
          </Text>
          
          <Text style={styles.labelText}>Server URL:</Text>
          <TextInput
            style={styles.input}
            placeholder="http://192.168.1.X:3000/record-mood"
            value={serverUrl}
            onChangeText={setServerUrl}
            autoCapitalize="none"
            keyboardType="url"
          />
          
          <Text style={styles.helpText}>
            Example formats:{'\n'}
            • For testing in browser: http://localhost:3000/record-mood{'\n'}
            • For Android emulator: http://10.0.2.2:3000/record-mood{'\n'}
            • For devices on same WiFi: http://192.168.1.X:3000/record-mood{'\n'}
            (Replace X with your computer's IP)
          </Text>
          
          <TouchableOpacity 
            onPress={saveServerUrl} 
            style={styles.button}
          >
            <Text style={styles.buttonText}>Save</Text>
          </TouchableOpacity>
          
        </View>
      </Modal>
      
      {/* Sync Status Modal */}
      <Modal 
        visible={syncModalVisible} 
        animationType="fade"
        transparent={true}
      >
        <View style={styles.syncModalContainer}>
          <View style={styles.syncModal}>
            {isSyncing && (
              <ActivityIndicator size="large" color="#3498db" style={styles.syncSpinner} />
            )}
            <Text style={styles.syncStatusText}>{syncStatus}</Text>
          </View>
        </View>
      </Modal>
      
      {/* Mood Recording Modal */}
      <Modal visible={modalVisible} animationType="slide">
        <View style={styles.modal}>
          <Text style={styles.modalTitle}>Record Mood</Text>
          <Text>Mood Level: {moodLevel}</Text>
          <Slider
            minimumValue={1}
            maximumValue={10}
            step={1}
            value={moodLevel}
            onValueChange={setMoodLevel}
            style={styles.slider}
          />
          <TextInput
            style={styles.input}
            placeholder="Notes"
            value={notes}
            onChangeText={setNotes}
          />
          <Text>Emotions:</Text>
          {['happy', 'sad', 'calm'].map(emotion => (
            <TouchableOpacity
              key={emotion}
              style={[styles.emotionButton, emotions.includes(emotion) && styles.selectedEmotion]}
              onPress={() => toggleEmotion(emotion)}
            >
              <Text>{emotion}</Text>
            </TouchableOpacity>
          ))}
          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}
          
          <TouchableOpacity 
            onPress={recordMood} 
            style={[styles.button, loading && styles.disabledButton]} 
            disabled={loading}
          >
            <Text style={styles.buttonText}>
              {loading ? 'Submitting...' : 'Submit'}
            </Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            onPress={() => {
              setModalVisible(false);
              setError(null);  // Clear any errors when closing
            }} 
            style={styles.button}
            disabled={loading}
          >
            <Text style={styles.buttonText}>Cancel</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#f0f0f0' },
  title: { fontSize: 24, color: '#2c3e50', marginBottom: 10 },
  
  // Status bar styles
  statusBar: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    justifyContent: 'space-between',
    width: 300,
    marginBottom: 10
  },
  points: { 
    fontSize: 18, 
    color: '#3498db', 
    flex: 1
  },
  offlineText: {
    color: '#e74c3c',
    fontWeight: 'bold',
    fontSize: 14,
    marginHorizontal: 10
  },
  syncButton: {
    backgroundColor: '#27ae60',
    padding: 5,
    borderRadius: 5,
    marginLeft: 5
  },
  syncButtonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold'
  },
  syncTime: {
    fontSize: 12,
    color: '#7f8c8d',
    marginBottom: 15,
    fontStyle: 'italic'
  },
  
  // Streak and main UI
  streakBar: { width: 300, height: 20, backgroundColor: '#ddd', marginBottom: 10 },
  streakFill: { height: '100%', backgroundColor: '#2ecc71' },
  menuTitle: { fontSize: 18, marginVertical: 10 },
  button: { padding: 10, backgroundColor: '#3498db', borderRadius: 5, margin: 5, width: 300 },
  buttonText: { color: 'white', fontSize: 16, textAlign: 'center' },
  disabledButton: { backgroundColor: '#95a5a6', opacity: 0.7 },
  
  // Modal styles
  modal: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: 'white', padding: 20 },
  modalTitle: { fontSize: 22, marginBottom: 20, fontWeight: 'bold' },
  modalText: { fontSize: 16, marginBottom: 15, textAlign: 'center' },
  labelText: { fontSize: 16, alignSelf: 'flex-start', marginTop: 10, marginBottom: 5 },
  helpText: { fontSize: 14, color: '#7f8c8d', marginTop: 10, marginBottom: 20, textAlign: 'left', alignSelf: 'stretch' },
  
  // Sync modal styles
  syncModalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)'
  },
  syncModal: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5,
    width: '80%'
  },
  syncSpinner: {
    marginBottom: 15
  },
  syncStatusText: {
    fontSize: 16,
    textAlign: 'center',
    color: '#2c3e50'
  },
  
  // Form elements
  slider: { width: 300, marginVertical: 10 },
  input: { width: 300, borderWidth: 1, padding: 10, marginVertical: 10, borderRadius: 5 },
  emotionButton: { padding: 10, borderWidth: 1, margin: 5, borderRadius: 5, width: 100, alignItems: 'center' },
  selectedEmotion: { backgroundColor: '#2ecc71' },
  errorContainer: {
    backgroundColor: '#ffebee',
    padding: 10,
    borderRadius: 5,
    marginVertical: 10,
    width: 300,
    borderWidth: 1,
    borderColor: '#e74c3c'
  },
  errorText: {
    color: '#e74c3c',
    textAlign: 'center'
  }
});

AppRegistry.registerComponent('main', () => App);
export default App;
