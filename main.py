import subprocess
import sys
import platform

# Lista de modelos em ordem da mais robusta para a mais leve
models = [
    ("deepseek-r1:14b", "DeepSeek 14B"),    # Muito robusto
    ("llama3", "LLaMA 3"),                           # Robusto
    ("mistral", "Mistral"),                          # Médio
    ("gemma:2b", "Gemma 2B"),                        # Leve
    ("phi", "Phi-2")                               # Muito leve
]

# Comando para instalar o Ollama (Windows)
def install_ollama():
    system = platform.system()
    if system == "Windows":
        print("[*] Baixando e instalando Ollama para Windows...")
        url = "https://ollama.com/download/OllamaSetup.exe"
        subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {url} -OutFile OllamaSetup.exe"], check=True)
        subprocess.run(["OllamaSetup.exe"], check=True)
    elif system == "Linux":
        print("[*] Instalando Ollama para Linux...")
        subprocess.run(["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"], shell=True)
    else:
        print("Sistema operacional não suportado automaticamente. Instale manualmente: https://ollama.com/download")

# Executar modelo
def run_model(index):
    try:
        model_name, display_name = models[index]
        print(f"[*] Baixando e executando modelo: {display_name} ({model_name})")
        subprocess.run(["ollama", "pull", model_name], check=True)
    except IndexError:
        print("Índice de modelo inválido.")
    except FileNotFoundError:
        print("Erro: Ollama não encontrado. Certifique-se que ele está instalado e no PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")

# Interpretar argumentos
def parse_flags():
    if len(sys.argv) < 2:
        print("Uso: python main.py --[1-5] ou --install")
        print("Modelos disponíveis:")
        for i, (_, name) in enumerate(models, start=1):
            print(f"  --{i} -> {name}")
        return

    arg = sys.argv[1]
    if arg == "--install":
        install_ollama()
    elif arg.startswith("--") and arg[2:].isdigit():
        index = int(arg[2:]) - 1
        run_model(index)
    else:
        print(f"Argumento desconhecido: {arg}")

if __name__ == "__main__":
    parse_flags()
