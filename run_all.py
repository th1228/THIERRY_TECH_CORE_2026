import os
import sys

# Corrige a localização da pasta raiz automaticamente
# O __file__ é o caminho deste arquivo run_all.py
raiz = os.path.dirname(os.path.abspath(__file__))

# O resto da sua lista de módulos continua igual:
modulos = [
    "core/neuro_gravidade_preditor.py",
    "core/biogemio_test.py",
    "core/motor_dados.py",
    "core/modulo_psiquico.py",
    "core/monaco/monaco_integrador.py",
    "core/gerador_relatorio_definitivo.py"
]