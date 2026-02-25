# Testing & Screenshot Instructions

To launch the app and take the required screenshots for the presentation/results slide:

1. **Start the app:**
   Open a terminal in the `electron-app` directory and run:
   ```bash
   npm run start
   ```
   This will start both the Vite dev server and launch the Electron window, automatically running the Python `simplify_server.py` in the background.

2. **Wait for AI to Load:**
   The very first time you ask it to simplify, it will load the `t5-simplifier` model, which might take a few seconds.

3. **Required Screenshots (Day 5 Goal):**

   *   **Screenshot 1: Light Theme - Dyslexia Mode (Default)**
       *   Open the app (it defaults to Light Theme and Dyslexia Mode).
       *   Paste some text into the left pane.
       *   Click "Simplify Text" and wait for the results.
       *   Take a screenshot of the entire window.

   *   **Screenshot 2: High-Contrast Theme - Autism Mode**
       *   Click the Gear icon (⚙) to open settings.
       *   Select "High Contrast" under Display & Theme.
       *   Close the settings panel.
       *   Change the mode dropdown from "Dyslexia Friendly" to "Literal Clarity" (Autism mode).
       *   Take a screenshot.

   *   **Screenshot 3: Dark Theme - ADHD Focus Mode**
       *   Open settings again (⚙).
       *   Select "Dark" under Display & Theme.
       *   Close settings.
       *   Change the mode dropdown to "ADHD Focus".
       *   Click "Next" a few times to highlight a middle sentence.
       *   Take a screenshot.

If you encounter any issues with the Python backend not starting, ensure `transformers`, `torch`, and `textstat` are installed in your Python environment.
