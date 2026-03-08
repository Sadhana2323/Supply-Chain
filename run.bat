@echo off
echo ========================================
echo Supply Chain Control Tower
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting application...
echo.
streamlit run app.py
