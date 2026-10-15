# 📚 Marksheet Management System

A professional Marksheet Management System built with **Python Flask**, **MySQL**, and **Bootstrap 5**.

## 🌟 Features

- 🔐 Login, Register, Forgot & Reset Password
- 👥 Role-Based Access (Admin / User)
- 📊 Dashboard with Stats (Total, Pass, Fail)
- ➕ Create, View, Edit, Delete Marksheets
- 🖨️ Printable Marksheet
- ⚡ AJAX Delete & Edit (No Page Reload)
- 📧 Real Email for Password Reset
- 🔒 Password Hashing & Session Protection
- 📱 Responsive Bootstrap 5 UI

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | MySQL (XAMPP) |
| Frontend | HTML5, Bootstrap 5, JavaScript |
| Templates | Jinja2 |
| Email | Flask-Mail (Gmail) |
| Version Control | Git & GitHub |

## 📊 Grading System

| Grade | Percentage |
|---|---|
| A | 80% and above |
| B | 70% – 79.99% |
| C | 60% – 69.99% |
| D | 50% – 59.99% |
| E | 40% – 49.99% |
| F | Below 40% (Fail) |

> A student **fails** if any subject mark is below 40.

## 🗄️ Database Schema

```sql
CREATE TABLE marksheets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(50) NOT NULL,
    class VARCHAR(50) NOT NULL,
    exam_name VARCHAR(100) NOT NULL,
    english INT NOT NULL,
    mathematics INT NOT NULL,
    computer INT NOT NULL,
    physics INT NOT NULL,
    chemistry INT NOT NULL,
    total INT NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    result VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/fayazahmedsaand123/marksheet-system.git
cd marksheet-system
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install flask mysql-connector-python python-dotenv flask-mail itsdangerous
```

### 4. Create `.env` file
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=marksheet_system
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password


### 5. Setup Database
- Start XAMPP (Apache + MySQL)
- Open phpMyAdmin
- Create database `marksheet_system`
- Run the SQL schema above

### 6. Run the project
```bash
python app.py
```

Open browser: **http://127.0.0.1:5000**

## 👨‍💻 Developer

**Fayaz Ahmed Saand**
Full Stack Web Developer
- PHP, Laravel, MySQL
- Python, Flask
- HTML, CSS, Bootstrap, JavaScript, AJAX

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
