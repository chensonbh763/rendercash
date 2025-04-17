from pyHoneygain import HoneyGain

# Credenciais do usuário
USERNAME = "felipeaugusto.machado@yahoo.com.br"
PASSWORD = "lived094"

try:
    # Inicializa o objeto HoneyGain
    user = HoneyGain()
    
    # Faz login com nome de usuário e senha
    user.login(USERNAME, PASSWORD)
    print("Login realizado com sucesso!")

    # Obtém informações do usuário
    user_info = user.me()
    print("\nInformações do usuário:")
    print(user_info)

    # Lista dispositivos conectados com os atributos corretos
    devices = user.devices()
    print("\nDispositivos conectados (detalhes):")
    for device in devices:
        print(f"Fabricante: {device.get('manufacturer', 'Indisponível')}, "
              f"Modelo: {device.get('model', 'Indisponível')}, "
              f"Plataforma: {device.get('platform', 'Indisponível')}, "
              f"Versão: {device.get('version', 'Indisponível')}, "
              f"Créditos: {device['stats'].get('total_credits', 'Indisponível')}, "
              f"Tráfego Total: {device['stats'].get('total_traffic', 'Indisponível')} bytes")

    # Obtém estatísticas de ganhos
    stats = user.stats()
    print("\nEstatísticas dos últimos 30 dias:")
    print(stats)

except Exception as e:
    print(f"Erro ao interagir com a API Honeygain: {e}")
