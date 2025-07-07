import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import numpy as np
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Configuration
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8001/ask")

# Page configuration
st.set_page_config(
    page_title="AI Insight Dashboard",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .sidebar .block-container {
        padding-top: 2rem;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>✨ AI Insight Dashboard</h1>
    <p>Transform Natural Language into Intelligent Data Visualizations</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🔧 Configuration")
    
    # Chart type selection with more options
    chart_type = st.selectbox(
        "📊 Select Visualization Type:",
        [
            "Table",
            "Bar Chart",
            "Line Chart",
            "Pie Chart",
            "Heatmap",
            "Scatter Plot",
            "Area Chart",
            "Histogram",
            "Box Plot",
            "Violin Plot",
            "Donut Chart",
            "Treemap",
            "Sunburst",
            "Waterfall Chart"
        ]
    )
    
    # Chart customization options
    st.markdown("### 🎨 Chart Customization")
    
    color_theme = st.selectbox(
        "Color Theme:",
        ["viridis", "plasma", "inferno", "magma", "blues", "reds", "greens", "rainbow"]
    )
    
    show_grid = st.checkbox("Show Grid", value=True)
    show_legend = st.checkbox("Show Legend", value=True)
    
    # Advanced options
    with st.expander("Advanced Options"):
        fig_width = st.slider("Figure Width", 6, 20, 12)
        fig_height = st.slider("Figure Height", 4, 15, 8)
        font_size = st.slider("Font Size", 8, 20, 12)
        
    # Sample questions
    st.markdown("### 💡 Sample Questions")
    sample_questions = [
        "Total sales by category",
        "Average order value per month",
        "Top 10 customers by revenue",
        "Monthly growth rate",
        "Product performance comparison",
        "Customer satisfaction by region"
    ]
    
    for question in sample_questions:
        if st.button(f"📝 {question}", key=f"sample_{question}"):
            st.session_state.user_question = question

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Question input
    user_question = st.text_input(
        "🤔 Ask your data question:",
        placeholder="e.g., Show me the total revenue by product category for the last quarter",
        value=st.session_state.get('user_question', ''),
        help="Type your question in natural language. Be specific about what you want to see."
    )

with col2:
    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    run_query = st.button("🚀 Run Query", type="primary", use_container_width=True)
    clear_query = st.button("🗑️ Clear", use_container_width=True)

if clear_query:
    st.session_state.user_question = ""
    st.rerun()

# Query execution
if run_query:
    if not user_question:
        st.warning("⚠️ Please enter a question to get started.")
    else:
        try:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Sending request to AI backend...")
            progress_bar.progress(25)
            
            # Send request to FastAPI backend
            res = requests.post(
                FASTAPI_URL,
                json={"question": f"{user_question}. In the format It will be helpful for this chart {chart_type}"},
                timeout=30
            )
            
            res.raise_for_status()
            
            status_text.text("🧠 Processing AI response...")
            progress_bar.progress(50)
            
            data = res.json()
            
            status_text.text("📊 Generating visualization...")
            progress_bar.progress(75)
            
            # Display results
            if "sql" in data:
                sql = data["sql"]
                columns = data.get("columns", [])
                rows = data.get("rows", [])
                
                # SQL Display
                with st.expander("🔍 Generated SQL Query", expanded=False):
                    st.code(sql, language="sql")
                
                # Data processing
                if rows and columns:
                    df = pd.DataFrame(rows, columns=columns)
                    
                    # Data summary
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📊 Total Rows", len(df))
                    with col2:
                        st.metric("📈 Columns", len(df.columns))
                    with col3:
                        if df.select_dtypes(include=[np.number]).empty:
                            st.metric("💰 Numeric Cols", 0)
                        else:
                            st.metric("💰 Numeric Cols", len(df.select_dtypes(include=[np.number]).columns))
                    with col4:
                        st.metric("⏰ Generated", datetime.now().strftime("%H:%M:%S"))
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Visualization ready!")
                    
                    # Chart generation
                    st.markdown("### 📊 Data Visualization")
                    
                    chart_container = st.container()
                    
                    with chart_container:
                        try:
                            if chart_type == "Table":
                                st.dataframe(df, use_container_width=True)
                                
                            elif chart_type == "Bar Chart" and len(df.columns) >= 2:
                                fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                                           color_discrete_sequence=px.colors.qualitative.Set3,
                                           title=f"Bar Chart: {user_question}")
                                fig.update_layout(showlegend=show_legend, 
                                                width=fig_width*80, height=fig_height*60)
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif chart_type == "Line Chart" and len(df.columns) >= 2:
                                fig = px.line(df, x=df.columns[0], y=df.columns[1],
                                            title=f"Line Chart: {user_question}")
                                fig.update_layout(showlegend=show_legend,
                                                width=fig_width*80, height=fig_height*60)
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif chart_type == "Pie Chart" and len(df.columns) >= 2:
                                fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                                           title=f"Pie Chart: {user_question}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif chart_type == "Heatmap":
                                # Create heatmap with numeric data
                                numeric_df = df.select_dtypes(include=[np.number])
                                if not numeric_df.empty:
                                    fig = px.imshow(numeric_df.corr(), 
                                                  color_continuous_scale=color_theme,
                                                  title="Correlation Heatmap")
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    # Alternative heatmap for categorical data
                                    if len(df.columns) >= 2:
                                        pivot_df = df.pivot_table(
                                            index=df.columns[0], 
                                            columns=df.columns[1] if len(df.columns) > 2 else df.columns[0],
                                            values=df.columns[-1] if len(df.columns) > 2 else df.columns[1],
                                            aggfunc='count', 
                                            fill_value=0
                                        )
                                        fig = px.imshow(pivot_df, color_continuous_scale=color_theme,
                                                      title="Data Heatmap")
                                        st.plotly_chart(fig, use_container_width=True)
                                    else:
                                        st.info("Heatmap requires numeric data or at least 2 columns")
                                        
                            elif chart_type == "Scatter Plot" and len(df.columns) >= 2:
                                fig = px.scatter(df, x=df.columns[0], y=df.columns[1],
                                               color=df.columns[2] if len(df.columns) > 2 else None,
                                               title=f"Scatter Plot: {user_question}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif chart_type == "Area Chart" and len(df.columns) >= 2:
                                fig = px.area(df, x=df.columns[0], y=df.columns[1],
                                            title=f"Area Chart: {user_question}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif chart_type == "Histogram":
                                numeric_cols = df.select_dtypes(include=[np.number]).columns
                                if len(numeric_cols) > 0:
                                    fig = px.histogram(df, x=numeric_cols[0],
                                                     title=f"Histogram: {numeric_cols[0]}")
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.info("Histogram requires numeric data")
                                    
                            elif chart_type == "Box Plot":
                                numeric_cols = df.select_dtypes(include=[np.number]).columns
                                if len(numeric_cols) > 0:
                                    fig = px.box(df, y=numeric_cols[0],
                                               title=f"Box Plot: {numeric_cols[0]}")
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.info("Box plot requires numeric data")
                                    
                            elif chart_type == "Violin Plot":
                                numeric_cols = df.select_dtypes(include=[np.number]).columns
                                if len(numeric_cols) > 0:
                                    fig = px.violin(df, y=numeric_cols[0],
                                                  title=f"Violin Plot: {numeric_cols[0]}")
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.info("Violin plot requires numeric data")
                                    
                            elif chart_type == "Donut Chart" and len(df.columns) >= 2:
                                fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                                           title=f"Donut Chart: {user_question}", hole=0.4)
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif chart_type == "Treemap" and len(df.columns) >= 2:
                                fig = px.treemap(df, path=[df.columns[0]], values=df.columns[1],
                                               title=f"Treemap: {user_question}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif chart_type == "Sunburst" and len(df.columns) >= 2:
                                fig = px.sunburst(df, path=[df.columns[0]], values=df.columns[1],
                                                title=f"Sunburst: {user_question}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                            elif chart_type == "Waterfall Chart" and len(df.columns) >= 2:
                                fig = go.Figure(go.Waterfall(
                                    name="Waterfall",
                                    orientation="v",
                                    measure=["relative"] * len(df),
                                    x=df[df.columns[0]],
                                    y=df[df.columns[1]],
                                    text=df[df.columns[1]],
                                    textposition="outside",
                                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                                ))
                                fig.update_layout(title=f"Waterfall Chart: {user_question}")
                                st.plotly_chart(fig, use_container_width=True)
                                
                            else:
                                st.warning(f"⚠️ {chart_type} requires appropriate data structure. Showing table instead.")
                                st.dataframe(df, use_container_width=True)
                                
                        except Exception as chart_error:
                            st.error(f"❌ Error creating {chart_type}: {str(chart_error)}")
                            st.info("📋 Displaying data as table instead:")
                            st.dataframe(df, use_container_width=True)
                    
                    # Data download
                    st.markdown("### 📥 Export Data")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📄 Download CSV",
                            data=csv,
                            file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        excel_buffer = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
                        df.to_excel(excel_buffer, index=False)
                        excel_buffer.close()
                        
                    with col3:
                        json_str = df.to_json(orient='records', indent=2)
                        st.download_button(
                            label="📊 Download JSON",
                            data=json_str,
                            file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                else:
                    st.info("ℹ️ No data returned from the query. Please try a different question.")
                    
            else:
                st.error("❌ Unexpected response format from API")
                st.json(data)  # Show raw response for debugging
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again or check your backend service.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to the backend service. Please ensure it's running on http://localhost:8001")
        except requests.exceptions.HTTPError as e:
            st.error(f"🌐 HTTP error occurred: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            
# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🧠 AI Insight Dashboard | Powered by FastAPI & Streamlit</p>
    <p>Transform your data questions into beautiful visualizations</p>
</div>
""", unsafe_allow_html=True)