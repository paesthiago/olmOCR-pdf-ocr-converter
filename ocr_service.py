"""Serviço de OCR usando OpenAI API."""
import base64
import io
from typing import Iterator, Optional
from PIL import Image
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk

from config import config


class OCRService:
    """Serviço responsável pela comunicação com a API de OCR."""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Inicializa o serviço de OCR.
        
        Args:
            base_url: URL base da API (usa config se não especificado)
            api_key: Chave da API (usa config se não especificado)
        """
        self.base_url = base_url or config.default_api_url
        self.api_key = api_key or config.api_key
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=config.api_timeout
        )
    
    @staticmethod
    def encode_image(image: Image.Image) -> str:
        """
        Codifica uma imagem PIL em base64.
        
        Args:
            image: Imagem PIL a ser codificada
            
        Returns:
            String base64 da imagem
        """
        buffered = io.BytesIO()
        
        # Converte para RGB se necessário
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        image.save(buffered, format="JPEG", quality=config.image_quality)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    def process_image(self, image: Image.Image, prompt: Optional[str] = None) -> Iterator[ChatCompletionChunk]:
        """
        Processa uma imagem usando a API de OCR.
        
        Args:
            image: Imagem PIL a ser processada
            prompt: Prompt customizado (usa config se não especificado)
            
        Returns:
            Iterator de chunks de resposta da API
        """
        image_base64 = self.encode_image(image)
        ocr_prompt = prompt or config.ocr_prompt
        
        return self.client.chat.completions.create(
            model=config.model_name,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": ocr_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    }
                ],
            }],
            stream=True,
            stream_options={"include_usage": True}
        )
