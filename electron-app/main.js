import { app, BrowserWindow, ipcMain } from 'electron'
import path from 'path'
import { fileURLToPath } from 'url'
import { spawn } from 'child_process'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

let pythonProcess = null;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    }
  })

  // Start Python backend process
  const backendPath = path.join(__dirname, '..', 'simplify_server.py');
  console.log('Starting Python backend:', backendPath);

  // Use python3 if available, otherwise python
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  pythonProcess = spawn(pythonCmd, [backendPath]);

  pythonProcess.stdout.on('data', (data) => {
    // We only use stdout for response processing in ipcMain below,
    // but log it here if needed for debugging
    // console.log(`Python stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });

  if (process.env.VITE_DEV_SERVER_URL) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL)
    win.webContents.openDevTools()
  } else {
    win.loadFile(path.join(__dirname, 'dist/index.html'))
  }
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('will-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
})

// IPC Handler
ipcMain.handle('simplify', async (event, payload) => {
  return new Promise((resolve, reject) => {
    if (!pythonProcess) {
      reject(new Error("Python process is not running"));
      return;
    }

    // Buffer to accumulate stdout data
    let buffer = '';

    // Function to handle stdout data
    const handleResponse = (data) => {
      buffer += data.toString();

      // Try to parse complete JSON objects from buffer
      while (buffer.length > 0) {
        try {
          // Look for the first complete JSON object (ending with newline)
          const newlineIndex = buffer.indexOf('\n');
          if (newlineIndex === -1) {
            // No complete JSON yet, wait for more data
            break;
          }

          const jsonStr = buffer.slice(0, newlineIndex);
          buffer = buffer.slice(newlineIndex + 1); // Remove processed data + newline

          if (jsonStr.trim() === '') {
            // Skip empty lines
            continue;
          }

          const result = JSON.parse(jsonStr);

          // Remove the listener since we got our response
          pythonProcess.stdout.off('data', handleResponse);

          if (result.error) {
            reject(new Error(result.error));
          } else {
            resolve(result);
          }
          return; // Exit after resolving/rejecting
        } catch (err) {
          // Invalid JSON, discard and continue (shouldn't happen with valid backend)
          console.error('Failed to parse JSON from Python backend:', err, 'Data:', buffer.slice(0, 100));
          buffer = ''; // Clear buffer on parse error to avoid infinite loop
          break;
        }
      }
    };

    pythonProcess.stdout.on('data', handleResponse);

    // Send the request
    const requestJson = JSON.stringify(payload) + '\n';
    pythonProcess.stdin.write(requestJson);

    // Set up timeout to prevent hanging requests
    const timeoutId = setTimeout(() => {
      pythonProcess.stdout.off('data', handleResponse);
      reject(new Error("Request to Python backend timed out"));
    }, 30000); // 30 second timeout

    // Clean up timeout when promise settles
    const cleanup = () => {
      clearTimeout(timeoutId);
      pythonProcess.stdout.off('data', handleResponse);
    };

    // Attach cleanup to both resolve and reject paths
    const originalResolve = resolve;
    const originalReject = reject;
    resolve = (...args) => {
      cleanup();
      return originalResolve(...args);
    };
    reject = (...args) => {
      cleanup();
      return originalReject(...args);
    };
  });
});