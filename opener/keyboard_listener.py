from networktables import NetworkTablesInstance
from pynput import keyboard
from threading import Timer
import time
import threading

def main():
    # Inicializa o cliente do NetworkTables
    print("Setting up NetworkTables client...")
    nt = NetworkTablesInstance.getDefault()
    nt.startClient("KeyboardToNT")  # Nome do cliente
    nt.setServer("10.10.1.2")  # IP do robo
    nt.startDSClient()  # Conecta ao DriverStation

    print("Conectando ao robo...")
    # Espera até conectar no servidor do robo
    while not nt.isConnected():
        print(".", end="", flush=True)
        time.sleep(0.1)
    print("\nConectado!")

    # Cria uma tabela de comunicação chamada “OperatorController”
    table = nt.getTable("OperatorController")

    # Função chamada para soltar uma tecla (define o valor como False)
    def release_key(key_name: str) -> None:
        print(f"Sending: {key_name} -> {False}")
        table.putBoolean(key_name, False)  # Envia tecla solta para o robo

    # Função chamada para pressionar uma tecla (define o valor como True)
    # e automaticamente soltar após um pequeno tempo
    def timed_keypress(key_name: str, press_time: float) -> None:
        print(f"Sending: {key_name} -> {True}")
        table.putBoolean(key_name, True)  # Envia tecla pressionada para o robo
        timer = Timer(press_time, release_key, [key_name])  # Cria um timer para soltar depois
        timer.start()

    # Função chamada sempre que uma tecla for pressionada
    def on_press(key):
        try:
            key_name = key.char.lower()  # Captura o nome da tecla
        except AttributeError:
            key_name = str(key)  # Caso seja uma tecla especial
        timed_keypress(key_name, 0.1)  # Envia a tecla pressionada por 0.1s

    # Função chamada sempre que uma tecla for solta
    def on_release(key):
        pass

    # Caso perca a conexão por algum motivo, tenta reconectar sem que precise rodar novamente
    def reconnect_loop():
        while True:
            if not nt.isConnected():
                print("\n[!] Conexão perdida. Tentando reconectar...")
                nt.startDSClient()
            time.sleep(1)

    # Inicia uma thread separada para manter a conexão
    threading.Thread(target=reconnect_loop, daemon=True).start()

    # Ativa o listener do teclado
    print("Keyboard listener ativo! Pressione teclas para enviar ao robô...")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  # Mantém o programa rodando

if __name__ == '__main__':
    main()