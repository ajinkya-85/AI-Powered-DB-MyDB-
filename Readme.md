# MyDB Manager - AI-Powered Database Assistant

**MyDB Manager** is a powerful, user-friendly desktop application that bridges the gap between natural language and database management. By integrating Google's advanced Gemini AI models, it allows users to interact with SQLite databases using plain English, eliminating the need to write complex SQL queries manually.

## 🚀 Features

- **🤖 AI Query Generation**: Describe what you need in natural language, and the application generates the corresponding SQL query using Google Gemini (supports models like Gemini 2.5 Flash, Pro, and more).
- **🔍 Smart Database Scanning**: Automatically detects SQLite databases (`.db`, `.sqlite`, `.sqlite3`) on your system or within specific folders.
- **⚡ Interactive Query Execution**: Execute generated queries safely and view results in a dynamic, scrollable grid.
- **📋 Table Inspector**: Browse database schemas and view table contents instantly.
- **💾 Data Export**: Export query results to CSV format for reporting or external analysis.
- **🎨 Modern Interface**: Built with CustomTkinter for a sleek look, featuring toggleable **Light** and **Dark** themes.
- **🔐 Secure Configuration**: Locally stores API keys and user preferences.

## 📋 Prerequisites

Ensure you have **Python 3.8** or higher installed on your system. You will also need a Google Gemini API key.

## 🛠️ Installation

1.  **Clone the repository** or download the source code to your local machine.
2.  **Install required dependencies** using pip:

    ```bash
    pip install customtkinter google-generativeai
    ```

## 🚀 Getting Started

1.  **Launch the Application**:
    Navigate to the project folder and run the main interface script:

    ```bash
    python user_interface.py
    ```

2.  **Configure API Key**:

    - On the first run, or via the **API Key** button in the navigation bar, enter your Google Gemini API Key.
    - To get a free key, visit Google AI Studio.

3.  **Connect to a Database**:

    - Click **Scan for Databases** to search your PC for SQLite files.
    - Alternatively, click **Folder** to select a specific directory containing your database files.
    - Select your target database from the dropdown menu.

4.  **Generate & Execute**:
    - Type your request in the prompt box (e.g., _"Find all customers who purchased 'Laptop' in 2024"_).
    - Click **Generate SQL Query**.
    - Review the generated SQL output, then click **Execute SQL Query** to see the results.

## 📂 Project Structure

| File                | Description                                                            |
| :------------------ | :--------------------------------------------------------------------- |
| `user_interface.py` | Main application entry point and controller logic.                     |
| `ui_panels.py`      | Defines the layout for the Left (Controls) and Right (Results) panels. |
| `ui_dialogs.py`     | Manages popup windows (About, API Key, Errors).                        |
| `QueryGenerator.py` | Handles communication with the Google Gemini API.                      |
| `DB_operation.py`   | Manages SQLite database connections and execution.                     |
| `searching.py`      | Utility for recursive file system scanning.                            |
| `config_manager.py` | Handles loading and saving of configuration settings.                  |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for bugs and feature requests.

## 👨‍💻 Developer Team

- **Developer**: Ajinkya Ghode
- **Contact**: ajinkyaghode85@gmail.com

## 📄 License

This project is open-source and available for personal and educational use.

---

_Built with Python, CustomTkinter, and Google Gemini._
