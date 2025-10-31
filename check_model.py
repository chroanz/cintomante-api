from tensorflow import keras
# Carregar o modelo
modelo = keras.models.load_model('modelos/modelo_cinto_otimizado.keras')

# Mostrar informações
print('=' * 60)
print('INFORMAÇÕES DO MODELO')
print('=' * 60)
print(f'\nInput shape: {modelo.input_shape}')
print(f'\nOutput shape: {modelo.output_shape}')
print('\n' + '=' * 60)
print('RESUMO DO MODELO')
print('=' * 60)
modelo.summary()

# Calcular o tamanho esperado
if len(modelo.input_shape) == 4:
    _, h, w, c = modelo.input_shape
    if h and w and c:
        print(f'\n\nTamanho de entrada esperado: {h}x{w}x{c}')
        print(f'Total de pixels: {h * w * c}')
    else:
        print('\n\nO modelo aceita entrada dinâmica')
        
# Tentar descobrir o tamanho correto baseado no erro
# O erro diz: expected axis -1 of input shape to have value 36992
print(f'\n\nBaseado no erro, o modelo espera {36992} valores')
print(f'Isso corresponde a aproximadamente:')
import math
lado = int(math.sqrt(36992 / 3))
print(f'  - {lado}x{lado}x3 = {lado * lado * 3} pixels (RGB)')

# Testar outras possibilidades
for size in [96, 100, 110, 112, 120, 128]:
    total = size * size * 3
    if abs(total - 36992) < 1000:
        print(f'  - {size}x{size}x3 = {total} pixels ← POSSÍVEL!')
