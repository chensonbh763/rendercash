import ctypes
from ctypes import c_int, CFUNCTYPE

# ********************************** SDK Integration **********************************
dll = ctypes.CDLL(r'C:/Users/j/OneDrive/Desktop/códigos/rendercash/packet_sdk.dll')  # Caminho ajustado para o DLL

dll.packet_strstatus.restype = ctypes.c_char_p

# Callback function to handle SDK async events
def asyncCallback(status):
    statusStringPtr = dll.packet_strstatus(status)
    print(f"PacketSDK async callback with status: {status} Message: {statusStringPtr.decode('utf-8')}")

CALLBACK_TYPE = CFUNCTYPE(None, c_int)
callback_func = CALLBACK_TYPE(asyncCallback)

# Setting the callback function
dll.packet_sdk_set_callBack(callback_func)

# Setting the appkey for authentication
result = dll.packet_sdk_set_appKey("pGF1vmwKr0F0dPIA".encode('utf-8'))
resultStringPtr = dll.packet_strstatus(result)
print(f"Result of set appkey: {result} Message: {resultStringPtr.decode('utf-8')}")

# Starting the SDK
result = dll.packet_sdk_start()
print("PacketSDK started! Result:", result)

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
        print("Atualizando dados do SDK a cada 5 segundos...")
        while True:
            atualizar_dados()
            import time
            time.sleep(5)  # Atualiza a cada 5 segundos
    except KeyboardInterrupt:
        print("\nEncerrando monitoramento...")
        finalizar_sdk()
