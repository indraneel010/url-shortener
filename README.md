# FastAPI Sample Project

This repository contains a sample FastAPI application demonstrating Python best practices, including PEP 8 compliance and type hinting. It provides a structured foundation for building and testing FastAPI applications.

---

## Features

- FastAPI backend with auto-generated Swagger UI (`/docs`)
- Example test cases included (`test_main.py`)
- PEP 8 compliant and type-annotated Python code
- Configured for development in VS Code Dev Containers

---

## Prerequisites
- **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Visual Studio Code** with the following extensions:
  - [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  - [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
  - [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

### Recommended VS Code Settings
- **Python > Analysis > Type Checking Mode**: `basic`
- **Python > Analysis > Inlay Hints > Function Return Types**: `enable`
- **Python > Analysis > Inlay Hints > Variable Types**: `enable`

---

## Setup
1. Open the project folder in VS Code (**File > Open Folder…**)
2. Reopen the folder in a Dev Container via the Command Palette:
   `View > Command Palette… > Dev Container: Reopen in Container`

---

## Running the Application
- Start the app using the **Run and Debug** view or by pressing `F5`
- Click the URL in the terminal (`Ctrl + click`) to open the app in a browser
- Access the Swagger UI at `/docs` to explore and test API endpoints

---

## Testing
- Configure tests via **Python: Configure Tests** from the Command Palette
- Run tests in the **Test Panel** or by clicking the run button next to individual tests in `test_main.py`
