@echo off
cd /d "%~dp0"
:: If using a virtual environment, activate it here:
:: call venv\Scripts\activate
streamlit run app.py
pause