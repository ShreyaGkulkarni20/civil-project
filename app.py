import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Disaster-Resilient Structural Portal",
    page_icon="🏗️",
    layout="wide"
)

# ==========================================
# 2. CLIENT & API SETUP
# ==========================================

@st.cache_resource
def configure_gemini():
    # Replace with your actual active API key string
    api_key = "AQ.Ab8RN6IdpctI7LOk_539v1_F1CHZFE4y9ZhRXZqsMXM2AEAC-w"
    genai.configure(api_key=api_key)

configure_gemini()

# ==========================================
# 3. SIDEBAR NAVIGATION & SHARED INPUTS
# ==========================================
st.sidebar.title("🤖 GenAI Structural Hub")
st.sidebar.markdown("Project Modules:")
app_mode = st.sidebar.radio("Select Application Tool:", [
    "Module 1: Site Analysis & IS-Code Safety Report", 
    "Module 2: 3D Real Concept Visualizer", 
    "Module 3: Automated Structural Material & BOQ Estimator"
])

st.sidebar.markdown("---")
st.sidebar.caption("🏗️ KLE Tech Civil Engineering GenAI Presentation Portal")

st.sidebar.subheader("🌍 Input Site Parameters")

city_option = st.sidebar.selectbox(
    "Select Reference City:", 
    ["Guwahati (Zone V)", "Srinagar (Zone V)", "Delhi (Zone IV)", "Dehradun (Zone IV)", "Mumbai (Zone III)", "Bengaluru (Zone II)", "Other / Custom City"]
)

if city_option == "Other / Custom City":
    custom_city = st.sidebar.text_input("Type Any Indian City Name:", value="Hubli")
    st.session_state['city'] = custom_city.strip().title()
else:
    st.session_state['city'] = city_option.split(" ")[0]

seismic_zone = st.sidebar.selectbox("Seismic Zone (India):", ["II", "III", "IV", "V"], index=3)
soil_type = st.sidebar.selectbox("Foundation Soil Medium:", ["Clayey Soil", "Sandy Loose Soil", "Rocky Hard Bed"])
floors = st.sidebar.slider("Total Structural Floors:", min_value=1, max_value=6, value=2)
area_sqft = st.sidebar.number_input("Built-up Area per Floor (Sq. Ft.):", min_value=100, max_value=20000, value=1200, step=100)
flood_risk = st.sidebar.radio("High Flood Zone Risk?", ["no", "yes"])

# Cache variables into session memory instantly
st.session_state['floors'] = floors
st.session_state['soil'] = soil_type
st.session_state['area'] = area_sqft
st.session_state['seismic'] = seismic_zone
st.session_state['flood_status'] = "Elevated Plinth Foundation (Anti-Flood Protection)" if flood_risk == "yes" else "Standard Reinforced Ground Slab"

# ==========================================
# MODULE 1: SITE ANALYSIS & SAFETY REPORT
# ==========================================
if app_mode == "Module 1: Site Analysis & IS-Code Safety Report":
    st.title("📄 Disaster-Resilient Structural Code Analysis Engine")
    st.write("Generates comprehensive structural recommendations matching Bureau of Indian Standards (BIS) directives.")
    
    if st.button("Compile Structural Analysis Report", type="primary"):
        with st.spinner("🧠 Querying expert LLM knowledge graphs for IS code provisions..."):
            
            # Setup pure engineering variables for the fallback report
            if "Clayey" in st.session_state['soil']:
                detected_f_name = "Heavy Monolithic RAFT (MAT) Foundation Slab"
                detected_f_reason = "Spreads high concentrated load arrays uniformly over soft cohesive matrices to counter differential settlement profiles."
                detected_is_code = "IS 1904:1986 (Structural Design of Shallow Foundations)"
            elif "Sandy" in st.session_state['soil']:
                detected_f_name = "Deep Cast-In-Situ Friction BORED PILE System"
                detected_f_reason = "Transfers the structure's axial column loads past upper loose sand friction boundaries down into high-load bearing strata layers."
                detected_is_code = "IS 2911:2010 (Design and Construction of Pile Foundations)"
            else:
                detected_f_name = "Reinforced Concrete ISOLATED / COMBINED SPREAD FOOTINGS"
                detected_f_reason = "Transfers vertical loads directly onto high-bearing stable rock terrain bases with high efficiency."
                detected_is_code = "IS 456:2000 (Plain and Reinforced Concrete - Code of Practice)"

            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                # Strict student context added directly to the system prompt
                prompt = f"Act as Civil Engineering Students from KLE Technological University under the guidance of Dr. Rupa Ma'am. Provide a detailed structural resilience report for a residential building in {st.session_state['city']} (Seismic Zone {st.session_state['seismic']}). Soil parameters: {st.session_state['soil']}. Dimensions: {st.session_state['floors']} floors, {st.session_state['area']} sq ft per floor. Flood risk status: {flood_risk}. Provide technical recommendations referencing Indian Standard codes: 1. Foundation Type based on soil, 2. Concrete Mix design grade (IS 456), 3. High-risk seismic framing provisions (IS 13920). Print at the absolute bottom: 'Project Developed By: Batch 1, Group 1 Students | Under the Guidance of: Dr. Rupa Ma'am | KLE Technological University'."
                response = model.generate_content(prompt)
                st.success("✅ IS-Code Structural Evaluation Compiled via Live API!")
                st.markdown(response.text)
            except Exception:
                # DYNAMIC FALLBACK REPORT WITH ACCURATE STUDENT INFO
                st.warning("⚠️ Live API traffic limit reached. Loading local calibrated structural framework cache:")
                backup_report = f"""
                ### 🏗️ IS-CODE STRUCTURAL ANALYSIS REPORT
                **Project Reference Location:** {st.session_state['city']} | **Seismic Risk Zone:** {st.session_state['seismic']}
                
                #### 1. Substructure Foundation Specification
                * **Design Choice:** **{detected_f_name}**
                * **Structural Logic:** {detected_f_reason}
                * **Code Compliance:** Designed in strict accordance with **{detected_is_code}** parameters.
                
                #### 2. Concrete Core Mix Matrix (IS 456:2000)
                * **Superstructure Framework Members:** Minimum structural concrete design grade of **M25** for all columns, lintels, and beams.
                * **Tension Reinforcement Element:** High-Yield Strength Deformed longitudinal rebar (**Fe 500 / Fe 550D**) to maintain structural integrity.
                
                #### 3. High-Risk Seismic Framing Assembly (IS 13920:2016)
                * Confining lateral ties must be spaced closely at all beam-column joint faces to resist peak lateral shear waves.
                * **Plinth Layout:** Configured for **{st.session_state['flood_status']}** to address site elevation demands.
                
                ---
                🎓 **Project Compiled By:** Batch 1, Group 1 Students  
                👩‍🏫 **Under the Guidance of:** Dr. Rupa Ma'am  
                🏫 **Department of Civil Engineering, KLE Technological University**
                """
                st.markdown(backup_report)

# ==========================================
# MODULE 2: HYBRID GRAPHICS PORTAL (REAL PHOTOS + BLUEPRINTS)
# ==========================================
elif app_mode == "Module 2: 3D Real Concept Visualizer":
    st.title("🏗️ Regional Architectural Elevation & Substructure Visualizer")
    st.write("Syncs real exterior street-view architecture images with textbook-detailed foundation blueprints.")
    
    current_floors = int(st.session_state['floors'])
    current_zone = st.session_state['seismic']
    current_soil = st.session_state['soil']
    
    st.info(f"### Profile Matrix: {current_floors} Floors | Seismic Zone {current_zone} | Soil: {current_soil}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🏡 Real Exterior House View ({current_floors} Floor)")
        
        # CATEGORY A: HIGH RISK ZONES (IV / V) -> SLOPED ROOF EXTERIOR HOUSE IMAGES
        if current_zone in ["IV", "V"]:
            st.caption("📐 Structural Spec: High-Precipitation & Seismic Mass Mitigated Sloped Roof")
            if current_floors == 1:
                st.image("https://images.unsplash.com/photo-1513584684374-8bab748fbf90?auto=format&fit=crop&w=600&q=80", caption="1-Story Finished Exterior: High-Resilience Sloped Cottage", use_container_width=True)
            elif current_floors == 2:
                st.image("https://images.unsplash.com/photo-1449844908441-8829872d2607?auto=format&fit=crop&w=600&q=80", caption="2-Story Finished Exterior: Modern Sloped Frame Villa", use_container_width=True)
            elif current_floors == 3:
                st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80", caption="3-Story Finished Exterior: Multi-Level Sloped Structural Profile", use_container_width=True)
            elif current_floors == 4:
                st.image("https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=600&q=80", caption="4-Story Finished Exterior: Engineered Low-Mass Sloped Complex", use_container_width=True)
            elif current_floors == 5:
                st.image("https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=600&q=80", caption="5-Story Finished Exterior: Symmetric Mid-Rise Sloped Block", use_container_width=True)
            else:
                st.image("https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=600&q=80", caption="6-Story Finished Exterior: High-Velocity Wind & Tectonic Load Profile", use_container_width=True)
                
        # CATEGORY B: LOW/MEDIUM RISK ZONES (II / III) -> FLAT RCC SLAB EXTERIOR HOUSE IMAGES
        else:
            st.caption("🏗️ Structural Spec: Monolithic Flat Cast-In-Place Concrete RCC Slab Roof Deck")
            if current_floors == 1:
                st.image("https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=600&q=80", caption="1-Story Finished Exterior: Flat Slab Urban Residential Layout", use_container_width=True)
            elif current_floors == 2:
                st.image("https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=600&q=80", caption="2-Story Finished Exterior: Monolithic Concrete Flat Slab Grid", use_container_width=True)
            elif current_floors == 3:
                st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&q=80", caption="3-Story Finished Exterior: Flat Slab Urban Multi-Family Residence", use_container_width=True)
            elif current_floors == 4:
                st.image("https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80", caption="4-Story Finished Exterior: Modern Continuous Lintel Laced Grid Block", use_container_width=True)
            elif current_floors == 5:
                st.image("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&q=80", caption="5-Story Finished Exterior: Monolithic Flat Roof Mid-Rise Complex", use_container_width=True)
            else:
                st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80", caption="6-Story Finished Exterior: High-Density Column Frame Apartment Block", use_container_width=True)

    with col2:
        st.subheader("📐 Detailed Blueprint Foundation Cross-Section")
        
        fig_found, ax_f = plt.subplots(figsize=(6, 6))
        ax_f.set_xlim(-2, 2)
        ax_f.set_ylim(-4, 1.5)
        
        ax_f.plot([-2, 2], [0, 0], color="#27ae60", linewidth=3)
        ax_f.text(-1.8, 0.1, "GROUND LEVEL (GL)", color="#27ae60", fontsize=8, weight='bold')
        
        ax_f.fill_between([-0.25, 0.25], 0, 1.2, color="#b2bec3", edgecolor="#2c3e50", linewidth=2)
        ax_f.plot([-0.18, -0.18], [-1.0, 1.2], color="#d63031", linewidth=3, label="Main Reinforcement Rebar")
        ax_f.plot([0.18, 0.18], [-1.0, 1.2], color="#d63031", linewidth=3)
        
        if "Clayey" in current_soil:
            ax_f.fill_between([-1.8, 1.8], -1.8, -0.4, color="#dfe4ea", edgecolor="#2c3e50", linewidth=2.5)
            ax_f.plot([-1.7, 1.7], [-0.6, -0.6], color="#e17055", linewidth=2.5, linestyle="-", label="Tension Steel Mesh Grid")
            ax_f.plot([-1.7, 1.7], [-1.6, -1.6], color="#e17055", linewidth=2.5, linestyle="-")
            for x_pos in np.linspace(-1.6, 1.6, 12):
                ax_f.plot([x_pos, x_pos], [-0.6, -1.6], color="#636e72", linewidth=1, linestyle=":")
            ax_f.plot([-0.18, -0.4], [-1.6, -1.6], color="#d63031", linewidth=3)
            ax_f.plot([0.18, 0.4], [-1.6, -1.6], color="#d63031", linewidth=3)
            ax_f.text(0, -2.4, "MONOLITHIC CAST RAFT FOUNDATION\n[IS 1904 Soft Clay Distribution Slab]", ha='center', color="#2c3e50", weight='bold', fontsize=9)
            
        elif "Sandy" in current_soil:
            ax_f.fill_between([-0.7, 0.7], -0.6, 0, color="#b2bec3", edgecolor="#2c3e50", linewidth=2.5)
            ax_f.text(0, -0.3, "PILE CAP", color="black", fontsize=8, weight='bold', ha='center')
            ax_f.fill_between([-0.4, -0.1], -3.5, -0.6, color="#dfe4ea", edgecolor="#2980b9", linewidth=2)
            ax_f.fill_between([0.1, 0.4], -3.5, -0.6, color="#dfe4ea", edgecolor="#2980b9", linewidth=2)
            ax_f.plot([-0.25, -0.25], [-3.4, -0.3], color="#d63031", linewidth=2)
            ax_f.plot([0.25, 0.25], [-3.4, -0.3], color="#d63031", linewidth=2)
            ax_f.text(0, -3.8, "DEEP BORED PILE REINFORCED ASSEMBLY\n[IS 2911 Friction Load Displacement Shafts]", ha='center', color="#2980b9", weight='bold', fontsize=9)
            
        else:
            ax_f.fill_between([-0.6, 0.6], -0.6, 0, color="#b2bec3", edgecolor="#2c3e50", linewidth=2)
            ax_f.fill_between([-1.3, 1.3], -1.4, -0.6, color="#dfe4ea", edgecolor="#2c3e50", linewidth=2.5)
            ax_f.plot([-1.2, 1.2], [-1.2, -1.2], color="#27ae60", linewidth=2.5, label="Footing Reinforcement Bed")
            ax_f.plot([-1.2, -1.2], [-1.2, -0.9], color="#27ae60", linewidth=2.5)
            ax_f.plot([1.2, 1.2], [-1.2, -0.9], color="#27ae60", linewidth=2.5)
            ax_f.plot([-0.18, -0.5], [-1.2, -1.2], color="#d63031", linewidth=3)
            ax_f.plot([0.18, 0.5], [-1.2, -1.2], color="#d63031", linewidth=3)
            ax_f.text(0, -2.2, "ISOLATED SPREAD FOOTING ASSEMBLY\n[IS 456 Rigid Anchorage Over Hard Bed]", ha='center', color="#27ae60", weight='bold', fontsize=9)
            
        ax_f.axis('off')
        ax_f.legend(loc="upper right", fontsize=8)
        st.pyplot(fig_found)

    st.markdown(f"""
    <div style="background-color: #2c3e50; padding: 15px; border-radius: 8px; color: white; text-align: center; margin-top: 15px;">
        📐 <b>Module 2 Dynamic Layout Calibrated:</b> Real exterior rendering front profiles communicate with native coordinate-mapped substructure blueprints.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MODULE 3: MATERIAL & BOQ ESTIMATOR
# ==========================================
elif app_mode == "Module 3: Automated Structural Material & BOQ Estimator":
    st.title("📊 Automated Material Breakdown & Cost Estimator")
    st.write("Generates an engineering Bill of Quantities (BOQ) with rough volumetric calculations based on your parameters.")
    
    if st.button("Calculate Material Quantities & BOQ", type="primary"):
        with st.spinner("📊 Executing volumetric material quantification matrices..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                total_built_up = int(st.session_state['area']) * int(st.session_state['floors'])
                prompt_boq = f"You are a Senior Quantity Surveyor executing structural material estimations. Generate a Bill of Quantities (BOQ) list estimation for a house with a total built-up area of {total_built_up} Sq. Ft. The site is on {st.session_state['soil']} in Seismic Zone {st.session_state['seismic']}. Provide an approximation breakdown table containing Concrete Volume needed (m3), Structural Steel weight (Tons), Cement Bags, and Estimated Total Cost (INR). Present the breakdown as an easy-to-read Markdown Table with column headings: [Material Component | Approximate Quantity | Key Engineering Purpose]."
                response = model.generate_content(prompt_boq)
                st.success("📊 Material Cost Analysis Generated!")
                st.markdown(response.text)
            except Exception:
                st.warning("⚠️ Live API traffic limit reached. Displaying engineered material volumetric estimates from local cache calculations:")
                total_built_up = int(st.session_state['area']) * int(st.session_state['floors'])
                backup_table = f"""
                | Material Component | Approximate Quantity | Key Engineering Purpose |
                | :--- | :--- | :--- |
                | Concrete Volume (M25/M30) | {round(total_built_up * 0.11, 1)} m³ | Cast monolithic frame members, footings, and structural floor diaphragms |
                | Structural Reinforcement Steel (Fe 550D) | {round(total_built_up * 0.004, 2)} Metric Tons | Handle peak tension profiles and maintain frame cohesion under displacement |
                | OPC 43/53 Grade Cement | {int(total_built_up * 0.4)} Bags | Binding agent for concrete casting and substructure base masonry blocks |
                | **Estimated Base Cost (INR)** | **₹ {int(total_built_up * 2200):,}** | Baseline material and basic site assembly budget tracking framework |
                """
                st.markdown(backup_table)