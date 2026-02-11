"""
olmOCR Dashboard - Aplicação Streamlit para OCR de documentos PDF.

Esta aplicação processa arquivos PDF usando OCR (Optical Character Recognition),
convertendo equações para LaTeX e tabelas para HTML.
"""
import streamlit as st
from pathlib import Path

from config import config
from styles import apply_custom_styles
from session_state import SessionState
from ui_components import UIComponents
from file_utils import get_pdf_files, create_output_directories
from ocr_service import OCRService
from document_processor import DocumentProcessor


def process_next_step(
    api_url: str,
    poppler_path: str,
    dpi: int,
    img_placeholder,
    txt_placeholder,
    status_bar
) -> None:
    """
    Executa um passo do processamento (uma página).
    """
    state_info = SessionState.get_processing_state()
    queue = state_info['queue']
    file_idx = state_info['file_index']
    page_idx = state_info['page_index']
    
    # Se terminou a fila
    if file_idx >= len(queue):
        SessionState.stop_processing()
        status_bar.update(label="✅ Processamento concluído!", state="complete", expanded=False)
        st.success("Todos os documentos foram processados!")
        return

    current_file = queue[file_idx]
    
    # Inicializa serviços (poderia ser cacheado, mas é rápido)
    ocr_service = OCRService(base_url=api_url)
    processor = DocumentProcessor(ocr_service, dpi=dpi, poppler_path=poppler_path)
    
    # Se for a primeira página do arquivo, inicializa contadores
    total_pages = state_info['total_pages']
    
    # Recupera nome da pasta de saída
    output_folder_name = SessionState.get_output_folder_name()
    
    # Se por algum motivo o nome não estiver no estado (ex: reinício inesperado), gera um novo AGORA
    if not output_folder_name:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_folder_name = f"Markdown_Outputs_{timestamp}"
        # Salva no estado para os próximos chunks
        if SessionState.OUTPUT_FOLDER_NAME in st.session_state:
             st.session_state[SessionState.OUTPUT_FOLDER_NAME] = output_folder_name
    
    if page_idx == 1 and total_pages == 0:
        total_pages = processor.get_pdf_page_count(current_file)
        SessionState.update_processing_state(file_idx, page_idx, total_pages)
        
        # Cria diretórios apenas uma vez por arquivo
        create_output_directories(
            current_file.parent,
            output_folder_name,
            config.images_folder_name
        )
    
    # Atualiza status visual
    status_bar.write(f"📄 Processando: **{current_file.name}** - Página {page_idx}/{total_pages}...")
    
    try:
        # Define diretório de imagens
        _, images_dir = create_output_directories(
            current_file.parent,
            output_folder_name,
            config.images_folder_name
        )
        
        # Processa página única
        image, text = processor.process_single_page(
            current_file,
            page_idx,
            images_dir
        )
        
        # Adiciona ao histórico e estado (isso permite navegação imediata para esta página)
        SessionState.add_page(image, text, page_idx, current_file.name)
        
        # Atualiza display APENAS se for a primeira página (para dar feedback inicial)
        # Nas próximas, deixamos o usuário onde ele está
        if SessionState.get_current_page_index() == 0 and len(SessionState.get_pages()) == 1:
             img_placeholder.image(image, caption=f"{current_file.name} - Pág {page_idx}", width="stretch")
             UIComponents.render_text_box(txt_placeholder, text)
        
        # Salva o markdown (append)
        markdown_dir, _ = create_output_directories(
            current_file.parent,
            output_folder_name,
            config.images_folder_name
        )
        output_md_path = markdown_dir / f"{current_file.stem}.md"
        
        # Lê existente ou cria novo
        existing_md = output_md_path.read_text(encoding="utf-8") if output_md_path.exists() and page_idx > 1 else ""
        new_md_chunk = f"## Página {page_idx}\n\n{text}\n\n---\n\n"
        output_md_path.write_text(existing_md + new_md_chunk, encoding="utf-8")
        
        # Avança contadores
        next_page = page_idx + 1
        next_file = file_idx
        next_total = total_pages
        
        if next_page > total_pages:
            next_file += 1
            next_page = 1
            next_total = 0 # Vai recalcular para o próximo arquivo
        
        SessionState.update_processing_state(next_file, next_page, next_total)
        
        # Força rerun para processar próximo chunk
        st.rerun()
        
    except Exception as e:
        status_bar.error(f"❌ Erro ao processar {current_file.name} pág {page_idx}: {e}")
        SessionState.stop_processing()


def main() -> None:
    """Função principal da aplicação."""
    # Configuração da página
    st.set_page_config(
        page_title="olmOCR Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Aplica estilos e inicializa estado
    apply_custom_styles()
    SessionState.initialize()
    
    # Título
    st.title("📄 olmOCR: Experimento")
    
    # Sidebar com configurações
    api_url, poppler_path, dpi = UIComponents.render_sidebar()
    
    # Seletor de pasta e botão iniciar
    folder_to_process = UIComponents.render_folder_selector()
    
    # Se o usuário clicou em iniciar (folder_to_process retornou path), iniciamos o estado
    if folder_to_process and not SessionState.is_processing():
         pdf_files = get_pdf_files(folder_to_process)
         if pdf_files:
             SessionState.start_processing(pdf_files)
             st.rerun()
         else:
             st.warning("Nenhum PDF encontrado.")

    st.divider()
    
    # Placeholder para controles de navegação
    nav_placeholder = st.empty()
    
    # Controles de navegação (Sempre renderiza se tiver páginas, independente do processamento)
    UIComponents.render_navigation_controls(nav_placeholder)
    
    # Área de visualização
    img_placeholder, txt_placeholder = UIComponents.create_display_placeholders()
    
    # Exibe último estado/página atual
    # Se estiver processando, o chunk vai atualizar. Se não, mostramos o atual.
    if SessionState.has_pages():
        current_page = SessionState.get_current_page()
        if current_page:
            img_placeholder.image(current_page["image"], width="stretch")
            UIComponents.render_text_box(txt_placeholder, current_page["text"])
    
    # Lógica de Loop de Processamento
    if SessionState.is_processing():
        status_bar = st.status("Processando...", expanded=True)
        
        # DEBUG: Verify state
        # folder_name = SessionState.get_output_folder_name()
        # cur_idx = SessionState.get_current_page_index()
        # st.write(f"DEBUG: Folder='{folder_name}', Index={cur_idx}")
        
        process_next_step(
            api_url,
            poppler_path,
            dpi,
            img_placeholder,
            txt_placeholder,
            status_bar
        )


if __name__ == "__main__":
    main()