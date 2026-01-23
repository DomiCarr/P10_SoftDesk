# P10_SoftDesk

# 🛡️ SoftDesk Support API

**SoftDesk** est une interface de programmation d'application (API) robuste conçue pour la gestion et le suivi des anomalies (issues) pour divers projets techniques. Elle permet aux collaborateurs d'un projet de centraliser les tickets, de suivre leur résolution et de communiquer via des commentaires dédiés.

---

## 📚 Table of Contents

- [Features](#-features)
- [Application Architecture](#-application-architecture)
- [Installation Guide](#-installation-guide)
- [Launch the Application](#-launch-the-application)
- [Built With](#-built-with)
- [Compliance & Ethics](#️-compliance--ethics)
- [Author](#-author)
- [License](#-license)

---

## 🧩 Features

- **User Authentication**: Secure signup and login system using **JSON Web Tokens (JWT)**.
- **Project Management**: Create and manage projects, including defining the platform type (Back-end, Front-end, iOS, or Android).
- **Contributor System**: Fine-grained management of users authorized to access specific project resources.
- **Issue Tracking**: Create and monitor tickets with priority levels (Low, Medium, High), tags (Bug, Feature, Task), and statuses (To Do, In Progress, Finished).
- **Comment System**: Collaborative communication through comments linked to specific issues.
- **Granular Permissions**:
    - Access restricted to authenticated users only.
    - Resources are visible to all project contributors and the project manager.
    - Only the **author** of a project, issue, or comment can update or delete it.
- **GDPR Compliance**:
    - Users can access and rectify their personal profile information.
    - **Right to be forgotten**: Users can delete their accounts and personal data entirely.
    - **Age Verification**: Mandatory check to ensure users are at least 15 years old during registration.
- **Green Code & Performance**:
    - **Pagination**: Systematic resource pagination to reduce server load and bandwidth usage.
    - **Query Optimization**: Implementation of `select_related` to eliminate "N+1" query problems and minimize server CPU cycles.

---

## 🧠 Application Architecture

**SoftDesk** is a REST API built with **Django REST Framework (DRF)**. Unlike the classic MTV model, this architecture focuses on data serialization and endpoint logic for consumption by frontend or mobile clients.

- **Models**: Define the database schema (Projects, Contributors, Issues, Comments) and security constraints (e.g., age validation).
- **Serializers**: Handle the conversion of complex data (models) into JSON and ensure incoming data validation.
- **Views (ViewSets)**: Contain the business logic and apply security filtering as well as SQL optimizations (`select_related`).
- **Permissions**: Custom classes that verify if the user is the author or a contributor before authorizing access or modification.
- **URLs (Routers)**: Manage routing, including nested routes to link issues to projects and comments to issues.

Here is the current project structure:

```
softdesk_project/
├── manage.py              # Django entry point
├── db.sqlite3             # SQLite database
├── Pipfile                # Pipenv dependencies
├── Pipfile.lock           # Dependency lock file
├── README.md              # Project documentation
├── _dev_utils/            # Developer utility scripts
├── softdesk_project/      # Project configuration
│   ├── settings.py        # Global settings (JWT, Pagination, Apps)
│   └── urls.py            # Root routing (api/users/, api/projects/)
└── apps/                  # Business applications
    ├── users/             # User management and authentication
    │   ├── models.py      # Custom User model (age, consent)
    │   ├── serializers.py # User serialization logic
    │   └── views.py       # Signup/Login endpoints (JWT)
    └── projects/          # Core domain
        ├── models.py      # Project, Contributor, Issue, Comment
        ├── serializers.py # Data validation and transformation
        ├── views.py       # Logic with select_related and pagination
        └── permissions.py # IsAuthor, IsProjectContributor
```
---

## 🚀 Installation Guide

> ⚠️ **Compatibility Note**
> This project requires **Python ≥ 3.10** and **Pipenv**.

> 🐧 **Note macOS/Linux**
> On Linux/Mac, the `python` command may not be available by default.
> Use `python3` instead.

Clone the repository from GitHub:

```bash
git clone https://github.com/DomiCarr/OCR_P10_SoftDesk
cd OCR_P10_SoftDesk
```


### 🛠️ Set up the virtual environment

This project uses **Pipenv** to manage its virtual environment and dependencies.
When you run the installation command, Pipenv reads the `Pipfile` and `Pipfile.lock` files included in the repository to recreate the exact environment used for development.

📝 Note Pipenv automatically handles the virtual environment creation and activation across all platforms (Windows, macOS, and Linux). It ensures that all dependencies are installed in their precise versions without modifying the existing Pipfile.

**Create and install:**

```bash
pipenv install
```

**Activate:**

```bash
pipenv shell
```

### ✅ Verify installation

Run the following to confirm packages are installed:

```bash
pip freeze
```

Expected output includes:

```text
asgiref==3.11.0
Django==6.0.1
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
drf-nested-routers==0.95.0
PyJWT==2.10.1
python-dotenv==1.2.1
sqlparse==0.5.5
```

---

### 🏃 Prepare the database

From the project root:

```bash
# If python doesn't work, use python3

# Apply all migrations to initialize the database
python manage.py migrate

# (Optional) Create a superuser for Django admin
# You will be prompted to enter username, email, and password
python manage.py createsuperuser

# Run the Django development server
python manage.py runserver

```

## 🏃 Launch the Application

The API will be available at: http://127.0.0.1:8000/

---

## ⚖️ Compliance & Ethics

This project is developed with a focus on modern web standards and data protection:

* **OWASP** — Security best practices are implemented to protect against common vulnerabilities, including secure authentication via JWT and strict permission management.
* **RGPD (GDPR)** — Data privacy by design: the system collects only necessary user information and ensures secure handling of personal data.
* **GreenCode** — Development focuses on efficiency and resource optimization to minimize the digital footprint of the application.

---

## 🧰 Built With

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

- **Python** — Main programming language
- **Django & Django REST Framework** — Web framework and API toolkit
- **Pipenv** — Dependency and environment management
- **Postman** — Used for API testing and documentation
- **Cross-platform compatibility** — Works on 🐧 Linux, 🍎 macOS, and 🪟 Windows

---

## 📦 Releases

- **Version 1.0** — Initial release

---

## 👤 Author

**Dominique Carrasco**
GitHub: [@DomiCarr](https://github.com/DomiCarr)

---

## 📄 License

This project is licensed under the [OpenClassrooms Terms & Conditions](https://openclassrooms.com/fr/policies/terms-conditions)