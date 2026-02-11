"""Configurações centralizadas da aplicação."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    """Configurações da aplicação."""
    
    # API Configuration
    model_name: str = "olmocr-2-7b-1025"
    default_api_url: str = "http://localhost:1234/v1"
    api_key: str = "lm-studio"
    api_timeout: float = 600.0
    
    # Poppler Configuration
    poppler_default_path: str = r"C:\poppler\Library\bin"
    
    # Image Processing
    default_dpi: int = 150
    min_dpi: int = 72
    max_dpi: int = 300
    image_quality: int = 85
    
    # Output Directories
    output_folder_name: str = "Markdown_Outputs"
    images_folder_name: str = "images"
    
    # OCR Prompt
    ocr_prompt: str = (
        "Attached is one page of a document that you must process. "
        "Convert equations to LaTeX and tables to HTML."
    )
    
    @property
    def output_path(self) -> Path:
        """Retorna o caminho completo da pasta de saída."""
        return Path(self.output_folder_name)
    
    @property
    def images_path(self) -> Path:
        """Retorna o caminho completo da pasta de imagens."""
        return self.output_path / self.images_folder_name


# Singleton instance
config = AppConfig()
