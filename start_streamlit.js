const { spawn } = require('child_process');
const path = require('path');

function startStreamlitServer() {
  console.log('Starting Streamlit server...');
  
  const streamlitProcess = spawn('python', [
    '-m', 'streamlit', 'run', 
    path.join(__dirname, 'dashboard.py'),
    '--server.port', '8501',
    '--server.headless', 'true'
  ]);

  streamlitProcess.stdout.on('data', (data) => {
    console.log(`Streamlit: ${data.toString().trim()}`);
  });

  streamlitProcess.stderr.on('data', (data) => {
    console.error(`Streamlit Error: ${data.toString().trim()}`);
  });

  streamlitProcess.on('close', (code) => {
    console.log(`Streamlit process exited with code ${code}`);
  });

  return streamlitProcess;
}

module.exports = { startStreamlitServer };
