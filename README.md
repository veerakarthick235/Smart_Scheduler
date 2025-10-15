🧠 AI-Powered Smart Timetable Scheduler
Introduction
The Smart Timetable Scheduler is a full-stack web application designed to solve the complex challenge of scheduling classes in higher education institutions. Traditional manual scheduling is prone to errors, resource conflicts, and inefficiencies. This project leverages a sophisticated genetic algorithm to automate and optimize the process, ensuring maximal resource utilization and minimizing conflicts.

Built with a modern, AI-themed interface, this application provides a complete solution from data entry to analytics and exporting, incorporating intelligent features to assist administrators in making informed decisions.

✨ Key Features
This project is packed with professional-grade features:

🤖 Intelligent Timetable Generation:

Core scheduling logic is powered by a Genetic Algorithm to find optimized solutions for complex constraints.

Generates multiple timetable options, ranked by a "fitness score" indicating the number of soft conflicts.

💻 Dynamic Data Management (CRUD):

A user-friendly "Manage Data" interface to dynamically add, view, and delete all necessary parameters:

Rooms & Classrooms

Batches / Programs

Subjects (including hours per week)

Faculty Members

Intuitive system for assigning subjects to the faculty who can teach them.

🔐 Secure User Authentication:

A complete user registration and login system.

Passwords are fully secured using industry-standard hashing (werkzeug).

📊 Analytics Dashboard:

A dedicated analytics page to visualize key university metrics.

Interactive charts (powered by Chart.js) display data like faculty workload distribution.

📄 PDF & Excel Export:

Seamlessly export any generated timetable option to universally compatible formats (PDF or MS Excel) for printing and sharing.

💡 Live AI Conflict Suggestions:

An AI-powered suggestion engine that provides real-time feedback on the "Manage Data" page.

Warns users about potential issues like faculty overload or unassigned subjects before generation is attempted.

🎨 Modern AI-Themed UI:

A sleek, dark-mode "AI College" theme with glowing interactive elements.

The entire application is fully responsive and designed for a professional user experience.

🛠️ Tech Stack
Backend
Python 3

Flask: A micro web framework for the server and APIs.

Flask-SQLAlchemy: For database object-relational mapping (ORM).

Werkzeug: For secure password hashing.

Pandas & openpyxl: For structuring data and exporting to Excel.

WeasyPrint: For generating PDF documents from HTML.

Frontend
HTML5

CSS3 (with Bootstrap 5 for layout)

JavaScript (ES6+): For all frontend interactivity, API calls (fetch), and dynamic content rendering.

Chart.js: For creating beautiful, interactive charts on the analytics dashboard.

Database
SQLite: A lightweight, file-based database perfect for this application.

🚀 Getting Started
Follow these steps to set up and run the project on your local machine.

1. Prerequisites
Python 3.x installed on your system.

pip (Python package installer).

2. Installation & Setup
Clone the repository to your local machine:

git clone [https://github.com/your-username/smart-scheduler.git](https://github.com/your-username/smart-scheduler.git)
cd smart-scheduler

Install all the required Python packages using the requirements.txt file:

pip install -r requirements.txt

3. Database Initialization
Before running the app for the first time, you need to create the database and the default admin user.

Important: If you have an old scheduler.db file in the /instance folder, delete it.

Run the database setup script in your terminal:

python database_setup.py

This will create an instance/scheduler.db file and an admin user with the credentials:

Username: admin

Password: password123

4. Running the Application
Once the database is set up, you can start the Flask web server:

python app.py

The application will be running and accessible at: http://127.0.0.1:5000

📖 How to Use
Register or Login: Access the application and either create a new account or log in with the default admin credentials.

Add Data: Navigate to the "Manage Data" page. This is the most important step. You must add at least one entry for every category:

Rooms

Batches

Subjects

Faculty

Finally, use the "Assign Subjects to Faculty" form to link teachers to the subjects they can teach.

Generate Timetable: Go to the "Dashboard" and click the "Generate Timetable" button. The algorithm will run, and the terminal will show its progress.

View & Export: The generated timetable options will appear on the dashboard. You can view them and use the "PDF" or "Excel" buttons to export them.

Check Analytics: Navigate to the "Analytics" page to see visual charts of your data.

🔮 Future Enhancements
Predictive Workload Analysis: An AI feature to analyze generated timetables for faculty burnout or student overload.

Conversational AI Assistant: A chatbot to allow users to manage data using natural language commands.

Drag-and-Drop Interface: Allow manual, fine-grained adjustments to the generated timetables.
