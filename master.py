import subprocess
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MasterApp(App):
    def build(self):
        self.processes = {}  # Dicionário para armazenar processos em execução

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Status geral
        self.status_label = Label(text="Status: Inicializando todos os módulos...")
        layout.add_widget(self.status_label)

        # Botão para parar todos os módulos
        stop_all_btn = Button(text="Parar Todos os Módulos")
        stop_all_btn.bind(on_press=self.stop_all_modules)
        layout.add_widget(stop_all_btn)

        # Botão para reiniciar todos os módulos
        restart_all_btn = Button(text="Reiniciar Todos os Módulos")
        restart_all_btn.bind(on_press=self.restart_all_modules)
        layout.add_widget(restart_all_btn)

        # Inicializar automaticamente os módulos
        self.start_all_modules()

        return layout

    def start_all_modules(self):
        # Caminho para a pasta de módulos
        modules_path = r"C:\Users\j\OneDrive\Desktop\códigos\rendercash\módulos"

        # Verifica se a pasta de módulos existe
        if not os.path.exists(modules_path):
            self.status_label.text = "Erro: Pasta de módulos não encontrada!"
            return

        # Varre todos os arquivos .py na pasta especificada
        py_files = [f for f in os.listdir(modules_path) if f.endswith(".py")]

        # Inicia cada arquivo .py como um módulo
        for py_file in py_files:
            module_name = py_file.replace(".py", "")
            script_path = os.path.join(modules_path, py_file)
            self.start_module(module_name, script_path)

        self.status_label.text = "Status: Todos os módulos iniciados!"

    def start_module(self, name, script_path):
        if name not in self.processes:
            try:
                # Inicia o script como um processo em segundo plano
                process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.processes[name] = process
                print(f"{name} iniciado com sucesso!")
            except Exception as e:
                print(f"Erro ao iniciar {name}: {e}")

    def stop_all_modules(self, instance):
        # Para todos os processos em execução
        if self.processes:
            for name, process in self.processes.items():
                process.terminate()
                print(f"{name} parado!")
            self.processes.clear()
            self.status_label.text = "Status: Todos os módulos parados!"
        else:
            self.status_label.text = "Status: Nenhum módulo em execução para parar!"

    def restart_all_modules(self, instance):
        # Reinicia todos os processos
        self.stop_all_modules(instance)
        self.start_all_modules()
        self.status_label.text = "Status: Todos os módulos reiniciados!"

if __name__ == "__main__":
    MasterApp().run()
