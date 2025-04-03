const { spawn } = require('child_process');
const path = require('path');
const readline = require('readline');

// Paths and commands
const serverPath = path.join('..', 'mobile', 'server');
const serverCommand = 'node';
const serverArgs = ['index.js'];
const reactCommand = 'react-scripts';
const reactArgs = ['start'];

console.log('Starting Mental Health Tracker Development Environment');
console.log('====================================================');

// Start Node.js server
console.log('\n📡 Starting Node.js server...');
const serverProcess = spawn(serverCommand, serverArgs, {
  cwd: serverPath,
  shell: true,
  stdio: 'pipe',
});

// Add prefix for server logs
const prefixServerLog = (data) => {
  return data
    .toString()
    .trim()
    .split('\n')
    .map(line => `[SERVER] ${line}`)
    .join('\n');
};

serverProcess.stdout.on('data', (data) => {
  console.log('\x1b[36m%s\x1b[0m', prefixServerLog(data)); // Cyan color for server logs
});

serverProcess.stderr.on('data', (data) => {
  console.error('\x1b[31m%s\x1b[0m', prefixServerLog(data)); // Red color for server errors
});

// Wait a moment before starting React app to give the server time to initialize
setTimeout(() => {
  console.log('\n🌐 Starting React development server...');
  const reactProcess = spawn(reactCommand, reactArgs, {
    cwd: process.cwd(),
    shell: true,
    stdio: 'pipe',
  });

  // Add prefix for React logs
  const prefixReactLog = (data) => {
    return data
      .toString()
      .trim()
      .split('\n')
      .map(line => `[REACT] ${line}`)
      .join('\n');
  };

  reactProcess.stdout.on('data', (data) => {
    console.log('\x1b[32m%s\x1b[0m', prefixReactLog(data)); // Green color for React logs
  });

  reactProcess.stderr.on('data', (data) => {
    console.error('\x1b[33m%s\x1b[0m', prefixReactLog(data)); // Yellow color for React warnings
  });

  // Handle process termination
  reactProcess.on('close', (code) => {
    console.log(`\n🌐 React development server exited with code ${code}`);
    serverProcess.kill();
    process.exit(code);
  });
}, 2000);

// Setup CLI interface for commands
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: 'dev> '
});

rl.prompt();

rl.on('line', (line) => {
  const command = line.trim();
  
  switch (command) {
    case 'exit':
    case 'quit':
      console.log('Shutting down development environment...');
      serverProcess.kill();
      process.exit(0);
      break;
      
    case 'help':
      console.log('\nAvailable commands:');
      console.log('  exit, quit - Shut down both servers and exit');
      console.log('  help       - Show this help message');
      console.log('  clear      - Clear the console\n');
      break;
      
    case 'clear':
      console.clear();
      break;
      
    default:
      console.log(`Unknown command: ${command}`);
      console.log('Type "help" for available commands');
  }
  
  rl.prompt();
}).on('close', () => {
  console.log('Shutting down development environment...');
  serverProcess.kill();
  process.exit(0);
});

// Handle process termination
process.on('SIGINT', () => {
  console.log('\nReceived SIGINT. Shutting down...');
  serverProcess.kill();
  process.exit(0);
});

console.log('\n🚀 Development environment starting up...');
console.log('Press Ctrl+C or type "exit" to shut down both servers');
