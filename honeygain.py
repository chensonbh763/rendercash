from pyHoneygain import HoneyGain

def main():
    try:
        USERNAME = "felipeaugusto.machado@yahoo.com.br"
        PASSWORD = "lived094"

        print("Fazendo login no Honeygain...")
        user = HoneyGain()
        user.login(USERNAME, PASSWORD)
        print("Login realizado com sucesso!\n")

        # Informações do usuário
        user_info = user.me()
        print(f"Usuário: {user_info.get('email', 'Indisponível')}, Status: {user_info.get('status', 'Indisponível')}")

        # Dispositivos conectados
        devices = user.devices()
        print("\nDispositivos Conectados:")
        for device in devices:
            print(f"- Fabricante: {device.get('manufacturer', 'Indisponível')}, "
                  f"Modelo: {device.get('model', 'Indisponível')}, "
                  f"Plataforma: {device.get('platform', 'Indisponível')}, "
                  f"Versão: {device.get('version', 'Indisponível')}, "
                  f"Créditos: {device['stats'].get('total_credits', 'Indisponível')}, "
                  f"Tráfego Total: {device['stats'].get('total_traffic', 'Indisponível')} bytes")

        # Estatísticas dos últimos 30 dias
        stats = user.stats()
        print("\nEstatísticas dos Últimos 30 Dias:")
        for date, stat in stats.items():
            print(f"- Data: {date}, Tráfego: {stat['gathering'].get('traffic', 0)} bytes, "
                  f"Créditos: {stat['gathering'].get('credits', 0)}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
