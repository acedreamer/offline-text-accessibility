# Structured Text Sources

## Source Files
- `first page details.txt`
- `litaerature_review_content.txt`
- `prompt.txt`
- `slide_design.txt`

---

## File: first page details.txt

### Extracted Content (text)

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

## File: litaerature_review_content.txt

### Extracted Content (text)

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

## File: prompt.txt

### Extracted Content (text)

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

## File: slide_design.txt

### Extracted Content (text)

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

