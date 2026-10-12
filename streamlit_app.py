"""
FinStart – FinTech Financial Super-App
Streamlit Deployment Entry Point
"""

import os
import subprocess
import streamlit as st
import streamlit.components.v1 as components

# Configure Streamlit page settings
st.set_page_config(
    page_title="FinStart – FinTech Financial Super-App",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for seamless fullscreen integration
st.markdown(
    """
    <style>
        /* Hide Streamlit default header decorations */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Maximize workspace viewport */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }

        /* Seamless iframe container */
        iframe {
            width: 100% !important;
            border: none !important;
            border-radius: 0px;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_INDEX_PATH = os.path.join(BASE_DIR, "dist", "index.html")

# Sidebar Information & Controls
with st.sidebar:
    st.markdown("### 🛡️ FinStart Project")
    st.caption("FinTech Financial Super-App • College Project")
    
    st.markdown(
        """
        **Educational Sandbox**:
        - 💳 ₹10,000 Virtual Wallet
        - 🎯 Targeted Savings Goals
        - 🧮 Loan & EMI Simulator
        - 📈 SIP Compounding Modeler
        - 🩺 100-Point Financial Health Score
        """
    )
    st.divider()

    app_height = st.slider(
        "Viewport Height (px)",
        min_value=750,
        max_value=1600,
        value=980,
        step=50,
        help="Adjust the display height for different screen sizes",
    )

    st.divider()
    st.markdown("##### 🚀 Deployment Info")
    st.caption(
        "Self-contained single-page bundle running inside Streamlit Components. "
        "Compatible with Streamlit Community Cloud, Docker, and local servers."
    )

    # Optional Rebuild button if Node is installed locally
    if st.button("🔨 Rebuild Frontend", help="Recompile React frontend with Vite"):
        with st.spinner("Building frontend..."):
            try:
                import shutil
                npm_bin = shutil.which("npm") or ("npm.cmd" if os.name == "nt" else "npm")
                env = os.environ.copy()
                local_node_bin = os.path.expanduser("~/.local/node/bin")
                if os.path.exists(local_node_bin):
                    env["PATH"] = f"{local_node_bin}:{env.get('PATH', '')}"
                
                result = subprocess.run(
                    [npm_bin, "run", "build"],
                    cwd=BASE_DIR,
                    env=env,
                    shell=(os.name == "nt"),
                    capture_output=True,
                    text=True,
                    check=True,
                )
                st.success("Frontend built successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Build failed: {e}")

def find_frontend_bundle():
    # 1. Standard production build location
    candidate = os.path.join(BASE_DIR, "dist", "index.html")
    if os.path.exists(candidate) and os.path.getsize(candidate) > 10000:
        return candidate

    # 2. Root bundle fallback (dist_index.html)
    candidate = os.path.join(BASE_DIR, "dist_index.html")
    if os.path.exists(candidate) and os.path.getsize(candidate) > 10000:
        return candidate

    # 3. Root index.html if it's the bundled production output (> 50KB)
    candidate = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(candidate) and os.path.getsize(candidate) > 50000:
        return candidate

    # 4. Search recursively for any built html file
    for root, dirs, files in os.walk(BASE_DIR):
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        if ".git" in dirs:
            dirs.remove(".git")
        for f in files:
            if f.endswith(".html"):
                p = os.path.join(root, f)
                try:
                    if os.path.getsize(p) > 50000:
                        return p
                except OSError:
                    pass
    return None

bundle_path = find_frontend_bundle()

if "uploaded_bundle_html" in st.session_state:
    html_content = st.session_state["uploaded_bundle_html"]
    components.html(html_content, height=app_height, scrolling=True)
elif bundle_path:
    with open(bundle_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=app_height, scrolling=True)
else:
    st.error("⚠️ Frontend build not found in GitHub repository!")
    st.markdown(
        """
        Streamlit Cloud could not locate the compiled `dist/index.html` or `dist_index.html` file in your repository.
        
        **Quick fix:** You can upload your local `dist_index.html` or `dist/index.html` right here to launch the app immediately:
        """
    )
    uploaded_file = st.file_uploader("Upload dist_index.html or dist/index.html", type=["html"])
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.session_state["uploaded_bundle_html"] = content
        # Also attempt to save locally for future runs
        try:
            with open(os.path.join(BASE_DIR, "dist_index.html"), "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass
        st.success("Bundle uploaded successfully! Loading app...")
        st.rerun()

    with st.expander("📁 Repository Diagnostics (Found files)"):
        try:
            st.write(os.listdir(BASE_DIR))
        except Exception as e:
            st.write(str(e))
