## 🧠 Priority Scoring & Volunteer Matching

### ⚡ Priority Scoring System
To identify the most urgent community needs, the system uses a simple yet effective scoring mechanism.

- Each task is assigned an **urgency value (1–10)**  
- A **priority score** is calculated using the formula: Score = Urgency × 1.5
 
- Based on the score, tasks are categorized into priority levels:

| Score Range | Priority | Description |
|------------|--------|-------------|
| ≥ 8        | 🔴 High   | Immediate attention required |
| 5 – 7      | 🟡 Medium | Moderate urgency |
| < 5        | 🟢 Low    | Can be addressed later |

- The dashboard visually represents these priorities using **color-coded rows**, enabling quick identification of critical needs.

---

### 🤝 Volunteer Matching System
To improve efficiency, the system suggests suitable volunteers for each task.

#### Matching Logic:
- Each volunteer has:
  - **Name**
  - **Skill**
  - **Location**

- Each task has:
  - **Category (Food, Medical, Education, etc.)**
  - **Location**

#### Matching Criteria:
- Volunteers are matched based on:
  - ✅ **Skill match** → Volunteer skill == Task category  
  - 📍 **Location similarity** (basic string match for prototype)

- The system returns:
  - 🎯 **Top 3 suitable volunteers** for each task  

#### Example:
- Task: *Medical help in T. Nagar*  
- Matching Volunteers:  
  → Alice (Medical)  
  → John (Medical)  
  → Priya (Medical)  

---

### 🚀 Outcome
- Ensures **high-priority tasks are handled first**  
- Reduces manual effort in assigning volunteers  
- Demonstrates a **data-driven approach to social impact**

---

### Preview
![Dashboard](Dashboard.PNG)


## 👥 Team

- **Angellina Joyce Paul**  
- **Aswini**  
- **Preethi**  
- **Aparajitha**  
