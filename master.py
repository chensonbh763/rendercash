import subprocess
import os

# Lista de scripts Python que você quer executar
scripts = [
    "honeygain.py",
    "kryptex_miner.py",
    "rendercash.py",
    "free.py",
]

# Caminho absoluto opcional se estiver rodando em servidor tipo Render.com
base_path = os.path.dirname(os.path.abspath(__file__))

# Dicionário para guardar os processos
processos = {}

# Inicia cada script em um subprocesso separado
for script in scripts:
    caminho_completo = os.path.join(base_path, script)
    if os.path.exists(caminho_completo):
        print(f"Iniciando: {script}")
        processos[script] = subprocess.Popen(["python", caminho_completo])
    else:
        print(f"Script não encontrado: {script}")

# Mantém o master rodando e monitora os subprocessos
try:
    for nome, processo in processos.items():
        processo.wait()
        print(f"{nome} finalizado.")
except KeyboardInterrupt:
    print("Encerrando todos os scripts...")
    for nome, processo in processos.items():
        processo.terminate()
        print(f"{nome} encerrado.")
