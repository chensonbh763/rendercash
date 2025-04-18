import ctypes
from ctypes import c_int, CFUNCTYPE
import os
import time

# ********************************** SDK Integration **********************************
# Caminho ajustado para o arquivo DLL, utilizando caminho relativo
dll_path = os.path.join(os.path.dirname(__file__), 'packet_sdk.dll')

# Verifique se o arquivo DLL existe
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"O arquivo DLL não foi encontrado no caminho especificado: {dll_path}")

# Carrega o DLL
dll = ctypes.CDLL(dll_path)

# Define o tipo de retorno para as funções do DLL
dll.packet_strstatus.restype = ctypes.c_char_p

# Callback function to handle SDK async events
def asyncCallback(status):
    try:
        statusStringPtr = dll.packet_strstatus(status)
        print(f"PacketSDK async callback with status: {status} Message: {statusStringPtr.decode('utf-8')}")
    except Exception as e:
        print(f"Erro no callback: {e}")

CALLBACK_TYPE = CFUNCTYPE(None, c_int)
callback_func = CALLBACK_TYPE(asyncCallback)

# Configurando a função de callback
try:
    dll.packet_sdk_set_callBack(callback_func)
except Exception as e:
    print(f"Erro ao configurar o callback: {e}")

# Definindo o appkey para autenticação
try:
    result = dll.packet_sdk_set_appKey("pGF1vmwKr0F0dPIA".encode('utf-8'))
    resultStringPtr = dll.packet_strstatus(result)
    print(f"Resultado da configuração do appkey: {result} Mensagem: {resultStringPtr.decode('utf-8')}")
except Exception as e:
    print(f"Erro ao configurar o appkey: {e}")

# Iniciando o SDK
try:
    result = dll.packet_sdk_start()
    print("PacketSDK iniciado! Resultado:", result)
except Exception as e:
    print(f"Erro ao iniciar o SDK: {e}")

# ********************************** Funções de Monitoramento **********************************
def atualizar_dados():
    try:
        # Consultando o status do servidor via SDK
        server_status = dll.packet_sdk_queryServerStatus()
        status_message = dll.packet_strstatus(server_status)
        print(f"Status do SDK: {status_message.decode('utf-8')}")

        # Simular ganhos e uso de banda
        earnings = 20.0
        bandwidth_usage = 150
        print(f"Ganhos: ${earnings:.2f}")
        print(f"Uso de Banda: {bandwidth_usage} MB")
    except Exception as e:
        print(f"Erro ao consultar SDK: {e}")

def finalizar_sdk():
    try:
        # Parar o SDK
        result = dll.packet_sdk_stop()
        stop_message = dll.packet_strstatus(result)
        print(f"PacketSDK finalizado! Status: {stop_message.decode('utf-8')}")
    except Exception as e:
        print(f"Erro ao finalizar SDK: {e}")

# ********************************** Execução do Sistema **********************************
if __name__ == "__main__":
    try:
        print("Atualizando dados do SDK a cada 5 segundos... (Pressione Ctrl+C para encerrar)")
        while True:
            atualizar_dados()
            time.sleep(5)  # Atualiza a cada 5 segundos
    except KeyboardInterrupt:
        print("\nEncerrando monitoramento...")
        finalizar_sdk()
