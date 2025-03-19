/**
 * Offline Storage Manager for Mental Health Pattern App
 * 
 * This module handles local storage of mood entries when offline and
 * synchronization with the server when connection is restored.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

// Storage keys
const OFFLINE_ENTRIES_KEY = 'offline_mood_entries';
const LAST_SYNC_KEY = 'last_sync_timestamp';

/**
 * Saves a mood entry to local storage for later synchronization
 * @param {Object} entry The mood entry to save
 * @returns {Promise<void>}
 */
export const saveOfflineEntry = async (entry) => {
  try {
    // Get existing entries
    const existingEntriesJson = await AsyncStorage.getItem(OFFLINE_ENTRIES_KEY);
    const existingEntries = existingEntriesJson ? JSON.parse(existingEntriesJson) : [];
    
    // Add new entry
    existingEntries.push({
      ...entry,
      offlineId: Date.now().toString(), // Add unique ID for tracking
      pendingSync: true
    });
    
    // Save back to storage
    await AsyncStorage.setItem(OFFLINE_ENTRIES_KEY, JSON.stringify(existingEntries));
    console.log('Entry saved to offline storage:', entry);
    return true;
  } catch (error) {
    console.error('Error saving offline entry:', error);
    return false;
  }
};

/**
 * Retrieves all pending offline entries
 * @returns {Promise<Array>} Array of pending entries
 */
export const getPendingOfflineEntries = async () => {
  try {
    const entriesJson = await AsyncStorage.getItem(OFFLINE_ENTRIES_KEY);
    const entries = entriesJson ? JSON.parse(entriesJson) : [];
    return entries.filter(entry => entry.pendingSync);
  } catch (error) {
    console.error('Error getting pending offline entries:', error);
    return [];
  }
};

/**
 * Marks entries as synchronized
 * @param {Array} offlineIds Array of offline IDs that were successfully synced
 * @returns {Promise<boolean>} Success status
 */
export const markEntriesAsSynced = async (offlineIds) => {
  try {
    const entriesJson = await AsyncStorage.getItem(OFFLINE_ENTRIES_KEY);
    let entries = entriesJson ? JSON.parse(entriesJson) : [];
    
    // Mark synced entries
    entries = entries.map(entry => {
      if (offlineIds.includes(entry.offlineId)) {
        return { ...entry, pendingSync: false };
      }
      return entry;
    });
    
    // Remove entries that have been synced for more than 7 days
    const sevenDaysAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
    entries = entries.filter(entry => 
      entry.pendingSync || new Date(entry.timestamp).getTime() > sevenDaysAgo
    );
    
    // Save updated entries
    await AsyncStorage.setItem(OFFLINE_ENTRIES_KEY, JSON.stringify(entries));
    
    // Update last sync timestamp
    await AsyncStorage.setItem(LAST_SYNC_KEY, Date.now().toString());
    
    return true;
  } catch (error) {
    console.error('Error marking entries as synced:', error);
    return false;
  }
};

/**
 * Attempts to synchronize all pending entries with the server
 * @param {string} serverUrl The server URL to sync with
 * @returns {Promise<Object>} Sync results with success and error counts
 */
export const syncOfflineEntries = async (serverUrl) => {
  // Check internet connection
  const netInfo = await NetInfo.fetch();
  if (!netInfo.isConnected) {
    console.log('No internet connection available for sync');
    return { success: false, synced: 0, failed: 0, error: 'No internet connection' };
  }
  
  try {
    const pendingEntries = await getPendingOfflineEntries();
    
    if (pendingEntries.length === 0) {
      console.log('No pending entries to sync');
      return { success: true, synced: 0, failed: 0 };
    }
    
    console.log(`Attempting to sync ${pendingEntries.length} offline entries`);
    
    const results = { success: true, synced: 0, failed: 0, errors: [] };
    const syncedIds = [];
    
    // Process each pending entry
    for (const entry of pendingEntries) {
      try {
        // Remove offline tracking properties before sending to server
        const { offlineId, pendingSync, ...serverEntry } = entry;
        
        const response = await fetch(serverUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(serverEntry),
          signal: AbortSignal.timeout(8000)
        });
        
        if (!response.ok) {
          throw new Error(`Server returned ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
          syncedIds.push(offlineId);
          results.synced += 1;
        } else {
          throw new Error(data.error || 'Server reported failure');
        }
      } catch (error) {
        console.error(`Failed to sync entry ${entry.offlineId}:`, error);
        results.failed += 1;
        results.errors.push({ 
          entryId: entry.offlineId, 
          error: error.message
        });
      }
    }
    
    // Update local storage to mark synced entries
    if (syncedIds.length > 0) {
      await markEntriesAsSynced(syncedIds);
    }
    
    // Update overall success flag if any failed
    if (results.failed > 0) {
      results.success = false;
    }
    
    console.log('Sync results:', results);
    return results;
    
  } catch (error) {
    console.error('Error during sync process:', error);
    return { 
      success: false, 
      synced: 0, 
      failed: 0, 
      error: `Sync process error: ${error.message}` 
    };
  }
};

/**
 * Gets the count of pending offline entries
 * @returns {Promise<number>} Number of pending entries
 */
export const getPendingEntryCount = async () => {
  const entries = await getPendingOfflineEntries();
  return entries.length;
};

/**
 * Gets the last sync timestamp
 * @returns {Promise<string>} Timestamp of last successful sync
 */
export const getLastSyncTime = async () => {
  try {
    return await AsyncStorage.getItem(LAST_SYNC_KEY);
  } catch (error) {
    console.error('Error getting last sync time:', error);
    return null;
  }
};

/**
 * Schedules regular sync attempts in the background
 * @param {string} serverUrl The server URL to sync with
 * @param {number} intervalMinutes How often to attempt sync (in minutes)
 * @returns {Function} Function to cancel the scheduled sync
 */
export const scheduleBackgroundSync = (serverUrl, intervalMinutes = 15) => {
  const intervalId = setInterval(async () => {
    const pendingCount = await getPendingEntryCount();
    if (pendingCount > 0) {
      console.log(`Background sync: attempting to sync ${pendingCount} entries`);
      await syncOfflineEntries(serverUrl);
    }
  }, intervalMinutes * 60 * 1000);
  
  return () => clearInterval(intervalId);
};
