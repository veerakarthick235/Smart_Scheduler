# 🧠 AI-Powered Smart Timetable Scheduler

## 📘 Introduction
The **Smart Timetable Scheduler** is a **full-stack AI web application** designed to automate and optimize class scheduling in higher education institutions.  
Manual scheduling often leads to **conflicts, inefficiencies, and underutilized resources**.  
This project uses a **Genetic Algorithm** to intelligently generate optimized timetables, ensuring **maximum resource utilization** and **minimal conflicts**.

With its **modern AI-themed interface**, the application provides an end-to-end solution — from **data entry** to **AI-powered scheduling, analytics, and export features** — empowering administrators to make informed decisions efficiently.

---

## ✨ Key Features

### 🤖 Intelligent Timetable Generation
- Core scheduling logic powered by a **Genetic Algorithm** to optimize for multiple constraints.  
- Generates **multiple timetable options** ranked by a **fitness score**, representing schedule quality.

### 💻 Dynamic Data Management (CRUD)
- Comprehensive **Manage Data** interface for adding, viewing, and deleting data such as:
  - Rooms & Classrooms  
  - Batches / Programs  
  - Subjects (including weekly hours)  
  - Faculty Members  
- Assign subjects dynamically to the faculty qualified to teach them.

### 🔐 Secure User Authentication
- Full **user registration and login** system.  
- Passwords secured using **Werkzeug hashing** for industry-standard security.

### 📊 Analytics Dashboard
- Interactive **Chart.js** dashboard for workload and utilization analytics.  
- Visual insights into faculty workloads, subject distribution, and schedule density.

### 📄 PDF & Excel Export
- Export any generated timetable to:
  - **PDF** via WeasyPrint  
  - **Excel** via openpyxl  
- Facilitates easy sharing and printing.

### 💡 Live AI Conflict Suggestions
- Real-time **AI-powered conflict detection**:
  - Detects faculty overload  
  - Warns about unassigned or conflicting subjects  
- Prevents generation errors before they occur.

### 🎨 Modern AI-Themed UI
- Dark-mode interface with glowing AI-style components.  
- Built with **Bootstrap 5**, fully **responsive**, and **mobile-friendly**.

---

## 🛠️ Tech Stack

### 🧩 Backend
- **Python 3**
- **Flask** – Backend framework & REST API  
- **Flask-SQLAlchemy** – ORM for database handling  
- **Werkzeug** – Secure password hashing  
- **Pandas** & **openpyxl** – Data analysis & Excel export  
- **WeasyPrint** – HTML to PDF conversion  

### 🎨 Frontend
- **HTML5**, **CSS3 (Bootstrap 5)**  
- **JavaScript (ES6+)** – Frontend logic and dynamic rendering  
- **Chart.js** – Interactive data visualization  

### 🗄️ Database
- **SQLite** – Lightweight, file-based database system.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure the following are installed:
- Python 3.x  
- pip (Python package installer)

### 2. Installation
Clone this repository and install dependencies:
```bash
git clone https://github.com/your-username/smart-scheduler.git
cd smart-scheduler
pip install -r requirements.txt
```

### 3. Database Initialization
Before the first run, initialize the database:
```bash
python database_setup.py
```

> **Default Admin Credentials**  
> Username: `admin`  
> Password: `password123`

### 4. Running the Application
Start the Flask development server:
```bash
python app.py
```
Then open in your browser:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📖 How to Use

1. **Register or Login** – Access using the admin credentials or create a new account.  
2. **Add Data** – In *Manage Data*, add Rooms, Batches, Subjects, and Faculty.  
3. **Assign Subjects** – Map each subject to the faculty who can teach it.  
4. **Generate Timetable** – From the dashboard, run the generator to produce optimized schedules.  
5. **View & Export** – Review timetables and export them to **PDF** or **Excel**.  
6. **Analyze Data** – Use the **Analytics Dashboard** for visual insights.

---

## 🔮 Future Enhancements
- **Predictive Workload Analysis:** AI-driven prediction of faculty burnout or overload.  
- **Conversational AI Assistant:** Chatbot interface for managing data via natural language.  
- **Drag-and-Drop Editing:** Manual fine-tuning of generated timetables.  

---

## 🌟 Project Outcomes
This project demonstrates:
- Mastery in **AI optimization algorithms (Genetic Algorithms)**  
- Strong **Full-Stack Development** skills (Flask + JS)  
- **Data Visualization** and **User-Centered Design** expertise  
- A real-world **AI application for education management**

---

## 🧑‍💻 Author
**Veera Karthick**  
*AI & Data Science Student | Aspiring Trillionaire | Real-World Problem Solver*  

📧 Email: [your-email@example.com]  
💼 LinkedIn: [https://linkedin.com/in/your-link](https://linkedin.com/in/your-link)  
🌐 GitHub: [https://github.com/your-username](https://github.com/your-username)

---

## 📜 License
This project is licensed under the **MIT License** – you’re free to use, modify, and distribute it with attribution.

---

**💡 “AI doesn’t replace humans — it amplifies human intelligence.”**
