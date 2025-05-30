style = """
    <style>
        /* --- HARDCODED FONT SIZES --- */

        /* 1. Base font size for the entire app */
        html, body, .stApp, p {
            font-size: 14px;
        }

        /* 2. Headers */
        h1 { font-size: 32px !important; }
        h2 { font-size: 26px !important; }
        h3 { font-size: 22px !important; }

        /* 3. Sidebar */
        div[data-testid="stSidebar"] * {
            font-size: 16px;
        }

        /* 4. Tables */
        .gdg-header {
            background-color: #293846 !important;
        }
        
        /* This targets the text within the header */
        .gdg-header-title {
            font-size: 16px !important;
            font-weight: bold !important;
            color: white !important;
        }
        
        /* This targets the data cells of the grid */
        .gdg-cell {
            font-size: 14px !important;
        }
        
        /* 5. Specific Streamlit Widgets */
        label[data-testid="stWidgetLabel"] { /* Labels for sliders, selectboxes etc. */
            font-size: 17px !important;
            font-weight: 600; /* Makes labels slightly bolder */
        }
        div[data-testid="stMarkdown"] { /* Markdown text */
            font-size: 16px;
        }
        button[data-testid="stButton"] > p { /* Button text */
            font-size: 16px;
            font-weight: bold;
        }

        /* --- LAYOUT RULES --- */
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 75%;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        div[data-testid="stSidebarUserContent"] {
            padding-top: 2rem;
        }
    </style>
"""
