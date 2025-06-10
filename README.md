# 🤖 Appointment Booking Multi-Agent System

This project demonstrates an **AI-powered multi-agent system** for booking, rescheduling, and canceling appointments in a human-like conversational interface. It uses `LangGraph`, `LangChain`, and `React-style agents`, backed by SQLite-based stateful memory for conversation tracking and tool usage.

---

## 📌 Table of Contents

* [Overview](#overview)
* [Architecture](#architecture)
* [Key Agents](#key-agents)
* [Tech Stack](#tech-stack)
* [Installation](#installation)
* [Usage](#usage)
* [API + Streamlit Guide](#api--streamlit-guide)
* [Conversation History](#conversation-history)
* [Folder Structure](#folder-structure)
* [Contact](#contact)

---

## 📖 Overview

This system supports:

* Intelligent **booking, rescheduling, and cancellation** of appointments
* Providing **doctor availability information** or handling **FAQ-style** queries
* **Memory-backed supervision and handoffs** between specialized agents
* Extensible via LangGraph with built-in SQLite checkpointing

---

## 🧠 Architecture

<p align="center">
  <img src="image.png" alt="Architecture Diagram" width="600"/>
</p>

* `User Message` ➝ `Supervisor Agent`
* `Supervisor` decides whether to route to:

  * `Booking Agent`: for booking, cancelling, rescheduling
  * `Information Agent`: for FAQs, doctor availability
* Each agent has tool access, and state is tracked using SQLite (`checkpoint.db`)

---

## 🧱 Key Agents

### 🗓️ Booking Agent

Handles:

* `set_appointment`
* `cancel_appointment`
* `reschedule_appointment`

### 📊 Information Agent

Handles:

* `check_availability`
* `check_availability_by_specialization`

### 🧑‍⚖️ Supervisor Agent

* Routes the query to the correct specialized agent
* Maintains history and handles handoffs
* Prompt provided via `prompt/system_prompt.py`

---

## 🛠️ Tech Stack

| Component      | Technology                           |
| -------------- | ------------------------------------ |
| Agents         | LangGraph + LangChain                |
| Language Model | OpenAI / LLM wrapper                 |
| State Saving   | SQLite (`checkpoint.db`)             |
| Tooling        | Custom Python tools                  |
| Prompting      | `ChatPromptTemplate`, `HumanMessage` |

---

## ⚙️ Installation

### Clone and Set Up

```bash
git clone https://github.com/rajkrishna92/Appointment-Booking-Multi-Agent.git
cd Appointment-Booking-Multi-Agent
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
````

### Environment Setup

Create a `.env` file and add your OpenAI key:

```
OPENAI_API_KEY=your_openai_key_here
```

---

## 🚀 Usage

Run the system:

```bash
python main.py
```

You’ll see a full conversation trace based on your initial message (e.g. `"what is my name?"`) and how agents respond using tools or handoffs.

---

## 🌐 API + Streamlit Guide

### Start FastAPI Server

```bash
uvicorn main:app --reload
```

Ensure `api.py` has the POST route `/execute` accepting JSON with `email` and `messages`.

### Start Streamlit Application

```bash
streamlit run stremlit.py
```

---

## 💬 Conversation History

```
You: Who is available for consultation today?

Assistant: I'm sorry, but Alice Johnson is fully booked for consultations on the date of 07-06-2025. Would you like to check availability for other days or for a different individual?

You: for AI ML related?

Assistant: I'm sorry, but there are no available slots today for consultations related to AI/ML. Can we check availability for another day?

You: for 9-6-2025

Assistant: On the 9th of June, 2025, George Kim is available for a consultation on AI/ML at 12:00 PM. Would you like me to book this appointment for you? If so, I'll need the name of the person for whom this appointment is being made.

You: book it for Rajkrishna

Assistant: The consultation with George Kim on June 9, 2025, at 12:00 PM has been successfully booked for Rajkrishna. Please let me know if you need assistance with anything else.

You: oh sorry I want to cancel it for now

Assistant: Alright, the appointment with George Kim on the 9th of June, 2025, for Rajkrishna has been canceled. If you wish to reschedule or need any other assistance, feel free to ask.

You: reschedule it

Assistant: Sure, I can assist you with that. Could you please provide the new date and time you would like to reschedule the appointment to?

You: after 7 day at the same time

Assistant: I have rescheduled your appointment with George Kim for AI/ML consultation on June 16, 2025, at 12:00 PM. If you have any other requests or need further information, feel free to ask.

You: Thanks

Assistant: You're welcome! If you have any other questions in the future, don't hesitate to ask. Have a great day!
```

---

## 📁 Folder Structure

```
Appointment-Booking-Multi-Agent/
├── agent.py
├── main.py                 # FastAPI interface
├── data
│   ├── availability.csv
│   └── checkpoint.db
├── prompt
│   ├── __init__.py
│   └── prompt.py
├── README.md
├── requirements.txt
├── stremlit.py
├── setup.py
├── toolkit
│   ├── __init__.py
│   └── tools.py
└── utils
    ├── data_model.py
    ├── helper.py
    ├── __init__.py
    └── llm.py
```

* **main.py**: FastAPI endpoint for integration
* **data/**: Contains records and other relevant data files.
* **prompt/**: Holds prompt templates for agent interactions.
* **toolkit/**: Includes tools and utilities for scheduling logic.
* **utils/**: Helper functions used across the project.
* **agent.py**: Entry point of the agent application.
* **stremlit.py**: Sample Streamlit application

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**

2. **Create a new branch**:

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit your changes**:

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to the branch**:

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a pull request**

---

## 📬 Contact

**Dr. Rajkrishna Mondal**

Data Scientist | Ph.D. in Computational Mathematics

[GitHub](https://github.com/rajkrishna92) | [Blog](https://www.rajkrishna92.github.io)
