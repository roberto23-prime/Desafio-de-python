import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import getpass


def obter_senha():
    senha = getpass.getpass("Digite a senha para criptografia/descriptografia: ")
    
    chave = hashlib.sha256(senha.encode()).digest()
    return chave


def listar_arquivos_pasta(pasta_origem):
    if not os.path.exists(pasta_origem):
        raise FileNotFoundError(f"A pasta {pasta_origem} não existe.")
    arquivos = [os.path.join(pasta_origem, f) for f in os.listdir(pasta_origem) if os.path.isfile(os.path.join(pasta_origem, f))]
    return arquivos


def criptografar_arquivo(arquivo_entrada, chave, arquivo_saida):
    
    iv = get_random_bytes(AES.block_size)
    
    
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    
   
    with open(arquivo_entrada, 'rb') as f:
        dados = f.read()
    
   
    padding_length = AES.block_size - len(dados) % AES.block_size
    dados += bytes([padding_length]) * padding_length
    
    
    dados_criptografados = cipher.encrypt(dados)
    
    # Salva o IV e os dados criptografados no arquivo de saída
    with open(arquivo_saida, 'wb') as f:
        f.write(iv + dados_criptografados)


def salvar_arquivos_criptografados(pasta_origem, pasta_backup, chave):
    if not os.path.exists(pasta_backup):
        os.makedirs(pasta_backup)
    
    for arquivo in listar_arquivos_pasta(pasta_origem):
        nome_arquivo = os.path.basename(arquivo)
        arquivo_saida = os.path.join(pasta_backup, nome_arquivo + '.enc')
        criptografar_arquivo(arquivo, chave, arquivo_saida)
        print(f"Arquivo {nome_arquivo} criptografado com sucesso.")


def descriptografar_arquivo(arquivo_entrada, chave, arquivo_saida):
    with open(arquivo_entrada, 'rb') as f:
        dados = f.read()
    
    
    iv = dados[:AES.block_size]
    dados_criptografados = dados[AES.block_size:]
    
    
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    
    
    dados_descriptografados = cipher.decrypt(dados_criptografados)
    
    
    padding_length = dados_descriptografados[-1]
    dados_descriptografados = dados_descriptografados[:-padding_length]
    
    
    with open(arquivo_saida, 'wb') as f:
        f.write(dados_descriptografados)

def descriptografar_pasta(pasta_backup, pasta_destino, chave):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    for arquivo in listar_arquivos_pasta(pasta_backup):
        if arquivo.endswith('.enc'):
            nome_arquivo = os.path.basename(arquivo)[:-4]  
            arquivo_saida = os.path.join(pasta_destino, nome_arquivo)
            descriptografar_arquivo(arquivo, chave, arquivo_saida)
            print(f"Arquivo {nome_arquivo} descriptografado com sucesso.")

# Função principal
def main():
    pasta_origem = input("Digite o caminho da pasta com os arquivos a criptografar: ")
    pasta_backup = input("Digite o caminho da pasta para salvar os arquivos criptografados: ")
    pasta_destino = input("Digite o caminho da pasta para salvar os arquivos descriptografados: ")
    
    # Obtém a senha e deriva a chave
    chave = obter_senha()
    
    # Menu de opções
    while True:
        print("\n1. Criptografar arquivos")
        print("2. Descriptografar arquivos")
        print("3. Sair")
        opcao = input("Escolha uma opção (1-3): ")
        
        if opcao == '1':
            try:
                salvar_arquivos_criptografados(pasta_origem, pasta_backup, chave)
            except Exception as e:
                print(f"Erro ao criptografar: {e}")
        
        elif opcao == '2':
            try:
                descriptografar_pasta(pasta_backup, pasta_destino, chave)
            except Exception as e:
                print(f"Erro ao descriptografar: {e}")
        
        elif opcao == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()