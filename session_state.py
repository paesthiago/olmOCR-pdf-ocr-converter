"""Gerenciamento de estado da sessão Streamlit."""
from typing import Optional
from PIL import Image
import streamlit as st


class SessionState:
    """Gerencia o estado da sessão Streamlit."""
    
    # Chaves de estado
    FOLDER_PATH = 'folder_path'
    LAST_TEXT = 'last_text'
    LAST_IMAGE = 'last_image'
    PAGES_HISTORY = 'pages_history'
    CURRENT_PAGE_INDEX = 'current_page_index'
    OUTPUT_FOLDER_NAME = 'output_folder_name'
    
    @classmethod
    def initialize(cls) -> None:
        """Inicializa todas as variáveis de estado necessárias."""
        if cls.FOLDER_PATH not in st.session_state:
            st.session_state[cls.FOLDER_PATH] = ""
        
        if cls.OUTPUT_FOLDER_NAME not in st.session_state:
             st.session_state[cls.OUTPUT_FOLDER_NAME] = "" # Inicializa vazio

        if cls.LAST_TEXT not in st.session_state:
            st.session_state[cls.LAST_TEXT] = ""
        
        if cls.LAST_IMAGE not in st.session_state:
            st.session_state[cls.LAST_IMAGE] = None
        
        if cls.PAGES_HISTORY not in st.session_state:
            st.session_state[cls.PAGES_HISTORY] = []
        
        if cls.CURRENT_PAGE_INDEX not in st.session_state:
            st.session_state[cls.CURRENT_PAGE_INDEX] = 0
            
        # Variáveis de controle de processamento
        if 'is_processing' not in st.session_state:
            st.session_state['is_processing'] = False
        
        if 'processing_queue' not in st.session_state:
            st.session_state['processing_queue'] = []
            
        if 'proc_file_index' not in st.session_state:
            st.session_state['proc_file_index'] = 0
            
        if 'proc_page_index' not in st.session_state:
            st.session_state['proc_page_index'] = 1  # 1-based index
            
        if 'total_pages_current_file' not in st.session_state:
            st.session_state['total_pages_current_file'] = 0
    
    @classmethod
    def get_output_folder_name(cls) -> str:
        """Retorna o nome da pasta de saída atual."""
        return st.session_state.get(cls.OUTPUT_FOLDER_NAME, "")

    @classmethod
    def get_folder_path(cls) -> str:
        """Retorna o caminho da pasta selecionada."""
        return st.session_state.get(cls.FOLDER_PATH, "")
    
    @classmethod
    def set_folder_path(cls, path: str) -> None:
        """Define o caminho da pasta."""
        st.session_state[cls.FOLDER_PATH] = path
    
    @classmethod
    def get_last_text(cls) -> str:
        """Retorna o último texto processado."""
        return st.session_state.get(cls.LAST_TEXT, "")
    
    @classmethod
    def set_last_text(cls, text: str) -> None:
        """Define o último texto processado."""
        st.session_state[cls.LAST_TEXT] = text
    
    @classmethod
    def get_last_image(cls) -> Optional[Image.Image]:
        """Retorna a última imagem processada."""
        return st.session_state.get(cls.LAST_IMAGE)
    
    @classmethod
    def set_last_image(cls, image: Image.Image) -> None:
        """Define a última imagem processada."""
        st.session_state[cls.LAST_IMAGE] = image
    
    @classmethod
    def update_last_state(cls, text: str, image: Image.Image) -> None:
        """Atualiza texto e imagem de uma vez."""
        cls.set_last_text(text)
        cls.set_last_image(image)
    
    # Page history methods
    @classmethod
    def add_page(cls, image: Image.Image, text: str, page_num: int, filename: str) -> None:
        """
        Adiciona uma página ao histórico.
        
        Args:
            image: Imagem da página
            text: Texto extraído
            page_num: Número da página
            filename: Nome do arquivo PDF
        """
        page_data = {
            "image": image,
            "text": text,
            "page_num": page_num,
            "filename": filename
        }
        st.session_state[cls.PAGES_HISTORY].append(page_data)
        
        # SÓ atualiza o índice se for a PRIMEIRA página adicionada
        # Isso evita que a visualização mude enquanto o usuário lê páginas anteriores
        if len(st.session_state[cls.PAGES_HISTORY]) == 1:
            st.session_state[cls.CURRENT_PAGE_INDEX] = 0
    
    @classmethod
    def get_pages(cls) -> list:
        """Retorna todas as páginas armazenadas."""
        return st.session_state.get(cls.PAGES_HISTORY, [])
    
    @classmethod
    def get_current_page_index(cls) -> int:
        """Retorna o índice da página atual."""
        return st.session_state.get(cls.CURRENT_PAGE_INDEX, 0)
    
    @classmethod
    def set_current_page_index(cls, index: int) -> None:
        """Define o índice da página atual."""
        pages = cls.get_pages()
        if 0 <= index < len(pages):
            st.session_state[cls.CURRENT_PAGE_INDEX] = index
    
    @classmethod
    def clear_pages(cls) -> None:
        """Limpa todas as páginas armazenadas."""
        st.session_state[cls.PAGES_HISTORY] = []
        st.session_state[cls.CURRENT_PAGE_INDEX] = 0
    
    @classmethod
    def has_pages(cls) -> bool:
        """Verifica se existem páginas armazenadas."""
        return len(st.session_state.get(cls.PAGES_HISTORY, [])) > 0
    
    @classmethod
    def get_current_page(cls) -> Optional[dict]:
        """Retorna a página atual baseada no índice."""
        pages = cls.get_pages()
        index = cls.get_current_page_index()
        if 0 <= index < len(pages):
            return pages[index]
        return None

    # Processing control methods
    @classmethod
    def start_processing(cls, files: list) -> None:
        """Inicia o processamento de uma lista de arquivos."""
        from datetime import datetime
        
        st.session_state['is_processing'] = True
        st.session_state['processing_queue'] = files
        st.session_state['proc_file_index'] = 0
        st.session_state['proc_page_index'] = 1
        st.session_state['total_pages_current_file'] = 0
        
        # Gera nome de pasta único com timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        st.session_state[cls.OUTPUT_FOLDER_NAME] = f"Markdown_Outputs_{timestamp}"
        
        cls.clear_pages()  # Limpa histórico anterior
    
    @classmethod
    def stop_processing(cls) -> None:
        """Para o processamento."""
        st.session_state['is_processing'] = False
        st.session_state['processing_queue'] = []
    
    @classmethod
    def is_processing(cls) -> bool:
        """Verifica se está processando."""
        return st.session_state.get('is_processing', False)
    
    @classmethod
    def get_processing_state(cls) -> dict:
        """Retorna o estado atual do processamento."""
        return {
            'file_index': st.session_state.get('proc_file_index', 0),
            'page_index': st.session_state.get('proc_page_index', 1),
            'queue': st.session_state.get('processing_queue', []),
            'total_pages': st.session_state.get('total_pages_current_file', 0)
        }
    
    @classmethod
    def update_processing_state(cls, file_index: int, page_index: int, total_pages: int = None) -> None:
        """Atualiza o estado do processamento."""
        st.session_state['proc_file_index'] = file_index
        st.session_state['proc_page_index'] = page_index
        if total_pages is not None:
            st.session_state['total_pages_current_file'] = total_pages

