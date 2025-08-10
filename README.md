# 🛡 Guardrails Agent Project

This repository contains 3 separate exercises demonstrating how to implement **Guardrails** for AI Agents to control and validate inputs/outputs.

---

## 📌 Project Overview

### **Exercise 1 — Input Guardrail Tripwire**
**Objective:**  
Create an agent that uses an **input guardrail** to trigger a tripwire when a specific condition is detected.

**Prompt to test:**  
**Expected Behavior:**  
- When this input is detected, the `InputGuardrailTripwireTriggered` exception should be raised.
- Exception is caught and logged as a message.

---

### **Exercise 2 — Father Agent & Temperature Guardrail**
**Objective:**  
Create a "Father" agent that stops his child from working if the temperature is below 26°C.

**Expected Behavior:**  
- If the temperature is **below 26°C**, the guardrail triggers and stops the child.
- If the temperature is **26°C or above**, the child is allowed.

---

### **Exercise 3 — Gate Keeper Agent & School Guardrail**
**Objective:**  
Create a gate keeper agent that only allows students from `"Green Valley School"`.

**Expected Behavior:**  
- If the student's school is `"Green Valley School"`, they are allowed to enter.
- If they are from another school, the `InputGuardrailTripwireTriggered` exception is raised.

---

## 🛠 Installation Steps

### 1️⃣ Create Project & Virtual Environment
```bash
# Create project directory
mkdir guardrails_agent
cd guardrails_agent

# Initialize with uv
uv init

# Create virtual environment
uv venv

# Activate venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

2️⃣ Install Dependencies
bash
Copy
Edit
uv add pydantic rich
⚠ Note: You must have agents.py and connection.py which contain the Guardrail framework logic and configuration.

3️⃣ Project File Structure
bash
Copy
Edit
guardrails_agent/
│
├── exercise1.py          # Input Guardrail Tripwire
├── exercise2.py          # Father Agent & Temperature Guardrail
├── exercise3.py          # Gate Keeper Agent & School Guardrail
├── agents.py             # Agents framework
├── connection.py         # Config & API setup
├── README.md             # Documentation
└── .venv/                # Virtual environment
🚀 Run Instructions
Exercise 1
bash
Copy
Edit
uv run exercise1.py
Example Output (Trigger case):

pgsql
Copy
Edit
Guardrail Triggered: Class timing change request detected.
Exercise 2
bash
Copy
Edit
uv run exercise2.py
Example Output (Temperature < 26°C):

csharp
Copy
Edit
Child denied: Temperature is too low.
Example Output (Temperature >= 26°C):

pgsql
Copy
Edit
Child allowed to work.
Exercise 3
bash
Copy
Edit
uv run exercise3.py
Example Output (Wrong School):

sql
Copy
Edit
Student denied: Only Green Valley School students allowed.
Example Output (Correct School):

css
Copy
Edit
Student allowed to enter the school.
📜 How Each Exercise Works
Exercise 1 — Input Guardrail Tripwire
The main agent accepts user input.

An input guardrail function checks for specific keywords or phrases.

If the trigger condition is met, the InputGuardrailTripwireTriggered exception is raised and handled.

Exercise 2 — Father Agent
The "Father" agent evaluates the temperature input.

If the temperature is below 26°C, the guardrail is triggered.

The child agent’s action is stopped when the tripwire triggers.

Exercise 3 — Gate Keeper
The gate keeper agent checks the student's school name.

If it’s not "Green Valley School", the output sets isOtherSchool=True.

The input guardrail detects this flag and triggers the tripwire.

The student is denied entry unless from the correct school.

⚠ Important Notes
All exercises use Guardrail decorators: @input_guardrail and @output_guardrail.

Pydantic v2 model syntax is used (field: type).

Windows-specific asyncio fix is included for event loop issues.

connection.py should contain your API configuration.

🏁 Conclusion
This project demonstrates how AI Guardrails can be applied to enforce rules and control the flow of conversation or operations in agents — making them safer, more controlled, and reliable.
uv add pydantic rich
uv add pydantic rich
