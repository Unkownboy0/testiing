# 24 — Technical Glossary & Conceptual Dictionary

> **Target Venue**: AURVEXX’2026 Hackathon  
> **Audience**: Non-technical judges, technical evaluators, and founder reference.  
> **Format**: Dual Explanation (Simple Technical English + Conversational Thanglish)

---

## 1. Core Platform Terminology

### 1. Control Plane (கண்ட்ரோல் பிளேன்)
* **Simple English**: The central management layer that monitors, coordinates, and enforces security rules across all autonomous agents without directly executing the raw work itself.
* **Thanglish**: *Ella agents-aiyum control panni, monitor panni, rules enforce panra central command center. Traffic police maathiri yaru eppo execute aaganum nu decide pannum.*

---

### 2. Virtual Company (விர்ச்சுவல் கம்பெனி)
* **Simple English**: A multi-agent organizational unit composed of specialized roles (Tech Lead, Coder, QA) with defined reporting lines, isolated data, and budget limits.
* **Thanglish**: *Oru digital engineering team. Namma company-la real employees irukura maathiri, inga Tech Lead, Developer, QA nu specialized AI agents team-ah work pannuvanga.*

---

### 3. Amber Gate (ஆம்பர் கேட் - Human-in-the-Loop Approval)
* **Simple English**: A safety mechanism that automatically pauses an agent's execution when it attempts a sensitive action (e.g. git commit, file delete, shell command) until a human operator clicks "Approve".
* **Thanglish**: *Traffic signal-la yellow light maathiri. Dangerous action ethavathu agent panna pona, system stop panni human permission keka pause aagirum. Namma approve pannatha proceed aagum.*

---

### 4. Heartbeat & Turn (ஹார்ட்பீட் & டர்ன்)
* **Simple English**: The recurring background timer loop that wakes up agents, inspects pending tasks, calls the AI model, and executes one discrete cycle of reasoning and tool calls (a "Turn").
* **Thanglish**: *Heart beat adikkira maathiri ovvoru second-um system check pannum. Pending task iruntha agent-ah eluppi oru round reasoning panni tool run panna vaikkum.*

---

### 5. Model Context Protocol (MCP)
* **Simple English**: An open standard protocol created by Anthropic that allows AI models to discover and interact with external tools and databases using standardized JSON schemas.
* **Thanglish**: *AI models external tools (file reader, terminal, database)-kooda connect aagi safe-ah communicate panna use aagura standard language.*

---

### 6. Execution Lease (எக்ஸிகியூஷன் லீஸ்)
* **Simple English**: A temporary, exclusive database lock acquired by an agent on a workspace to ensure no other agent can modify the same files simultaneously.
* **Thanglish**: *Oru task-ah oru agent eduthu vela seiyum pothu, vera agent vanthu interfere aagatha maathiri database-la podura temporary lock.*

---

### 7. Git Worktree (கிட் ஒர்க்ட்ரீ)
* **Simple English**: An isolated linked copy of a Git repository on disk that allows an agent to work on an independent branch without modifying the main working directory.
* **Thanglish**: *Main code folder-ah disturb pannama, oru branch-kku separate duplicate folder create panni anga agent safe-ah code edit panna use aagura Git feature.*

---

### 8. Token Gate (டோக்கன் கேட்)
* **Simple English**: An architectural test rule in Geetorus that fails the build if a developer hardcodes raw CSS hex codes or pixel numbers instead of using design tokens.
* **Thanglish**: *Frontend styling check panra gate. Raw colors direct-ah code-la pota reject pannirum, centralized design tokens mattum thaan use panna vidum.*

---

### 9. Task Watchdog (டாஸ்க் வாட்ச்டாக்)
* **Simple English**: A background supervisor process that monitors active turns. If an agent hangs or becomes unresponsive for more than 5 minutes, the watchdog cancels the turn and alerts the operator.
* **Thanglish**: *Kaval kaaran maathiri. Agent ethavathu infinite loop-la maatikittalo illa internet cut aagi hang aanalum, 5 minutes-la detect panni lease release pannirum.*

---

### 10. Drizzle ORM
* **Simple English**: A lightweight, high-performance TypeScript Object-Relational Mapper that translates TypeScript queries into raw SQL with zero runtime overhead.
* **Thanglish**: *TypeScript code-ah fast-ah SQL queries-ah maathi PostgreSQL database-kooda safe-ah communicate panna use panra database tool.*
