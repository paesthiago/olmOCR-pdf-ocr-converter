"""Processador de documentos PDF para OCR."""
import re
from pathlib import Path
from typing import Callable, Optional
from PIL import Image
from pdf2image import convert_from_path, pdfinfo_from_path

from ocr_service import OCRService
from config import config


class DocumentProcessor:
    """Processa documentos PDF usando OCR."""
    
    def __init__(self, ocr_service: OCRService, dpi: int = None, poppler_path: Optional[str] = None):
        """
        Inicializa o processador de documentos.
        
        Args:
            ocr_service: Instância do serviço de OCR
            dpi: DPI para conversão de PDF (usa config se não especificado)
            poppler_path: Caminho do Poppler (usa config se não especificado)
        """
        self.ocr_service = ocr_service
        self.dpi = dpi or config.default_dpi
        self.poppler_path = poppler_path or config.poppler_default_path
    
    def convert_pdf_to_images(self, pdf_path: Path) -> list[Image.Image]:
        """
        Converte um PDF em lista de imagens.
        
        Args:
            pdf_path: Caminho do arquivo PDF
            
        Returns:
            Lista de imagens PIL
        """
        return convert_from_path(
            str(pdf_path),
            dpi=self.dpi,
            poppler_path=self.poppler_path
        )
    
    def process_page(
        self,
        page_image: Image.Image,
        on_chunk: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        Processa uma única página usando OCR.
        
        Args:
            page_image: Imagem da página
            on_chunk: Callback chamado para cada chunk de texto recebido
            
        Returns:
            Texto completo extraído da página
        """
        stream = self.ocr_service.process_image(page_image)
        page_text = ""
        
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                page_text += content
                
                if on_chunk:
                    on_chunk(page_text)
        
        return page_text
    
    @staticmethod
    def fix_image_references(markdown_text: str, image_filename: str, images_folder: str) -> str:
        """
        Substitui referências de imagens no markdown com caminhos locais.
        
        Args:
            markdown_text: Texto markdown original
            image_filename: Nome do arquivo de imagem
            images_folder: Nome da pasta de imagens
            
        Returns:
            Texto markdown com referências atualizadas
        """
        if "![" not in markdown_text:
            return markdown_text
        
        relative_path = f"{images_folder}/{image_filename}"
        return re.sub(r'!\[.*?\]\(.*?\)', f'![Imagem]({relative_path})', markdown_text)
    
    def process_document(
        self,
        pdf_path: Path,
        output_md_path: Path,
        output_images_dir: Path,
        on_page_start: Optional[Callable[[int, int, Image.Image], None]] = None,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_page_complete: Optional[Callable[[int, Image.Image, str], None]] = None
    ) -> str:
        """
        Processa um documento PDF completo.
        
        Args:
            pdf_path: Caminho do PDF
            output_md_path: Caminho para salvar o markdown
            output_images_dir: Diretório para salvar imagens
            on_page_start: Callback ao iniciar página (page_num, total_pages, image)
            on_chunk: Callback ao receber chunk de texto
            on_page_complete: Callback ao completar página (page_num, image, text)
            
        Returns:
            Markdown completo do documento
        """
        pages = self.convert_pdf_to_images(pdf_path)
        full_markdown = ""
        
        for page_idx, page_image in enumerate(pages, start=1):
            # Notifica início da página com a imagem para exibição imediata
            if on_page_start:
                on_page_start(page_idx, len(pages), page_image)
            
            # Processa OCR da página
            page_text = self.process_page(page_image, on_chunk)
            
            # Salva imagem se houver referências
            if "![" in page_text:
                image_filename = f"{pdf_path.stem}_p{page_idx}.png"
                image_path = output_images_dir / image_filename
                page_image.save(str(image_path))
                
                # Atualiza referências
                page_text = self.fix_image_references(
                    page_text,
                    image_filename,
                    config.images_folder_name
                )
            
            # Notifica conclusão da página com o texto final
            if on_page_complete:
                on_page_complete(page_idx, page_image, page_text)
            
            # Adiciona ao markdown completo
            full_markdown += f"## Página {page_idx}\n\n{page_text}\n\n---\n\n"
        
        # Salva arquivo markdown
        output_md_path.write_text(full_markdown, encoding="utf-8")
        
        return full_markdown

    def get_pdf_page_count(self, pdf_path: Path) -> int:
        """Retorna o número total de páginas do PDF."""
        try:
            info = pdfinfo_from_path(str(pdf_path), poppler_path=self.poppler_path)
            return info["Pages"]
        except Exception:
            return 0

    def process_single_page(
        self,
        pdf_path: Path,
        page_num: int,
        output_images_dir: Path
    ) -> tuple[Image.Image, str]:
        """
        Processa uma única página de um PDF.
        
        Args:
            pdf_path: Caminho do PDF
            page_num: Número da página (1-based)
            output_images_dir: Diretório para salvar imagens
            
        Returns:
            Tupla (imagem, texto)
        """
        # Converte APENAS a página solicitada
        images = convert_from_path(
            str(pdf_path),
            dpi=self.dpi,
            poppler_path=self.poppler_path,
            first_page=page_num,
            last_page=page_num
        )
        
        if not images:
            raise ValueError(f"Não foi possível converter a página {page_num}")
            
        page_image = images[0]
        
        # Processa OCR
        page_text = self.process_page(page_image)
        
        # Salva imagem e corrige referências se necessário
        if "![" in page_text:
            image_filename = f"{pdf_path.stem}_p{page_num}.png"
            image_path = output_images_dir / image_filename
            page_image.save(str(image_path))
            
            page_text = self.fix_image_references(
                page_text,
                image_filename,
                config.images_folder_name
            )
            
        return page_image, page_text
