import ctypes
from ctypes import c_int, CFUNCTYPE
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

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

# ********************************** Kivy UI **********************************
class RenderCashApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Logs dos eventos
        self.logs_label = Label(text="Logs do SDK:")
        self.status_label = Label(text="Status do SDK: Inicializando...")
        self.ganhos_label = Label(text="Ganhos: Consultando...")
        self.uso_banda_label = Label(text="Uso de Banda: Consultando...")

        atualizar_btn = Button(text="Atualizar Dados")
        atualizar_btn.bind(on_press=self.atualizar_dados)

        finalizar_btn = Button(text="Parar SDK")
        finalizar_btn.bind(on_press=self.finalizar_sdk)

        layout.add_widget(self.logs_label)
        layout.add_widget(self.status_label)
        layout.add_widget(self.ganhos_label)
        layout.add_widget(self.uso_banda_label)
        layout.add_widget(atualizar_btn)
        layout.add_widget(finalizar_btn)

        Clock.schedule_interval(self.atualizar_dados, 5)
        return layout

    def atualizar_dados(self, instance=None):
        try:
            server_status = dll.packet_sdk_queryServerStatus()
            status_message = dll.packet_strstatus(server_status)

            self.status_label.text = f"Status do SDK: {status_message.decode('utf-8')}"
            self.logs_label.text = f"Logs do SDK: {status_message.decode('utf-8')}"

            # Simular ganhos e banda até funções reais serem identificadas
            earnings = 20.0
            bandwidth_usage = 150

            self.ganhos_label.text = f"Ganhos: ${earnings:.2f}"
            self.uso_banda_label.text = f"Uso de Banda: {bandwidth_usage} MB"
        except Exception as e:
            print(f"Erro ao consultar SDK: {e}")
            self.logs_label.text = "Logs do SDK: Erro ao atualizar"

    def finalizar_sdk(self, instance):
        result = dll.packet_sdk_stop()
        stop_message = dll.packet_strstatus(result)
        self.status_label.text = f"Status do SDK: {stop_message.decode('utf-8')}"
        self.logs_label.text = "Logs do SDK: Conexão finalizada."
        print("PacketSDK finalizado!")

if __name__ == "__main__":
    RenderCashApp().run()
