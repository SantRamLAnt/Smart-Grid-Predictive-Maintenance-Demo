import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List

# Configure page
st.set_page_config(
    page_title="Smart Grid Predictive Maintenance on AKS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #ff6b35;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #ff6b35;
        padding-bottom: 1rem;
        background: linear-gradient(90deg, #ff6b35, #f7931e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .asset-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        border-left: 5px solid #ff6b35;
        position: relative;
        overflow: hidden;
    }
    
    .asset-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .asset-card:hover::before {
        left: 100%;
    }
    
    .asset-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .high-risk {
        border-left-color: #dc3545 !important;
        background: linear-gradient(135deg, #fff5f5, #ffe6e6);
        animation: pulse-red 3s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 5px 15px rgba(220,53,69,0.3); }
        50% { box-shadow: 0 8px 25px rgba(220,53,69,0.5); }
    }
    
    .medium-risk {
        border-left-color: #ffc107 !important;
        background: linear-gradient(135deg, #fffdf5, #fff9e6);
    }
    
    .low-risk {
        border-left-color: #28a745 !important;
        background: linear-gradient(135deg, #f5fff5, #e6ffe6);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }
    
    .risk-indicator {
        display: inline-block;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        margin-right: 10px;
        position: relative;
    }
    
    .risk-high { 
        background-color: #dc3545; 
        animation: blink-red 2s infinite;
        box-shadow: 0 0 10px rgba(220,53,69,0.5);
    }
    .risk-medium { 
        background-color: #ffc107;
        box-shadow: 0 0 8px rgba(255,193,7,0.5);
    }
    .risk-low { 
        background-color: #28a745;
        box-shadow: 0 0 8px rgba(40,167,69,0.5);
    }
    
    @keyframes blink-red {
        0%, 50% { opacity: 1; transform: scale(1); }
        51%, 100% { opacity: 0.6; transform: scale(1.2); }
    }
    
    .model-performance {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .model-performance:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }
    
    .pipeline-step {
        background: linear-gradient(135deg, #6f42c1, #6610f2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .pipeline-step::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .pipeline-step:hover::before {
        left: 100%;
    }
    
    .pipeline-step:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }
    
    .flow-arrow {
        text-align: center;
        font-size: 2.5rem;
        color: #ff6b35;
        margin: 1rem 0;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .alert-banner {
        background: linear-gradient(45deg, #dc3545, #c82333);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        display: inline-block;
        margin: 0.5rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(220,53,69,0.3);
        animation: pulse-alert 3s infinite;
        cursor: pointer;
    }
    
    @keyframes pulse-alert {
        0%, 100% { box-shadow: 0 4px 15px rgba(220,53,69,0.3); }
        50% { box-shadow: 0 6px 25px rgba(220,53,69,0.5); }
    }
    
    .cost-savings {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        display: inline-block;
        margin: 0.5rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(40,167,69,0.3);
        animation: pulse-green 3s infinite;
        cursor: pointer;
    }
    
    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 4px 15px rgba(40,167,69,0.3); }
        50% { box-shadow: 0 6px 25px rgba(40,167,69,0.5); }
    }
    
    .tech-stack-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .tech-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        border-top: 4px solid #ff6b35;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .tech-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,107,53,0.1), transparent);
        transition: left 0.6s;
    }
    
    .tech-card:hover::before {
        left: 100%;
    }
    
    .tech-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border-top-color: #f7931e;
    }
    
    .live-status {
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 15px;
        margin: 0.3rem 0;
        animation: pulse-glow 3s infinite;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .live-status:hover {
        transform: scale(1.05);
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 8px rgba(255,107,53,0.5); }
        50% { box-shadow: 0 0 20px rgba(255,107,53,0.8); }
    }
    
    .prediction-output {
        background: #1a1a1a;
        color: #00ff41;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        border: 2px solid #00ff41;
        animation: terminal-glow 2s infinite;
    }
    
    @keyframes terminal-glow {
        0%, 100% { box-shadow: 0 0 10px rgba(0,255,65,0.3); }
        50% { box-shadow: 0 0 20px rgba(0,255,65,0.6); }
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Generate realistic asset data with more details
def generate_detailed_asset_data():
    asset_types = ["Transformer", "Circuit Breaker", "Power Line", "Substation", "Generator", "Switch Gear"]
    locations = ["North Grid Sector A", "South Grid Sector B", "East Distribution Hub", "West Transmission", "Central Control"]
    manufacturers = ["ABB", "Siemens", "GE", "Schneider", "Mitsubishi"]
    
    assets = []
    for i in range(20):  # More detailed subset
        failure_prob = random.uniform(0.05, 0.95)
        if failure_prob > 0.80:
            risk_level = "High"
            risk_color = "high-risk"
            risk_class = "risk-high"
        elif failure_prob > 0.40:
            risk_level = "Medium" 
            risk_color = "medium-risk"
            risk_class = "risk-medium"
        else:
            risk_level = "Low"
            risk_color = "low-risk"
            risk_class = "risk-low"
            
        install_date = datetime.now() - timedelta(days=random.randint(365*2, 365*25))
        last_maint = datetime.now() - timedelta(days=random.randint(30, 730))
        
        assets.append({
            "Asset ID": f"AST-{random.randint(1000, 9999)}",
            "Type": random.choice(asset_types),
            "Location": random.choice(locations),
            "Manufacturer": random.choice(manufacturers),
            "Install Date": install_date.strftime("%Y-%m-%d"),
            "Failure Probability": failure_prob,
            "Risk Level": risk_level,
            "Risk Color": risk_color,
            "Risk Class": risk_class,
            "Last Maintenance": last_maint.strftime("%Y-%m-%d"),
            "Expected Cost": random.randint(15000, 250000),
            "Crew Priority": random.randint(1, 10),
            "Voltage Level": random.choice(["4kV", "12kV", "23kV", "115kV", "138kV"]),
            "Customer Impact": random.randint(50, 5000),
            "Confidence Score": random.uniform(0.75, 0.99)
        })
    
    return sorted(assets, key=lambda x: x["Failure Probability"], reverse=True)

# Generate time series data for simple charts
def generate_trend_data():
    dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
    
    high_risk_counts = []
    accuracy_scores = []
    
    for i, date in enumerate(dates):
        base_high_risk = 146
        high_risk_variation = random.randint(-15, 15)
        high_risk_counts.append(max(100, base_high_risk + high_risk_variation))
        
        base_accuracy = 0.94
        accuracy_variation = random.uniform(-0.03, 0.02)
        accuracy_scores.append(min(0.99, max(0.85, base_accuracy + accuracy_variation)))
    
    return dates, high_risk_counts, accuracy_scores

def main():
    # Enhanced header
    st.markdown('<h1 class="main-header">⚡ Smart Grid Predictive Maintenance on AKS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #666; font-weight: 300;">AI-Powered Equipment Failure Prevention & Crew Optimization</p>', unsafe_allow_html=True)
    
    # Enhanced hero section
    st.markdown("""
    <div class="hero-section">
        <h2>🎯 Enterprise-Grade Predictive Maintenance Solution</h2>
        <p style="font-size: 1.2rem; margin: 1rem 0; opacity: 0.9;">
            ML ensemble models running on Azure Kubernetes Service to prevent equipment failures and optimize maintenance scheduling.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">🤖</div>
                <div style="font-size: 1.3rem; font-weight: bold;">100%</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Recall Rate</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">⚙️</div>
                <div style="font-size: 1.3rem; font-weight: bold;">146</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">High Risk Assets</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">💰</div>
                <div style="font-size: 1.3rem; font-weight: bold;">$2.3M</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Annual Savings</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">☁️</div>
                <div style="font-size: 1.3rem; font-weight: bold;">AKS</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Auto-scaling</div>
            </div>
        </div>
        <p style="margin-top: 2rem; font-style: italic;">
            Experience how AI transforms grid maintenance from reactive to predictive operations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar with real-time updates
    with st.sidebar:
        st.markdown("## 🔧 Live System Status")
        
        # Auto-refresh functionality
        if "last_refresh" not in st.session_state:
            st.session_state.last_refresh = datetime.now()
        
        current_time = datetime.now()
        if st.button("🔄 Refresh All Metrics", help="Update live system metrics"):
            st.session_state.last_refresh = current_time
        
        st.caption(f"Last updated: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
        
        # Live model performance with variations
        st.markdown("### 🤖 ML Model Ensemble")
        
        base_accuracy = 0.94
        time_variation = random.uniform(-0.02, 0.02)
        current_accuracy = min(0.99, max(0.90, base_accuracy + time_variation))
        
        st.markdown('<div class="live-status">📊 XGBoost + TensorFlow + RF</div>', unsafe_allow_html=True)
        st.metric("Ensemble Accuracy", f"{current_accuracy:.1%}", f"{time_variation:+.1%}")
        st.metric("Recall Rate", "100.0%", "🎯 Perfect")
        st.metric("Assets Monitored", "9,247", "+12 today")
        
        # Live infrastructure with realistic metrics
        st.markdown("### ☁️ AKS Infrastructure")
        
        pod_count = random.randint(10, 15)
        cpu_usage = random.randint(18, 35)
        memory_usage = random.randint(60, 75)
        
        st.markdown(f'<div class="live-status">🚀 Pods: {pod_count}/15 Running</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="live-status">📈 CPU: {cpu_usage}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="live-status">💾 Memory: {memory_usage}%</div>', unsafe_allow_html=True)
        
        # Live Airflow DAGs
        st.markdown("### 🔄 Airflow Orchestration")
        dag_statuses = ["✅ Success", "🔄 Running", "⏳ Queued"]
        
        st.markdown(f'<div class="live-status">{random.choice(dag_statuses)} Daily Retrain</div>', unsafe_allow_html=True)
        st.markdown('<div class="live-status">✅ Data Pipeline</div>', unsafe_allow_html=True)
        st.markdown('<div class="live-status">✅ Alert Generation</div>', unsafe_allow_html=True)

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Live Dashboard", "🏗️ ML Architecture", "📈 Business Impact", "⚙️ Technical Deep Dive"])
    
    with tab1:
        st.markdown("## 🚨 Real-Time Asset Monitoring Dashboard")
        
        # Enhanced control panel
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown("### 📊 System Overview")
            
        with col2:
            scan_button = st.button("🔍 Run ML Scan", help="Execute prediction model on all assets")
            
        with col3:
            schedule_button = st.button("📋 Optimize Crew", help="Generate optimized crew assignments")
            
        with col4:
            simulate_button = st.button("⚡ Simulate Alert", help="Test alert generation system")
        
        # Process button interactions
        if scan_button:
            with st.spinner("🤖 Running ensemble models on 9,247 assets..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
            st.success("✅ Scan complete! 5 new high-risk assets identified.")
            st.balloons()
                
        if schedule_button:
            with st.spinner("🔄 Optimizing crew assignments with constraint solver..."):
                time.sleep(2)
            st.success("✅ Schedule optimized! 23% efficiency improvement projected.")
            
        if simulate_button:
            st.error("🚨 CRITICAL ALERT: Transformer AST-7429 showing 96.3% failure probability!")
            st.markdown('<div class="alert-banner">⚠️ Immediate Maintenance Required</div>', unsafe_allow_html=True)
        
        # Enhanced live metrics with animations
        st.markdown("### ⚡ Live System Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Generate real-time variations
        high_risk_base = 146
        high_risk_current = high_risk_base + random.randint(-5, 8)
        
        with col1:
            st.markdown(f'<div class="metric-card">🎯<br><strong>{high_risk_current}</strong><br>High Risk Assets<br><small>↑ {random.randint(1,3)} from yesterday</small></div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">⚙️<br><strong>9,247</strong><br>Assets Monitored<br><small>Real-time IoT data</small></div>', unsafe_allow_html=True)
            
        with col3:
            crew_available = random.randint(20, 25)
            st.markdown(f'<div class="metric-card">👥<br><strong>{crew_available}</strong><br>Crews Available<br><small>Optimally scheduled</small></div>', unsafe_allow_html=True)
            
        with col4:
            savings_today = random.randint(450, 520)
            st.markdown(f'<div class="metric-card">💰<br><strong>${savings_today}K</strong><br>Failures Prevented<br><small>This month</small></div>', unsafe_allow_html=True)
        
        # Interactive risk distribution with real data
        st.markdown("### 🎯 Interactive Asset Risk Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Asset filtering options
            st.markdown("**🔍 Filter Assets:**")
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            
            with filter_col1:
                risk_filter = st.selectbox("Risk Level", ["All", "High", "Medium", "Low"])
            with filter_col2:
                type_filter = st.selectbox("Asset Type", ["All", "Transformer", "Circuit Breaker", "Power Line", "Substation"])
            with filter_col3:
                location_filter = st.selectbox("Location", ["All", "North Grid", "South Grid", "East Grid", "West Grid"])
            
            # Generate and filter asset data
            all_assets = generate_detailed_asset_data()
            
            # Apply filters
            filtered_assets = all_assets
            if risk_filter != "All":
                filtered_assets = [a for a in filtered_assets if a["Risk Level"] == risk_filter]
            if type_filter != "All":
                filtered_assets = [a for a in filtered_assets if type_filter in a["Type"]]
            
            # Display filtered assets with enhanced cards
            st.markdown(f"**🚨 Showing {len(filtered_assets)} Assets (Click for details):**")
            
            for i, asset in enumerate(filtered_assets[:8]):  # Show top 8
                with st.expander(f"🏗️ {asset['Asset ID']} - {asset['Type']} ({asset['Risk Level']} Risk)", expanded=False):
                    asset_col1, asset_col2, asset_col3 = st.columns(3)
                    
                    with asset_col1:
                        st.markdown(f"**📍 Location:** {asset['Location']}")
                        st.markdown(f"**🏭 Manufacturer:** {asset['Manufacturer']}")
                        st.markdown(f"**⚡ Voltage:** {asset['Voltage Level']}")
                        
                    with asset_col2:
                        st.markdown(f"**📅 Installed:** {asset['Install Date']}")
                        st.markdown(f"**🔧 Last Maintenance:** {asset['Last Maintenance']}")
                        st.markdown(f"**👥 Customers Affected:** {asset['Customer Impact']:,}")
                        
                    with asset_col3:
                        st.markdown(f"**⚠️ Failure Risk:** {asset['Failure Probability']:.1%}")
                        st.markdown(f"**💰 Failure Cost:** ${asset['Expected Cost']:,}")
                        st.markdown(f"**🎯 Confidence:** {asset['Confidence Score']:.1%}")
                        
                    # Add action buttons
                    action_col1, action_col2, action_col3 = st.columns(3)
                    with action_col1:
                        if st.button(f"📋 Schedule Maintenance", key=f"maint_{i}"):
                            st.success(f"✅ Maintenance scheduled for {asset['Asset ID']}")
                    with action_col2:
                        if st.button(f"📊 View History", key=f"hist_{i}"):
                            st.info(f"📈 Displaying maintenance history for {asset['Asset ID']}")
                    with action_col3:
                        if st.button(f"🚨 Create Alert", key=f"alert_{i}"):
                            st.warning(f"⚠️ Alert created for {asset['Asset ID']}")
        
        with col2:
            st.markdown("**📈 Risk Analytics**")
            
            # Create simple trend charts using Streamlit charts
            dates, high_risk_counts, accuracy_scores = generate_trend_data()
            
            # Risk trend chart using Streamlit line chart
            st.markdown("**📈 High Risk Assets (30 Days)**")
            trend_df = pd.DataFrame({
                'Date': dates,
                'High Risk Count': high_risk_counts
            })
            st.line_chart(trend_df.set_index('Date')['High Risk Count'], height=250)
            
            # Model accuracy chart
            st.markdown("**🎯 Model Accuracy Trend**")
            accuracy_df = pd.DataFrame({
                'Date': dates,
                'Accuracy': [acc * 100 for acc in accuracy_scores]
            })
            st.line_chart(accuracy_df.set_index('Date')['Accuracy'], height=250)
            
            # Live alerts
            st.markdown("**🚨 Active Alerts**")
            st.markdown('<div class="alert-banner">⚠️ 3 Critical Failures Predicted</div>', unsafe_allow_html=True)
            st.markdown('<div class="cost-savings">💰 $187K Failure Cost Avoided Today</div>', unsafe_allow_html=True)
        
        # Enhanced crew scheduling
        st.markdown("### 👥 Real-Time Crew Optimization")
        
        crew_data = {
            "Crew ID": ["Alpha-01", "Beta-02", "Gamma-03", "Delta-04", "Echo-05"],
            "Current Status": ["🔧 Maintenance", "🚗 Traveling", "✅ Available", "🔧 Emergency", "🍽️ Break"],
            "Current Assignment": ["AST-8847 Transformer", "Transit to Grid-North", "Ready for dispatch", "AST-9234 Circuit Breaker", "Lunch break"],
            "Next Priority": ["AST-7721", "AST-6654", "AST-5443", "AST-8901", "AST-7334"],
            "ETA Completion": ["45 min", "15 min", "Ready", "2.5 hours", "30 min"],
            "Efficiency Score": ["96%", "89%", "94%", "91%", "88%"],
            "Specialization": ["HV Transformer", "Distribution", "General", "Protection", "Substation"]
        }
        
        crew_df = pd.DataFrame(crew_data)
        
        # Add crew optimization controls
        opt_col1, opt_col2, opt_col3 = st.columns(3)
        
        with opt_col1:
            if st.button("🎯 Optimize All Crews"):
                with st.spinner("🔄 Running optimization algorithm..."):
                    time.sleep(2)
                st.success("✅ Optimal assignments calculated!")
                
        with opt_col2:
            if st.button("📍 Update Locations"):
                st.info("📡 GPS locations updated for all crews")
                
        with opt_col3:
            if st.button("⚡ Emergency Dispatch"):
                st.error("🚨 Emergency crew dispatched to Grid Sector C!")
        
        st.dataframe(crew_df, use_container_width=True)
        
        # Real-time model predictions with terminal-style output
        st.markdown("### 🤖 Live ML Model Predictions")
        
        if st.button("🎯 Execute Model Inference", help="Run ensemble prediction on current asset data"):
            with st.spinner("⚡ Processing 9,247 assets through ML pipeline..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                stages = [
                    "🔄 Loading sensor data...",
                    "🧮 Feature engineering...", 
                    "🤖 XGBoost inference...",
                    "🧠 TensorFlow prediction...",
                    "🌲 Random Forest ensemble...",
                    "📊 Risk scoring...",
                    "✅ Results ready!"
                ]
                
                for i, stage in enumerate(stages):
                    status_text.text(stage)
                    time.sleep(0.5)
                    progress_bar.progress((i + 1) * 100 // len(stages))
            
            # Display terminal-style output
            current_time = datetime.now().strftime("%H:%M:%S")
            st.markdown(f"""
            <div class="prediction-output">
            📊 ML ENSEMBLE PREDICTION RESULTS | Runtime: {current_time}
            ================================================================
            
            🎯 MODEL PERFORMANCE:
            ├── XGBoost Accuracy:     91.2% | Recall: 97.8% | Latency: 23ms
            ├── TensorFlow NN:        89.7% | Recall: 100%  | Latency: 31ms  
            └── Random Forest:        88.9% | Recall: 94.2% | Latency: 18ms
            
            🔥 ENSEMBLE CONSENSUS:    94.1% | Recall: 100%  | Avg: 24ms
            
            ⚠️  HIGH PRIORITY PREDICTIONS (>85% failure risk):
            ├── AST-8847: 94.7% | Transformer 138kV    | Cost: $187K
            ├── AST-9234: 91.2% | Circuit Breaker 23kV | Cost: $45K
            ├── AST-7721: 89.8% | Power Line 115kV     | Cost: $78K
            ├── AST-6654: 87.3% | Substation Control   | Cost: $156K
            └── AST-5443: 86.1% | Generator 4kV        | Cost: $92K
            
            💡 TOP FEATURE IMPORTANCE:
            ├── vibration_rms_30d:        23.4%
            ├── temperature_gradient:     19.8%
            ├── load_factor_variance:     16.7%
            ├── maintenance_age_days:     14.3%
            ├── electrical_harmonics:     12.1%
            └── environmental_stress:      8.9%
            
            🎯 BUSINESS IMPACT: $487K potential failure cost identified
            📋 CREW ASSIGNMENTS: 8 high-priority tasks queued
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("## 🏗️ Interactive ML Architecture & Infrastructure")
        
        # Enhanced component selector
        st.markdown("### 🎯 Explore the ML Pipeline Components")
        
        architecture_options = {
            "Complete ML Pipeline": "End-to-end workflow from data to predictions",
            "Model Ensemble Strategy": "XGBoost + TensorFlow + Random Forest ensemble",
            "AKS Deployment": "Kubernetes auto-scaling and container orchestration",
            "Airflow Orchestration": "Automated training and deployment pipelines",
            "Feature Engineering": "146 sensor features and domain expertise",
            "Model Validation": "Rolling window validation and business metrics"
        }
        
        selected_component = st.selectbox(
            "🔍 Select Architecture Component:",
            list(architecture_options.keys()),
            help="Choose a component to explore its technical implementation"
        )
        
        st.info(f"💡 **{selected_component}**: {architecture_options[selected_component]}")
        
        if selected_component == "Complete ML Pipeline":
            st.markdown("### 🌐 Interactive End-to-End ML Architecture")
            
            # Enhanced pipeline with click interactions
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                pipeline_components = [
                    ("📊 Data Ingestion", "9,247 IoT sensors + maintenance history", "Real-time streaming data"),
                    ("🔄 Feature Engineering", "146 engineered features", "Rolling windows + domain expertise"),
                    ("🤖 Model Ensemble", "XGBoost + TensorFlow + RF", "Weighted voting with 94% accuracy"),
                    ("☁️ AKS Inference", "Auto-scaling prediction service", "3-20 pods based on load"),
                    ("💼 Business Logic", "Cost optimization + crew capacity", "Multi-objective optimization"),
                    ("🚨 Alert Generation", "Risk scoring + prioritization", "87% precision, 100% recall"),
                    ("👥 Crew Optimization", "Schedule with constraints", "34% efficiency improvement")
                ]
                
                for i, (title, subtitle, details) in enumerate(pipeline_components):
                    with st.expander(f"{title} - {subtitle}", expanded=(i == 0)):
                        st.markdown(f"**Technical Details:** {details}")
                        
                        if "Data Ingestion" in title:
                            st.code("""
# Real-time data pipeline
from azure.eventhub import EventHubConsumerClient
import pandas as pd

def process_sensor_data(partition_context, event):
    sensor_data = json.loads(event.body_as_str())
    
    # Parse IoT telemetry
    features = {
        'asset_id': sensor_data['asset_id'],
        'timestamp': sensor_data['timestamp'],
        'vibration_rms': sensor_data['vibration']['rms'],
        'temperature_avg': sensor_data['thermal']['average'],
        'voltage_thd': sensor_data['electrical']['thd'],
        'load_factor': sensor_data['load']['factor']
    }
    
    # Store in time-series database
    store_features(features)
                            """)
                        
                        elif "Model Ensemble" in title:
                            # Model comparison table
                            model_comparison = {
                                "Model": ["XGBoost", "TensorFlow", "Random Forest", "Ensemble"],
                                "Accuracy": ["91.2%", "89.7%", "88.9%", "94.1%"],
                                "Recall": ["97.8%", "100%", "94.2%", "100%"],
                                "Latency (ms)": [23, 31, 18, 24],
                                "Weight": [0.4, 0.35, 0.25, "N/A"]
                            }
                            
                            model_df = pd.DataFrame(model_comparison)
                            st.dataframe(model_df, use_container_width=True)
                            
                            if st.button(f"🔬 Test Model {i}", key=f"test_model_{i}"):
                                with st.spinner("🧪 Running model validation..."):
                                    time.sleep(1)
                                st.success("✅ Validation passed! Model ready for production.")
                        
                        elif "AKS" in title:
                            # Live AKS metrics
                            aks_metrics = {
                                "Metric": ["CPU Usage", "Memory Usage", "Active Pods", "Request Rate"],
                                "Current": ["24%", "67%", "12", "847/min"],
                                "Target": ["70%", "80%", "3-20", "1000/min"],
                                "Status": ["🟢 Normal", "🟡 Medium", "🟢 Optimal", "🟢 Good"]
                            }
                            
                            aks_df = pd.DataFrame(aks_metrics)
                            st.dataframe(aks_df, use_container_width=True)
                            
                            if st.button(f"📈 Scale Up Pods", key=f"scale_{i}"):
                                st.success("⚡ Scaling from 12 to 18 pods...")
            
            # Performance metrics
            st.markdown("### ⚡ Live Pipeline Performance")
            
            perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
            
            with perf_col1:
                latency = random.randint(180, 220)
                st.markdown(f'<div class="model-performance">{latency}ms<br>End-to-End<br>Latency</div>', unsafe_allow_html=True)
                
            with perf_col2:
                throughput = random.randint(840, 880)
                st.markdown(f'<div class="model-performance">{throughput}/min<br>Prediction<br>Throughput</div>', unsafe_allow_html=True)
                
            with perf_col3:
                accuracy = random.uniform(93.8, 94.5)
                st.markdown(f'<div class="model-performance">{accuracy:.1f}%<br>Model<br>Accuracy</div>', unsafe_allow_html=True)
                
            with perf_col4:
                uptime = random.uniform(99.7, 99.9)
                st.markdown(f'<div class="model-performance">{uptime:.1f}%<br>System<br>Uptime</div>', unsafe_allow_html=True)
        
        elif selected_component == "Model Ensemble Strategy":
            st.markdown("### 🤖 Interactive Ensemble Model Analysis")
            
            # Model configuration interface
            model_col1, model_col2 = st.columns(2)
            
            with model_col1:
                st.markdown("**🎛️ Ensemble Configuration:**")
                
                xgb_weight = st.slider("XGBoost Weight", 0.0, 1.0, 0.4, 0.05)
                tf_weight = st.slider("TensorFlow Weight", 0.0, 1.0, 0.35, 0.05)
                rf_weight = st.slider("Random Forest Weight", 0.0, 1.0, 0.25, 0.05)
                
                total_weight = xgb_weight + tf_weight + rf_weight
                if abs(total_weight - 1.0) > 0.01:
                    st.warning(f"⚠️ Weights sum to {total_weight:.2f}, should equal 1.0")
                else:
                    st.success("✅ Weight configuration valid")
                
                if st.button("🧪 Test Ensemble Configuration"):
                    with st.spinner("🔄 Training ensemble with new weights..."):
                        time.sleep(2)
                    
                    # Simulate performance based on weights
                    estimated_accuracy = (0.912 * xgb_weight + 0.897 * tf_weight + 0.889 * rf_weight)
                    estimated_recall = (0.978 * xgb_weight + 1.000 * tf_weight + 0.942 * rf_weight)
                    
                    st.success(f"🎯 Estimated Performance:")
                    st.write(f"• Accuracy: {estimated_accuracy:.1%}")
                    st.write(f"• Recall: {estimated_recall:.1%}")
            
            with model_col2:
                st.markdown("**📊 Model Performance Comparison:**")
                
                # Simple bar chart using Streamlit
                performance_data = pd.DataFrame({
                    'Model': ['XGBoost', 'TensorFlow', 'Random Forest'],
                    'Accuracy': [91.2, 89.7, 88.9],
                    'Recall': [97.8, 100.0, 94.2]
                })
                
                st.bar_chart(performance_data.set_index('Model'))
                
                st.markdown("**🏆 Ensemble Advantages:**")
                st.write("• XGBoost: Best overall accuracy")
                st.write("• TensorFlow: Perfect recall (100%)")
                st.write("• Random Forest: Fastest inference")
                st.write("• **Ensemble: Best of all worlds**")
        
        # Enhanced technology stack
        st.markdown("---")
        st.markdown("### 🛠️ Interactive Technology Stack")
        
        tech_categories = {
            "🤖 ML Frameworks": {
                "technologies": ["XGBoost 1.7", "TensorFlow 2.8", "scikit-learn 1.1", "Pandas 1.5"],
                "description": "Production ML libraries with GPU acceleration"
            },
            "☁️ Cloud Infrastructure": {
                "technologies": ["Azure AKS", "Container Registry", "Azure Storage", "Virtual Networks"],
                "description": "Scalable Kubernetes infrastructure"
            },
            "🔄 MLOps Pipeline": {
                "technologies": ["Apache Airflow 2.4", "Azure DevOps", "Helm Charts", "Terraform"],
                "description": "Automated deployment and orchestration"
            },
            "📊 Monitoring": {
                "technologies": ["Grafana", "Prometheus", "App Insights", "Log Analytics"],
                "description": "Full-stack monitoring and alerting"
            },
            "🗄️ Data Platform": {
                "technologies": ["Event Hubs", "Cosmos DB", "Data Factory", "Time Series Insights"],
                "description": "Real-time data ingestion and storage"
            },
            "🔧 DevOps & Security": {
                "technologies": ["Azure DevOps", "Key Vault", "RBAC", "Container Security"],
                "description": "Secure development and deployment"
            }
        }
        
        # Create interactive grid
        cols = st.columns(3)
        for i, (category, details) in enumerate(tech_categories.items()):
            with cols[i % 3]:
                with st.expander(f"{category}", expanded=False):
                    st.markdown(f"**Description:** {details['description']}")
                    st.markdown("**Technologies:**")
                    for tech in details['technologies']:
                        st.markdown(f"• {tech}")
                    
                    if st.button(f"📋 View Config", key=f"config_{i}"):
                        st.code(f"""
# {category} Configuration
version: "1.0"
technologies: {details['technologies']}
deployment: production
auto_scaling: enabled
monitoring: comprehensive
                        """)
    
    with tab3:
        st.markdown("## 📈 Interactive Business Impact & ROI Analysis")
        
        # Enhanced financial metrics
        st.markdown("### 💰 Real-Time Financial Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Generate dynamic metrics
        annual_savings = random.randint(2200000, 2400000)
        downtime_reduction = random.randint(75, 82)
        crew_efficiency = random.randint(32, 37)
        alert_precision = random.randint(86, 91)
        
        with col1:
            st.metric(
                "Annual Savings", 
                f"${annual_savings:,}", 
                f"+${random.randint(15000, 25000):,} this month",
                help="Total operational cost avoidance"
            )
            
        with col2:
            st.metric(
                "Downtime Reduction", 
                f"{downtime_reduction}%", 
                f"+{random.randint(1,3)}% vs baseline",
                help="Reduction in equipment downtime"
            )
            
        with col3:
            st.metric(
                "Crew Efficiency", 
                f"+{crew_efficiency}%", 
                f"+{random.randint(1,2)}% this quarter",
                help="Improvement in crew productivity"
            )
            
        with col4:
            st.metric(
                "Alert Precision", 
                f"{alert_precision}%", 
                f"+{random.randint(2,4)}% improvement",
                help="Percentage of alerts leading to actual issues"
            )
        
        # Cost savings breakdown
        st.markdown("### 💡 Cost Savings Analysis")
        
        cost_breakdown = pd.DataFrame({
            'Category': ['Equipment Replacement', 'Emergency Repairs', 'Crew Optimization', 'Outage Prevention', 'Insurance'],
            'Annual Savings': [1200000, 580000, 340000, 150000, 30000],
            'Percentage': [52.2, 25.2, 14.8, 6.5, 1.3]
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.bar_chart(cost_breakdown.set_index('Category')['Annual Savings'])
            
        with col2:
            st.markdown("**💡 Cost Driver Analysis:**")
            for _, row in cost_breakdown.iterrows():
                st.markdown(f"**{row['Category']}**")
                st.progress(row['Percentage'] / 100)
                st.caption(f"${row['Annual Savings']:,} ({row['Percentage']:.1f}%)")
        
        # Interactive ROI projection
        st.markdown("### 📊 Interactive ROI Calculator")
        
        proj_col1, proj_col2, proj_col3 = st.columns(3)
        
        with proj_col1:
            implementation_cost = st.slider("Implementation Cost ($K)", 500, 1500, 825)
            
        with proj_col2:
            monthly_savings = st.slider("Monthly Savings ($K)", 150, 250, 190)
            
        with proj_col3:
            projection_months = st.slider("Projection Period (months)", 12, 36, 24)
        
        # Calculate and display ROI
        months = list(range(1, projection_months + 1))
        cumulative_savings = [month * monthly_savings for month in months]
        net_benefit = [savings - implementation_cost for savings in cumulative_savings]
        
        roi_data = pd.DataFrame({
            'Month': months,
            'Cumulative Savings': cumulative_savings,
            'Net Benefit': net_benefit
        })
        
        st.line_chart(roi_data.set_index('Month')[['Cumulative Savings', 'Net Benefit']])
        
        # Find break-even
        break_even_month = None
        for i, benefit in enumerate(net_benefit):
            if benefit > 0:
                break_even_month = i + 1
                break
        
        if break_even_month:
            final_roi = (net_benefit[-1] / implementation_cost) * 100
            st.success(f"💡 **Break-even Point**: Month {break_even_month} | **{projection_months}-Month ROI**: {final_roi:.0f}%")
        
        # Asset impact analysis
        st.markdown("### ⚙️ Asset-Specific Impact")
        
        asset_impact = pd.DataFrame({
            'Asset Type': ['Transformers', 'Circuit Breakers', 'Power Lines', 'Substations', 'Generators'],
            'Failure Rate Reduction (%)': [67, 52, 43, 71, 58],
            'Avg Cost per Failure ($)': [125000, 45000, 35000, 180000, 95000],
            'Annual Failures Prevented': [18, 31, 22, 8, 12]
        })
        
        st.dataframe(asset_impact, use_container_width=True)
        
        # Operational transformation
        st.markdown("### 👥 Operational Transformation")
        
        before_after = pd.DataFrame({
            'Metric': ['Service Interruptions', 'Emergency Callouts', 'Crew Overtime', 'Customer Complaints', 'Safety Incidents'],
            'Before ML (Annual)': [147, 1068, 14880, 804, 12],
            'After ML (Annual)': [32, 276, 9840, 216, 2],
            'Improvement (%)': [78, 74, 34, 73, 83]
        })
        
        st.dataframe(before_after, use_container_width=True)
        
        st.info("💡 **Key Success Factor**: Feature calibration with business cost framing eliminated alert fatigue while maintaining 100% recall for critical failures")
    
    with tab4:
        st.markdown("## ⚙️ Technical Deep Dive & Implementation")
        
        # Enhanced Eversource applications
        st.markdown("### 🏢 Eversource Grid Modernization Applications")
        
        eversource_tabs = st.tabs(["🔌 Transmission", "🏠 Distribution", "⛈️ Resilience", "🌿 Renewables"])
        
        with eversource_tabs[0]:
            st.markdown("**230kV+ Transmission Infrastructure**")
            st.markdown("""
            - **High-voltage asset monitoring**: Critical backbone infrastructure serving 1.2M+ customers
            - **Bulk power system reliability**: ISO-NE compliance and grid stability requirements  
            - **Transmission line health**: Weather impact assessment and aging infrastructure management
            - **Substation automation**: SCADA integration and remote monitoring capabilities
            """)
            
            if st.button("🔍 Analyze Transmission Assets"):
                st.success("⚡ Found 23 transmission assets requiring priority maintenance")
                
        with eversource_tabs[1]:
            st.markdown("**4-35kV Distribution Network**")
            st.markdown("""
            - **Distribution transformer monitoring**: Residential and commercial service optimization
            - **Feeder automation**: Smart grid capabilities and self-healing networks
            - **Underground cable health**: Urban infrastructure in Connecticut's dense areas
            - **Load balancing**: Peak demand management and grid efficiency
            """)
            
        with eversource_tabs[2]:
            st.markdown("**Storm Hardening & Coastal Resilience**") 
            st.markdown("""
            - **Weather impact modeling**: Hurricane and Nor'easter preparation strategies
            - **Salt corrosion analysis**: Coastal Connecticut asset degradation patterns
            - **Flood resilience**: Climate change adaptation for critical infrastructure
            - **Emergency restoration**: Optimized crew deployment during major events
            """)
            
        with eversource_tabs[3]:
            st.markdown("**Clean Energy Integration**")
            st.markdown("""
            - **Solar interconnection**: Distributed generation impact on grid stability
            - **Wind integration**: Offshore wind preparation and grid modernization
            - **Energy storage**: Battery system integration and grid balancing
            - **Smart meters**: AMI data integration for predictive analytics
            """)
        
        st.markdown("---")
        
        # Feature engineering section
        st.markdown("### 🔬 Feature Engineering Laboratory")
        
        feature_tabs = st.tabs(["📊 Sensor Features", "⚙️ Maintenance Features", "💼 Business Features"])
        
        with feature_tabs[0]:
            st.markdown("**IoT Sensor Feature Categories (146 total features)**")
            
            sensor_categories = {
                "Vibration Analysis": ["RMS amplitude", "Peak frequency", "Harmonic content", "Bearing signatures"],
                "Thermal Monitoring": ["Hot spot temperature", "Gradient analysis", "Thermal imaging", "Ambient correlation"],
                "Electrical Parameters": ["Voltage THD", "Current unbalance", "Power factor", "Partial discharge"],
                "Environmental Factors": ["Humidity impact", "Wind loading", "Temperature cycling", "UV exposure"],
                "Load Characteristics": ["Demand patterns", "Peak ratios", "Load factor", "Cycling frequency"]
            }
            
            for category, features in sensor_categories.items():
                with st.expander(f"🔍 {category}", expanded=False):
                    for feature in features:
                        st.write(f"• {feature}")
                    
                    if st.button(f"📈 Generate Sample Data", key=f"sensor_{category}"):
                        # Generate sample feature data
                        sample_data = pd.DataFrame({
                            'Hour': range(24),
                            'Feature Value': np.random.normal(50, 10, 24) + np.sin(np.linspace(0, 2*np.pi, 24)) * 5
                        })
                        st.line_chart(sample_data.set_index('Hour')['Feature Value'])
        
        with feature_tabs[1]:
            st.markdown("**Maintenance History Feature Engineering**")
            
            st.code("""
# Advanced maintenance feature engineering
def create_maintenance_features(maintenance_history):
    features = {}
    
    # Temporal patterns
    features['days_since_last_maintenance'] = calculate_days_since(maintenance_history)
    features['maintenance_frequency_12m'] = count_maintenance_events(maintenance_history, 365)
    features['seasonal_maintenance_pattern'] = encode_seasonal_patterns(maintenance_history)
    
    # Cost and severity patterns
    features['avg_maintenance_cost_trend'] = calculate_cost_trend(maintenance_history, window=6)
    features['maintenance_type_severity'] = encode_severity_scores(maintenance_history)
    features['escalating_issues_pattern'] = detect_escalation_patterns(maintenance_history)
    
    return features
            """)
            
        with feature_tabs[2]:
            st.markdown("**Business Context Integration**")
            
            business_features = {
                "Asset Criticality": "Grid topology importance scoring",
                "Customer Impact": "Downstream customer count and priority",
                "Replacement Cost": "Current asset valuation and replacement timeline",
                "Regulatory Impact": "NERC CIP compliance and reporting requirements",
                "Crew Availability": "Resource constraints and skill matching",
                "Economic Factors": "Load growth, rate structures, and ROI calculations"
            }
            
            for feature, description in business_features.items():
                st.markdown(f"**{feature}**: {description}")
        
        # Production infrastructure
        st.markdown("### 🚀 Production Infrastructure")
        
        infra_
