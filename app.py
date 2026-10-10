import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Google Maps Directory Scraper", page_icon="📍", layout="centered")

# Custom CSS for modern UI tweaks
st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .stButton>button { width: 100%; font-weight: bold; }
    div[data-testid="stCodeBlock"] { border-radius: 8px; border: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

st.title("📍 Google Maps Directory Scraper")
st.markdown("Extract business listings directly into Excel with ease.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    city = st.text_input("City (شهر)", placeholder="e.g., Isfahan")
with col2:
    category = st.text_input("Business Category (حوزه فعالیت)", placeholder="e.g., شرکت حسابداری")

if st.button("🚀 Start Scraping", type="primary"):
    if not city or not category:
        st.error("Please enter both City and Business Category.")
    else:
        st.info(f"Scraping '{category}' in '{city}'. The browser window will open shortly...")
        
        # Real-time console output container
        status_box = st.empty()
        log_text = ""
        
        # Prepare environment to stream stdout unbuffered
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        # Run the existing scraper as a subprocess
        cmd = ["python", "execution/scrape_google_maps.py", "--city", city, "--category", category]
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            encoding='utf-8', 
            bufsize=1, 
            env=env
        )
        
        # Stream the output line-by-line
        for line in iter(process.stdout.readline, ''):
            log_text += line
            # Keep only the last 15 lines so the UI doesn't blow up
            display_text = "\n".join(log_text.splitlines()[-15:])
            status_box.code(display_text, language="bash")
            
        process.stdout.close()
        return_code = process.wait()
        
        if return_code == 0:
            st.success("✅ Scraping Completed Successfully!")
            st.balloons()
            
            # Look for the generated Excel file
            out_path = os.path.join(".tmp", "google_maps_directory_output.xlsx")
            if os.path.exists(out_path):
                with open(out_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Excel File",
                        data=file,
                        file_name=f"{city}_{category}_maps_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning("No data was extracted or the file was not found.")
        else:
            st.error("❌ An error occurred during scraping. Check the terminal logs above.")
