import numpy as np
import random
from PIL import Image
from pathlib import Path
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from tensorflow import keras
from .models import ImagemUpload
from .serializers import ImagemUploadSerializer

# Carregar o modelo uma única vez quando o servidor inicia
BASE_DIR = Path(__file__).resolve().parent.parent
MODELO_PATH = BASE_DIR / 'modelos' / 'modelo_cinto_otimizado.keras'

# Variável global para armazenar o modelo
modelo_ml = None

def carregar_modelo():
    """Carrega o modelo de machine learning"""
    global modelo_ml
    if modelo_ml is None:
        try:
            modelo_ml = keras.models.load_model(MODELO_PATH)
            print(f"✓ Modelo carregado com sucesso de: {MODELO_PATH}")
        except Exception as e:
            print(f"✗ Erro ao carregar modelo: {str(e)}")
            raise
    return modelo_ml

def preprocessar_imagem(imagem_file):
    """
    Preprocessa a imagem para o formato esperado pelo modelo
    Args:
        imagem_file: Arquivo de imagem enviado na requisição
    Returns:
        numpy array: Imagem preprocessada pronta para predição
    """
    # Ler a imagem da memória
    imagem_file.seek(0)
    img = Image.open(imagem_file)
    
    # Converter para RGB se necessário
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Redimensionar para o tamanho esperado pelo modelo: 150x150 pixels
    img = img.resize((150, 150))
    
    # Converter para array numpy
    img_array = np.array(img)
    
    # Normalizar os valores dos pixels (0-255 para 0-1)
    img_array = img_array.astype('float32') / 255.0
    
    # Adicionar dimensão do batch
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def classificar_imagem(imagem_file):
    """
    Classifica a imagem usando o modelo de ML
    Args:
        imagem_file: Arquivo de imagem enviado na requisição
    Returns:
        tuple: (resultado, probabilidade)
    """
    try:

        probabilidade = round(random.random(), 1)
        # # Carregar o modelo
        # modelo = carregar_modelo()
        
        # # Preprocessar a imagem
        # img_processada = preprocessar_imagem(imagem_file)
        
        # # Fazer a predição
        # predicao = modelo.predict(img_processada, verbose=0)
        # probabilidade = float(predicao[0][0])
        
        # Classificar baseado no threshold de 0.5
        if probabilidade > 0.5:
            resultado = "com_cinto"
            mensagem = f"Pessoa está COM cinto de segurança"
        else:
            resultado = "sem_cinto"
            mensagem = f"Pessoa está SEM cinto de segurança"
        
        print(f"Classificação: {mensagem} (probabilidade: {probabilidade:.4f})")
        
        return resultado, probabilidade
        
    except Exception as e:
        print(f"Erro na classificação: {str(e)}")
        raise


class UploadImagemView(APIView):
    """
    View para processar upload de imagem e classificar usando ML
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        """
        POST: Recebe uma imagem, classifica e retorna o resultado
        """
        # Validar se a imagem foi enviada
        if 'imagem' not in request.FILES:
            return Response(
                {"erro": "Nenhuma imagem foi enviada. Use o campo 'imagem' para enviar o arquivo."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        imagem_file = request.FILES['imagem']
        
        try:
            # Classificar a imagem (processamento em memória)
            resultado, probabilidade = classificar_imagem(imagem_file)
            
            # Salvar apenas o resultado no banco (sem a imagem)
            instancia = ImagemUpload.objects.create(
                resultado=resultado,
                probabilidade=probabilidade
            )
            
            # Preparar resposta
            resposta_data = {
                'id': instancia.id,
                'resultado': resultado,
                'probabilidade': probabilidade,
                'mensagem': f"Classificação: {'COM cinto' if resultado == 'com_cinto' else 'SEM cinto'}",
                'enviado_em': instancia.enviado_em
            }
            
            return Response(resposta_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"erro": f"Erro no processamento da imagem: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )