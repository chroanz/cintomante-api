from django.db import models

class ImagemUpload(models.Model):
    resultado = models.CharField(max_length=255, blank=True, null=True)
    probabilidade = models.FloatField(blank=True, null=True)
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem {self.id} - {self.resultado} ({self.probabilidade:.2%}) em {self.enviado_em.strftime('%d/%m/%Y %H:%M')}"