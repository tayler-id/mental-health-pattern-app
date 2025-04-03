/**
 * Python Bridge Service
 * 
 * Provides a bridge between the Node.js server and the Python CLI application.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Path to the Python executable and main script
const PYTHON_PATH = process.env.PYTHON_PATH || 'python';
const SCRIPT_PATH = path.resolve(__dirname, '../../../src/web_bridge.py');

// Check if the bridge script exists
if (!fs.existsSync(SCRIPT_PATH)) {
  console.error(`Error: Python bridge script not found at ${SCRIPT_PATH}`);
  console.error('Please make sure the web_bridge.py file exists in the src directory.');
}

/**
 * Call a Python function in the CLI application
 * 
 * @param {string} functionName - Name of the Python function to call
 * @param {object} params - Parameters to pass to the function
 * @returns {Promise<any>} - Promise resolving to the function result
 */
exports.callPythonFunction = async (functionName, params = {}) => {
  return new Promise((resolve, reject) => {
    // Create a unique ID for this request
    const requestId = Date.now().toString();
    
    // Prepare the input data
    const inputData = {
      function: functionName,
      params: params,
      request_id: requestId
    };
    
    // Spawn a Python process
    const pythonProcess = spawn(PYTHON_PATH, [SCRIPT_PATH], {
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    let outputData = '';
    let errorData = '';
    
    // Collect stdout data
    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
    });
    
    // Collect stderr data
    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString();
      console.error(`Python stderr: ${data}`);
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`Python process exited with code ${code}: ${errorData}`));
      }
      
      try {
        // Parse the JSON output
        const result = JSON.parse(outputData);
        
        // Check for errors
        if (result.error) {
          return reject(new Error(result.error.message || 'Unknown error from Python'));
        }
        
        // Return the result data
        resolve(result.data);
      } catch (error) {
        reject(new Error(`Failed to parse Python output: ${error.message}`));
      }
    });
    
    // Handle process errors
    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to start Python process: ${error.message}`));
    });
    
    // Send input data to the Python process
    pythonProcess.stdin.write(JSON.stringify(inputData));
    pythonProcess.stdin.end();
  });
};

/**
 * Run a Python script and return the result
 * 
 * @param {string} scriptPath - Path to the Python script
 * @param {Array<string>} args - Arguments to pass to the script
 * @returns {Promise<string>} - Promise resolving to the script output
 */
exports.runPythonScript = async (scriptPath, args = []) => {
  return new Promise((resolve, reject) => {
    // Spawn a Python process
    const pythonProcess = spawn(PYTHON_PATH, [scriptPath, ...args], {
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    let outputData = '';
    let errorData = '';
    
    // Collect stdout data
    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
    });
    
    // Collect stderr data
    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString();
      console.error(`Python stderr: ${data}`);
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`Python process exited with code ${code}: ${errorData}`));
      }
      
      resolve(outputData.trim());
    });
    
    // Handle process errors
    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to start Python process: ${error.message}`));
    });
  });
};
