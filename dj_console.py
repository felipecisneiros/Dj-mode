import threading
import time
import os
import pygame
import numpy as np
from scipy.io.wavfile import write

# Inicializa mixer do pygame
pygame.mixer.init()

# --- Funções para gerar sons ---
def gerar_tom(nome, freq, duracao=0.5, samplerate=44100):
    t = np.linspace(0, duracao, int(samplerate*duracao), False)
    onda = 0.5 * np.sin(2 * np.pi * freq * t)
    onda = np.int16(onda * 32767)
    write(f"{nome}.wav", samplerate, onda)

def gerar_sons_faltantes():
    sons_para_gerar = {
        'bateria': (60, 0.3),
        'baixo': (110, 0.4),
        'guitarra': (220, 0.5),
        'synth': (440, 0.6),
        'sample1': (880, 0.2),
        'sample2': (660, 0.3)
    }
    for nome, (freq, duracao) in sons_para_gerar.items():
        if not os.path.exists(f"{nome}.wav"):
            gerar_tom(nome, freq, duracao)
            print(f"🎵 {nome}.wav gerado")
    print("✅ Sons prontos!")

# --- Classe Instrumento ---
class Instrument:
    def __init__(self, name, file_path, bpm=60):
        self.name = name
        self.file_path = file_path
        self.bpm = max(1, int(bpm))
        self.volume = 1.0
        
        self._play_event = threading.Event()
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread_started = False

        try:
            self.sound = pygame.mixer.Sound(file_path)
            self.sound.set_volume(self.volume)
        except Exception as e:
            print(f"Erro ao carregar {file_path}: {e}")
            self.sound = None

        self._play_event.set()

    def start(self):
        if not self._thread_started:
            self._thread.start()
            self._thread_started = True

    def _run(self):
        while not self._stop_event.is_set():
            if not self._play_event.is_set():
                time.sleep(0.1)
                continue
            if self.sound:
                self.sound.play()
            with self._lock:
                tempo = 60.0 / self.bpm
            time.sleep(tempo)

    def pause(self): self._play_event.clear()
    def resume(self): self._play_event.set()
    def stop(self): self._stop_event.set()
    def is_playing(self): return self._play_event.is_set()
    def is_stopped(self): return self._stop_event.is_set()
    def set_bpm(self, bpm):
        with self._lock: self.bpm = max(1, int(bpm))
    def set_volume(self, vol):
        with self._lock:
            self.volume = max(0.0, min(1.0, float(vol)))
            if self.sound: self.sound.set_volume(self.volume)

# --- Função para mostrar status ---
def mostrar_status(instruments):
    print("\n" + "="*50)
    print("=== STATUS DJ MODE ===")
    print("="*50)
    for name, inst in instruments.items():
        status = "Tocando" if inst.is_playing() else "Pausado"
        print(f"- {name:12} | {status:8} | BPM: {inst.bpm:3} | Vol: {inst.volume:.2f}")
    print("="*50)

# --- Função para mostrar ajuda ---
def mostrar_ajuda():
    print("\n=== Comandos disponíveis ===")
    print("status                     → mostra status dos instrumentos")
    print("ajuda                      → mostra esta ajuda")
    print("tocar <nome>               → toca um instrumento (ex: tocar bateria)")
    print("tocar todos                → toca todos os instrumentos")
    print("pausar <nome>              → pausa um instrumento (ex: pausar baixo)")
    print("pausar todos               → pausa todos os instrumentos")
    print("bpm <nome> <valor>         → muda BPM de um instrumento (ex: bpm guitarra 150)")
    print("bpm todos <valor>          → muda BPM de todos (ex: bpm todos 120)")
    print("volume <nome> <valor>      → muda volume (0.0 a 1.0) (ex: volume synth 0.7)")
    print("volume todos <valor>       → muda volume de todos (ex: volume todos 0.5)")
    print("sair                       → encerra o programa")
    print("="*50)

# --- Programa principal ---
def main():
    gerar_sons_faltantes()
    
    instruments = {}
    instrument_list = [
        ('bateria', 'bateria.wav', 120),
        ('baixo', 'baixo.wav', 100),
        ('guitarra', 'guitarra.wav', 140),
        ('synth', 'synth.wav', 110),
        ('sample1', 'sample1.wav', 80),
        ('sample2', 'sample2.wav', 130)
    ]
    
    for name, file_path, bpm in instrument_list:
        if os.path.exists(file_path):
            instruments[name] = Instrument(name, file_path, bpm=bpm)
            instruments[name].start()
            instruments[name].pause()

    try:
        while True:
            cmd = input("🎧 DJ> ").strip()
            if not cmd: continue
            parts = cmd.split()
            action = parts[0].lower()

            if action == 'pausar' and len(parts) > 1:
                if parts[1] == 'todos':
                    for inst in instruments.values(): inst.pause()
                else:
                    inst = instruments.get(parts[1])
                    if inst: inst.pause()

            elif action == 'tocar' and len(parts) > 1:
                if parts[1] == 'todos':
                    for inst in instruments.values(): inst.resume()
                else:
                    inst = instruments.get(parts[1])
                    if inst: inst.resume()

            elif action == 'bpm' and len(parts) > 2:
                if parts[1] == 'todos':
                    for inst in instruments.values(): inst.set_bpm(int(parts[2]))
                else:
                    inst = instruments.get(parts[1])
                    if inst: inst.set_bpm(int(parts[2]))

            elif action == 'volume' and len(parts) > 2:
                if parts[1] == 'todos':
                    for inst in instruments.values(): inst.set_volume(float(parts[2]))
                else:
                    inst = instruments.get(parts[1])
                    if inst: inst.set_volume(float(parts[2]))

            elif action == 'status':
                mostrar_status(instruments)

            elif action == 'ajuda':
                mostrar_ajuda()

            elif action in ('sair', 'exit', 'quit'):
                break

            else:
                print("❌ Comando inválido. Digite 'ajuda' para ver a lista.")
    except KeyboardInterrupt:
        pass
    finally:
        for inst in instruments.values():
            inst.stop()
        pygame.mixer.quit()
        print("👋 Encerrando DJ Mode...")

if __name__ == "__main__":
    main()
