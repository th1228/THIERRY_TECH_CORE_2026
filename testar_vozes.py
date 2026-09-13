# -*- coding: utf-8 -*-
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("=== LISTA DE VOZES DISPONÍVEIS ===")
for i, v in enumerate(voices):
    print(f"[{i}] Nome: {v.name}")
    print(f"    ID: {v.id}\n")

print("Testando a voz atual...")
engine.say("Teste de áudio do sistema Mônaco. Vozes ajustadas com sucesso.")
engine.runAndWait()