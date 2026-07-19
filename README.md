# User Management API

This project provides a comprehensive user management system using FastAPI. It includes features for user creation, retrieval, update, and deletion, with JWT authentication and role-based access control (RBAC). Additionally, it supports email verification, real-time notifications via WebSocket, and a GraphQL endpoint.

## Architecture Overview

The architecture of the User Management API is designed as a monolith using FastAPI. It utilizes SQLAlchemy for ORM operations, Redis for caching, and Celery for background tasks like sending emails. The application is configured using the `src/config.py` module, which contains all necessary settings such as database credentials and debug mode.

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL or SQLite (optional)
- Redis (optional)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/python-skills.git
   cd python-skills
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database (if using SQLite):**
   ```bash
   alembic init migrations
   python src/db_migrate.py create_tables
   ```

5. **Run the application:**
   ```bash
   uvicorn src.main:app --reload
   ```

## Contribution Guidelines

1. **Fork the repository** and clone your fork.
2. **Create a new branch** for your feature or bug fix.
3. **Make changes** to the codebase, ensuring you follow the coding standards outlined below.
4. **Write tests** for any new features or changes that affect existing functionality.
5. **Run the tests:**
   ```bash
   pytest
   ```
6. **Commit your changes** with a descriptive commit message.
7. **Push to your forked repository.**
8. **Create a pull request** against the main branch of the original repository.

### Coding Standards

- **Type hints:** Use type hints for function and variable declarations.
- **PEP 8 Compliance:** Follow PEP 8 guidelines for code formatting and style.
- **Docstrings:** Write docstrings for all public functions, classes, and modules.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.