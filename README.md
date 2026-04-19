# Employee-Management-System

A web-based Employee Management System built using **Flask**, **MySQL**, **Pandas**, **Matplotlib**, and **ReportLab**. It helps manage employees, attendance, and salary visualization with user roles like Admin and HR.

---

##  Features

-  User authentication (Login/Register)
-  Admin & HR role-based access
-  View employee records
-  Mark and view attendance
-  Salary bar chart using Matplotlib
-  Export employee data to Excel and PDF
-  Clean and simple UI with templates

---

##  Technologies Used

- **Flask** – Web framework
- **MySQL** – Database
- **Pandas** – Data handling, used to convert into excel
- **Matplotlib** – Data visualization,used to converts into chart
- **ReportLab** – PDF generation
- **HTML/CSS** – Frontend templates

---

##  Database Schema

```sql
CREATE DATABASE employee_db;

USE employee_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(10) NOT NULL
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    salary INT
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    date DATE,
    status VARCHAR(10),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
```

---

##  Installation Steps

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/employee-management-system.git
   cd employee-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-mysqldb pandas matplotlib reportlab
   ```

3. **Configure your MySQL in `app.py`**
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'yourpassword'
   app.config['MYSQL_DB'] = 'employee_db'
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the system**
   - Open your browser and go to: `http://localhost:5000`

---

## 👤 User Roles

| Role  | Access Permissions                          |
|--------|---------------------------------------------|
| Admin  | Register users, View/export data, Mark attendance |
| HR     | View/export data, Mark attendance           |

---

##  Project Structure

```
employee-management-system/
│
├── app.py                 # Main application file
├── templates/             # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── employees.html
│   ├── attendance.html
│   ├── attendance_logs.html
│   └── salary_chart.html
├── static/
│   └── salary_chart.png   # Auto-generated salary chart
├── README.md              # Project documentation
```

---

##  Output Examples

-  Employee list in table view
-  Mark attendance (present/absent)
-  View salary distribution chart
-  Export reports to Excel and PDF

---

##  License

This project is created for academic/educational purposes. You are free to use and modify it.

---

> 💡 Tip: Upload this project with a `.gitignore` to avoid uploading `__pycache__` or `*.pyc` files.
