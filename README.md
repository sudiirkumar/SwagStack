# 🧢 SwagStack – Inventory & Order Management System

SwagStack is a sleek, full-stack inventory and order management system tailored for managing college merchandise. Built with Python Flask, MySQL, and HTML/CSS/JavaScript, it allows users to handle products, orders, users, and transaction logs with ease.

---

## 🚀 Features

- 🔐 **User Management**
  - Role-based access: Admin and Staff
  - Manage user accounts, toggle admin status

- 📦 **Product Management**
  - Add, update, delete merchandise items
  - Auto-log changes via SQL triggers

- 🧾 **Order Management**
  - Create new orders
  - Mark orders as completed
  - Auto-decrease product stock
  - Handle product deletions gracefully

- 📚 **Transaction Log**
  - Logs every add/update/delete/sale/restock
  - Trigger-based with timestamps and user tracking

- ⚙️ **Tech Stack**
  - Backend: Flask (Python)
  - Frontend: HTML, CSS, JavaScript
  - Database: MySQL
  - ORM: Raw SQL + Flask-MySQLdb
  - Styling: Minimal, responsive design

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sudiirkumar/SwagStack.git
cd SwagStack
```

### 2. Set Up the MySQL Database


### 3. Update MySQL Configuration in `app.py`

```python
app.config['MYSQL_USER'] = 'yourusername'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'swagstack'
```

## 📌 Notes

- Triggers log all important inventory operations.
- Role-based control is enforced on frontend & backend.
- All critical actions show confirmation alerts.

---

## 🧑‍💻 Contributors

- [Sudhir Kumar](https://github.com/sudiirkumar)
- [Shrey Gupta](https://github.com/ShreyIND)

---

## 📄 License

MIT License © 2025 [Sudhir Kumar]
