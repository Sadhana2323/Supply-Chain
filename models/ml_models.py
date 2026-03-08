import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import networkx as nx

class DisruptionPredictor:
    """Random Forest model for predicting disruption probability"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.le_location = LabelEncoder()
        self.le_type = LabelEncoder()
        self.trained = False
    
    def train(self, historical_data):
        """Train model on historical disruption data"""
        if len(historical_data) == 0:
            return
        
        # Feature engineering
        historical_data['month'] = pd.to_datetime(historical_data['date']).dt.month
        historical_data['is_monsoon'] = historical_data['month'].isin([6, 7, 8, 9, 10, 11]).astype(int)
        
        # Encode categorical variables
        historical_data['location_encoded'] = self.le_location.fit_transform(historical_data['location'])
        historical_data['type_encoded'] = self.le_type.fit_transform(historical_data['type'])
        
        # Create binary target (high severity = 1)
        y = (historical_data['severity'] == 'High').astype(int)
        
        X = historical_data[['month', 'is_monsoon', 'location_encoded', 'type_encoded']]
        
        self.model.fit(X, y)
        self.trained = True
    
    def predict_risk(self, location, event_type, month):
        """Predict disruption probability for given conditions"""
        if not self.trained:
            # Return default probabilities if not trained
            return np.random.uniform(0.3, 0.8)
        
        is_monsoon = 1 if month in [6, 7, 8, 9, 10, 11] else 0
        
        try:
            location_encoded = self.le_location.transform([location])[0]
            type_encoded = self.le_type.transform([event_type])[0]
        except:
            return 0.5  # Default if unseen category
        
        X = np.array([[month, is_monsoon, location_encoded, type_encoded]])
        prob = self.model.predict_proba(X)[0][1]
        
        return prob

class CascadeSimulator:
    """Monte Carlo simulation for cascade effect modeling"""
    
    def __init__(self, suppliers_df, dependencies_df, products_df, customers_df):
        self.suppliers_df = suppliers_df
        self.dependencies_df = dependencies_df
        self.products_df = products_df
        self.customers_df = customers_df
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build directed graph of supply chain network"""
        G = nx.DiGraph()
        
        # Add supplier nodes
        for _, supplier in self.suppliers_df.iterrows():
            G.add_node(supplier['id'], **supplier.to_dict())
        
        # Add dependency edges
        for _, dep in self.dependencies_df.iterrows():
            G.add_edge(dep['from'], dep['to'], **dep.to_dict())
        
        return G
    
    def simulate_cascade(self, failed_node, delay_days, num_simulations=1000):
        """Simulate cascade effect of a supplier failure using Monte Carlo"""
        
        # Find all downstream nodes
        try:
            downstream = list(nx.descendants(self.graph, failed_node))
        except:
            downstream = []
        
        affected_suppliers = [failed_node] + downstream
        
        # Calculate impact timeline
        timeline = {}
        for node in affected_suppliers:
            if node == failed_node:
                timeline[node] = 0  # Immediate impact
            else:
                # Calculate path length from failed node
                try:
                    path_length = nx.shortest_path_length(self.graph, failed_node, node)
                    # Add lead time delays
                    cumulative_delay = 0
                    path = nx.shortest_path(self.graph, failed_node, node)
                    for i in range(len(path) - 1):
                        edge_data = self.graph.get_edge_data(path[i], path[i+1])
                        if edge_data:
                            cumulative_delay += edge_data.get('lead_time', 2)
                    timeline[node] = cumulative_delay
                except:
                    timeline[node] = delay_days
        
        # Find affected products
        affected_products = []
        for _, product in self.products_df.iterrows():
            if product['supplier'] in affected_suppliers or product['port'] in affected_suppliers:
                affected_products.append(product)
        
        # Find affected customers
        affected_customers = []
        affected_product_ids = [p['id'] for p in affected_products]
        for _, customer in self.customers_df.iterrows():
            if any(pid in customer['products'] for pid in affected_product_ids):
                affected_customers.append(customer)
        
        # Monte Carlo simulation for cost impact
        cost_impacts = []
        for _ in range(num_simulations):
            total_cost = 0
            for product in affected_products:
                # Random delay between delay_days and delay_days * 1.5
                actual_delay = np.random.uniform(delay_days, delay_days * 1.5)
                # Cost = daily revenue loss + expediting costs
                daily_revenue = product['monthly_volume'] * product['value_per_unit'] / 30
                expediting_cost = daily_revenue * 0.3  # 30% premium for expediting
                total_cost += (daily_revenue + expediting_cost) * actual_delay
            
            cost_impacts.append(total_cost)
        
        return {
            'affected_suppliers': affected_suppliers,
            'affected_products': affected_products,
            'affected_customers': affected_customers,
            'timeline': timeline,
            'cost_impact_mean': np.mean(cost_impacts),
            'cost_impact_std': np.std(cost_impacts),
            'cost_impact_95th': np.percentile(cost_impacts, 95)
        }

class WhatIfOptimizer:
    """Optimizer for testing different mitigation strategies"""
    
    def __init__(self, products_df):
        self.products_df = products_df
    
    def optimize_strategy(self, delay_days, supplier_failure_prob, demand_spike_pct):
        """Test multiple strategies and recommend optimal one"""
        
        # Calculate baseline impact
        baseline_cost = self._calculate_baseline_cost(delay_days)
        
        strategies = []
        
        # Strategy 1: Air Freight
        air_freight_cost = baseline_cost * 0.4 + (baseline_cost * 0.5)  # 40% of loss + 50% premium
        air_freight_resilience = 0.9  # 90% resilience
        strategies.append({
            'name': 'Air Freight Expediting',
            'cost': air_freight_cost,
            'resilience_score': air_freight_resilience,
            'implementation_time': '1-2 days',
            'description': 'Use air freight for critical shipments'
        })
        
        # Strategy 2: Alternate Suppliers
        alt_supplier_cost = baseline_cost * 0.6 + (baseline_cost * 0.2)  # 60% of loss + 20% switching cost
        alt_supplier_resilience = 0.75
        strategies.append({
            'name': 'Alternate Supplier Activation',
            'cost': alt_supplier_cost,
            'resilience_score': alt_supplier_resilience,
            'implementation_time': '3-5 days',
            'description': 'Switch to pre-qualified backup suppliers'
        })
        
        # Strategy 3: Inventory Buffer
        inventory_cost = baseline_cost * 0.3 + (baseline_cost * 0.15)  # 30% of loss + 15% holding cost
        inventory_resilience = 0.85
        strategies.append({
            'name': 'Safety Stock Increase',
            'cost': inventory_cost,
            'resilience_score': inventory_resilience,
            'implementation_time': 'Immediate',
            'description': 'Increase buffer inventory by 20%'
        })
        
        # Strategy 4: Hybrid Approach
        hybrid_cost = baseline_cost * 0.25 + (baseline_cost * 0.35)
        hybrid_resilience = 0.95
        strategies.append({
            'name': 'Hybrid Strategy',
            'cost': hybrid_cost,
            'resilience_score': hybrid_resilience,
            'implementation_time': '2-3 days',
            'description': 'Combine air freight + alternate suppliers + buffer stock'
        })
        
        # Calculate cost-resilience score (lower is better)
        for strategy in strategies:
            strategy['score'] = strategy['cost'] / strategy['resilience_score']
        
        # Sort by score
        strategies.sort(key=lambda x: x['score'])
        
        return {
            'baseline_cost': baseline_cost,
            'strategies': strategies,
            'recommended': strategies[0]
        }
    
    def _calculate_baseline_cost(self, delay_days):
        """Calculate baseline cost impact of disruption"""
        total_cost = 0
        for _, product in self.products_df.iterrows():
            daily_revenue = product['monthly_volume'] * product['value_per_unit'] / 30
            total_cost += daily_revenue * delay_days
        
        return total_cost

def forecast_delay(historical_delays, horizon=7):
    """Simple time-series forecasting for delay prediction"""
    if len(historical_delays) < 3:
        return [np.random.randint(1, 4) for _ in range(horizon)]
    
    # Simple moving average with trend
    recent = historical_delays[-7:]
    mean_delay = np.mean(recent)
    trend = (recent[-1] - recent[0]) / len(recent) if len(recent) > 1 else 0
    
    forecast = []
    for i in range(horizon):
        predicted = mean_delay + trend * i + np.random.normal(0, 0.5)
        forecast.append(max(0, predicted))
    
    return forecast
