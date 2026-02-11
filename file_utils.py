"""Utilitários para manipulação de arquivos."""
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Optional, List
import streamlit as st


def select_folder() -> Optional[str]:
    """
    Abre diálogo para seleção de pasta.
    
    Returns:
        Caminho da pasta selecionada ou None se cancelado
    """
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askdirectory(master=root)
        root.destroy()
        return path if path else None
    except Exception as e:
        st.error(f"Erro ao abrir seletor: {e}")
        return None


def get_pdf_files(folder_path: str) -> List[Path]:
    """
    Lista todos os arquivos PDF em uma pasta.
    
    Args:
        folder_path: Caminho da pasta a ser verificada
        
    Returns:
        Lista de objetos Path para arquivos PDF encontrados
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return []
    
    return [f for f in folder.iterdir() if f.suffix.lower() == '.pdf']


def create_output_directories(base_path: str, markdown_folder: str, images_folder: str) -> tuple[Path, Path]:
    """
    Cria diretórios de saída para markdown e imagens.
    
    Args:
        base_path: Caminho base
        markdown_folder: Nome da pasta de markdown
        images_folder: Nome da pasta de imagens
        
    Returns:
        Tupla com (caminho_markdown, caminho_imagens)
    """
    base = Path(base_path)
    markdown_dir = base / markdown_folder
    images_dir = markdown_dir / images_folder
    
    markdown_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    
    return markdown_dir, images_dir
