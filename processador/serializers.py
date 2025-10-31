from rest_framework import serializers
from .models import ImagemUpload

class ImagemUploadSerializer(serializers.ModelSerializer):
    # Campo para receber a imagem via base64 ou upload direto
    imagem = serializers.ImageField(write_only=True)
    
    class Meta:
        model = ImagemUpload
        fields = ['id', 'imagem', 'resultado', 'probabilidade', 'enviado_em']
        read_only_fields = ['resultado', 'probabilidade', 'enviado_em']