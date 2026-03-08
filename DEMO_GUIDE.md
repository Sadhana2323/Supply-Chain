# 🎯 DEMO GUIDE FOR JUDGES

## Quick Start
```bash
python -m streamlit run app.py
```
The app will open automatically in your browser at http://localhost:8501

---

## 5-Minute Demo Flow

### 1. LANDING PAGE (30 seconds)
- Shows all 4 problems with color-coded cards
- Highlights Tamil Nadu context with real metrics
- Sets up the value proposition

**Key Points to Mention:**
- ₹2.5Cr average cost per Chennai Port disruption
- 40% cost reduction with proactive response

---

### 2. LIVE RISK DASHBOARD (1 minute)
**What to Show:**
- Interactive map with Tamil Nadu ports and suppliers
- Color-coded risk zones (Red = Flood-prone, Orange = Cyclone-prone)
- Real-time risk alerts with probability scores
- Risk distribution charts

**Key Demo Actions:**
- Hover over map markers to see supplier details
- Point out Chennai Port with HIGH risk (75% probability)
- Show risk breakdown by type (Weather, Geopolitical, Congestion)

**Solves:** PROBLEM 1 - NO WARNING SYSTEM

---

### 3. DNA VISUALIZER (1 minute)
**What to Show:**
- Interactive network graph of multi-tier supply chain
- Red lines = Single-source dependencies (HIGH RISK)
- Blue lines = Multi-source dependencies (LOW RISK)
- Node colors show geographic risk zones

**Key Demo Actions:**
- Hover over nodes to see supplier details
- Point out single-source dependencies in red
- Highlight suppliers in flood-prone zones
- Show the vulnerability analysis section

**Solves:** PROBLEM 2 - HIDDEN WEAKNESSES

---

### 4. CASCADE SIMULATOR (1.5 minutes)
**What to Show:**
- Dropdown to select any supplier
- Monte Carlo simulation (1000 iterations)
- Timeline showing when each node is affected
- Cost impact with mean, std dev, and 95th percentile

**Key Demo Actions:**
1. Select "S007 - Chennai Cotton Suppliers"
2. Set delay to 5 days
3. Click "Run Cascade Simulation"
4. Show:
   - 4 affected suppliers
   - 2 affected products
   - 2 affected customers
   - ₹X.XX Cr cost impact
   - Day-by-day timeline

**Solves:** PROBLEM 3 - INVISIBLE DOMINO EFFECT

---

### 5. WHAT-IF OPTIMIZER (1 minute)
**What to Show:**
- Scenario configuration sliders
- 4 strategy comparisons
- Cost vs Resilience trade-off
- AI recommendation with ROI

**Key Demo Actions:**
1. Set: 7 days delay, 50% failure probability, 20% demand spike
2. Click "Optimize Strategy"
3. Show:
   - Baseline cost (do nothing)
   - 4 strategies with costs and resilience scores
   - Recommended strategy (usually Hybrid)
   - Savings calculation

**Solves:** PROBLEM 4 - PANIC MODE PLANNING

---

### 6. TAMIL NADU CASE STUDIES (30 seconds)
**What to Show:**
- 3 real scenarios from 2023-2025
- Chennai Floods (Dec 2023)
- Thoothukudi Closure (Mar 2024)
- US Tariff Shock (Jul 2024)

**Key Demo Actions:**
- Select "Chennai Floods - December 2023"
- Show actual impact: 6 days delay, ₹4.5L cost
- Show how Control Tower would have saved 35%

---

## Key Talking Points

### Technical Innovation
✓ Random Forest ML for disruption prediction
✓ Monte Carlo simulation (1000 iterations) for cascade modeling
✓ NetworkX graph algorithms for dependency analysis
✓ Real-time data integration architecture

### Business Impact
✓ 24-72 hour advance warning vs reactive response
✓ 35-40% cost reduction in disruption scenarios
✓ Identifies hidden single-point failures
✓ Data-driven decision making vs panic mode

### Tamil Nadu Context
✓ Chennai Port, Thoothukudi VOC Port, Krishnapatnam Port
✓ Tiruppur knitwear, Coimbatore engineering, Karur textiles
✓ Monsoon season patterns (June-November)
✓ Real case studies from 2023-2025

---

## Impressive Features to Highlight

1. **Interactive Visualizations**: All charts are Plotly-based, fully interactive
2. **Real-time Simulation**: Monte Carlo runs 1000 iterations in seconds
3. **Multi-tier Mapping**: Shows Tier 1 (Ports), Tier 2 (Manufacturers), Tier 3 (Raw Materials)
4. **Geographic Overlay**: Risk zones mapped to actual Tamil Nadu locations
5. **Cost-Resilience Optimization**: AI recommends optimal strategy, not just cheapest

---

## Questions Judges Might Ask

**Q: Is this real data?**
A: Synthetic data based on real Tamil Nadu supply chain structure. Ports, cities, and case studies are real; volumes are realistic estimates.

**Q: How does the ML model work?**
A: Random Forest trained on historical disruption patterns considering location, season, event type. Monte Carlo simulates 1000 scenarios for cost impact range.

**Q: Can this scale to larger networks?**
A: Yes, NetworkX handles thousands of nodes efficiently. Current demo has 10 suppliers for clarity, but architecture supports enterprise scale.

**Q: How do you get real-time data?**
A: Architecture designed to integrate with weather APIs, news feeds, port systems. Demo shows the interface with simulated real-time data.

**Q: What's the ROI?**
A: Based on case studies, 35-40% cost reduction in disruptions. For a company with ₹10Cr annual disruption costs, that's ₹3.5-4Cr savings.

---

## Troubleshooting

**If app doesn't start:**
```bash
python -m streamlit run app.py
```

**If modules not found:**
```bash
pip install streamlit plotly pandas numpy scikit-learn networkx
```

**If port 8501 is busy:**
```bash
python -m streamlit run app.py --server.port 8502
```

---

## Post-Demo

**GitHub/Documentation:**
- Full code with comments
- README with setup instructions
- Modular architecture for easy extension
- MIT License for open use

**Future Enhancements:**
- Live API integration (weather, news, port data)
- Mobile app for on-the-go monitoring
- Blockchain for supply chain transparency
- AI chatbot for natural language queries

---

Good luck with your demo! 🚀
