from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from pyHoneygain import HoneyGain

class HoneygainApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título principal
        self.layout.add_widget(Label(text="Honeygain Dashboard", font_size='20sp', bold=True, size_hint=(1, 0.1)))

        # Área de status
        self.status_label = Label(text="Carregando informações...", size_hint=(1, 0.1))
        self.layout.add_widget(self.status_label)

        # Scroll para dispositivos e estatísticas
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        self.scroll.add_widget(self.content_layout)
        self.layout.add_widget(self.scroll)

        # Botão para recarregar
        reload_button = Button(text="Recarregar", size_hint=(1, 0.1))
        reload_button.bind(on_press=self.reload_data)
        self.layout.add_widget(reload_button)

        # Inicializa dados
        self.reload_data()

        return self.layout

    def reload_data(self, *args):
        # Atualiza os dados exibidos
        try:
            USERNAME = "felipeaugusto.machado@yahoo.com.br"
            PASSWORD = "lived094"

            self.status_label.text = "Fazendo login no Honeygain..."
            user = HoneyGain()
            user.login(USERNAME, PASSWORD)
            self.status_label.text = "Login realizado com sucesso!"

            # Limpa o conteúdo anterior
            self.content_layout.clear_widgets()

            # Informações do usuário
            user_info = user.me()
            self.content_layout.add_widget(Label(text=f"Usuário: {user_info.get('email', 'Indisponível')}, Status: {user_info.get('status', 'Indisponível')}", size_hint_y=None, height=30))

            # Dispositivos conectados
            devices = user.devices()
            self.content_layout.add_widget(Label(text="Dispositivos Conectados:", bold=True, size_hint_y=None, height=30))
            for device in devices:
                self.content_layout.add_widget(Label(
                    text=f"Fabricante: {device.get('manufacturer', 'Indisponível')}, "
                         f"Modelo: {device.get('model', 'Indisponível')}, "
                         f"Plataforma: {device.get('platform', 'Indisponível')}, "
                         f"Versão: {device.get('version', 'Indisponível')}, "
                         f"Créditos: {device['stats'].get('total_credits', 'Indisponível')}, "
                         f"Tráfego Total: {device['stats'].get('total_traffic', 'Indisponível')} bytes",
                    size_hint_y=None, height=30))

            # Estatísticas dos últimos 30 dias
            stats = user.stats()
            self.content_layout.add_widget(Label(text="Estatísticas dos Últimos 30 Dias:", bold=True, size_hint_y=None, height=30))
            for date, stat in stats.items():
                self.content_layout.add_widget(Label(
                    text=f"Data: {date}, Tráfego: {stat['gathering'].get('traffic', 0)} bytes, "
                         f"Créditos: {stat['gathering'].get('credits', 0)}",
                    size_hint_y=None, height=30))
        except Exception as e:
            self.status_label.text = f"Erro: {e}"

if __name__ == "__main__":
    HoneygainApp().run()
