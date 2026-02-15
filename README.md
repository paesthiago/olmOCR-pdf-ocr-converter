# olmOCR Dashboard

Aplicação Streamlit para processamento de documentos PDF usando OCR (Optical Character Recognition).

## 🚀 Funcionalidades

- **OCR de PDFs**: Converte documentos PDF em texto markdown
- **Processamento de Equações**: Converte equações para formato LaTeX
- **Processamento de Tabelas**: Converte tabelas para HTML
- **Interface Interativa**: Visualização em tempo real do processamento
- **Extração de Imagens**: Salva imagens referenciadas nos documentos

## 📁 Estrutura do Projeto

```
Convert/
├── app.py                    # Aplicação principal Streamlit
├── config.py                 # Configurações centralizadas
├── styles.py                 # Estilos CSS customizados
├── session_state.py          # Gerenciamento de estado
├── ui_components.py          # Componentes de interface
├── file_utils.py             # Utilitários de arquivo
├── ocr_service.py            # Serviço de OCR
├── document_processor.py     # Processador de documentos
└── README.md                 # Esta documentação
```

## 🛠️ Instalação

### Dependências

```bash
pip install streamlit openai pdf2image pillow
```

### Poppler

O Poppler é necessário para converter PDFs em imagens.

1. Baixe a versão para Windows: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extraia o arquivo ZIP.
3. Adicione a pasta `bin` (onde fica o `pdfinfo.exe`) ao **PATH** do sistema.
   - Pesquise por "Editar as variáveis de ambiente do sistema" no Windows.
   - Clique em "Variáveis de Ambiente".
   - Em "Variáveis do sistema", selecione `Path` e clique em "Editar".
   - Clique em "Novo" e cole o caminho da pasta `bin`.
4. Reinicie o terminal/aplicação.

## ⚙️ Configuração

Edite `config.py` se necessário. O caminho do Poppler agora é detectado automaticamente se estiver no PATH.


### Timeout de API

Ajuste o timeout em `config.py`:
```python
api_timeout: float = 600.0  # segundos
```

## 📄 Licença

Este projeto é fornecido como está, para uso educacional e experimental.