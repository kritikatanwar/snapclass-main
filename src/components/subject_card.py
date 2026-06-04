import streamlit as st

st.markdown("""
<style>

.subject-card{
    transition:0.25s ease;
}

.subject-card:hover{
    transform:translateY(-4px);
    box-shadow:inset 6px 0 0 #D9468F, 0 10px 22px rgba(0,0,0,0.10) !important;
}

</style>
""", unsafe_allow_html=True)


def subject_card(name, code, section, stats=None, footer_callback=None):

    html = f"""
    <div class="subject-card" style="background:#F5F3FF; padding:25px; border-radius:24px; border:1px solid #E4E4F5; box-shadow:inset 6px 0 0 #D9468F, 0 4px 10px rgba(0,0,0,0.05); margin-bottom:20px; width:100%; min-height:230px;">

    <h3 style="margin:0; color:#1E293B; font-size:1.5rem; font-weight:700;">
    📘 {name}
    </h3>

    <p style="color:#64748b; margin:14px 0; font-size:1rem;">
    Code :
    <span style="background:#E0E3FF; color:#5865F2; padding:4px 10px; border-radius:8px; font-weight:600;">{code}</span>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    Section :
    <span style="color:#1E293B; font-weight:600;">{section}</span>
    </p>
    """

    if stats:

        html += '<div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:10px;">'

        for icon, label, value in stats:

            html += f'<div style="background:#FCE7F3; padding:8px 14px; border-radius:14px; font-size:0.9rem; color:#1E293B; font-weight:500;">{icon} <b>{value}</b> {label}</div>'

        html += '</div>'

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()

        