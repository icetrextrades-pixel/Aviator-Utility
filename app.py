import streamlit as st
import random
import time

# UI Setup for Mobile and Laptop
st.set_page_config(page_title="ICETREX Aviator Predictor", layout="centered")

st.title("🚀 Aviator Signal Predictor")
st.subheader("Statistical Probability Engine")

# Sidebar for User Input
st.sidebar.header("Current Game Data")
history_input = st.sidebar.text_input("Enter last 5 results (e.g. 1.2, 5.4, 1.1, 2.0, 1.5)", "")

def generate_signal(data):
    if not data:
        return "Waiting for data...", "grey"
    
    # Logic: If many low numbers (Blue) appear, probability of a high (Pink) increases
    try:
        nums = [float(x.strip()) for x in data.split(",")]
        avg = sum(nums) / len(nums)
        
        if nums[-1] < 1.5 and nums[-2] < 1.5:
            return "HIGH PROBABILITY: NEXT ROUND 2.0x+", "green"
        elif avg > 3.0:
            return "WAIT: Market is cooling down", "orange"
        else:
            return "SIGNAL: Small Bet (1.2x - 1.5x)", "blue"
    except:
        return "Error: Enter numbers separated by commas", "red"

# Main Display
if st.button("Generate Signal"):
    with st.spinner('Analyzing Patterns...'):
        time.sleep(1) # Simulates "thinking"
        result, color = generate_signal(history_input)
        st.markdown(f"### Result: :{color}[{result}]")

st.divider()
st.write("⚠️ *Note: This tool uses probability, not a hack. Play responsibly.*")