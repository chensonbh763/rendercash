import socket
import json
import time

class KryptexMiner:
    def __init__(self, pool_address, wallet_address, worker_name):
        self.pool_address = pool_address.replace("stratum+tcp://", "")  # Remove o prefixo stratum+tcp://
        self.wallet_address = wallet_address
        self.worker_name = worker_name
        self.connection = None

    def connect_to_pool(self):
        try:
            # Divide o endereço em host e porta
            host, port = self.pool_address.split(":")
            self.connection = socket.create_connection((host, int(port)))
            print(f"Conectado ao pool Kryptex: {self.pool_address}")
        except ValueError:
            print("Erro: Endereço do pool inválido. Certifique-se de que está no formato host:porta.")
        except Exception as e:
            print(f"Erro ao conectar ao pool Kryptex: {e}")

    def authenticate_worker(self):
        try:
            if self.connection:
                # Mensagem para se conectar ao pool
                message = {
                    "id": 1,
                    "method": "mining.subscribe",
                    "params": [f"{self.wallet_address}.{self.worker_name}"]
                }
                self.connection.sendall((json.dumps(message) + "\n").encode('utf-8'))
                print(f"Worker {self.worker_name} autenticado com sucesso!")

                # Recebendo resposta do pool
                response = self.connection.recv(1024).decode('utf-8')
                print(f"Resposta do pool: {response}")
            else:
                print("Erro: Sem conexão ativa com o pool.")
        except Exception as e:
            print(f"Erro ao autenticar no pool: {e}")

    def start_mining(self):
        if not self.connection:
            print("Erro: Não há conexão ativa para iniciar a mineração.")
            return

        print("Minerando... pressione Ctrl+C para interromper.")
        try:
            while True:
                # Simula a mineração enviando mensagens ao pool
                heartbeat_message = {"id": 2, "method": "mining.heartbeat", "params": []}
                self.connection.sendall((json.dumps(heartbeat_message) + "\n").encode('utf-8'))
                print("Enviei sinal de heartbeat ao pool.")
                time.sleep(10)  # Pausa para simular tempo de mineração
        except KeyboardInterrupt:
            print("\nMineração interrompida pelo usuário.")
        except Exception as e:
            print(f"Erro durante a mineração: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Desconectado do pool Kryptex.")

# Configuração do minerador
if __name__ == "__main__":
    pool_address = "stratum+tcp://ltc.kryptex.network:7777"  # Endereço Kryptex Pool
    wallet_address = "ltc1qmpza2v3sxnfr69mkdawhrpzkuu9hvplls3ufcu"  # Sua carteira LTC
    worker_name = "krxYMGNGED.worker"  # Nome do worker

    miner = KryptexMiner(pool_address, wallet_address, worker_name)
    miner.connect_to_pool()
    miner.authenticate_worker()
    miner.start_mining()
    miner.disconnect()
