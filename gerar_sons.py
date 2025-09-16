import numpy as np
from scipy.io.wavfile import write
import os

def gerar_tom(nome, freq, duracao=0.5, samplerate=44100):
    """Gera um tom simples"""
    t = np.linspace(0, duracao, int(samplerate*duracao), False)
    onda = 0.5 * np.sin(2 * np.pi * freq * t)
    onda = np.int16(onda * 32767)
    write(f"{nome}.wav", samplerate, onda)
    print(f"🎵 {nome}.wav gerado!")

def gerar_sons_faltantes():
    """Gera todos os sons automaticamente"""
    print("🎹 Gerando sons para DJ Mode...")
    print("=" * 40)
    
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
        else:
            print(f"✅ {nome}.wav já existe")
    
    print("=" * 40)
    print("🎉 Todos os sons prontos!")
    print("👉 Agora execute: python dj_console.py")

if __name__ == "__main__":
    gerar_sons_faltantes()