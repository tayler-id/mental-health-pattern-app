# Mental Health Tracker Web Application

This is the web version of the Mental Health Pattern Recognition Assistant. It provides an enhanced user experience with animations, sound effects, and interactive UI components.

## Features

- **Interactive UI**: Smooth animations and transitions for a modern user experience
- **Audio Feedback**: Sound effects and voice announcements provide auditory feedback
- **Gamification Elements**: Points system and animated streak tracking
- **Mood Tracking**: Record mood levels with descriptive emotions and notes
- **Achievement System**: Celebrate streaks and consistent tracking
- **Responsive Design**: Works on desktop and mobile devices

## Technologies Used

- **React**: Component-based UI library
- **GSAP**: Advanced animation library
- **Framer Motion**: Animation framework for React
- **Howler.js**: Audio library for sound effects
- **FontAwesome**: Icon library
- **Web Speech API**: For text-to-speech capabilities
- **React Confetti**: For celebration effects

## Project Structure

- `/public`: Static assets and HTML entry point
- `/src`: Source code
  - `/components`: React components
  - `/hooks`: Custom React hooks
  - `/contexts`: React context providers
  - `/styles`: CSS files
  - `/utils`: Utility functions
  - `/services`: API services and data handling

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the web directory
3. Install dependencies:

```bash
npm install
```

### Running the Development Server

```bash
npm start
```

The application will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

## Communication with Backend

The web application communicates with the Node.js server to record mood data. The server then interacts with the Python backend for data storage and analysis.

## Audio Features

The application includes several audio features:
- UI interaction sounds (clicks, form submissions, etc.)
- Achievement celebration sounds
- Voice announcements for significant achievements
- Text-to-speech for insights and feedback

## Animations

Interactive elements feature animations to enhance user experience:
- Menu transitions
- Mood slider feedback
- Achievement celebrations with confetti
- Form element interactions

## Extending the Application

To add new features:
1. Create new components in `/src/components`
2. Add new styles in `/src/styles`
3. Extend the audio manager in `/src/hooks/useAudioManager.js` for new sounds
4. Update the main App.js to include new screens

## Future Development

Future enhancements planned:
- Speech recognition for voice input
- Offline capabilities with local storage
- More visualizations for mood data
- Enhanced achievement system
- Social sharing options
