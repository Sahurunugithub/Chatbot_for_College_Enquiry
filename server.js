// Import the required modules
const express = require('express');
const { spawn } = require('child_process');

// Create an instance of the Express server
const app = express();

// Define a route that will spawn a new child process for the chatbot program
app.get('/', (req, res) => {
  // Spawn a new child process for the chatbot program
  const chatbotProcess = spawn('python', ['chatgui1.py']);

  // When the child process outputs data, send it to the client
  chatbotProcess.stdout.on('data', (data) => {
    res.write(data.toString());
  });

  // When the child process exits, end the response
  chatbotProcess.on('exit', (code) => {
    res.end();
  });
});

// Start the server on port 3000
app.listen(3000, () => {
  console.log('Chatbot server listening on port 3000');
});

// Open a new browser window to the chatbot server URL
function openChatbot() {
  var chatWindow = window.open('http://localhost:3000/', 'Chat GUI', 'width=400,height=600');
  chatWindow.focus();
}
