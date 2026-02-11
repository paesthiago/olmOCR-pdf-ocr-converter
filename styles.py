"""Estilos CSS para a aplicação Streamlit."""
import streamlit as st


def apply_custom_styles() -> None:
    """Aplica estilos CSS customizados à interface Streamlit."""
    st.markdown("""
        <style>
        .decipher-box {
            height: 600px;
            overflow-y: auto;
            padding: 15px;
            border: 1px solid #4b4b4b;
            border-radius: 8px;
            background-color: #0e1117;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            line-height: 1.5;
            color: #e0e0e0;
        }
        .stButton button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
