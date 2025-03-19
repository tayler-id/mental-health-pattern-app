# Mobile App Offline Storage

## Overview

The Mental Health Pattern Recognition mobile app now supports offline data entry, allowing users to record mood entries even when there's no internet connection. The app will automatically synchronize these entries with the server when connectivity is restored.

## Features

### Offline Data Entry

- Users can record mood entries without an internet connection
- Entries are stored locally on the device
- Visual indicators show when the app is operating in offline mode
- Reduced point awards for offline entries (5 points vs 10 points when online)

### Synchronization

- Automatic detection of network connectivity changes
- Prompt to sync entries when connection is restored
- Background synchronization every 15 minutes
- Manual sync option when entries are pending
- Visual feedback during the sync process
- Detailed sync status and error reporting

### User Interface Elements

- **OFFLINE** label appears in the status bar when no connection is available
- Sync button with pending entry count appears when offline entries need to be synchronized
- Last sync time displayed to indicate when entries were last synchronized
- Sync status modal provides feedback during synchronization

## Technical Implementation

### Components

1. **offline-storage.js**: Core module for offline storage functionality
   - Manages AsyncStorage operations for local data storage
   - Handles entry synchronization with the server
   - Tracks pending entries and sync status

2. **App.js**: UI Integration
   - Network connectivity monitoring
   - Offline mode detection and visual indicators
   - Sync status display
   - Background sync scheduling

### Dependencies

The following dependencies were added to support offline storage:

- **@react-native-async-storage/async-storage**: For persistent local storage
- **@react-native-community/netinfo**: For network connectivity monitoring

## User Guide

### Recording Entries Offline

1. When your device has no internet connection, the app will display "OFFLINE" in the status bar
2. Record your mood entry as usual
3. The entry will be saved locally with a confirmation message
4. A sync button will appear showing the number of pending entries

### Synchronizing Entries

Entries can be synchronized in several ways:

1. **Automatic Sync**: When internet connection is restored, the app will prompt you to sync
2. **Background Sync**: The app attempts to sync pending entries every 15 minutes
3. **Manual Sync**: Tap the "Sync" button in the status bar to manually trigger synchronization

### Checking Sync Status

- The last successful sync time is displayed below the streak bar
- During synchronization, a modal appears showing the current status
- Sync results (success, partial, or failure) are displayed in the modal

## Error Handling

The app provides robust error handling for various scenarios:

1. **Network Errors**: When a server request fails due to network issues, the app offers to save the entry offline
2. **Server Errors**: Detailed error messages from the server are displayed
3. **Sync Failures**: The app shows which entries were successfully synced and which failed

## Future Enhancements

Planned improvements for offline functionality:

1. **Conflict Resolution**: More sophisticated handling of conflicting entries
2. **Selective Sync**: Allow users to choose which entries to synchronize
3. **Sync History**: Detailed log of synchronization attempts and results
4. **Data Compression**: Reduce bandwidth usage during synchronization
