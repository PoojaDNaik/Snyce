# Checklist Application

The **Checklist Application** is a web application built using **FastAPI**. This application allows users to manage checklists by creating, viewing, and responding to their personal checklists.

## Features
- User authentication and login
- Create, view, and manage checklists
- Backend API with **FastAPI**
- **MySQL** database for data storage

## Installation

### Prerequisites
- **Python 3.11.6**

### Steps to Install

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/checklist-application.git
    cd checklist-application
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    Ensure you are in the virtual environment, then install the required packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the database initialization script**:
    If you're using a different server or environment, you will need to initialize the database before starting the application. Run the following command to set up the necessary tables:
    ```bash
    python initDB.py
    ```

5. **Run the application**:
    Use **uvicorn** to start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

    The server should start at `http://127.0.0.1:8000`.

---

You can now visit `http://127.0.0.1:8000` in your browser to use the Checklist Application.
