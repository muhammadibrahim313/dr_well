import streamlit as st 
from groq import Groq
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from fpdf import FPDF
import time
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Dr. Well", page_icon="👨‍⚕️", layout="wide")

# Initialize Groq API with environment variable
groq_api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=groq_api_key)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# --- Initialize Appointments Data in Session State ---
def generate_dummy_data():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    health_metrics = pd.DataFrame({
        'Date': dates,
        'Heart Rate': [random.randint(60, 100) for _ in range(30)],
        'Blood Pressure': [random.randint(110, 140) for _ in range(30)],
        'Sleep Hours': [random.randint(5, 9) for _ in range(30)],
        'Steps': [random.randint(5000, 15000) for _ in range(30)]
    })
    
    appointments = [
        {"id": 1, "doctor": "Dr. Sarah Smith", "specialty": "Cardiologist", "date": "2024-03-01", "time": "10:00 AM", "status": "Scheduled"},
        {"id": 2, "doctor": "Dr. John Davis", "specialty": "Dermatologist", "date": "2024-03-15", "time": "2:30 PM", "status": "Scheduled"},
        {"id": 3, "doctor": "Dr. Emily Wilson", "specialty": "Nutritionist", "date": "2024-03-20", "time": "11:15 AM", "status": "Scheduled"}
    ]
    
    medications = [
        {"name": "Vitamin D", "dosage": "1000 IU", "frequency": "Daily", "remaining": 45},
        {"name": "Omega-3", "dosage": "500mg", "frequency": "Twice daily", "remaining": 30},
        {"name": "Multivitamin", "dosage": "1 tablet", "frequency": "Daily", "remaining": 60}
    ]
    
    return health_metrics, appointments, medications

if 'appointments_data' not in st.session_state:
    _, appointments, _ = generate_dummy_data()
    st.session_state["appointments_data"] = appointments

# Helper function to call the AI chat API
def get_ai_response(prompt, system_role):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Dr. Well, an AI medical assistant who provides evidence-based advice and suggestions. Always introduce yourself as Dr. Well and maintain a professional yet friendly tone."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.5,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error in AI response: {str(e)}")
        return "I apologize, but I'm unable to provide a response at this time. - Dr. Well"

# Sidebar and Navigation
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0; background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); border-radius: 10px; margin-bottom: 20px;">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" style="width: 100px; height: 100px; border-radius: 50%; border: 3px solid #fff; margin-bottom: 10px;">
            <h3 style="color: white; margin: 10px 0;">John Doe</h3>
            <p style="color: #90caf9; margin: 0;">Patient ID: #12345</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard", 
            "Consultations", 
            "Nutrition", 
            "Medications",
            "Appointments",
            "Reports",
            "Settings",
            "About"
        ],
        icons=[
            "speedometer2",
            "chat-dots", 
            "file-medical", 
            "apple", 
            "capsule",
            "calendar-check",
            "graph-up",
            "gear",
            "info-circle"
        ],
        menu_icon="hospital",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#90caf9", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px", "text-align": "left", "margin": "0px",
                "padding": "15px 20px", "border-radius": "7px", "background": "transparent",
                "height": "50px", "color": "#ffffff", "--hover-color": "#1565c0"
            },
            "nav-link-selected": {"background": "linear-gradient(90deg, #1565c0 0%, #1976d2 100%)", "color": "white", "font-weight": "600"},
            "separator": {"margin": "15px 0", "background-color": "#263238", "height": "1px"}
        }
    )
    
    st.markdown("""
        <div style="background: rgba(26, 35, 126, 0.2); border-radius: 10px; padding: 15px; margin-top: 20px;">
            <h4 style="color: #90caf9; margin-bottom: 15px;">Quick Stats</h4>
            <div style="color: white; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>💗 Heart Rate</span>
                    <span>72 BPM</span>
                </div>
                <div style="background: #1565c0; height: 3px; border-radius: 2px; width: 80%;"></div>
            </div>
            <div style="color: white; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>🩺 BP</span>
                    <span>120/80</span>
                </div>
                <div style="background: #1565c0; height: 3px; border-radius: 2px; width: 90%;"></div>
            </div>
            <div style="color: white;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>👟 Steps</span>
                    <span>8,543</span>
                </div>
                <div style="background: #1565c0; height: 3px; border-radius: 2px; width: 70%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%); border-radius: 10px; padding: 15px; margin-top: 20px;">
            <h4 style="color: white; margin-bottom: 10px;">Next Appointment</h4>
            <p style="color: #90caf9; margin-bottom: 5px;">Dr. Sarah Smith</p>
            <p style="color: white; margin-bottom: 5px;">📅 March 1, 2024</p>
            <p style="color: white;">⏰ 10:00 AM</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(26, 35, 126, 0.9); padding: 15px; text-align: center;">
            <button style="background: #1565c0; color: white; border: none; padding: 8px 15px; border-radius: 5px; margin: 5px; cursor: pointer;">⚡ Quick Help</button>
            <button style="background: #1565c0; color: white; border: none; padding: 8px 15px; border-radius: 5px; margin: 5px; cursor: pointer;">🔔 Notifications</button>
        </div>
    """, unsafe_allow_html=True)
    
    if selected:
        st.session_state.page = selected

# Page functions
def dashboard():
    health_metrics, _, _ = generate_dummy_data()
    
    st.markdown("""
    <div class="welcome-header">
        <h1>👋 Welcome to Dr. Well</h1>
        <p>Your personal health dashboard - Updated as of today</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Heart Rate</h3>
            <div class="stat-number">72 <span style="font-size: 1rem;">BPM</span></div>
            <p class="status-normal">✓ Normal Range</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Blood Pressure</h3>
            <div class="stat-number">120/80</div>
            <p class="status-normal">✓ Optimal</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Sleep Quality</h3>
            <div class="stat-number">7.5 <span style="font-size: 1rem;">hrs</span></div>
            <p class="status-normal">✓ Well Rested</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Daily Steps</h3>
            <div class="stat-number">8,543</div>
            <p class="status-warning">! Below Target</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='section-header'>Health Trends</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📊 Activity Metrics", "💗 Vital Signs"])
    with tab1:
        fig_steps = px.line(health_metrics, x='Date', y='Steps', title='Daily Steps', line_shape='spline')
        fig_steps.update_layout(
            plot_bgcolor='#162447', paper_bgcolor='#162447', font_color='#ffffff',
            title_font_size=20, xaxis=dict(gridcolor='#283747'), yaxis=dict(gridcolor='#283747')
        )
        st.plotly_chart(fig_steps, use_container_width=True)
    with tab2:
        fig_vitals = go.Figure()
        fig_vitals.add_trace(go.Scatter(x=health_metrics['Date'], 
                                        y=health_metrics['Heart Rate'], name='Heart Rate',
                                        line=dict(color='#e74c3c', width=2)))
        fig_vitals.add_trace(go.Scatter(x=health_metrics['Date'], 
                                        y=health_metrics['Blood Pressure'], name='Blood Pressure',
                                        line=dict(color='#3498db', width=2)))
        fig_vitals.update_layout(
            title='Vital Signs Trend', plot_bgcolor='#162447', paper_bgcolor='#162447',
            font_color='#ffffff', title_font_size=20, xaxis=dict(gridcolor='#283747'),
            yaxis=dict(gridcolor='#283747')
        )
        st.plotly_chart(fig_vitals, use_container_width=True)

def consultations():
    st.markdown("""
    <div class="welcome-header">
        <h1>🩺 Consultations</h1>
        <p>Review your confirmed (running) consultations</p>
    </div>
    """, unsafe_allow_html=True)
    
    confirmed = [apt for apt in st.session_state["appointments_data"] if apt["status"] == "Confirmed"]
    if confirmed:
        st.markdown("<h2 class='section-header'>Running Consultations</h2>", unsafe_allow_html=True)
        for apt in confirmed:
            st.markdown(f"""
            <div class="appointment-card">
                <h4>🏥 {apt['doctor']} - {apt['specialty']}</h4>
                <p>📅 {apt['date']} at {apt['time']}</p>
                <p style="color: #4CAF50; font-weight: bold;">Status: {apt['status']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p>No confirmed consultations at this time.</p>", unsafe_allow_html=True)

def nutrition():
    st.markdown("""
    <div class="welcome-header">
        <h1>🍏 Nutrition</h1>
        <p>Get personalized nutrition advice from Dr. Well</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Chat with Dr. Well")
    st.markdown("_Your personal AI nutrition advisor_")
    
    chatbot_option = st.selectbox("How can I help you today?", 
                                   ["Ask a nutrition question", "Get a healthy recipe", "Calculate daily calories", "Find food substitutes"])
    
    user_input = ""
    if chatbot_option == "Ask a nutrition question":
        user_input = st.text_input("What would you like to know about nutrition?")
    elif chatbot_option == "Get a healthy recipe":
        user_input = "Could you suggest a healthy recipe that's high in protein, low in carbs, and vegetarian?"
        st.info("I'll help you find a healthy recipe that matches your preferences.")
    elif chatbot_option == "Calculate daily calories":
        age = st.number_input("Your age", min_value=10, max_value=100, value=30)
        weight = st.number_input("Your weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("Your height (cm)", min_value=100, max_value=250, value=170)
        user_input = f"Please calculate the daily calorie needs for someone who is {age} years old, weighs {weight} kg, and is {height} cm tall."
    elif chatbot_option == "Find food substitutes":
        user_input = st.text_input("What ingredient would you like to substitute?", "sugar")
        if user_input:
            user_input = f"What are some healthy substitutes for {user_input} in cooking or baking?"
    
    if st.button("Ask Dr. Well"):
        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            with st.chat_message("assistant", avatar="👨‍⚕️"):
                response = get_ai_response(user_input, "nutrition_advisor")
                st.write(response)
        else:
            st.warning("Please enter your question or select an option above.")
    st.markdown("<p>Here you can view and manage your nutrition plans.</p>", unsafe_allow_html=True)

def health_records():
    st.markdown("""
    <div class="welcome-header">
        <h1>📋 Health Records</h1>
        <p>View and manage your health records</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<p>Here you can view and manage your health records.</p>", unsafe_allow_html=True)

def about():
    st.markdown("""
    <div class="welcome-header">
        <h1>ℹ️ About Dr. Well</h1>
        <p>Your Comprehensive Health Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-container">
        <h2>Overview</h2>
        <p>Dr. Well is a next-generation digital health platform designed to empower you with personalized health insights, appointment management, and evidence-based medical advice. Our application brings together a suite of powerful features, including:</p>
        <ul>
            <li><strong>Dashboard:</strong> A centralized view of your vital signs, activity trends, and health metrics.</li>
            <li><strong>Consultations:</strong> Manage your appointments and view confirmed consultations with our team of experts.</li>
            <li><strong>Nutrition:</strong> Chat with Dr. Well to receive personalized nutrition advice, healthy recipes, and calorie calculations.</li>
            <li><strong>Medications:</strong> Keep track of your medication schedules and request refills effortlessly.</li>
            <li><strong>Reports:</strong> Access detailed health reports and download them as PDF files for your records.</li>
            <li><strong>Settings:</strong> Customize your experience to suit your individual health needs.</li>
        </ul>
        <h2>Technology & Innovation</h2>
        <p>Built on the robust Streamlit framework and enhanced with interactive visualizations via Plotly, Dr. Well leverages cutting-edge AI powered by the Groq API to deliver evidence-based recommendations. Our intuitive design ensures that every feature is accessible and actionable, enabling you to take charge of your health with confidence.</p>
        <h2>Why Choose Dr. Well?</h2>
        <p>At Dr. Well, our mission is to bridge the gap between technology and personalized healthcare. With our platform, you benefit from:</p>
        <ul>
            <li>Real-time insights into your health status</li>
            <li>Seamless management of consultations and appointments</li>
            <li>Customized nutrition and lifestyle guidance</li>
            <li>A user-friendly interface designed with your well-being in mind</li>
        </ul>
        <p>Join us on a journey towards better health, where technology meets care—welcome to Dr. Well!</p>
    </div>
    """, unsafe_allow_html=True)

def medications():
    st.markdown("""
    <div class="welcome-header">
        <h1>💊 Medications</h1>
        <p>Track and manage your medications</p>
    </div>
    """, unsafe_allow_html=True)
    
    _, _, medications = generate_dummy_data()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2 class='section-header'>Current Medications</h2>", unsafe_allow_html=True)
        for med in medications:
            st.markdown(f"""
            <div class="medication-card" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4>💊 {med['name']}</h4>
                    <p>Dosage: {med['dosage']} - {med['frequency']}</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: {'#4CAF50' if med['remaining'] > 30 else '#f39c12'}">
                        {med['remaining']} days remaining
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown("<h2 class='section-header'>Refill Requests</h2>", unsafe_allow_html=True)
        for med in medications:
            if med['remaining'] <= 30:
                st.button(f"Request Refill: {med['name']}")

def appointments():
    st.markdown("""
    <div class="welcome-header">
        <h1>📅 Appointments</h1>
        <p>Manage your medical appointments</p>
    </div>
    """, unsafe_allow_html=True)
    
    appointments_data = st.session_state["appointments_data"]
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h2 class='section-header'>Upcoming Appointments</h2>", unsafe_allow_html=True)
        for i, apt in enumerate(appointments_data):
            st.markdown(f"""
            <div class="appointment-card">
                <h4>🏥 {apt['doctor']} - {apt['specialty']}</h4>
                <p>📅 {apt['date']} at {apt['time']}</p>
                <p>Status: {apt['status']}</p>
            """, unsafe_allow_html=True)
            if apt["status"] == "Scheduled":
                if st.button("Confirm", key=f"confirm_{apt['id']}"):
                    st.session_state["appointments_data"][i]["status"] = "Confirmed"
                    st.success("Appointment confirmed!")
                    st.rerun()
                st.button("Reschedule", key=f"reschedule_{apt['id']}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h2 class='section-header'>Schedule New</h2>", unsafe_allow_html=True)
        # New selection for doctor gender added here
        specialty = st.selectbox("Select Specialty", ["Cardiology", "Dermatology", "Neurology", "Orthopedics", "General Medicine"])
        doctor_gender = st.selectbox("Select Doctor Gender", ["Male", "Female"])
        date = st.date_input("Select Date")
        time_val = st.time_input("Select Time")
        if st.button("Schedule Appointment"):
            new_id = max([apt["id"] for apt in appointments_data]) + 1 if appointments_data else 1
            new_apt = {
                "id": new_id,
                "doctor": f"Dr. {doctor_gender} {specialty} Specialist",
                "specialty": specialty,
                "date": date.strftime("%Y-%m-%d"),
                "time": time_val.strftime("%I:%M %p"),
                "status": "Scheduled"
            }
            st.session_state["appointments_data"].append(new_apt)
            st.success("New appointment scheduled!")
            st.rerun()

def reports():
    st.markdown("""
    <div class="welcome-header">
        <h1>📊 Health Reports</h1>
        <p>View and download your health reports</p>
    </div>
    """, unsafe_allow_html=True)
    
    reports_list = [
        {"name": "Annual Health Check", "date": "2024-01-15", "type": "General"},
        {"name": "Blood Work Analysis", "date": "2024-02-01", "type": "Laboratory"},
        {"name": "Cardiac Assessment", "date": "2024-02-15", "type": "Specialist"}
    ]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2 class='section-header'>Available Reports</h2>", unsafe_allow_html=True)
        for report in reports_list:
            st.markdown(f"""
            <div class="appointment-card">
                <h4>📄 {report['name']}</h4>
                <p>Date: {report['date']} | Type: {report['type']}</p>
                <div style="display: flex; gap: 10px; margin-top: 10px;">
                    <button style="background: #1565c0; color: white; border: none; padding: 5px 10px; border-radius: 5px;">
                        View Report
                    </button>
                    <button style="background: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 5px;">
                        Download PDF
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown("<h2 class='section-header'>Generate Report</h2>", unsafe_allow_html=True)
        report_type = st.selectbox("Report Type", ["Health Summary", "Medication History", "Vital Signs", "Lab Results"])
        date_range = st.date_input("Date Range", [])
        if st.button("Generate Report"):
            st.info("Generating report... Please wait")
            time.sleep(2)
            st.success("Report generated successfully!")

def settings():
    st.markdown("""
    <div class="welcome-header">
        <h1>⚙️ Settings</h1>
        <p>Customize your Dr. Well experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Profile", "Notifications", "Privacy"])
    with tab1:
        st.markdown("<h2 class='section-header'>Profile Settings</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", "John Doe")
            st.text_input("Email", "john.doe@email.com")
            st.text_input("Phone", "+1 234 567 8900")
        with col2:
            st.date_input("Date of Birth")
            st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            st.text_area("Medical Conditions")
    with tab2:
        st.markdown("<h2 class='section-header'>Notification Preferences</h2>", unsafe_allow_html=True)
        st.checkbox("Email Notifications", value=True)
        st.checkbox("SMS Notifications", value=True)
        st.checkbox("Appointment Reminders", value=True)
        st.checkbox("Medication Reminders", value=True)
        st.checkbox("Health Tips", value=True)
    with tab3:
        st.markdown("<h2 class='section-header'>Privacy Settings</h2>", unsafe_allow_html=True)
        st.checkbox("Share health data with doctors", value=True)
        st.checkbox("Allow anonymous data use for research", value=False)
        st.checkbox("Enable two-factor authentication", value=True)
        if st.button("Download My Data"):
            st.success("Your data export has been initiated!")

# Add CSS styles
st.markdown("""
<style>
/* Base styles */
.main { background-color: #1a1a2e; color: #ffffff; }
.stApp { background-color: #1a1a2e; }

/* Custom container */
.content-container {
    background-color: #16213e; padding: 20px; border-radius: 15px;
    margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* Welcome header */
.welcome-header {
    background: linear-gradient(135deg, #0f3460 0%, #533483 100%);
    color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
.welcome-header h1 { font-size: 2.5rem; margin-bottom: 10px; color: #ffffff; font-weight: 700; }
.welcome-header p { font-size: 1.2rem; color: #e2e8f0; margin-bottom: 0; }

/* Metric card */
.metric-card {
    background: linear-gradient(145deg, #162447 0%, #1f4068 100%);
    padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    text-align: center; height: 100%; transition: transform 0.3s ease;
}
.metric-card:hover { transform: translateY(-5px); }
.metric-card h3 { color: #e2e8f0; font-size: 1.2rem; margin-bottom: 15px; }
.stat-number { font-size: 2rem; font-weight: bold; color: #4CAF50; margin: 10px 0; }
.stat-label { color: #bdc3c7; font-size: 0.9rem; }

/* Cards */
.appointment-card, .medication-card {
    background-color: #1f4068; padding: 20px; border-radius: 12px;
    margin: 15px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    border-left: 4px solid #4CAF50;
}
.appointment-card h4, .medication-card h4 { color: #ffffff; margin-bottom: 10px; font-size: 1.1rem; }
.appointment-card p, .medication-card p { color: #bdc3c7; margin: 0; }

/* Charts */
.chart-container {
    background-color: #162447; padding: 20px; border-radius: 15px;
    margin: 20px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* Section headers */
.section-header { color: #ffffff; font-size: 1.5rem; margin: 30px 0 20px 0; padding-bottom: 10px; border-bottom: 2px solid #3498db; }

/* Status indicators */
.status-normal { color: #4CAF50; }
.status-warning { color: #f39c12; }
.status-alert { color: #e74c3c; }

/* Button styles */
.stButton > button {
    background-color: #3498db !important; color: white !important;
    border: none !important; padding: 10px 24px !important;
    border-radius: 5px !important; font-weight: 500 !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background-color: #2980b9 !important; transform: translateY(-2px) !important;
}

/* Input fields */
.stTextInput > div > div > input {
    background-color: #1f4068 !important; color: white !important;
    border: 1px solid #3498db !important;
}
.stSelectbox > div > div > select {
    background-color: #1f4068 !important; color: white !important;
    border: 1px solid #3498db !important;
}
</style>
""", unsafe_allow_html=True)

# Main content router
if st.session_state.page == "Dashboard":
    dashboard()
elif st.session_state.page == "Consultations":
    consultations()
elif st.session_state.page == "Health Records":
    health_records()
elif st.session_state.page == "Nutrition":
    nutrition()
elif st.session_state.page == "Medications":
    medications()
elif st.session_state.page == "Appointments":
    appointments()
elif st.session_state.page == "Reports":
    reports()
elif st.session_state.page == "Settings":
    settings()
elif st.session_state.page == "About":
    about()
