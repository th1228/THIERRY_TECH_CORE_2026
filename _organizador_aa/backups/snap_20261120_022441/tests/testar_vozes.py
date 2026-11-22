# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

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