const fs = require('fs');
const path = require('path');

// Source sound file
const sourceSoundPath = '../mobile/ding.mp3';

// Destination directory
const soundsDir = path.join('public', 'assets', 'sounds');

// Sound files to create
const soundFiles = [
  'click.mp3',
  'success.mp3',
  'achievement.mp3',
  'error.mp3',
  'streak.mp3',
  'level-up.mp3',
  'notification.mp3',
  'typing.mp3',
  'sliderMove.mp3',
  'ui-sounds.mp3'
];

// Check if source file exists
if (!fs.existsSync(sourceSoundPath)) {
  console.error(`Source sound file not found: ${sourceSoundPath}`);
  process.exit(1);
}

// Create all sound files as copies of the source file
soundFiles.forEach(file => {
  const destPath = path.join(soundsDir, file);
  fs.copyFileSync(sourceSoundPath, destPath);
  console.log(`Created placeholder sound: ${destPath}`);
});

console.log('All placeholder sound files created successfully!');
