import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image
import base64
import io
import time
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(page_title="Voice Navigator", layout="wide")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.directions = ["Start at Main St", "Turn left on Oak Ave", "Continue for 0.5 miles", "Destination on right"]
    st.session_state.obstacles = []
    st.session_state.distance = 0
    st.session_state.start_time = datetime.now()

# Title
st.title("🎤 Voice Navigator Pro")
st.markdown("---")

# Sidebar for audio input
with st.sidebar:
    st.header("🎵 Navigation Input")
    audio_file = st.file_uploader("Upload destination voice command", type=['mp3', 'wav', 'ogg', 'm4a'])
    
    if audio_file:
        st.audio(audio_file)
        if st.button("Process Voice Command"):
            with st.spinner("Processing navigation..."):
                # Simulate Groq API processing
                time.sleep(2)
                st.session_state.processed = True
                st.success("Destination set: Downtown Station")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Navigation", "📊 Dashboard", "⚠️ Alerts", "📈 Report"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Navigation Steps")
        for i, direction in enumerate(st.session_state.directions):
            if i <= st.session_state.step:
                st.info(f"✅ {direction}")
            else:
                st.write(f"⏳ {direction}")
        
        if st.session_state.step < len(st.session_state.directions) - 1:
            if st.button("▶️ Next Direction", use_container_width=True):
                st.session_state.step += 1
                st.session_state.distance += 0.3
                
                # Random obstacle generation
                if random.random() > 0.7:
                    obs = f"⚠️ Traffic ahead at {datetime.now().strftime('%H:%M')}"
                    st.session_state.obstacles.append(obs)
                    st.warning(obs)
    
    with col2:
        st.subheader("Current Status")
        eta = datetime.now() + timedelta(minutes=15 - st.session_state.step*3)
        st.metric("Distance Covered", f"{st.session_state.distance:.1f} miles")
        st.metric("Arriving in", eta.strftime("%H:%M"))
        
        # Mini map
        fig = go.Figure(data=go.Scattermapbox(
            lat=[37.77, 37.78, 37.79],
            lon=[-122.42, -122.43, -122.44],
            mode='markers+lines',
            marker={'size': 10}))
        fig.update_layout(mapbox_style="open-street-map", height=200, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Distance", f"{st.session_state.distance:.1f} mi")
        st.metric("Remaining", f"{3.5 - st.session_state.distance:.1f} mi")
    
    with col2:
        # Pie chart
        fig, ax = plt.subplots()
        ax.pie([st.session_state.distance, 3.5 - st.session_state.distance], 
               labels=['Completed', 'Remaining'], autopct='%1.1f%%')
        st.pyplot(fig)
    
    with col3:
        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=st.session_state.distance * 28.57,
            title={'text': "Progress %"},
            gauge={'axis': {'range': [0, 100]}}))
        fig.update_layout(height=200)
        st.plotly_chart(fig, use_container_width=True)
    
    # Line chart for progress
    progress_data = pd.DataFrame({
        'Time': pd.date_range(start=st.session_state.start_time, periods=10, freq='2min'),
        'Distance': [i * 0.35 for i in range(10)]
    })
    st.line_chart(progress_data.set_index('Time'))

with tab3:
    st.subheader("Obstacle Alerts")
    
    if st.session_state.obstacles:
        for obs in st.session_state.obstacles:
            st.error(obs)
    else:
        st.success("No obstacles detected")
    
    if st.button("➕ Add Test Alert"):
        new_obs = f"🚧 Construction at {datetime.now().strftime('%H:%M')}"
        st.session_state.obstacles.append(new_obs)
        st.rerun()

with tab4:
    if st.button("📥 Generate Final Report"):
        st.subheader("Journey Summary Report")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Trip Details**")
            st.write(f"Start Time: {st.session_state.start_time.strftime('%H:%M:%S')}")
            st.write(f"End Time: {datetime.now().strftime('%H:%M:%S')}")
            st.write(f"Total Distance: {st.session_state.distance:.2f} miles")
            st.write(f"Obstacles Encountered: {len(st.session_state.obstacles)}")
        
        with col2:
            st.write("**Voice Commands Processed**")
            st.write("✓ Destination: Downtown Station")
            st.write("✓ Route optimized")
            st.write("✓ Real-time navigation active")
        
        # Summary charts
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        # Bar chart - Directions
        axes[0].bar(range(len(st.session_state.directions)), [1]*len(st.session_state.directions))
        axes[0].set_title("Navigation Steps")
        
        # Obstacles pie
        axes[1].pie([len(st.session_state.obstacles), max(1, 5-len(st.session_state.obstacles))], 
                    labels=['Obstacles', 'Clear Path'], autopct='%1.1f%%')
        axes[1].set_title("Obstacle Report")
        
        # Progress line
        axes[2].plot([0, 25, 50, 75, 100], [0, 20, 45, 70, 100])
        axes[2].set_title("Journey Progress")
        axes[2].set_xlabel("Time %")
        axes[2].set_ylabel("Distance %")
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Convert to PDF
        pdf_buffer = io.BytesIO()
        fig.savefig(pdf_buffer, format='pdf', bbox_inches='tight')
        pdf_buffer.seek(0)
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_buffer,
            file_name="voice_navigator_report.pdf",
            mime="application/pdf"
        )

# Footer
st.markdown("---")
st.caption("Voice Navigator Pro - AI-Powered Voice Navigation System")
