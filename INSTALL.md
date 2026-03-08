# 🚀 INSTALLATION & USAGE GUIDE

## Quick Start (3 Steps)

### Step 1: Open Command Prompt
- Press `Win + R`
- Type `cmd`
- Press Enter

### Step 2: Navigate to Project
```bash
cd "c:\Supply chain"
```

### Step 3: Run Application
```bash
python -m streamlit run app.py
```

The application will automatically open in your browser at http://localhost:8501

---

## Alternative: Manual Installation

If you get errors, install dependencies first:

```bash
cd "c:\Supply chain"
pip install streamlit plotly pandas numpy scikit-learn networkx
python -m streamlit run app.py
```

---

## Verify Installation

Test all modules before running:
```bash
python test_app.py
```

Expected output:
```
Testing Supply Chain Control Tower modules...

1. Testing data generator...
   [OK] Generated 10 suppliers
   [OK] Generated 9 dependencies
   [OK] Generated 4 risk events

2. Testing ML models...
   [OK] Trained predictor on 76 historical events
   [OK] Initialized cascade simulator
   [OK] Initialized what-if optimizer

3. Testing page modules...
   [OK] All page modules loaded successfully

[SUCCESS] All tests passed! Application is ready to run.
```

---

## Troubleshooting

### Issue: "python not found"
**Solution:** Install Python 3.8+ from python.org

### Issue: "streamlit not found"
**Solution:** 
```bash
pip install streamlit plotly pandas numpy scikit-learn networkx
```

### Issue: "Port 8501 already in use"
**Solution:**
```bash
python -m streamlit run app.py --server.port 8502
```

### Issue: Module import errors
**Solution:**
```bash
cd "c:\Supply chain"
python test_app.py
```

---

## Application Features

Once running, you'll see 6 pages in the sidebar:

1. **🏠 Home** - Overview of 4 problems
2. **📊 Live Risk Dashboard** - Real-time monitoring
3. **🧬 DNA Visualizer** - Network dependencies
4. **⚡ Cascade Simulator** - Impact simulation
5. **🎯 What-If Optimizer** - Strategy comparison
6. **📚 Tamil Nadu Case Studies** - Real scenarios

---

## Demo Flow (5 Minutes)

1. Start on Home page - explain 4 problems
2. Risk Dashboard - show Chennai Port alert (75% risk)
3. DNA Visualizer - point out red lines (single-source)
4. Cascade Simulator - select S007, run simulation
5. What-If Optimizer - set 7 days, optimize strategy
6. Case Studies - show Chennai floods savings

---

## Stop Application

Press `Ctrl + C` in the command prompt window

---

## Need Help?

- Check DEMO_GUIDE.md for detailed instructions
- Check QUICK_REFERENCE.md for demo script
- Check PROJECT_SUMMARY.md for full documentation

---

## Ready to Present! 🎉

Your application is complete and tested.
Just run: `python -m streamlit run app.py`
