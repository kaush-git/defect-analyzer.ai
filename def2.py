import os
import streamlit as st 
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from PIL import Image
import datetime

# Enhanced page configuration
st.set_page_config(
    page_title='AI Structural Defect Analyzer',
    page_icon='🏗️',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Enhanced CSS with improved color scheme
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #2d3748 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 50%, #1e40af 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Feature cards with gradient backgrounds */
    .feature-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.8rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(148, 163, 184, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .feature-card strong {
        color: #1e40af;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .feature-card small {
        color: #475569;
        line-height: 1.5;
    }
    
    /* Result container */
    .result-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2.5rem;
        border-radius: 15px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    }
    
    
    /* Button improvements */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 2px dashed #3b82f6;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    
    .stFileUploader label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    /* Selectbox and slider styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
        border: 1px solid #4b5563;
        border-radius: 8px;
        color: #f9fafb;
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
    }
    
    /* Success boxes */
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 4px solid #10b981;
        border-radius: 8px;
    }
    
    /* Error boxes */
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
    }
    
    /* Severity indicators */
    .severity-high {
        border-left: 4px solid #ef4444;
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #7f1d1d;
    }
    
    .severity-medium {
        border-left: 4px solid #f59e0b;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #78350f;
    }
    
    .severity-low {
        border-left: 4px solid #10b981;
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #064e3b;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    /* Column headers */
    .stSubheader {
        color: #1e40af;
        font-weight: 600;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Footer styling */
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #94a3b8;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 3rem;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced header
st.markdown("""
<div class="main-header">
    <h1>🏗️ AI Structural Defect Detection & Analysis System</h1>
    <p>Advanced AI-powered solution for automated structural inspection and analysis</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("🔧 Analysis Configuration")
    
    analysis_type = st.selectbox(
        "Select Analysis Type:",
        ["General Structural Analysis", "Concrete Defects", "Steel Structure Issues", 
         "Bridge Inspection", "Building Facade", "Foundation Problems"]
    )
    
    severity_threshold = st.select_slider(
        "Detection Sensitivity:",
        options=["Low", "Medium", "High", "Very High"],
        value="High"
    )
    
    include_recommendations = st.checkbox("Include Repair Recommendations", value=True)
    include_cost_estimate = st.checkbox("Include Cost Estimation", value=False)
    generate_report = st.checkbox("Generate Detailed Report", value=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📤 Upload Structural Image")
    
    # Enhanced file uploader
    input_image = st.file_uploader(
        'Select an image for analysis',
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Supported formats: PNG, JPG, JPEG, WebP. Max size: 200MB"
    )
    
    if input_image is not None:
        img = Image.open(input_image)
        st.image(img, caption=f'Uploaded: {input_image.name}', use_column_width=True)
        
        # Image info
        st.info(f"📊 Image Info: {img.size[0]}x{img.size[1]} pixels, Format: {img.format}")

with col2:
    st.subheader("📊 Analysis Configuration")
    st.write("Use the sidebar to configure analysis settings")

# Enhanced expandable section
with st.expander("📚 About This Application", expanded=False):
    st.markdown("""
    ### 🎯 Purpose
    This advanced AI system specializes in detecting and analyzing structural defects in construction and infrastructure projects.
    
    ### 🔬 Technology
    - **AI Model**: Google Gemini 2.0 Flash for image analysis
    - **Detection Types**: Cracks, corrosion, spalling, deformation, and more
    - **Analysis Scope**: Buildings, bridges, tunnels, and other structures
    
    ### 📈 Capabilities
    - **Multi-defect Detection**: Identifies various types of structural issues
    - **Severity Classification**: Categorizes defects by urgency and risk
    - **Professional Reporting**: Generates inspection-ready documentation
    - **Maintenance Planning**: Provides prioritized repair recommendations
    """)

# Analysis section
if input_image is not None:
    if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
        with st.spinner("🔄 Analyzing structural defects..."):
            # Enhanced prompt based on configuration
            base_prompt = f"""
            You are an expert structural engineer and defect detection specialist. Analyze the uploaded image for structural defects with the following specifications:

            **ANALYSIS TYPE**: {analysis_type}
            **DETECTION SENSITIVITY**: {severity_threshold}
            
            **ANALYSIS REQUIREMENTS**:
            1. **Defect Identification**: Systematically scan the image and identify ALL visible structural defects including:
               - Cracks (hairline, structural, settlement)
               - Corrosion and rust stains
               - Spalling and concrete deterioration  
               - Deformation and misalignment
               - Joint failures and separations
               - Surface damage and weathering
               - Water damage and staining
               - Structural displacement
            
            2. **Detailed Assessment**: For each defect found, provide:
               - Exact location description
               - Defect type and classification
               - Severity level (Critical/High/Medium/Low)
               - Potential causes
               - Immediate safety concerns
            
            3. **Technical Analysis**: Include:
               - Structural integrity assessment
               - Load-bearing capacity concerns
               - Progressive deterioration risks
               - Environmental factors contributing to defects
            
            4. **Risk Prioritization**: Rank defects by:
               - Safety risk level
               - Urgency of repair needed
               - Potential for progression
               - Impact on overall structural integrity
            """
            
            if include_recommendations:
                base_prompt += """
            
            5. **Repair Recommendations**: Provide specific:
               - Immediate temporary measures
               - Permanent repair solutions
               - Recommended materials and methods
               - Professional expertise required
               - Timeline for repairs
            """
            
            if include_cost_estimate:
                base_prompt += """
            
            6. **Cost Estimation**: Provide preliminary cost ranges for:
               - Emergency repairs
               - Permanent solutions
               - Material costs
               - Labor requirements
            """
            
            if generate_report:
                base_prompt += """
            
            7. **Professional Report Format**: Structure your response as:
               - Executive Summary
               - Detailed Findings
               - Risk Assessment
               - Recommendations
               - Next Steps
            """
            
            base_prompt += """
            
            **OUTPUT FORMAT**: Provide a comprehensive, professional analysis that would be suitable for:
            - Engineering documentation
            - Insurance reports
            - Maintenance planning
            - Safety compliance
            
            **IMPORTANT**: If no defects are visible, state this clearly and provide a general structural condition assessment.
            Be specific, technical, and actionable in all recommendations.
            """
            
            # API configuration and call
            key = os.getenv('GOOGLE_API_KEY')
            if not key:
                st.error("⚠️ Google API key not found. Please check your environment variables.")
                st.stop()
                
            genai.configure(api_key=key)
            
            try:
                gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
                if img is not None:
                    response = gemini_model.generate_content([base_prompt, img])
                else:
                    st.error("❌ Image not loaded properly. Please try uploading again.")
                    st.stop()
                
                # Enhanced results display
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.subheader("🔍 Analysis Results")
                st.markdown("---")
                
                # Display timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.caption(f"Analysis completed at: {timestamp}")
                
                # Main results
                if response and response.text:
                    st.markdown(response.text)
                else:
                    st.warning("⚠️ No response generated. Please try again.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📥 Download Report"):
                        # Create downloadable report
                        if response and response.text:
                            report_content = f"""
STRUCTURAL DEFECT ANALYSIS REPORT
Generated: {timestamp}
Image: {input_image.name}
Analysis Type: {analysis_type}
Sensitivity: {severity_threshold}

{response.text}
                            """
                            st.download_button(
                                label="📄 Download Full Report",
                                data=report_content,
                                file_name=f"defect_analysis_{timestamp.replace(':', '-').replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error("No report to download")
                
                with col2:
                    if st.button("🔄 Re-analyze"):
                        st.rerun()
                
                with col3:
                    if st.button("📧 Share Results"):
                        st.info("Feature coming soon: Email sharing functionality")
                        
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("Please check your API key and try again.")

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <h4 style="color: #e2e8f0; margin-bottom: 1rem;">🏗️ AI Structural Defect Detection System</h4>
    <p style="margin-bottom: 0.5rem;">Powered by Google Gemini AI | Advanced Computer Vision Technology</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">⚠️ This tool provides preliminary analysis. Always consult with certified structural engineers for critical assessments.</p>
</div>
""", unsafe_allow_html=True)