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

O Poppler é necessário para converter PDFs em imagens. Configure o caminho correto em `config.py` ou na interface.

**Windows**: Baixe de https://github.com/oschwartz10612/poppler-windows/releases/

## ⚙️ Configuração

Edite `config.py` para ajustar:

- **API URL**: Endpoint da API de OCR (padrão: `http://localhost:1234/v1`)
- **Modelo**: Nome do modelo de OCR (padrão: `olmocr-2-7b-1025`)
- **Poppler Path**: Caminho do executável Poppler
- **DPI**: Qualidade de conversão das imagens (72-300)

## 🎯 Uso

1. **Inicie a aplicação**:
   ```bash
   streamlit run app.py
   ```

2. **Configure a API** na barra lateral (se necessário)

3. **Selecione uma pasta** contendo arquivos PDF

4. **Clique em "Iniciar"** para processar

5. **Visualize os resultados** em tempo real

6. **Arquivos de saída** serão salvos em `Markdown_Outputs/` dentro da pasta selecionada

## 📊 Saída

A aplicação gera:

- **Arquivos Markdown** (`.md`) com o texto extraído
- **Pasta `images/`** com imagens referenciadas nos documentos
- **Formatação especial** para equações (LaTeX) e tabelas (HTML)

## 🏗️ Arquitetura

### Módulos

- **config.py**: Configurações usando dataclass
- **ocr_service.py**: Comunicação com API OpenAI
- **document_processor.py**: Lógica de processamento de PDFs
- **ui_components.py**: Componentes reutilizáveis da UI
- **session_state.py**: Gerenciamento de estado do Streamlit
- **file_utils.py**: Operações de arquivo e diálogo
- **styles.py**: Estilos CSS da aplicação

### Padrões Utilizados

- **Callback Pattern**: Para atualização assíncrona da UI
- **Service Layer**: Separação entre lógica de negócio e apresentação
- **Singleton Config**: Configuração centralizada e acessível
- **Type Hints**: Tipagem forte para melhor manutenibilidade

## 🔧 Personalização

### Modificar Prompt de OCR

Edite `config.py`:

```python
ocr_prompt: str = "Seu prompt customizado aqui"
```

### Ajustar Qualidade de Imagem

```python
image_quality: int = 85  # 0-100
```

### Alterar Pastas de Saída

```python
output_folder_name: str = "Markdown_Outputs"
images_folder_name: str = "images"
```

## 📝 Melhorias Implementadas

✅ **Separação de responsabilidades** em módulos
✅ **Type hints** em todo o código
✅ **Configuração centralizada** via dataclass
✅ **Tratamento de erros** robusto
✅ **Callbacks** para UI responsiva
✅ **Uso de Path** ao invés de strings
✅ **Documentação** completa com docstrings
✅ **Código limpo** e manutenível

## 🐛 Troubleshooting

### Erro de Poppler

Se aparecer erro relacionado ao Poppler, verifique:
- O caminho está correto em `config.py`
- O Poppler está instalado
- O executável está acessível

### Timeout de API

Ajuste o timeout em `config.py`:
```python
api_timeout: float = 600.0  # segundos
```

## 📄 Licença

Este projeto é fornecido como está, para uso educacional e experimental.