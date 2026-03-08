@echo off
cls
echo ============================================================
echo    AI-Powered Resilient Supply Chain Control Tower
echo    Hackathon 2025 - Tamil Nadu Supply Chain Initiative
echo ============================================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
python --version
echo.

echo [2/3] Testing application modules...
python test_app.py
if errorlevel 1 (
    echo.
    echo [ERROR] Module test failed! Installing dependencies...
    pip install streamlit plotly pandas numpy scikit-learn networkx
    echo.
    echo Retesting...
    python test_app.py
)
echo.

echo [3/3] Starting Streamlit application...
echo.
echo ============================================================
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python -m streamlit run app.py

pause
