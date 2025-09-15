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
    }
    
    .asset-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .high-risk {
        border-left-color: #dc3545 !important;
        background: linear-gradient(135deg, #fff5f5, #ffe6e6);
    }
    
    .medium-risk {
        border-left-color: #ffc107 !important;
        background: linear-gradient(135deg, #fffdf5, #fff9e6);
    }
    
    .low-risk {
        border-left-color: #28a745 !important;
        background: linear-gradient(135deg, #f5fff5, #e6ffe6);
    }
    
    .dashboard-container {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
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
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }
    
    .risk-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .risk-high { background-color: #dc3545; animation: blink-red 2s infinite; }
    .risk-medium { background-color: #ffc107; }
    .risk-low { background-color: #28a745; }
    
    @keyframes blink-red {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.5; }
    }
    
    .model-performance {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
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
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }
    
    .flow-arrow {
        text-align: center;
        font-size: 2.5rem;
        color: #ff6b35;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
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
    }
    
    .tech-stack-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .tech-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        border-top: 4px solid #ff6b35;
    }
    
    .tech-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .live-status {
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.2rem 0;
        animation: pulse-glow 3s infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 5px rgba(255,107,53,0.5); }
        50% { box-shadow: 0 0 20px rgba(255,107,53,0.8); }
    }
    
    .crew-schedule {
        background: linear-gradient(135deg, #6f42c1, #6610f2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate realistic asset data
def generate_asset_data():
    asset_types = ["Transformer", "Circuit Breaker", "Power Line", "Substation", "Generator", "Switch Gear"]
    locations = ["North Grid", "South Grid", "East Grid", "West Grid", "Central Hub"]
    
    assets = []
    for i in range(50):  # Show subset of 9000+ assets
        failure_prob = random.uniform(0.01, 0.95)
        if failure_prob > 0.85:
            risk_level = "High"
            risk_color = "high-risk"
        elif failure_prob > 0.5:
            risk_level = "Medium" 
            risk_color = "medium-risk"
        else:
            risk_level = "Low"
            risk_color = "low-risk"
            
        assets.append({
            "Asset ID": f"AST-{random.randint(1000, 9999)}",
            "Type": random.choice(asset_types),
            "Location": random.choice(locations),
            "Failure Probability": failure_prob,
            "Risk Level": risk_level,
            "Risk Color": risk_color,
            "Last Maintenance": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "Expected Cost": random.randint(5000, 150000),
            "Crew Priority": random.randint(1, 10)
        })
    
    return sorted(assets, key=lambda x: x["Failure Probability"], reverse=True)

# Generate model performance data
def generate_model_metrics():
    return {
        "Ensemble Model Accuracy": 0.94,
        "Recall (Failure Detection)": 1.00,  # 100% recall as mentioned
        "Precision": 0.87,
        "F1 Score": 0.93,
        "Assets Monitored": 9247,
        "High Risk Identified": 146,
        "False Positive Rate": 0.13,
        "Model Confidence": 0.91
    }

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
                <div style="font-size: 2rem;">🤖</div>
                <div>100% Recall</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Failure Detection</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">⚙️</div>
                <div>146 Assets</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">High Risk Identified</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">💰</div>
                <div>$2.3M Savings</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Potential Annual</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">☁️</div>
                <div>AKS Deployment</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Auto-scaling ML</div>
            </div>
        </div>
        <p style="margin-top: 2rem; font-style: italic;">
            Experience how AI transforms grid maintenance from reactive to predictive operations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with live system status
    with st.sidebar:
        st.markdown("## 🔧 System Status")
        
        # Live model performance
        st.markdown("### 🤖 ML Models")
        model_metrics = generate_model_metrics()
        
        st.markdown('<div class="live-status">📊 Ensemble Active</div>', unsafe_allow_html=True)
        st.caption("XGBoost + TensorFlow + scikit-learn")
        
        st.metric("Model Accuracy", f"{model_metrics['Ensemble Model Accuracy']:.0%}")
        st.metric("Recall Rate", f"{model_metrics['Recall (Failure Detection)']:.0%}", "🎯 Perfect")
        st.metric("Assets Monitored", f"{model_metrics['Assets Monitored']:,}")
        
        # Live infrastructure
        st.markdown("### ☁️ AKS Infrastructure")
        st.markdown('<div class="live-status">🚀 Pods Running: 12/12</div>', unsafe_allow_html=True)
        st.markdown('<div class="live-status">📈 CPU: 23%</div>', unsafe_allow_html=True)
        st.markdown('<div class="live-status">💾 Memory: 67%</div>', unsafe_allow_html=True)
        
        # Airflow DAGs
        st.markdown("### 🔄 Airflow Orchestration")
        st.markdown('<div class="live-status">✅ Daily Retrain DAG</div>', unsafe_allow_html=True)
        st.markdown('<div class="live-status">✅ Data Pipeline DAG</div>', unsafe_allow_html=True)
        st.markdown('<div class="live-status">✅ Alert Generation DAG</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Refresh Status"):
            st.rerun()

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Live Dashboard", "🏗️ ML Architecture", "📈 Business Impact", "⚙️ Technical Deep Dive"])
    
    with tab1:
        st.markdown("## 🚨 Real-Time Asset Monitoring Dashboard")
        
        # Control panel
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("### 📊 System Overview")
            
        with col2:
            if st.button("🔍 Run Prediction Scan"):
                with st.spinner("🤖 Running ML inference on all assets..."):
                    time.sleep(2)
                st.success("✅ Scan complete! 3 new high-risk assets identified.")
                
        with col3:
            if st.button("📋 Generate Crew Schedule"):
                with st.spinner("🔄 Optimizing crew assignments..."):
                    time.sleep(1.5)
                st.success("✅ Schedule optimized for next 7 days.")
        
        # Key metrics dashboard
        st.markdown("### ⚡ Live Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">🎯<br><strong>146</strong><br>High Risk Assets</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">⚙️<br><strong>9,247</strong><br>Assets Monitored</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-card">👥<br><strong>23</strong><br>Crews Available</div>', unsafe_allow_html=True)
            
        with col4:
            st.markdown('<div class="metric-card">💰<br><strong>$487K</strong><br>Failures Prevented</div>', unsafe_allow_html=True)
        
        # Risk distribution
        st.markdown("### 🎯 Risk Distribution")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Generate and display top risky assets
            assets = generate_asset_data()
            high_risk_assets = [a for a in assets if a["Risk Level"] == "High"][:10]
            
            st.markdown("**🚨 Top Priority Assets for Maintenance:**")
            
            for asset in high_risk_assets:
                risk_class = "risk-high" if asset["Risk Level"] == "High" else "risk-medium" if asset["Risk Level"] == "Medium" else "risk-low"
                
                st.markdown(f'''
                <div class="asset-card {asset["Risk Color"]}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="risk-indicator {risk_class}"></span>
                            <strong>{asset["Asset ID"]}</strong> - {asset["Type"]}
                            <br><small>📍 {asset["Location"]} | Last Maintenance: {asset["Last Maintenance"]}</small>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.2rem; font-weight: bold; color: #dc3545;">
                                {asset["Failure Probability"]:.1%}
                            </div>
                            <div style="font-size: 0.9rem;">
                                ${asset["Expected Cost"]:,}
                            </div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📈 Risk Breakdown**")
            
            total_assets = len(assets)
            high_risk_count = len([a for a in assets if a["Risk Level"] == "High"])
            medium_risk_count = len([a for a in assets if a["Risk Level"] == "Medium"])
            low_risk_count = len([a for a in assets if a["Risk Level"] == "Low"])
            
            st.metric("🔴 High Risk", f"{high_risk_count}", f"{high_risk_count/total_assets:.1%} of total")
            st.metric("🟡 Medium Risk", f"{medium_risk_count}", f"{medium_risk_count/total_assets:.1%} of total")
            st.metric("🟢 Low Risk", f"{low_risk_count}", f"{low_risk_count/total_assets:.1%} of total")
            
            # Alert system
            st.markdown("**🚨 Active Alerts**")
            st.markdown('<div class="alert-banner">⚠️ 3 Critical Failures Predicted</div>', unsafe_allow_html=True)
            st.markdown('<div class="cost-savings">💰 $156K Failure Cost Avoided</div>', unsafe_allow_html=True)
        
        # Crew scheduling optimization
        st.markdown("### 👥 Optimized Crew Scheduling")
        
        crew_data = {
            "Crew ID": ["Crew-A", "Crew-B", "Crew-C", "Crew-D", "Crew-E"],
            "Current Assignment": ["Transformer T-4521", "Circuit Breaker CB-891", "Available", "Power Line PL-334", "Substation SS-12"],
            "Next Priority Asset": ["AST-8847", "AST-9234", "AST-7721", "AST-6654", "AST-5443"],
            "Estimated Completion": ["2 hours", "4 hours", "Ready", "6 hours", "3 hours"],
            "Efficiency Score": ["94%", "87%", "91%", "89%", "96%"]
        }
        
        crew_df = pd.DataFrame(crew_data)
        st.dataframe(crew_df, use_container_width=True)
        
        # Real-time model predictions
        st.markdown("### 🤖 Live ML Predictions")
        
        if st.button("🎯 Show Latest Model Output"):
            with st.spinner("🔄 Fetching latest model predictions..."):
                time.sleep(1)
            
            st.code("""
            📊 Latest Ensemble Model Predictions (Last Run: 14:23:47)
            
            🎯 XGBoost Model: 0.891 accuracy | 0.945 recall
            🧠 TensorFlow NN: 0.887 accuracy | 1.000 recall  
            📈 scikit-learn: 0.882 accuracy | 0.987 recall
            
            🔥 ENSEMBLE OUTPUT: 0.940 accuracy | 1.000 recall
            
            ⚠️  HIGH PRIORITY PREDICTIONS:
            • AST-8847: 94.2% failure risk (Transformer)
            • AST-9234: 91.7% failure risk (Circuit Breaker)  
            • AST-7721: 89.3% failure risk (Power Line)
            
            💡 Feature Importance:
            1. Vibration_Amplitude: 0.234
            2. Temperature_Delta: 0.198  
            3. Load_Factor: 0.167
            4. Maintenance_Age: 0.143
            """)
    
    with tab2:
        st.markdown("## 🏗️ ML Architecture & Infrastructure")
        
        # Architecture selector
        st.markdown("### 🎯 Explore the ML Pipeline")
        
        selected_component = st.selectbox(
            "🔍 Deep Dive into Architecture Components:",
            ["Complete ML Pipeline", "Model Ensemble Strategy", "AKS Deployment", "Airflow Orchestration", "Feature Engineering", "Model Validation"],
            help="Select a component to explore its technical implementation"
        )
        
        if selected_component == "Complete ML Pipeline":
            st.markdown("### 🌐 End-to-End ML Architecture")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                pipeline_steps = [
                    ("📊 Data Ingestion", "9,247 IoT sensors + historical maintenance"),
                    ("🔄 Feature Engineering", "Rolling windows + domain expertise"),
                    ("🤖 Model Ensemble", "XGBoost + TensorFlow + scikit-learn"),
                    ("☁️ AKS Inference", "Auto-scaling prediction service"),
                    ("📈 Business Logic", "Cost optimization + crew capacity"),
                    ("🚨 Alert Generation", "Risk scoring + maintenance prioritization"),
                    ("👥 Crew Optimization", "Schedule optimization with constraints")
                ]
                
                for title, subtitle in pipeline_steps:
                    st.markdown(f'''
                    <div class="pipeline-step">
                        <strong>{title}</strong><br>
                        <small style="opacity: 0.8;">{subtitle}</small>
                    </div>
                    ''', unsafe_allow_html=True)
                    if title != pipeline_steps[-1][0]:
                        st.markdown('<div class="flow-arrow">⬇️</div>', unsafe_allow_html=True)
            
            # Performance metrics
            st.markdown("### ⚡ Pipeline Performance")
            perf_cols = st.columns(4)
            
            performance_metrics = [
                ("< 5min", "Model Inference"),
                ("100%", "Recall Rate"),
                ("94%", "Accuracy"),
                ("Auto-scale", "AKS Pods")
            ]
            
            for i, (value, label) in enumerate(performance_metrics):
                with perf_cols[i]:
                    st.markdown(f'<div class="model-performance">{value}<br><small>{label}</small></div>', unsafe_allow_html=True)
        
        elif selected_component == "Model Ensemble Strategy":
            st.markdown("### 🤖 Ensemble Model Architecture")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎯 Model Configuration:**")
                st.code("""
# Ensemble Model Setup
models = {
    'xgboost': {
        'n_estimators': 500,
        'max_depth': 8,
        'learning_rate': 0.1,
        'objective': 'binary:logistic'
    },
    'tensorflow': {
        'layers': [256, 128, 64, 32],
        'dropout': 0.3,
        'activation': 'relu',
        'optimizer': 'adam'
    },
    'sklearn_rf': {
        'n_estimators': 300,
        'max_depth': 15,
        'min_samples_split': 5
    }
}

# Ensemble Strategy: Weighted Voting
weights = [0.4, 0.35, 0.25]  # XGB, TF, RF
final_prediction = weighted_average(predictions)
                """)
            
            with col2:
                st.markdown("**📊 Individual Model Performance:**")
                
                model_performance = {
                    "Model": ["XGBoost", "TensorFlow NN", "Random Forest", "**Ensemble**"],
                    "Accuracy": ["89.1%", "88.7%", "88.2%", "**94.0%**"],
                    "Recall": ["94.5%", "100.0%", "98.7%", "**100.0%**"],
                    "Precision": ["84.2%", "83.1%", "85.6%", "**87.3%**"],
                    "F1-Score": ["89.2%", "90.8%", "91.8%", "**93.2%**"]
                }
                
                model_df = pd.DataFrame(model_performance)
                st.dataframe(model_df, use_container_width=True)
                
                st.success("🎯 **Key Insight**: Ensemble achieves 100% recall through complementary model strengths")
        
        elif selected_component == "AKS Deployment":
            st.markdown("### ☁️ Azure Kubernetes Service Architecture")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🚀 Kubernetes Configuration:**")
                st.code("""
# ML Inference Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: predictive-maintenance
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: ml-api
        image: acr.io/pred-maint:v2.1
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2
            memory: 4Gi
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: ml-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
                """)
            
            with col2:
                st.markdown("**📊 AKS Cluster Metrics:**")
                
                aks_metrics = {
                    "Resource": ["Nodes", "Pods", "CPU Usage", "Memory Usage", "Storage", "Network"],
                    "Current": ["4", "12", "23%", "67%", "2.1TB", "1.2GB/s"],
                    "Capacity": ["6", "24", "100%", "100%", "5TB", "10GB/s"],
                    "Status": ["✅ Healthy", "✅ Running", "🟢 Normal", "🟡 Medium", "🟢 Available", "🟢 Normal"]
                }
                
                aks_df = pd.DataFrame(aks_metrics)
                st.dataframe(aks_df, use_container_width=True)
                
                # Auto-scaling simulation
                if st.button("🔄 Simulate Load Spike"):
                    with st.spinner("📈 Triggering horizontal pod autoscaler..."):
                        time.sleep(2)
                    st.success("✅ Scaled from 3 to 8 pods in 45 seconds!")
        
        elif selected_component == "Airflow Orchestration":
            st.markdown("### 🔄 Airflow DAG Architecture")
            
            st.markdown("**📋 Daily Model Retrain DAG:**")
            st.code("""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'predictive_maintenance_retrain',
    default_args=default_args,
    description='Daily model retraining pipeline',
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False
)

# DAG Tasks
extract_data = PythonOperator(
    task_id='extract_sensor_data',
    python_callable=extract_iot_data,
    dag=dag
)

feature_engineering = PythonOperator(
    task_id='feature_engineering',
    python_callable=create_features,
    dag=dag
)

train_ensemble = PythonOperator(
    task_id='train_models',
    python_callable=train_ensemble_models,
    dag=dag
)

validate_model = PythonOperator(
    task_id='validate_performance',
    python_callable=rolling_window_validation,
    dag=dag
)

deploy_model = PythonOperator(
    task_id='deploy_to_aks',
    python_callable=deploy_to_kubernetes,
    dag=dag
)

# Task Dependencies
extract_data >> feature_engineering >> train_ensemble >> validate_model >> deploy_model
            """)
            
            # DAG status simulation
            st.markdown("**📊 Current DAG Status:**")
            dag_status = {
                "Task": ["extract_sensor_data", "feature_engineering", "train_models", "validate_performance", "deploy_to_aks"],
                "Status": ["✅ Success", "✅ Success", "🔄 Running", "⏳ Queued", "⏳ Queued"],
                "Duration": ["2m 34s", "8m 12s", "15m 23s", "-", "-"],
                "Start Time": ["02:00:15", "02:02:49", "02:11:01", "-", "-"]
            }
            
            dag_df = pd.DataFrame(dag_status)
            st.dataframe(dag_df, use_container_width=True)
        
        # Technology stack overview
        st.markdown("---")
        st.markdown("### 🛠️ Technology Stack")
        
        st.markdown('<div class="tech-stack-grid">', unsafe_allow_html=True)
        
        tech_components = [
            ("🤖 ML Frameworks", "XGBoost 1.7\nTensorFlow 2.8\nscikit-learn 1.1"),
            ("☁️ Infrastructure", "Azure AKS\nAzure Container Registry\nAzure Storage"),
            ("🔄 Orchestration", "Apache Airflow 2.4\nKubernetes 1.24\nHelm Charts"),
            ("📊 Monitoring", "Grafana\nPrometheus\nApplication Insights"),
            ("🗄️ Data Pipeline", "Azure Data Factory\nEvent Hubs\nCosmos DB"),
            ("🔧 DevOps", "Azure DevOps\nTerraform\nDocker")
        ]
        
        for title, technologies in tech_components:
            st.markdown(f'''
            <div class="tech-card">
                <h4>{title}</h4>
                <div style="font-size: 0.9rem; line-height: 1.6; color: #666;">
                    {technologies.replace(chr(10), "<br>")}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("## 📈 Business Impact & ROI Analysis")
        
        # Enhanced business metrics
        st.markdown("### 💰 Financial Impact")
        
        col1, col2, col3, col4 = st.columns(4)
        
        business_metrics = [
            ("Potential Annual Savings", "$2.3M", "Failure prevention", "Total operational cost avoidance"),
            ("Equipment Downtime Reduction", "78%", "Faster response", "Proactive vs reactive maintenance"),
            ("Crew Efficiency Improvement", "34%", "Optimized scheduling", "Better resource allocation"),
            ("Alert Fatigue Elimination", "89%", "Precise targeting", "High-confidence predictions only")
        ]
        
        for i, (label, value, delta, help_text) in enumerate(business_metrics):
            with [col1, col2, col3, col4][i]:
                st.metric(label, value, delta, help=help_text)
        
        # Detailed cost breakdown
        st.markdown("### 💡 Cost Savings Breakdown")
        
        cost_data = {
            "Category": ["Equipment Replacement Avoidance", "Reduced Emergency Repairs", "Optimized Crew Scheduling", "Prevented Service Outages", "Lower Insurance Claims"],
            "Annual Savings": ["$1,200,000", "$580,000", "$340,000", "$150,000", "$30,000"],
            "Impact": ["Prevent catastrophic failures", "Proactive maintenance", "Efficient resource use", "Customer satisfaction", "Risk reduction"],
            "Confidence": ["High", "High", "Medium", "Medium", "Low"]
        }
        
        cost_df = pd.DataFrame(cost_data)
        st.dataframe(cost_df, use_container_width=True)
        
        # ROI timeline
        st.markdown("### 📊 ROI Timeline")
        
        roi_timeline = {
            "Quarter": ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025"],
            "Implementation Cost": ["$450K", "$200K", "$100K", "$50K", "$25K"],
            "Savings Realized": ["$180K", "$420K", "$650K", "$780K", "$920K"],
            "Cumulative ROI": ["-60%", "-12%", "+47%", "+89%", "+134%"],
            "Failures Prevented": ["12", "28", "41", "52", "63"]
        }
        
        roi_df = pd.DataFrame(roi_timeline)
        st.dataframe(roi_df, use_container_width=True)
        
        st.success("💡 **Break-even Point**: Q3 2024 | **12-Month ROI**: 134%")
        
        # Asset impact analysis
        st.markdown("### ⚙️ Asset-Specific Impact")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 High-Impact Asset Types:**")
            
            asset_impact = {
                "Asset Type": ["Transformers", "Circuit Breakers", "Power Lines", "Substations", "Generators"],
                "Failure Rate Reduction": ["67%", "52%", "43%", "71%", "58%"],
                "Avg Cost per Failure": ["$125K", "$45K", "$35K", "$180K", "$95K"],
                "Annual Failures Prevented": ["18", "31", "22", "8", "12"]
            }
            
            asset_df = pd.DataFrame(asset_impact)
            st.dataframe(asset_df, use_container_width=True)
        
        with col2:
            st.markdown("**📈 Performance Trends:**")
            
            # Show key insights
            insights = [
                "🎯 **Alert Precision**: 87% of alerts lead to actual issues found",
                "⚡ **Response Time**: 34% faster crew deployment to critical assets",
                "💰 **Cost Accuracy**: Predicted failure costs within 12% of actual",
                "📊 **Model Drift**: <3% monthly performance degradation",
                "🔄 **Retrain Frequency**: Weekly retraining maintains 94%+ accuracy"
            ]
            
            for insight in insights:
                st.markdown(insight)
            
            st.info("💡 **Key Success Factor**: Feature calibration with business cost framing eliminated alert fatigue")
        
        # Customer impact
        st.markdown("### 👥 Operational Impact")
        
        operational_data = {
            "Metric": ["Service Interruptions", "Emergency Callouts", "Crew Overtime Hours", "Customer Complaints", "Regulatory Incidents"],
            "Before ML": ["147/year", "89/month", "1,240/month", "67/month", "3/year"],
            "After ML": ["32/year", "23/month", "820/month", "18/month", "0/year"],
            "Improvement": ["78% reduction", "74% reduction", "34% reduction", "73% reduction", "100% reduction"]
        }
        
        operational_df = pd.DataFrame(operational_data)
        st.dataframe(operational_df, use_container_width=True)
    
    with tab4:
        st.markdown("## ⚙️ Technical Deep Dive")
        
        # Eversource-specific applications
        st.markdown("### 🏢 Eversource Grid Applications")
        
        eversource_use_cases = {
            "🔌 Transmission Grid": "230kV+ transmission line monitoring and failure prediction for critical backbone infrastructure",
            "🏭 Distribution Network": "4-35kV distribution equipment optimization for residential and commercial customers",
            "⛈️ Storm Hardening": "Weather-resilient equipment identification and targeted reinforcement strategies",
            "🌊 Coastal Resilience": "Salt corrosion and storm surge impact modeling for coastal Connecticut operations",
            "🌿 Green Energy Integration": "Solar/wind integration equipment stress analysis and maintenance optimization",
            "📋 Regulatory Compliance": "ISO-NE reliability standards and NERC CIP compliance through predictive maintenance"
        }
        
        for category, description in eversource_use_cases.items():
            st.markdown(f"**{category}**: {description}")
        
        st.markdown("---")
        
        # Feature engineering deep dive
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔬 Feature Engineering Strategy")
            
            with st.expander("**Sensor Data Features**", expanded=False):
                st.code("""
# IoT Sensor Features (146 total)
sensors = {
    'vibration': ['amplitude', 'frequency', 'acceleration'],
    'thermal': ['temperature', 'gradient', 'hot_spots'],
    'electrical': ['voltage', 'current', 'power_factor'],
    'environmental': ['humidity', 'precipitation', 'wind'],
    'load': ['demand', 'peak_ratio', 'variability']
}

# Rolling window aggregations
for sensor in sensors:
    features[f'{sensor}_7d_mean'] = rolling_mean(sensor, 7)
    features[f'{sensor}_30d_std'] = rolling_std(sensor, 30)
    features[f'{sensor}_trend'] = linear_trend(sensor, 14)
                """)
            
            with st.expander("**Maintenance History Features**", expanded=False):
                st.code("""
# Maintenance-derived features
maintenance_features = {
    'days_since_last_maintenance': days_since_event,
    'maintenance_frequency': count_last_year,
    'maintenance_type_severity': severity_score,
    'repair_cost_trend': cost_regression,
    'failure_history': failure_count_5year,
    'seasonal_maintenance_pattern': seasonal_encoding
}

# Business context features
business_features = {
    'criticality_score': grid_importance_rating,
    'replacement_cost': asset_value,
    'outage_customer_impact': downstream_customers,
    'crew_availability': resource_constraints
}
                """)
        
        with col2:
            st.markdown("### 📊 Model Validation Strategy")
            
            st.markdown("**🎯 Rolling Window Validation:**")
            st.code("""
# Time-series cross-validation
def rolling_window_validation(data, window_size=365):
    results = []
    
    for i in range(len(data) - window_size):
        # Training window
        train_end = i + window_size
        train_data = data[:train_end]
        
        # Test window (next 30 days)
        test_data = data[train_end:train_end+30]
        
        # Train ensemble
        model = train_ensemble(train_data)
        
        # Evaluate
        predictions = model.predict(test_data)
        metrics = calculate_metrics(test_data.y, predictions)
        results.append(metrics)
    
    return aggregate_results(results)

# Business-aware validation
def business_cost_validation(predictions, actual):
    # False positive cost: unnecessary maintenance
    fp_cost = false_positives * avg_maintenance_cost
    
    # False negative cost: missed failures
    fn_cost = false_negatives * avg_failure_cost
    
    # Total business impact
    total_cost = fp_cost + fn_cost
    cost_savings = baseline_cost - total_cost
    
    return cost_savings
            """)
            
            st.markdown("**📈 Validation Results:**")
            validation_results = {
                "Metric": ["Precision", "Recall", "F1-Score", "Business Cost Accuracy", "Alert Precision"],
                "Training": ["89.2%", "96.7%", "92.8%", "88.4%", "83.1%"],
                "Validation": ["87.3%", "100.0%", "93.2%", "91.7%", "87.0%"],
                "Production": ["87.1%", "100.0%", "93.1%", "89.2%", "87.3%"]
            }
            
            validation_df = pd.DataFrame(validation_results)
            st.dataframe(validation_df, use_container_width=True)
        
        # Crew optimization algorithm
        st.markdown("### 👥 Crew Capacity Optimization")
        
        st.code("""
# Crew scheduling optimization
def optimize_crew_schedule(high_risk_assets, crews, constraints):
    '''
    Multi-objective optimization:
    1. Minimize total failure risk exposure
    2. Balance crew workload
    3. Respect skill/geographic constraints
    4. Optimize travel time between assets
    '''
    
    from scipy.optimize import linprog
    import networkx as nx
    
    # Objective function: minimize risk * time_to_failure
    c = [asset.failure_prob * asset.urgency_score for asset in high_risk_assets]
    
    # Constraints
    A_eq = []  # Crew capacity constraints
    b_eq = []  # Available crew hours
    
    for crew in crews:
        constraint = [1 if asset.location in crew.coverage_area else 0 
                     for asset in high_risk_assets]
        A_eq.append(constraint)
        b_eq.append(crew.available_hours)
    
    # Skill matching constraints
    for asset in high_risk_assets:
        if asset.requires_specialist:
            specialist_constraint = [
                1 if crew.has_specialist(asset.type) else 0 
                for crew in crews
            ]
    
    # Solve optimization
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, method='highs')
    
    return create_schedule(result.x, crews, high_risk_assets)

# Example output
schedule = {
    'Crew-A': ['AST-8847 (2h)', 'AST-9234 (3h)', 'Travel (1h)'],
    'Crew-B': ['AST-7721 (4h)', 'AST-6654 (2h)', 'Break (1h)'],
    'efficiency_score': 94.2,
    'total_risk_reduction': 87.3
}
        """)
        
        # Production deployment details
        st.markdown("### 🚀 Production Infrastructure")
        
        infra_tabs = st.tabs(["☁️ AKS Setup", "🔄 CI/CD Pipeline", "📊 Monitoring Stack"])
        
        with infra_tabs[0]:
            st.markdown("**Kubernetes Deployment Configuration:**")
            st.code("""
# Terraform AKS Configuration
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "pred-maint-aks"
  location            = "East US 2"
  resource_group_name = "rg-predictive-maintenance"
  dns_prefix          = "predmaint"
  
  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D4s_v3"
    auto_scaling_enabled = true
    min_count = 2
    max_count = 10
  }
  
  identity {
    type = "SystemAssigned"
  }
}

# HPA Configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-inference-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-inference
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
            """)
        
        with infra_tabs[1]:
            st.markdown("**Azure DevOps CI/CD Pipeline:**")
            st.code("""
# azure-pipelines.yml
trigger:
  branches:
    include:
    - main
    - develop
  paths:
    include:
    - src/models/*
    - src/api/*

stages:
- stage: Test
  jobs:
  - job: ModelValidation
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.9'
    
    - script: |
        pip install -r requirements.txt
        python -m pytest tests/test_models.py
        python scripts/validate_model_performance.py
      displayName: 'Model Testing'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFiles: '**/test-results.xml'

- stage: Build
  condition: succeeded()
  jobs:
  - job: BuildImage
    steps:
    - task: Docker@2
      inputs:
        command: 'buildAndPush'
        repository: 'predmaint/ml-api'
        containerRegistry: 'acrConnection'
        tags: '$(Build.BuildNumber)'

- stage: Deploy
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: DeployToAKS
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: KubernetesManifest@0
            inputs:
              action: 'deploy'
              kubernetesServiceConnection: 'aksConnection'
              manifests: 'k8s/*.yaml'
            """)
        
        with infra_tabs[2]:
            st.markdown("**Grafana Monitoring Dashboard:**")
            st.code("""
# Grafana Dashboard Configuration (JSON)
{
  "dashboard": {
    "title": "Predictive Maintenance ML Pipeline",
    "panels": [
      {
        "title": "Model Performance",
        "type": "stat",
        "targets": [
          {
            "expr": "model_accuracy{job='ml-api'}",
            "legendFormat": "Accuracy"
          },
          {
            "expr": "model_recall{job='ml-api'}",
            "legendFormat": "Recall"
          }
        ]
      },
      {
        "title": "Prediction Volume",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(predictions_total[5m])",
            "legendFormat": "Predictions/sec"
          }
        ]
      },
      {
        "title": "High Risk Assets",
        "type": "table",
        "targets": [
          {
            "expr": "high_risk_assets_count",
            "legendFormat": "Count"
          }
        ]
      },
      {
        "title": "Business Impact",
        "type": "stat",
        "targets": [
          {
            "expr": "estimated_cost_savings",
            "legendFormat": "Cost Savings ($)"
          }
        ]
      }
    ]
  }
}

# Prometheus Alerts
groups:
- name: ml-pipeline
  rules:
  - alert: ModelAccuracyDrop
    expr: model_accuracy < 0.90
    for: 5m
    annotations:
      summary: "Model accuracy below 90%"
      
  - alert: HighRiskAssetsSpike
    expr: high_risk_assets_count > 200
    for: 2m
    annotations:
      summary: "Unusual spike in high-risk assets"
            """)
    
    # Enhanced footer
    st.markdown("---")
    st.markdown("### 🎯 Ready to Transform Grid Operations")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="demo-card" style="text-align: center;">
            <h3>⚡ Ready to deploy at Eversource scale?</h3>
            <p style="font-size: 1.1rem; line-height: 1.6; margin: 1.5rem 0;">
                This ML solution demonstrates enterprise-grade predictive maintenance capabilities 
                that could prevent millions in equipment failures while optimizing crew operations 
                across Eversource's Connecticut and Massachusetts service territories.
            </p>
            <div style="background: linear-gradient(45deg, #ff6b35, #f7931e); color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <strong>🎯 Key Achievement: 100% recall with 89% alert precision eliminated alert fatigue</strong>
            </div>
            <p style="font-size: 1rem; color: #666; margin-top: 1rem;">
                Let's discuss how to implement this for Eversource's 9,000+ grid assets.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
