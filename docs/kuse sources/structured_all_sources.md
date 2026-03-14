# Structured All Sources

This consolidated file combines all source material from `docs/slides sources` for ingestion into retrieval/generation tools such as NotebookLM.

## Coverage Summary

- Markup files: 3
- Text files: 4
- Binary/non-text files: 1

## Part 1 - Markup Sources (MD + HTML)

### Source Files
- `presentation.html`
- `project_design.md`
- `project_explanation.md`

---

### File: presentation.html

#### Extracted Content (markup)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SimplyAI Presentation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #F8F8F6;
            --primary-accent: #2C4A6E;
            --text-color: #2D2D2D;
            --border-color: #D1D1D1;
            --footer-text: #666666;
            --white: #FFFFFF;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            overflow: hidden;
            width: 100vw;
            height: 100vh;
        }

        .presentation-container {
            height: 100vh;
            width: 100vw;
            scroll-snap-type: y mandatory;
            overflow-y: auto;
            scrollbar-width: none;
            -ms-overflow-style: none;
        }

        .presentation-container::-webkit-scrollbar {
            display: none;
        }

        .slide {
            height: 100vh;
            width: 100vw;
            scroll-snap-align: start;
            padding: 4rem 6rem;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
            border-bottom: 1px solid #EEE;
        }

        /* Typography */
        h1, h2, h3 {
            color: var(--primary-accent);
            line-height: 1.2;
        }

        h1 {
            font-size: clamp(2.5rem, 4vw, 3.5rem);
            font-weight: 700;
            margin-bottom: 1.5rem;
        }

        h2 {
            font-size: clamp(1.8rem, 3vw, 2.5rem);
            font-weight: 700;
            margin-bottom: 2rem;
            border-bottom: 2px solid var(--primary-accent);
            padding-bottom: 0.5rem;
            display: inline-block;
        }

        p, li, td, th {
            font-size: clamp(1rem, 1.2vw, 1.3rem);
            line-height: 1.6;
        }

        ul, ol {
            margin-left: 2rem;
            margin-bottom: 1rem;
        }

        li {
            margin-bottom: 0.8rem;
        }

        strong {
            font-weight: 600;
            color: var(--primary-accent);
        }

        /* Tables */
        .table-wrapper {
            width: 100%;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            overflow: hidden;
            background: var(--white);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid var(--border-color);
            padding: 1rem;
            text-align: left;
            vertical-align: top;
        }

        th {
            background-color: #F0F4F8;
            font-weight: 600;
            color: var(--primary-accent);
        }

        /* Slide specific layouts */
        .slide-center {
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .slide-content {
            flex: 1;
            width: 100%;
            display: flex;
            flex-direction: column;
        }

        /* Footer & Slide Number */
        .footer {
            position: absolute;
            bottom: 1.5rem;
            left: 2rem;
            font-size: 0.85rem;
            color: var(--footer-text);
        }

        .slide-num {
            position: absolute;
            bottom: 1.5rem;
            right: 2rem;
            font-size: 1rem;
            font-weight: 600;
            color: var(--primary-accent);
        }

        /* Navigation */
        .nav-controls {
            position: fixed;
            bottom: 1.5rem;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 1.5rem;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.9);
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border: 1px solid var(--border-color);
        }

        .nav-btn {
            background: var(--primary-accent);
            color: var(--white);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: opacity 0.2s;
        }

        .nav-btn:hover {
            opacity: 0.8;
        }

        .nav-btn:disabled {
            background: #CCC;
            cursor: not-allowed;
        }

        .slide-counter {
            font-weight: 600;
            font-size: 1rem;
            min-width: 60px;
            text-align: center;
        }

        /* Architecture Diagram */
        .arch-diagram {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 2rem 0;
            width: 100%;
        }

        .arch-node {
            border: 2px solid var(--primary-accent);
            padding: 1rem;
            background: var(--white);
            border-radius: 4px;
            text-align: center;
            font-weight: 600;
            font-size: 0.9rem;
            min-width: 140px;
            box-shadow: 2px 2px 0 var(--primary-accent);
        }

        .arch-arrow {
            font-size: 1.5rem;
            color: var(--primary-accent);
            font-weight: bold;
        }

        /* Results Split */
        .split-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            height: 100%;
        }

        .placeholder-box {
            border: 2px dashed var(--border-color);
            background: #F0F0EE;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 4px;
            padding: 2rem;
            text-align: center;
        }

        /* Literature Review Scroll */
        .scroll-container {
            flex: 1;
            overflow-y: auto;
            border: 1px solid var(--border-color);
            margin-top: 1rem;
        }

        .lit-table td {
            font-size: clamp(0.55rem, 0.9vw, 0.8rem);
            line-height: 1.4;
        }

        /* Gantt chart colors */
        .gantt-fill {
            background-color: var(--primary-accent);
            color: white;
            text-align: center;
        }

        @media print {
            .nav-controls { display: none; }
            .presentation-container { overflow: visible; height: auto; }
            .slide { page-break-after: always; height: 100vh; }
        }
    </style>
</head>
<body>

    <div class="nav-controls">
        <button class="nav-btn" id="prevBtn" onclick="prevSlide()">Prev</button>
        <div class="slide-counter" id="counter">1 / 13</div>
        <button class="nav-btn" id="nextBtn" onclick="nextSlide()">Next</button>
    </div>

    <div class="presentation-container" id="container">

        <!-- SLIDE 1: Title Slide -->
        <section class="slide slide-center">
            <div style="margin-bottom: 2rem;">
                <h3 style="margin-bottom: 0.5rem; font-weight: 500;">CEK Kottarakkara</h3>
                <p style="font-weight: 400; color: #555;">Course: Mini Project (CSD 334)</p>
            </div>
            <h1>SimplyAI — A Disability-Aware, Privacy-First, Local AI Chat Editor</h1>
            <p style="font-weight: 600; margin-bottom: 2rem;">Group No: 3</p>

            <div class="table-wrapper" style="max-width: 600px; margin: 0 auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Roll No</th>
                            <th>Register No</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Abishek S</td><td>4</td><td>CEK23CS005</td></tr>
                        <tr><td>Alfred Jaison</td><td>9</td><td>CEK23CS011</td></tr>
                        <tr><td>Karthik B</td><td>36</td><td>CEK23CS042</td></tr>
                        <tr><td>Ashish S</td><td>18</td><td>CEK23CS020</td></tr>
                    </tbody>
                </table>
            </div>

            <p style="margin-top: 2rem;"><strong>Project Guide:</strong> Neethu Thomas, Asst. Prof.</p>

            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">1 / 13</div>
        </section>

        <!-- SLIDE 2: Table of Contents -->
        <section class="slide">
            <h2>Table of Contents</h2>
            <div class="slide-content">
                <ol style="column-count: 2; column-gap: 4rem; margin-top: 1rem;">
                    <li>Introduction</li>
                    <li>Problem Statement</li>
                    <li>Literature Review</li>
                    <li>Objectives</li>
                    <li>System Architecture</li>
                    <li>Accessibility Features</li>
                    <li>Implementation Details</li>
                    <li>Work Plan & Task Allocation</li>
                    <li>Results</li>
                    <li>Conclusion & Future Work</li>
                    <li>References</li>
                </ol>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">2 / 13</div>
        </section>

        <!-- SLIDE 3: Introduction -->
        <section class="slide">
            <h2>Introduction</h2>
            <div class="slide-content">
                <ul>
                    <li>Accessible digital writing tools are essential for inclusive education and modern employment.</li>
                    <li>Standard text interfaces present significant reading barriers for users with dyslexia and cognitive differences.</li>
                    <li>Artificial intelligence can dynamically adapt text readability and interface structure to suit individual cognitive needs.</li>
                    <li>A vital shift toward <strong>"Accessibility-First"</strong> engineering — prioritizing inclusive design at the core, not as an afterthought.</li>
                </ul>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">3 / 13</div>
        </section>

        <!-- SLIDE 4: Problem Statement -->
        <section class="slide">
            <h2>Problem Statement</h2>
            <div class="slide-content">
                <ul>
                    <li><strong>Cloud Dependence:</strong> Current assistive writing technologies rely on external cloud processing, introducing latency and risk.</li>
                    <li><strong>Privacy Concerns:</strong> Processing sensitive user text on external servers creates significant security vulnerabilities.</li>
                    <li><strong>Limited Accessibility Support:</strong> Standard editors treat accessibility as superficial overlays rather than native integration.</li>
                    <li><strong>The Gap:</strong> A critical need exists for an offline, privacy-secure editor with real-time AI adaptations for neurodivergent users.</li>
                </ul>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">4 / 13</div>
        </section>

        <!-- SLIDE 5: Literature Review -->
        <section class="slide">
            <h2>Literature Review</h2>
            <div class="scroll-container">
                <table class="lit-table">
                    <thead>
                        <tr>
                            <th style="width: 18%">Title & Year</th>
                            <th style="width: 25%">Methodology / Technique</th>
                            <th style="width: 25%">Inference / Key Findings</th>
                            <th style="width: 32%">Limitations / Research Gap</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Bork et al. (2025) — Inclusive model-driven engineering</td>
                            <td>Model-driven engineering with accessibility embedded during design</td>
                            <td>Integrating accessibility early improves long-term usability</td>
                            <td>Largely conceptual; no AI-based real-time text editing system</td>
                        </tr>
                        <tr>
                            <td>Sharma et al. (2024) — Privacy risks in cloud-based assistive AI</td>
                            <td>Security and privacy analysis of cloud-based assistive AI</td>
                            <td>Highlights privacy risks when sensitive text is processed externally</td>
                            <td>Does not propose a local or offline AI alternative</td>
                        </tr>
                        <tr>
                            <td>Koushik et al. (2024) — Assistive writing for neurodivergent users</td>
                            <td>Review and evaluation of assistive writing tools</td>
                            <td>Assistive writing tools improve confidence for neurodivergent users</td>
                            <td>Systems are static; lack adaptive or real-time AI support</td>
                        </tr>
                        <tr>
                            <td>Ferres et al. (2023) — WCAG-compliant adaptive interfaces</td>
                            <td>Design and evaluation of WCAG-compliant adaptive UIs</td>
                            <td>High-contrast designs improve usability for low-vision users</td>
                            <td>Does not integrate AI-based content transformation</td>
                        </tr>
                        <tr>
                            <td>Chen et al. (2023) — Cognitive load-aware UI design</td>
                            <td>Cognitive load analysis applied to UI design</td>
                            <td>Reducing visual clutter lowers cognitive load</td>
                            <td>Does not focus on AI-assisted text editing</td>
                        </tr>
                        <tr>
                            <td>Alonzo et al. (2023) — Accessibility-aware text editing interfaces</td>
                            <td>HCI study of accessibility-aware text editors</td>
                            <td>Accessibility-focused designs improve task completion</td>
                            <td>Semantic text simplification using AI is not addressed</td>
                        </tr>
                        <tr>
                            <td>Vacher et al. (2023) — AI-based real-time text transformation</td>
                            <td>AI pipeline for real-time text transformation</td>
                            <td>Improved readability for dyslexic users via real-time adaptation</td>
                            <td>Relies on cloud-based processing; no privacy-first local execution</td>
                        </tr>
                        <tr>
                            <td>Saggion et al. (2022) — Automatic text simplification survey</td>
                            <td>Survey of rule-based and neural text simplification</td>
                            <td>Neural approaches reduce lexical and syntactic complexity</td>
                            <td>Real-time editor integration not extensively discussed</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">5 / 13</div>
        </section>

        <!-- SLIDE 6: Objectives -->
        <section class="slide">
            <h2>Objectives</h2>
            <div class="slide-content">
                <ol>
                    <li><strong>Develop</strong> a desktop-based, offline AI chat editor tailored for users with dyslexia and cognitive differences.</li>
                    <li><strong>Implement</strong> a privacy-first architecture where sensitive text data never leaves the user's device.</li>
                    <li><strong>Deploy</strong> localized T5-based AI inference for real-time text simplification without external cloud APIs.</li>
                    <li><strong>Integrate</strong> specialized accessibility modes — Dyslexia, ADHD Focus, and Autism/Literal Clarity.</li>
                    <li><strong>Provide</strong> quantitative readability metrics (word count, sentence length, Flesch Reading Ease) before and after simplification.</li>
                </ol>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">6 / 13</div>
        </section>

        <!-- SLIDE 7: System Architecture -->
        <section class="slide">
            <h2>System Architecture</h2>
            <div class="slide-content">
                <p style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; color: #666; margin-bottom: 0.5rem;">Part A — Flow Diagram</p>
                <div class="arch-diagram">
                    <div class="arch-node">User Input<br><span style="font-size: 0.75rem; font-weight: 400;">Electron UI / CLI</span></div>
                    <div class="arch-arrow">→</div>
                    <div class="arch-node">simplify_server.py<br><span style="font-size: 0.75rem; font-weight: 400;">JSON IPC Bridge</span></div>
                    <div class="arch-arrow">→</div>
                    <div class="arch-node">simplify.py<br><span style="font-size: 0.75rem; font-weight: 400;">T5 Inference + Dispatch</span></div>
                    <div class="arch-arrow">→</div>
                    <div class="arch-node">Mode Modules<br><span style="font-size: 0.75rem; font-weight: 400;">dyslexia / adhd / autism</span></div>
                    <div class="arch-arrow">→</div>
                    <div class="arch-node">utils.py<br><span style="font-size: 0.75rem; font-weight: 400;">Metrics</span></div>
                </div>

                <p style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; color: #666; margin-top: 1.5rem; margin-bottom: 0.5rem;">Part B — Technical Overview</p>
                <ul>
                    <li><strong>Desktop Shell:</strong> Packaged using Electron for native OS integration and Python subprocess spawning.</li>
                    <li><strong>Local AI Core:</strong> Fine-tuned T5-small model running CPU-only inference — no GPU required.</li>
                    <li><strong>IPC Bridge:</strong> Electron communicates with Python via stdin/stdout JSON (python-bridge.js → simplify_server.py).</li>
                    <li><strong>Mode Dispatch:</strong> Each accessibility mode handled by a dedicated post-processing module.</li>
                </ul>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">7 / 13</div>
        </section>

        <!-- SLIDE 8: Accessibility Features -->
        <section class="slide">
            <h2>Accessibility Features</h2>
            <div class="slide-content">
                <ul>
                    <li><strong>Dyslexia Mode:</strong> Neural T5 simplification + rule-based compound sentence splitting, one sentence per line, dyslexia typography, text-to-speech via Web Speech API.</li>
                    <li><strong>ADHD Focus Mode:</strong> [i/N] progress markers, bullet layout, bold first content word; cognitive navigator with Prev/Next sentence navigation.</li>
                    <li><strong>Autism / Literal Clarity Mode:</strong> Regex-based replacement of 20 common English idioms with literal meanings (e.g., "piece of cake" → "easy").</li>
                    <li><strong>Visual Accessibility:</strong> Three themes — Light, Dark, WCAG AAA High-Contrast; font options include Lexend and OpenDyslexic.</li>
                </ul>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">8 / 13</div>
        </section>

        <!-- SLIDE 9: Implementation Details -->
        <section class="slide">
            <h2>Implementation Details</h2>
            <div class="slide-content">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                    <div>
                        <p style="font-weight: 600; margin-bottom: 0.5rem;">Section A — Technology Stack</p>
                        <ul style="font-size: 0.95rem;">
                            <li>Python 3.x, HuggingFace Transformers, textstat, psutil</li>
                            <li>Electron + React + Vite + Tailwind CSS</li>
                            <li>No external APIs — fully local execution</li>
                        </ul>

                        <p style="font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem;">Section C — Fine-tuning note</p>
                        <p style="font-size: 0.95rem;">T5-small fine-tuned on GEM/wiki_auto_asset_turk, filtered for &lt;80% word overlap to enforce meaningful simplification.</p>
                    </div>
                    <div>
                        <p style="font-weight: 600; margin-bottom: 0.5rem;">Section B — Model Selection</p>
                        <div class="table-wrapper">
                            <table style="font-size: 0.85rem;">
                                <thead>
                                    <tr>
                                        <th>Option</th>
                                        <th>Model</th>
                                        <th>Use Case</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr><td>small (def.)</td><td>./t5-simplifier</td><td>Fast, any hardware</td></tr>
                                    <tr><td>medium</td><td>t5-medium</td><td>Better quality</td></tr>
                                    <tr><td>auto-task</td><td>Logic based</td><td>By complexity</td></tr>
                                    <tr><td>auto-device</td><td>Logic based</td><td>By available RAM</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">9 / 13</div>
        </section>

        <!-- SLIDE 10: Work Plan & Task Allocation -->
        <section class="slide">
            <h2>Work Plan & Task Allocation</h2>
            <div class="slide-content">
                <div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 2rem;">
                    <div>
                        <p style="font-weight: 600; margin-bottom: 0.5rem;">Task Distribution</p>
                        <div class="table-wrapper">
                            <table style="font-size: 0.85rem;">
                                <thead>
                                    <tr><th>Task</th><th>Member</th></tr>
                                </thead>
                                <tbody>
                                    <tr><td>Python Backend</td><td>Abishek S</td></tr>
                                    <tr><td>Electron Frontend</td><td>Alfred Jaison</td></tr>
                                    <tr><td>Model Fine-tuning</td><td>Karthik B</td></tr>
                                    <tr><td>Testing & Docs</td><td>Ashish S</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div>
                        <p style="font-weight: 600; margin-bottom: 0.5rem;">Gantt-Style Timeline</p>
                        <div class="table-wrapper">
                            <table style="font-size: 0.8rem; text-align: center;">
                                <thead>
                                    <tr><th>Phase</th><th>W1</th><th>W2</th><th>W3</th><th>W4</th><th>W5</th><th>W6</th></tr>
                                </thead>
                                <tbody>
                                    <tr><td style="text-align: left">Requirements</td><td class="gantt-fill">■</td><td class="gantt-fill">■</td><td></td><td></td><td></td><td></td></tr>
                                    <tr><td style="text-align: left">Backend</td><td></td><td class="gantt-fill">■</td><td class="gantt-fill">■</td><td></td><td></td><td></td></tr>
                                    <tr><td style="text-align: left">Frontend</td><td></td><td></td><td class="gantt-fill">■</td><td class="gantt-fill">■</td><td></td><td></td></tr>
                                    <tr><td style="text-align: left">Integration</td><td></td><td></td><td></td><td></td><td class="gantt-fill">■</td><td></td></tr>
                                    <tr><td style="text-align: left">Docs & Slides</td><td></td><td></td><td></td><td></td><td class="gantt-fill">■</td><td class="gantt-fill">■</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">10 / 13</div>
        </section>

        <!-- SLIDE 11: Results -->
        <section class="slide">
            <h2>Results</h2>
            <div class="slide-content">
                <div class="split-layout">
                    <div>
                        <ul>
                            <li>Noticeable reductions in textual complexity achieved across all three accessibility modes.</li>
                            <li>Complete data sovereignty: zero external server dependency.</li>
                            <li>Distraction-free unified environment lowering cognitive load for neurodivergent readers.</li>
                            <li>Zero-cost operation: no commercial cloud API reliance.</li>
                            <li>Readability metrics show improvement in Flesch Reading Ease after simplification.</li>
                        </ul>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        <div class="placeholder-box" style="height: 45%;">
                            <p style="font-weight: 600; color: var(--primary-accent);">ADHD Focus Mode</p>
                            <p style="font-size: 0.8rem; color: #777; margin-top: 0.5rem;">[Screenshot]</p>
                        </div>
                        <div class="placeholder-box" style="height: 45%;">
                            <p style="font-weight: 600; color: var(--primary-accent);">Dyslexia Friendly Mode</p>
                            <p style="font-size: 0.8rem; color: #777; margin-top: 0.5rem;">[Screenshot]</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">11 / 13</div>
        </section>

        <!-- SLIDE 12: Conclusion & Future Work -->
        <section class="slide">
            <h2>Conclusion & Future Work</h2>
            <div class="slide-content">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4rem;">
                    <div>
                        <p style="font-weight: 700; color: var(--primary-accent); margin-bottom: 1rem; text-transform: uppercase; font-size: 0.9rem;">Conclusion</p>
                        <ul>
                            <li>Addressed the critical conflict between advanced AI accessibility tools and protecting sensitive user data privacy.</li>
                            <li>Transformed a privacy-by-design concept into a functional engineering prototype with three distinct accessibility modes.</li>
                            <li>Demonstrated that commercial-grade accessibility tools can run entirely offline on standard consumer hardware.</li>
                        </ul>
                    </div>
                    <div>
                        <p style="font-weight: 700; color: var(--primary-accent); margin-bottom: 1rem; text-transform: uppercase; font-size: 0.9rem;">Future Work</p>
                        <ul>
                            <li>Formal user studies with neurodivergent participants.</li>
                            <li>Multilingual simplification support.</li>
                            <li>Model quantization via ONNX export for improved inference speed.</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">12 / 13</div>
        </section>

        <!-- SLIDE 13: References -->
        <section class="slide">
            <h2>References</h2>
            <div class="slide-content">
                <ol style="font-size: 0.9rem; line-height: 1.4;">
                    <li>[1] L. Bork et al., "Inclusive model-driven engineering for accessible software," Springer, 2025.</li>
                    <li>[2] R. Sharma et al., "Privacy risks in cloud-based assistive AI systems," IEEE Access, 2024.</li>
                    <li>[3] S. Koushik et al., "Assistive writing technologies for neurodivergent users," Springer, 2024.</li>
                    <li>[4] L. Ferres et al., "WCAG-compliant adaptive interfaces for low-vision users," Springer, 2023.</li>
                    <li>[5] J. Chen et al., "Cognitive load-aware user interface design," IEEE Transactions on Human-Machine Systems, 2023.</li>
                    <li>[6] M. Alonzo et al., "Designing accessibility-aware text editing interfaces," ACM TOCHI, 2023.</li>
                    <li>[7] M. Vacher et al., "AI-based real-time text transformation to support people with dyslexia," ACM ASSETS, 2023.</li>
                    <li>[8] H. Saggion et al., "Automatic text simplification: A survey of methods, resources, and applications," ACM Computing Surveys, 2022.</li>
                </ol>
            </div>
            <div class="footer">CEK Kottarakkara | Mini Project (CSD 334)</div>
            <div class="slide-num">13 / 13</div>
        </section>

    </div>

    <script>
        const container = document.getElementById('container');
        const slides = document.querySelectorAll('.slide');
        const counter = document.getElementById('counter');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        let currentIdx = 0;

        function updateUI() {
            counter.innerText = `${currentIdx + 1} / ${slides.length}`;
            prevBtn.disabled = currentIdx === 0;
            nextBtn.disabled = currentIdx === slides.length - 1;
        }

        function scrollToSlide(index) {
            if (index < 0 || index >= slides.length) return;
            currentIdx = index;
            slides[currentIdx].scrollIntoView({ behavior: 'smooth' });
            updateUI();
        }

        function nextSlide() { scrollToSlide(currentIdx + 1); }
        function prevSlide() { scrollToSlide(currentIdx - 1); }

        window.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown') nextSlide();
            if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') prevSlide();
        });

        // Intersection Observer to update state on scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    currentIdx = Array.from(slides).indexOf(entry.target);
                    updateUI();
                }
            });
        }, { threshold: 0.5 });

        slides.forEach(slide => observer.observe(slide));

        updateUI();
    </script>
</body>
</html>
```

---

### File: project_design.md

#### Extracted Content (markup)

```md
# Project Design Context

This project is an offline, privacy-preserving AI text simplification tool with a
full-stack architecture: a Python backend and an Electron/React desktop frontend.

## Scope and Mode Support

The system supports three accessibility-oriented modes through a unified architecture.
All three modes are fully implemented in both the Python backend and the React frontend.

Implemented modes:
- Dyslexia (sentence simplification, hyphenation, one-sentence-per-line, dyslexia typography)
- ADHD (progress markers, bullet formatting, key term bolding, cognitive focus navigator)
- Autism (idiom replacement with literal meanings, clean paragraph output)

## ADHD Mode

ADHD mode formats simplified text to reduce cognitive load and help users maintain
attention. Python backend features (`adhd_mode.py`):

- Progress markers: Each sentence is prefixed with `[i/N]` where N is the total
  sentence count. This gives users a concrete sense of how far through the text they are.
- Bullet-style layout: One sentence per line, visually chunked.
- Key term bolding: The first significant content word in each sentence is wrapped in
  `**bold**` markers to anchor the reader's attention.

Frontend (`ADHDFocusMode.jsx`): A cognitive focus reading navigator where a sidebar
shows the dimmed source document and the main panel shows the active sentence enlarged,
with Previous/Next navigation buttons and a "Sentence N of Total" badge.

## Autism Mode

Autism mode targets literal interpretation by replacing figurative and idiomatic
language with explicit, unambiguous alternatives. Python backend features (`autism_mode.py`):

- Idiom replacement: A curated dictionary of 20 common English idioms is applied
  via regex, replacing each with its literal meaning.
  Example: "piece of cake" → "easy", "under the weather" → "feeling sick"
- Case-insensitive matching with word-boundary constraints to avoid false positives.

Frontend (`AutismOutput.jsx`): Clean paragraph rendering of the literal output.

## Model Selection

The CLI supports four model selection strategies via `--model`:

- `small` (default): Uses the fine-tuned `./t5-simplifier` local model. Fast, CPU-friendly.
- `medium`: Uses `t5-medium` from HuggingFace Hub. Better quality, slower.
- `auto-task`: Selects model based on text complexity (avg word length, token count).
- `auto-device`: Selects model based on available system RAM via `psutil`.

## Core Constraints

- Must run fully offline
- CPU-only inference
- T5-based text simplification
- CLI tool + Electron desktop app (both implemented)
- Sentence-by-sentence output in Dyslexia mode

## Architecture

```
User Input (Electron UI or CLI)
        │
        ▼
simplify_server.py (JSON stdin/stdout bridge)
        │
        ▼
simplify.py (model loading, T5 inference, mode dispatch)
        │
        ├── dyslexia_mode.py
        ├── adhd_mode.py
        └── autism_mode.py
                │
                ▼
        utils.py (split_sentences, compute_metrics, print_metrics)
```

- Shared AI simplification core (`simplify_with_t5`)
- Mode-specific post-processing (separate files per mode)
- No cloud calls
- Electron frontend communicates with Python via IPC → `python-bridge.js` → spawns `simplify_server.py`

## T5 Task Conditioning Strategy

Text simplification uses a fine-tuned T5-small model (`./t5-simplifier/`).
The model was fine-tuned on a filtered subset of GEM/wiki_auto_asset_turk with the
`simplify:` task prefix. Data curation was critical: raw WikiLarge contains many
near-identical pairs (source ≈ target), so we filtered for pairs with <80% word
overlap, enforcing that the target is shorter and meaningfully different. This teaches
the model actual simplification patterns rather than copying.

## Dyslexia-Oriented Linguistic Heuristics

Following neural simplification, rule-based post-processing is applied to optimize
readability for dyslexic users (`dyslexia_mode.py`). These heuristics include:

- Splitting compound sentences into single-idea statements
- One sentence per line with additional spacing
- Conservative punctuation and capitalization

These heuristics are intentionally simple and transparent, aligning with accessibility
writing guidelines and avoiding opaque transformations.

## Electron Frontend

A full desktop application built with Electron + React + Vite + Tailwind CSS.

Key UI features:
- Split-pane editor: input (left) / output (right)
- Three theme modes: Light, Dark, High-Contrast (WCAG AAA)
- Mode-specific output renderers per accessibility mode
- Settings panel: font family (Lexend, OpenDyslexic, Merriweather, Mono), font size,
  line spacing, cognitive focus toggle, reduce motion
- Metrics bar: word count, sentence count, readability grade before/after
- Privacy badge: "Processed Locally On Your Device"
- Text-to-speech via Web Speech API in DyslexiaOutput

IPC wiring: `preload.js` exposes `window.electronAPI.simplify(payload)` which routes
via `main.js` → `python-bridge.js` → `simplify_server.py` over stdin/stdout JSON.
```

---

### File: project_explanation.md

#### Extracted Content (markup)

```md
# Project Explanation: Offline Text Simplification Tool

## What We Built

A **privacy-first text simplification tool** that helps people with dyslexia, ADHD,
and autism read complex text more easily. The tool runs completely offline on your
laptop — no internet needed, no data sent anywhere.

It ships as both a **CLI tool** (`simplify.py`) and a **full Electron desktop app**
(`electron-app/`) with a React UI, theme switching, and accessibility-first design.

---

## The Problem We're Solving

People with reading difficulties struggle with:
- Long, complex sentences
- Dense paragraphs with multiple ideas
- Technical vocabulary
- Figurative/idiomatic language (autism)
- Distraction and loss of focus mid-reading (ADHD)

Existing solutions (like online AI tools) require sending your documents to the cloud.
This is a privacy problem — you might be simplifying personal emails, medical
documents, homework, or work files.

**Our solution:** Everything stays on your computer.

---

## How It Works

```
Input Text → T5 Neural Simplification → Mode Post-Processing → Output
```

1. **You provide text** (file via CLI, or paste into the Electron app)
2. **T5 model simplifies the language** — shorter words, simpler phrasing
3. **Mode-specific post-processing formats the output** for the user's accessibility need
4. **You see readable output** with metrics showing the improvement

---

## Technical Architecture

```
User Input (Electron UI or CLI)
        │
        ▼
simplify_server.py   ← JSON stdin/stdout bridge for Electron IPC
        │
        ▼
simplify.py          ← model loading, T5 inference, mode dispatch
        │
        ├── dyslexia_mode.py
        ├── adhd_mode.py
        └── autism_mode.py
                │
                ▼
        utils.py     ← split_sentences, compute_metrics, print_metrics
```

### Step 1: Neural Simplification
- Uses **T5-small fine-tuned** on GEM/wiki_auto_asset_turk (`./t5-simplifier/`)
- Runs on CPU only — no GPU required
- `"simplify:"` prefix for task conditioning
- Each sentence is processed individually for better results

### Step 2: Mode-Specific Post-Processing

| Mode | Post-Processing |
|------|----------------|
| `dyslexia` | Split compound sentences, one sentence per line, extra spacing |
| `adhd` | `[i/N]` progress markers, bullet layout, bold first content word |
| `autism` | Replace 20 idioms with literal meanings via regex |

### Step 3: Metrics
Before/after comparison:
- Word count
- Average sentence length
- Flesch Reading Ease score

---

## Model Selection

The `--model` flag (CLI) or `model` payload field (server) controls which model runs:

| Option | Model | When to use |
|--------|-------|-------------|
| `small` (default) | `./t5-simplifier` (fine-tuned local) | Fast, any hardware |
| `medium` | `t5-medium` (HuggingFace Hub) | Better quality, more RAM |
| `auto-task` | Picks based on text complexity | Automatic |
| `auto-device` | Picks based on available RAM | Automatic |

---

## Project Structure

```
chat editor ( mini project )/
├── simplify.py            # CLI tool
├── simplify_server.py     # JSON stdin/stdout server for Electron IPC
├── dyslexia_mode.py       # Dyslexia post-processing
├── adhd_mode.py           # ADHD post-processing
├── autism_mode.py         # Autism idiom replacement
├── utils.py               # Shared utilities (split_sentences, metrics)
├── t5-simplifier/         # Fine-tuned T5-small model weights
├── electron-app/          # Electron + React + Vite desktop app
│   ├── main.js            # Electron main process
│   ├── preload.js         # contextBridge (electronAPI)
│   ├── python-bridge.js   # Spawns simplify_server.py
│   └── src/
│       ├── App.jsx
│       ├── context/
│       │   ├── AppContext.jsx   # Global state
│       │   └── ThemeContext.jsx # Light/dark/high-contrast
│       └── components/
│           ├── layout/
│           │   ├── Header.jsx
│           │   ├── MetricsBar.jsx
│           │   └── SettingsPanel.jsx
│           ├── editor/
│           │   ├── InputPanel.jsx
│           │   └── OutputPanel.jsx
│           └── modes/
│               ├── DyslexiaOutput.jsx
│               ├── ADHDFocusMode.jsx
│               └── AutismOutput.jsx
├── stitch/                # UI design screens (5 reference designs)
└── docs/
    ├── design.md          # Design constraints and decisions
    ├── paper.tex          # Research paper (LaTeX)
    ├── paper.txt          # Research paper (plain text)
    ├── references.bib     # Bibliography
    ├── ui-plan.md         # Electron UI implementation plan
    ├── testing-instructions.md
    └── finetune_colab.ipynb  # Colab notebook for fine-tuning T5
```

---

## How to Use

### CLI

```bash
# Dyslexia mode
python simplify.py --input sample.txt --mode dyslexia

# ADHD mode with metrics
python simplify.py --input sample.txt --mode adhd --metrics

# Autism mode with medium model
python simplify.py --input sample.txt --mode autism --model medium

# Auto model selection
python simplify.py --input sample.txt --mode dyslexia --model auto-device
```

### Electron Desktop App

```bash
cd electron-app
npm run start
```

Launches the Vite dev server and Electron window. The Python server starts automatically.

---

## What Each Mode Does

| Mode | Status | CLI | UI |
|------|--------|-----|----|
| `dyslexia` | Fully implemented | Short sentences, one per line | Dyslexia typography, TTS, active sentence highlight |
| `adhd` | Fully implemented | `[i/N]` markers, bullet list, bold key term | Cognitive focus navigator (prev/next, dimmed context) |
| `autism` | Fully implemented | Idiom → literal replacement | Clean paragraph output |

---

## Design Decisions

### Why T5-small?
- Small enough for CPU inference (~60M parameters)
- Fine-tunable on consumer hardware
- Publicly available, easy to deploy

### Why `"simplify:"` prefix instead of `"summarize:"`?
- Summarization removes information
- Simplification preserves content but makes it easier to read
- For accessibility, we can't lose content

### Why rule-based post-processing?
- Transparent and auditable
- Deterministic (same input = same output)
- Easy to modify without retraining

### Why offline/local?
- Privacy: documents never leave your device
- Works without internet
- No API costs

### Why Electron for the UI?
- Cross-platform desktop app with native OS integration
- Can spawn Python subprocess directly (no web server needed)
- Existing React/Tailwind ecosystem

---

## Limitations (Be Honest About These)

1. **No user studies** — Not tested with actual dyslexic/ADHD/autistic users
2. **English only** — Doesn't work for other languages
3. **T5 imperfections** — Sometimes loses information or makes grammar errors
4. **ADHD/Autism not formally evaluated** — Only Dyslexia mode has quantitative metrics
5. **Autism idiom coverage is limited** — 20 idioms; no coreference resolution

---

## Future Work

1. **User studies** with target participants
2. **Quantitative evaluation** for ADHD and Autism modes
3. **Pronoun/coreference resolution** in Autism mode
4. **Model optimization** — quantization, ONNX export for speed
5. **More languages**

---

## Tech Stack

- **Python 3.x**
- **HuggingFace Transformers** — T5 model
- **textstat** — readability metrics
- **Electron** — desktop app shell
- **React + Vite** — UI framework
- **Tailwind CSS** — styling
- **No external APIs** — everything local

---

## Installation

### Python backend
```bash
pip install transformers torch textstat psutil
```

### Electron app
```bash
cd electron-app
npm install
npm run start
```
```

---

## Part 2 - Text Sources (TXT)

### Source Files
- `first page details.txt`
- `litaerature_review_content.txt`
- `prompt.txt`
- `slide_design.txt`

---

### File: first page details.txt

#### Extracted Content (text)

```txt
Fill out this for the first slide:
College Name: CEK Kottarakkara
Group Number: 3
Member 1: Abishek S, Roll no: 4, Register no: CEK23CS005
Member 2: Alfred Jaison, Roll no: 9, Register no: CEK23CS011
Member 3: Karthik B, Roll no: 36, Register no: CEK23CS042
Member 4: Ashish S, Roll no: 18, Register no: CEK23CS020
Project Guide: Neethu Thomas, designation: Asst. Prof.
```

---

### File: litaerature_review_content.txt

#### Extracted Content (text)

```txt
Paper (Year) Methodology / Technique Inference / Key Findings Limitations / Research Gap Focus Area Technology Level
Bork et al. (2025)
Model-driven engineering approach with accessibility embedded during software design
The authors emphasize integrating accessibility early in the development lifecycle to improve long-term usability
The work is largely conceptual and does not present an AI-based real-time text editing system
Software Development Lifecycle Conceptual
Sharma et al. (2024) Security and privacy analysis of cloud-based assistive AI systems
The study highlights potential privacy risks when sensitive user text is processed on external servers
The paper does not propose a concrete local or offline AI alternative
Cloud Security & Privacy Analysis
Koushik et al. (2024) Review and evaluation of assistive writing tools for neurodivergent users
Assistive writing technologies can improve writing confidence and usability for users with cognitive differences
Most systems are static and lack adaptive or real-time AI support
Assistive Technology Review Evaluation
Ferres et al. (2023) Design and evaluation of WCAG-compliant adaptive user interfaces
High-contrast and scalable interface designs improve usability for low-vision users
The work does not integrate AI-based content transformation User Interface Design (WCAG) Design
Chen et al. (2023) Cognitive load analysis applied to user interface design
Reducing visual clutter and improving layout predictability can lower cognitive load
The study does not focus on AI-assisted text editing applications
Cognitive Science & HCI Analysis
Alonzo et al. (2023) Human-computer interaction study of accessibility-aware text editors
Accessibility-focused editor designs improve task completion and user experience
Semantic text simplification using AI is not addressed Human-Computer Interaction Empirical Study
Vacher et al. (2023) AI-based pipeline for real-time text transformation
The authors report improved readability for dyslexic users through real-time text adaptation
The system relies on cloud-based processing and does not consider privacy-first local execution
Real-time AI Text Adaptation System Prototype
Saggion et al. (2022) Survey of rule-based and neural text simplification techniques
Neural approaches are effective in reducing lexical and syntactic complexity
Real-time editor integration and user-controlled simplification are not extensively discussed
Text Simplification Techniques Survey
```

---

### File: prompt.txt

#### Extracted Content (text)

```txt
Act as a professional academic slide-generation assistant for a Computer Science B.Tech mini project. Your task is to generate a strictly formal, 12-slide presentation based on the exact constraints and structure below.

ABSOLUTE DESIGN & CONTENT CONSTRAINTS (YOU MUST FOLLOW THESE):
1. NO INLINE CITATIONS: Do not include any inline citations (e.g., [1], [Author, 2024], etc.) anywhere in the slide body text. The only place papers should be listed is the Literature Review table and the References slide.
2. CONSERVATIVE ACADEMIC TONE: Use abstract-level language only (e.g., "the authors propose...", "the study highlights..."). Do NOT mention experimental metrics, dataset sizes, or numerical performance improvements.
3. NO HALLUCINATIONS: Do not invent new papers, authors, venues, or features. Stick only to the provided structure.

LOCKED LITERATURE SET (Use only these 8 papers for Slide 5 and Slide 12):
1. Bork et al., “Inclusive model-driven engineering for accessible software,” Springer, 2025.
2. Sharma et al., “Privacy risks in cloud-based assistive AI systems,” IEEE Access, 2024.
3. Koushik et al., “Assistive writing technologies for neurodivergent users,” Springer, 2024.
4. Ferres et al., “WCAG-compliant adaptive interfaces for low-vision users,” Springer, 2023.
5. Chen et al., “Cognitive load-aware user interface design,” IEEE Transactions on Human-Machine Systems, 2023.
6. Alonzo et al., “Designing accessibility-aware text editing interfaces,” ACM TOCHI, 2023.
7. Vacher et al., “AI-based real-time text transformation to support people with dyslexia,” ACM ASSETS, 2023.
8. Saggion et al., “Automatic text simplification: A survey of methods, resources, and applications,” ACM Computing Surveys, 2022.

GENERATE THE PRESENTATION USING THE EXACT STRUCTURE BELOW:

---
SLIDE 1: Title Slide
Title: SimplyAI-A Disability-Aware, Privacy-First, Local AI Chat Editor
Subtitle: Mini Project (CSD 334)
Institution: 
Group Members: 
Project Guide: 

---
SLIDE 2: Introduction
- Importance: Accessible digital writing tools are essential for inclusive education and modern employment.
- Target Challenges: Standard text interfaces present significant reading barriers for users with dyslexia, low vision, and cognitive differences.
- Role of AI: Artificial intelligence can dynamically adapt text readability and interface structure to suit individual cognitive needs.
- Current Trend: A vital shift toward "Accessibility-First" engineering, prioritizing inclusive design at the core rather than as an afterthought.

---
SLIDE 3: Problem Statement
- Cloud Dependence: Current assistive writing technologies rely heavily on external cloud processing, which introduces latency.
- Privacy Concerns: Processing sensitive user text on external servers creates significant security and privacy vulnerabilities.
- Limited Accessibility Support: Standard editors treat accessibility features as superficial overlays rather than integrating them natively.
- The Gap: There is a critical need for an offline, privacy-secure text editor that provides real-time AI adaptations for neurodivergent users.

---
SLIDE 4: Objectives
- Develop a desktop-based, offline chat editor tailored for users with dyslexia and visual impairments.
- Implement a privacy-first architecture where sensitive text data never leaves the user's device.
- Deploy localized AI inference to execute real-time text simplification without relying on external cloud APIs.
- Integrate specialized accessibility reading modes, including dyslexia support and high-contrast visual aids.

---
SLIDE 5: Literature Review
(Render this strictly as a Markdown table in reverse chronological order: 2025 -> 2022. Use the 8 locked papers provided above. Columns must be: Title & Year | Methodology / Technique | Inference / Key Findings | Limitations / Research Gap). Keep descriptions brief and abstract-level.

---
SLIDE 6: Research Gap & Motivation
- Lack of Unified Tools: Absence of integrated, accessibility-first AI editors that treat inclusion as a core component.
- Dependence on Cloud Processing: Prior work and existing tools rely heavily on cloud servers, compromising real-time performance.
- Privacy Vulnerabilities: Limited focus on privacy-first, local execution for processing sensitive communication data.
- The Motivation: To bridge the gap between advanced neural simplification and absolute user data sovereignty.

---
SLIDE 7: System Architecture
- Desktop Shell: Packaged using Electron to support multithreaded performance and native OS integration.
- Editor Engine: Utilizes the Lexical framework to support complex, highly accessible document structures.
- Local AI Core: Driven by a localized neural inference engine (Transformers.js) for semantic simplification.
- Accessibility Modules: Integrated layers for dyslexia formatting, low-vision contrast, and cognitive load reduction.

---
SLIDE 8: Accessibility Features & Academic Justification
- Text Simplification: Neural reduction of lexical complexity to support reading comprehension for dyslexia.
- Dyslexia-Friendly Formatting: Rule-based heuristics for compound sentence splitting and specialized typography adjustments.
- Cognitive Focus Aids: Visual chunking and progress markers to reduce cognitive load and maintain focus.
- Visual Contrast: WCAG AAA compliant visual scaling and dynamic contrast themes for low-vision users.

---
SLIDE 9: Implementation Details
- Technology Stack: Built using a React frontend, Electron desktop shell, and Tailwind CSS.
- Local AI Rationale: CPU-only local inference ensures the system runs smoothly on standard consumer hardware without API costs.
- Privacy Architecture: The hybrid framework enforces strict offline execution, completely eliminating data transmission risks.

---
SLIDE 10: Results / Expected Outcomes
(FORMATTING INSTRUCTION: Layout this slide in a two-column format. The left column should contain the text below. The right column MUST be a large, blank visual placeholder box labeled "[INSERT SCREENSHOT OF PC WINDOW HERE]" so the user can drop an 16:9 image of the application interface into it.)
- Expected Improvements: Noticeable reductions in textual complexity and improved readability for target personas.
- Privacy Benefits: Complete data sovereignty achieved through zero external server dependency.
- User Experience: A unified, distraction-free environment that actively lowers the cognitive load for neurodivergent readers.
- Zero-Cost Operation: Sustainable, free usage enabled by removing reliance on commercial cloud APIs.

---
SLIDE 11: Conclusion & Future Work
- Problem Summary: Addressed the critical conflict between utilizing advanced AI accessibility tools and protecting sensitive user data privacy.
- Solution Contribution: Transformed a theoretical privacy-by-design concept into a functional engineering prototype.
- Key Learning: Demonstrated that commercial-grade accessibility tools can run entirely offline on standard hardware.
- Future Enhancements: Potential expansion to include formal user studies and optimization for multilingual simplification models.

---
SLIDE 12: References
(List ONLY the 8 locked papers provided at the top of this prompt. Format in strict standard IEEE style. Order them in reverse chronological order, 2025 to 2022.)
```

---

### File: slide_design.txt

#### Extracted Content (text)

```txt
Design a university mini-project presentation for an AI-based Disability-Aware Chat Editor developed for neurodivergent users.

The presentation must strictly follow an academic mini-project structure required for engineering faculty evaluation, but the visual identity should subtly reflect accessibility, cognitive clarity, and assistive AI principles.

The design must feel professional, structured, and technically mature — not like a startup pitch deck and not like an overly rigid black-and-white government report.

GENERAL DESIGN STYLE:

• Use a clean, minimal academic layout.
• Maintain strong visual hierarchy.
• Ensure readability when printed.
• Use generous white space for cognitive comfort.
• Avoid clutter and dense slides.

Color Scheme:
• Background: very light neutral tone (off-white or soft light grey).
• Primary accent color: muted deep blue or desaturated teal (used only for titles, section dividers, or subtle highlights).
• Body text: dark grey (not pure black).
• High contrast and accessible color usage.

Strictly Avoid:
• Gradients
• Heavy shadows
• Decorative illustrations
• Bright or saturated colors
• Startup pitch aesthetics
• Overly dramatic layouts
• Marketing-style visuals

TYPOGRAPHY:

• Use one professional sans-serif font consistently (Inter, Calibri, Arial, or Source Sans).
• Slide titles: bold, larger size, clear spacing.
• Body text: regular weight, readable size.
• Maintain consistent margins and alignment.
• Maximum 5–6 bullet points per slide.

SLIDE STRUCTURE (MANDATORY ORDER):

Title Slide

Table of Contents

Introduction

Problem Statement

Literature Review (Tabular Format)

Objectives

System Design

Work Plan & Task Allocation

Implementation

Results

Conclusion

References

TITLE SLIDE:

• Center aligned.
• Include only:

College Name

Course Name & Code: Mini Project (CSD 334)

Project Title (technical and specific)

Group Number

Group Members (Name, Roll No, Register No)

Project Guide Name & Designation
• No additional text.
• No decorative graphics.

TABLE OF CONTENTS:

• Numbered list of section titles only.
• No descriptions.

INTRODUCTION:

• Bullet points only.
• Cover domain overview, importance, motivation, and current challenges.
• One idea per bullet.

PROBLEM STATEMENT:

• Clearly define the specific problem.
• Identify affected users.
• Mention limitations of existing systems.
• Explain why improvement is required.
• Avoid vague language.

LITERATURE REVIEW:

• Must be in clean tabular format with visible grid lines.
• Columns:

Title, Author(s), Year

Methodology / Technique Used

Inference / Key Findings

Limitations / Research Gaps
• Reverse chronological order.
• No color coding.

OBJECTIVES:

• Numbered list.
• Each objective must begin with an action verb.
• Directly address the problem statement.

SYSTEM DESIGN:

• Include:

Process Flow (Input → Processing → Output)

System Architecture (Modules and Data Flow)

Database Design (if applicable)
• Use clean labeled diagrams.
• Use soft bordered boxes.
• Ensure left-to-right logical flow.
• Keep diagrams neat and readable.

WORK PLAN & TASK ALLOCATION:

• Use simple tables.
• Include task distribution per member.
• Include project timeline (Gantt chart style, minimal and clean).
• No decorative timeline elements.

IMPLEMENTATION:

• Subsections:

Technology Stack

Development Methodology

Key Modules

Core Algorithms / Logic
• Bullet points only.
• No code snippets.

RESULTS:

• Include labeled output screenshots.
• Show accessibility features clearly.
• Include performance metrics if applicable.
• Maintain alignment and spacing.
• No visual clutter.

CONCLUSION:

• Bullet points only.
• Summarize problem addressed, solution impact, achievements, learning outcomes, and future enhancements.
• Avoid repetition.

REFERENCES:

• IEEE format.
• Reverse chronological order.
• Include all literature review papers.
• No visible hyperlinks.

OVERALL FEELING:

The presentation should communicate:

“An academically strong engineering solution built with empathy, clarity, and structured intelligence.”

It must remain formal, but not lifeless.
It must reflect accessibility and cognitive comfort without losing academic credibility.
```

---

## Part 3 - Binary/Non-Text Sources

- `Presentation Template.pdf` (212.13 KB)

