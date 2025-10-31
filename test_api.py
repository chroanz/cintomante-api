"""
Script de teste para validar a integração da API com o modelo de ML
Execute: python test_api.py
"""

import requests
import sys
from pathlib import Path

# URL da API
API_URL = "http://localhost:8000/processador/"

def testar_upload_imagem(caminho_imagem):
    """
    Testa o upload de uma imagem para a API
    """
    print(f"\n{'='*60}")
    print(f"Testando API com imagem: {caminho_imagem}")
    print(f"{'='*60}\n")
    
    # Verificar se o arquivo existe
    if not Path(caminho_imagem).exists():
        print(f"❌ Erro: Arquivo não encontrado: {caminho_imagem}")
        return False
    
    try:
        # Abrir e enviar a imagem
        with open(caminho_imagem, 'rb') as img_file:
            files = {'imagem': img_file}
            print("📤 Enviando imagem para a API...")
            
            response = requests.post(API_URL, files=files, timeout=30)
            
            print(f"📊 Status HTTP: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                print("\n✅ Sucesso! Resposta da API:")
                print(f"   ID: {data.get('id')}")
                print(f"   Resultado: {data.get('resultado')}")
                print(f"   Probabilidade: {data.get('probabilidade'):.4f} ({data.get('probabilidade')*100:.2f}%)")
                print(f"   Mensagem: {data.get('mensagem')}")
                print(f"   Processado em: {data.get('enviado_em')}")
                
                # Interpretar resultado
                print("\n📋 Interpretação:")
                if data.get('resultado') == 'com_cinto':
                    print("   ✓ A pessoa ESTÁ usando cinto de segurança")
                else:
                    print("   ✗ A pessoa NÃO está usando cinto de segurança")
                
                return True
            else:
                print(f"\n❌ Erro na requisição:")
                print(f"   {response.text}")
                return False
                
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("   Verifique se o servidor está rodando: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

def verificar_servidor():
    """
    Verifica se o servidor está rodando
    """
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False

def main():
    print("\n🔍 Verificando servidor...")
    
    if not verificar_servidor():
        print("❌ Servidor Django não está rodando!")
        print("\nPor favor, inicie o servidor primeiro:")
        print("   python manage.py runserver")
        sys.exit(1)
    
    print("✅ Servidor está rodando!\n")
    
    # Você pode passar o caminho da imagem como argumento
    if len(sys.argv) > 1:
        caminho_imagem = sys.argv[1]
    else:
        # Ou usar uma imagem padrão
        print("💡 Uso: python test_api.py <caminho_da_imagem>")
        print("\nExemplo:")
        print("   python test_api.py imagem_teste.jpg")
        sys.exit(0)
    
    # Testar o upload
    sucesso = testar_upload_imagem(caminho_imagem)
    
    if sucesso:
        print("\n" + "="*60)
        print("✅ Teste concluído com sucesso!")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("❌ Teste falhou!")
        print("="*60 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
