"""Componentes de interface do Streamlit."""
import streamlit as st
from typing import Optional
from PIL import Image

from config import config
from session_state import SessionState
from file_utils import select_folder


class UIComponents:
    """Componentes reutilizáveis da interface."""
    
    @staticmethod
    def render_sidebar() -> tuple[str, str, int]:
        """
        Renderiza a barra lateral com configurações.
        
        Returns:
            Tupla com (api_url, poppler_path, dpi)
        """
        with st.sidebar:
            st.header("⚙️ Configurações")
            
            api_url = st.text_input("API URL", config.default_api_url)
            poppler_path = st.text_input("Poppler Path", config.poppler_default_path)
            dpi = st.slider("DPI (Qualidade)", config.min_dpi, config.max_dpi, config.default_dpi)
            
            st.divider()
            st.caption(f"Modelo: {config.model_name}")
            
            return api_url, poppler_path, dpi
    
    @staticmethod
    def render_folder_selector() -> Optional[str]:
        """
        Renderiza o seletor de pasta.
        
        Returns:
            Caminho da pasta ou None
        """
        col_sel, col_path, col_btn = st.columns([1, 3, 1])
        
        with col_sel:
            if st.button("📂 Escolher Pasta"):
                folder = select_folder()
                if folder:
                    SessionState.set_folder_path(folder)
                    st.rerun()
        
        with col_path:
            current_path = SessionState.get_folder_path()
            st.text_input(
                "Pasta Atual",
                value=current_path,
                disabled=True,
                label_visibility="collapsed"
            )
        
        with col_btn:
            folder_path = SessionState.get_folder_path()
            start_process = st.button(
                "🚀 Iniciar",
                type="primary",
                disabled=not folder_path
            )
        
        return folder_path if start_process else None
    
    @staticmethod
    def create_display_placeholders() -> tuple:
        """
        Cria placeholders para visualização.
        
        Returns:
            Tupla com (image_placeholder, text_placeholder)
        """
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.markdown("**Visualização da Página**")
            img_placeholder = st.empty()
        
        with col2:
            st.markdown("**Texto Extraído (Markdown/LaTeX)**")
            txt_placeholder = st.empty()
        
        return img_placeholder, txt_placeholder
    
    @staticmethod
    def display_last_state(img_placeholder, txt_placeholder, should_display: bool) -> None:
        """
        Exibe o último estado processado ou página atual do histórico.
        
        Args:
            img_placeholder: Placeholder da imagem
            txt_placeholder: Placeholder do texto
            should_display: Se deve exibir o estado
        """
        folder_path = SessionState.get_folder_path()
        
        # Se temos páginas no histórico, exibe a página atual
        if SessionState.has_pages():
            current_page = SessionState.get_current_page()
            if current_page:
                img_placeholder.image(current_page["image"], width="stretch")
                UIComponents.render_text_box(txt_placeholder, current_page["text"])
        # Caso contrário, usa o comportamento antigo
        elif should_display:
            last_image = SessionState.get_last_image()
            last_text = SessionState.get_last_text()
            if last_image:
                img_placeholder.image(last_image, width="stretch")
                txt_placeholder.markdown(
                    f'<div class="decipher-box">{last_text}</div>',
                    unsafe_allow_html=True
                )
        elif not folder_path:
            txt_placeholder.info("Selecione uma pasta para começar.")
    
    @staticmethod
    def render_navigation_controls(placeholder=None) -> None:
        """
        Renderiza controles de navegação para páginas processadas.
        
        Args:
            placeholder: Placeholder opcional para renderizar os controles
        """
        # Só exibe controles quando houver pelo menos uma página completa
        if not SessionState.has_pages() or len(SessionState.get_pages()) == 0:
            return
        
        pages = SessionState.get_pages()
        current_index = SessionState.get_current_page_index()
        current_page = pages[current_index]
        
        # Define onde renderizar (placeholder ou st diretamente)
        parent = placeholder.container() if placeholder else st
        
        with parent:
            # Layout de navegação
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                # Botão "Anterior"
                if st.button("◀ Anterior", disabled=(current_index == 0), use_container_width=True, key=f"prev_{len(pages)}"):
                    SessionState.set_current_page_index(current_index - 1)
                    st.rerun()
            
            with col2:
                # Informações da página
                st.markdown(
                    f"<div style='text-align: center; padding: 8px;'>"
                    f"<strong>Página {current_page['page_num']} de {len(pages)}</strong><br>"
                    f"<small>{current_page['filename']}</small>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            with col3:
                # Botão "Próxima"
                if st.button("Próxima ▶", disabled=(current_index == len(pages) - 1), use_container_width=True, key=f"next_{len(pages)}"):
                    SessionState.set_current_page_index(current_index + 1)
                    st.rerun()
    
    @staticmethod
    def render_text_box(placeholder, text: str) -> None:
        """
        Renderiza texto em uma caixa estilizada.
        
        Args:
            placeholder: Placeholder do Streamlit
            text: Texto a ser renderizado
        """
        placeholder.markdown(
            f'<div class="decipher-box">{text}</div>',
            unsafe_allow_html=True
        )
