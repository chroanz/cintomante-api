# Integração da API com Modelo de Machine Learning

## 📋 Descrição

Esta API recebe imagens via requisição HTTP e classifica se a pessoa está usando cinto de segurança ou não, utilizando um modelo de Machine Learning (TensorFlow/Keras).

## 🚀 Características

- ✅ **Processamento em Memória**: Imagens são processadas em tempo de execução sem armazenamento no disco
- ✅ **Classificação ML**: Utiliza modelo Keras para classificar imagens
- ✅ **Threshold 0.5**: Probabilidade > 0.5 = COM cinto, caso contrário SEM cinto
- ✅ **API RESTful**: Interface simples usando Django REST Framework

## 📦 Instalação

1. **Instale as dependências:**
```powershell
pip install -r requirements.txt
```

2. **Execute as migrações do banco de dados:**
```powershell
python manage.py makemigrations
python manage.py migrate
```

3. **Inicie o servidor:**
```powershell
python manage.py runserver
```

## 🔧 Configuração

### Modelo de Machine Learning

O modelo deve estar localizado em:
```
modelos/modelo_cinto_otimizado.keras
```

**Importante:** O modelo será carregado automaticamente quando o servidor iniciar.

### Tamanho da Imagem

O código atual redimensiona imagens para **224x224 pixels**. Se seu modelo usar um tamanho diferente, ajuste em `processador/views.py`:

```python
# Linha ~38
img = img.resize((224, 224))  # Ajuste conforme seu modelo
```

## 📡 Uso da API

### Endpoint

```
POST http://localhost:8000/processador/
```

### Requisição

**Content-Type:** `multipart/form-data`

**Campo:** `imagem` (arquivo de imagem)

### Exemplo usando cURL:

```powershell
curl -X POST http://localhost:8000/processador/ -F "imagem=@caminho/para/sua/imagem.jpg"
```

### Exemplo usando Python (requests):

```python
import requests

url = "http://localhost:8000/processador/"
files = {'imagem': open('imagem_teste.jpg', 'rb')}
response = requests.post(url, files=files)

print(response.json())
```

### Exemplo usando JavaScript (Fetch):

```javascript
const formData = new FormData();
formData.append('imagem', arquivoImagem);

fetch('http://localhost:8000/processador/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Erro:', error));
```

## 📤 Resposta

### Sucesso (201 Created)

```json
{
    "id": 1,
    "resultado": "com_cinto",
    "probabilidade": 0.8745,
    "mensagem": "Classificação: COM cinto",
    "enviado_em": "2025-10-17T14:30:00Z"
}
```

ou

```json
{
    "id": 2,
    "resultado": "sem_cinto",
    "probabilidade": 0.2341,
    "mensagem": "Classificação: SEM cinto",
    "enviado_em": "2025-10-17T14:31:00Z"
}
```

### Erro (400 Bad Request)

```json
{
    "erro": "Nenhuma imagem foi enviada. Use o campo 'imagem' para enviar o arquivo."
}
```

### Erro (500 Internal Server Error)

```json
{
    "erro": "Erro no processamento da imagem: [detalhes do erro]"
}
```

## 🔍 Campos da Resposta

- **id**: Identificador único do registro
- **resultado**: `"com_cinto"` ou `"sem_cinto"`
- **probabilidade**: Valor entre 0 e 1 indicando a confiança da predição
- **mensagem**: Descrição legível do resultado
- **enviado_em**: Data e hora do processamento

## 🎯 Lógica de Classificação

```python
if probabilidade > 0.5:
    resultado = "com_cinto"  # Pessoa está usando cinto
else:
    resultado = "sem_cinto"  # Pessoa NÃO está usando cinto
```

## 🗄️ Banco de Dados

Apenas os **resultados** são salvos no banco, não as imagens:

- `resultado`: String com a classificação
- `probabilidade`: Float com a confiança da predição
- `enviado_em`: Timestamp do processamento

## ⚙️ Processamento da Imagem

1. **Recepção**: Imagem recebida via `multipart/form-data`
2. **Leitura**: Imagem carregada diretamente na memória
3. **Conversão**: Convertida para RGB se necessário
4. **Redimensionamento**: Ajustada para 224x224 pixels
5. **Normalização**: Pixels normalizados de 0-255 para 0-1
6. **Predição**: Modelo Keras faz a classificação
7. **Resposta**: Resultado retornado ao cliente

**Nenhum arquivo é salvo no disco!**

## 🧪 Testando a API

### 1. Teste Básico com cURL

```powershell
curl -X POST http://localhost:8000/processador/ `
  -F "imagem=@teste.jpg" `
  -H "Accept: application/json"
```

### 2. Teste Interativo (Swagger/OpenAPI)

Se configurado, acesse:
```
http://localhost:8000/swagger/
```

## 🐛 Troubleshooting

### Erro: "Modelo não encontrado"

Verifique se o arquivo existe:
```powershell
Test-Path .\modelos\modelo_cinto_otimizado.keras
```

### Erro: "TensorFlow não instalado"

Reinstale as dependências:
```powershell
pip install -r requirements.txt --force-reinstall
```

### Erro: "CORS blocked"

Adicione a origem permitida em `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://seu-frontend.com",
]
```

## 📊 Logs

O servidor imprime informações úteis no console:

```
✓ Modelo carregado com sucesso de: modelos/modelo_cinto_otimizado.keras
Classificação: Pessoa está COM cinto de segurança (probabilidade: 0.8745)
```

## 🔒 Segurança

- ✅ Valida tipo de arquivo (apenas imagens)
- ✅ Processa em memória (sem arquivos temporários)
- ✅ Tratamento de erros robusto
- ✅ Sem armazenamento de dados sensíveis

## 📝 Notas Importantes

1. **Performance**: O modelo é carregado apenas uma vez na inicialização
2. **Memória**: Imagens são descartadas após o processamento
3. **Tamanho**: Configure limites de upload em `settings.py` se necessário
4. **Formato**: Aceita JPG, PNG, BMP, etc. (convertidos para RGB)

## 🤝 Contribuindo

Para modificar o comportamento:

- **Threshold**: Ajuste em `views.py` linha ~68
- **Tamanho da imagem**: Ajuste em `views.py` linha ~38
- **Campos salvos**: Modifique `models.py`

## 📄 Licença

[Sua licença aqui]
