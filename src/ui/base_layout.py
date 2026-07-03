import streamlit as st


_HOME_BG_PATTERN = (
    "%3Csvg%20width%3D%221400%22%20height%3D%22900%22%20viewBox%3D%220%200%201400%20900%22%20"
    "xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Crect%20width%3D%221400%22%20height%3D%22900%22%20"
    "fill%3D%22%235865F2%22/%3E%3Cg%20fill%3D%22none%22%20stroke%3D%22%237B82F5%22%20stroke-width%3D%222.5%22%20"
    "stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%20opacity%3D%220.6%22%3E"
    
    # --- The Floating Animation Tag ---
    "%3CanimateTransform%20attributeName%3D%22transform%22%20type%3D%22translate%22%20values%3D%220%2C0%3B%200%2C-12%3B%200%2C0%22%20dur%3D%227s%22%20repeatCount%3D%22indefinite%22/%3E"
    
    # --- Original Icons ---
    "%3Cg%20transform%3D%22translate%28170%2C150%29%22%3E%20%3Cpath%20d%3D%22M-45%200%20L0%20-20%20L45%200%20L0%2020%20Z%22/%3E%20"
    "%3Cpath%20d%3D%22M-22%208%20L-22%2028%20Q0%2040%2022%2028%20L22%208%22/%3E%20"
    "%3Cline%20x1%3D%2238%22%20y1%3D%223%22%20x2%3D%2238%22%20y2%3D%2226%22/%3E%20"
    "%3Ccircle%20cx%3D%2238%22%20cy%3D%2231%22%20r%3D%223.5%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%2890%2C420%29%22%3E%20"
    "%3Cpath%20d%3D%22M-38%20-22%20Q-38%20-28%20-32%20-28%20L-4%20-28%20Q0%20-28%200%20-22%20L0%2024%20Q0%2018%20-4%2018%20L-32%2018%20Q-38%2018%20-38%2024%20Z%22/%3E%20"
    "%3Cpath%20d%3D%22M38%20-22%20Q38%20-28%2032%20-28%20L4%20-28%20Q0%20-28%200%20-22%20L0%2024%20Q0%2018%204%2018%20L32%2018%20Q38%2018%2038%2024%20Z%22/%3E%20"
    "%3Cline%20x1%3D%22-28%22%20y1%3D%22-16%22%20x2%3D%22-8%22%20y2%3D%22-16%22/%3E%20"
    "%3Cline%20x1%3D%22-28%22%20y1%3D%22-6%22%20x2%3D%22-8%22%20y2%3D%22-6%22/%3E%20"
    "%3Cline%20x1%3D%22-28%22%20y1%3D%224%22%20x2%3D%22-8%22%20y2%3D%224%22/%3E%20"
    "%3Cline%20x1%3D%228%22%20y1%3D%22-16%22%20x2%3D%2228%22%20y2%3D%22-16%22/%3E%20"
    "%3Cline%20x1%3D%228%22%20y1%3D%22-6%22%20x2%3D%2228%22%20y2%3D%22-6%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%281230%2C250%29%22%3E%20"
    "%3Cpath%20d%3D%22M-40%20-28%20L-26%20-28%20L-20%20-38%20L20%20-38%20L26%20-28%20L40%20-28%22/%3E%20"
    "%3Cpath%20d%3D%22M-40%20-28%20L-40%2028%20Q-40%2034%20-34%2034%20L34%2034%20Q40%2034%2040%2028%20L40%20-28%22/%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%222%22%20r%3D%2220%22/%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%222%22%20r%3D%2210%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%281300%2C470%29%22%3E%20"
    "%3Cpath%20d%3D%22M-30%20-42%20L30%20-42%20Q40%20-42%2040%20-32%20L40%2010%20Q40%2020%2030%2020%20L0%2020%20L-14%2036%20L-12%2020%20L-30%2020%20Q-40%2020%20-40%2010%20L-40%20-32%20Q-40%20-42%20-30%20-42%20Z%22/%3E%20"
    "%3Ccircle%20cx%3D%22-16%22%20cy%3D%22-11%22%20r%3D%222.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%22-11%22%20r%3D%222.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%2216%22%20cy%3D%22-11%22%20r%3D%222.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%28700%2C90%29%22%3E%20"
    "%3Cpath%20d%3D%22M-30%200%20Q-15%200%200%20-30%20Q15%200%2030%200%20Q15%200%200%2030%20Q-15%200%20-30%200%20Z%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%28440%2C260%29%22%3E%20"
    "%3Cpath%20d%3D%22M-14%200%20Q-7%200%200%20-14%20Q7%200%2014%200%20Q7%200%200%2014%20Q-7%200%20-14%200%20Z%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%28950%2C620%29%22%3E%20"
    "%3Cpath%20d%3D%22M-18%200%20Q-9%200%200%20-18%20Q9%200%2018%200%20Q9%200%200%2018%20Q-9%200%20-18%200%20Z%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%281080%2C120%29%22%20stroke-width%3D%222%22%3E%20"
    "%3Cline%20x1%3D%22-34%22%20y1%3D%220%22%20x2%3D%2234%22%20y2%3D%220%22/%3E%20"
    "%3Cline%20x1%3D%220%22%20y1%3D%22-34%22%20x2%3D%220%22%20y2%3D%2234%22/%3E%20"
    "%3Cline%20x1%3D%22-24%22%20y1%3D%22-24%22%20x2%3D%2224%22%20y2%3D%2224%22/%3E%20"
    "%3Cline%20x1%3D%22-24%22%20y1%3D%2224%22%20x2%3D%2224%22%20y2%3D%22-24%22/%3E%3C/g%3E"
    "%3Ccircle%20cx%3D%2260%22%20cy%3D%22280%22%20r%3D%226%22/%3E"
    "%3Ccircle%20cx%3D%221340%22%20cy%3D%22700%22%20r%3D%226%22/%3E"
    "%3Ccircle%20cx%3D%22610%22%20cy%3D%22430%22%20r%3D%225%22/%3E"
    "%3Ccircle%20cx%3D%22780%22%20cy%3D%22780%22%20r%3D%225%22/%3E"
    "%3Cg%20transform%3D%22translate%281170%2C800%29%20rotate%288%29%22%3E%20"
    "%3Crect%20x%3D%22-24%22%20y%3D%22-32%22%20width%3D%2248%22%20height%3D%2264%22%20rx%3D%223%22/%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%22-10%22%20r%3D%2210%22/%3E%20"
    "%3Cline%20x1%3D%22-14%22%20y1%3D%2214%22%20x2%3D%2214%22%20y2%3D%2214%22/%3E%20"
    "%3Cline%20x1%3D%22-14%22%20y1%3D%2222%22%20x2%3D%2214%22%20y2%3D%2222%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%28370%2C720%29%22%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%220%22%20r%3D%2230%22/%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%220%22%20r%3D%2214%22/%3E%20"
    "%3Cline%20x1%3D%2221%22%20y1%3D%2221%22%20x2%3D%2234%22%20y2%3D%2234%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%281240%2C40%29%22%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%220%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%2216%22%20cy%3D%220%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%2232%22%20cy%3D%220%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%2216%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%2216%22%20cy%3D%2216%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%2232%22%20cy%3D%2216%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%220%22%20cy%3D%2232%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%2216%22%20cy%3D%2232%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%20"
    "%3Ccircle%20cx%3D%2232%22%20cy%3D%2232%22%20r%3D%223.5%22%20fill%3D%22%237B82F5%22%20stroke%3D%22none%22/%3E%3C/g%3E"
    
    # --- New Added Icons (To increase density) ---
    "%3Cg%20transform%3D%22translate%28250%2C650%29%20scale%280.7%29%22%3E%20%3Cpath%20d%3D%22M-30%200%20Q-15%200%200%20-30%20Q15%200%2030%200%20Q15%200%200%2030%20Q-15%200%20-30%200%20Z%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%28150%2C800%29%20rotate%28-15%29%20scale%280.8%29%22%3E%20%3Crect%20x%3D%22-24%22%20y%3D%22-32%22%20width%3D%2248%22%20height%3D%2264%22%20rx%3D%223%22/%3E%20%3Ccircle%20cx%3D%220%22%20cy%3D%22-10%22%20r%3D%2210%22/%3E%20%3Cline%20x1%3D%22-14%22%20y1%3D%2214%22%20x2%3D%2214%22%20y2%3D%2214%22/%3E%20%3Cline%20x1%3D%22-14%22%20y1%3D%2222%22%20x2%3D%2214%22%20y2%3D%2222%22/%3E%3C/g%3E"
    "%3Cg%20transform%3D%22translate%28850%2C450%29%20scale%280.6%29%22%3E%20%3Cpath%20d%3D%22M-45%200%20L0%20-20%20L45%200%20L0%2020%20Z%22/%3E%20%3Cpath%20d%3D%22M-22%208%20L-22%2028%20Q0%2040%2022%2028%20L22%208%22/%3E%20%3Cline%20x1%3D%2238%22%20y1%3D%223%22%20x2%3D%2238%22%20y2%3D%2226%22/%3E%20%3Ccircle%20cx%3D%2238%22%20cy%3D%2231%22%20r%3D%223.5%22/%3E%3C/g%3E"
    
    "%3C/g%3E%3C/svg%3E"
)

def style_background_home():
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: #5865F2 !important;
            background-image: url("data:image/svg+xml,{_HOME_BG_PATTERN}") !important;
            background-repeat: no-repeat !important;
            background-size: cover !important;
            background-position: center !important;
        }}
        .stApp div[data-testid="stColumn"] {{
            background-color: #E0E3FF !important;
            padding: 2.5rem !important;
            border-radius: 5rem !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
        .stApp {
            background: #E0E3FF !important;
        }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

        #MainMenu, footer, header {
            visibility: hidden;
        }
        .block-container {
            padding-top: 1rem !important;
        }

        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
        }
        h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem !important;
            line-height: 0.9 !important;
            margin-bottom: 0rem !important;
            color: #343434 !important;
        }
        h3, h4, p {
            font-family: 'Outfit', sans-serif;
        }

        button {
            border-radius: 1.5rem !important;
            background-color: #5865F2 !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
        button[kind="secondary"] {
            border-radius: 1.5rem !important;
            background-color: #EB459E !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
        button[kind="tertiary"] {
            border-radius: 1.5rem !important;
            background-color: black !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
        button:hover {
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)


    