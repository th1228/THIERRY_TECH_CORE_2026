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

import wave
import struct
import math
import os
import json

# 1. Criação do Som Tecnológico (Bipe digital)
os.makedirs("assets", exist_ok=True)
caminho_som = "assets/scan_ping.wav"

sample_rate = 44100
duration = 0.08  # 80 milissegundos
frequency = 1200.0

with wave.open(caminho_som, 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit
    wav_file.setframerate(sample_rate)
    
    for i in range(int(sample_rate * duration)):
        t = i / sample_rate
        envelope = 1.0 - (i / (sample_rate * duration))
        value = int(32767 * 0.3 * envelope * math.sin(2 * math.pi * frequency * t))
        wav_file.writeframes(struct.pack('<h', value))

print(f"[SUCESSO] O arquivo de som foi criado em: {caminho_som}")


# 2. Geração e Salvamento das Métricas do Dossiê (JSON Oficial)
os.makedirs("dados", exist_ok=True)
caminho_json = "dados/estado_atual.json"

dados_dossie = {
    "status": "sucesso",
    "cabecalho_institucional": {
        "instituicao": "Thierry Technology Concept Global",
        "titulo_do_dossie": "Dossiê Mestre de Leitura Oximétrica e Tricológica",
        "autoridade_tecnologica": "Thierry Concept Global",
        "paciente_id": "Paciente_salao",
        "medico_responsavel": "Dr. Especialista TTC",
        "estilista_responsavel": "Thierry Concept Global"
    },
    "timestamp": "2026-08-12 01:15:45",
    "gateway_salao_de_beleza": {
        "setor": "Tricologia Avançada e Estética Capilar",
        "leitura_hidratação_facial_e_couro_cabeludo": "77.1% retenção",
        "refletancia_da_pele": "41.2%",
        "densidade_capilar": "217 fios/cm²",
        "alerta_clinico_queda_e_alopecia": "Densidade capilar estável (217 fios/cm²). Manutenção preventiva.",
        "formato_de_rosto": "Quadrado / Mandíbula e Topo Largos",
        "classificacao_profundidade_olhar": "Dinâmico / Reativo (Alta Dinâmica Visual)",
        "saude_do_fio_capilar": "Córtex intermediário; necessita acidificação.",
        "parametros_de_corte_e_manutencao": {
            "frequencia_ideal_de_corte": "A cada 3 meses",
            "intervalo_em_meses": "3 meses",
            "diretriz_visagismo": "Corte simétrico para valorizar traços."
        },
        "dez_opcoes_de_corte_visagismo": [
            {
                "id": 1,
                "categoria": "Curto",
                "nome": "Pixie Contour",
                "visagismo": "Emoldura traços finos com leveza.",
                "tipo_de_franja": "Lateral desfiada",
                "penteado_indicado": "Pomada matte",
                "harmonia_refletancia_e_cor": "Ideal pele 41.2%."
            },
            {
                "id": 2,
                "categoria": "Curto",
                "nome": "Bixie Estruturado",
                "visagismo": "Volume controlado no topo.",
                "tipo_de_franja": "Baby fringe",
                "penteado_indicado": "Spray seco",
                "harmonia_refletancia_e_cor": "Bom contraste pele 41.2%."
            },
            {
                "id": 3,
                "categoria": "Curto",
                "nome": "French Bob",
                "visagismo": "Base reta elegante no queixo.",
                "tipo_de_franja": "Reta clássica",
                "penteado_indicado": "Liso polido",
                "harmonia_refletancia_e_cor": "Harmonia pele 41.2%."
            },
            {
                "id": 4,
                "categoria": "Médio",
                "nome": "Long Bob Geométrico",
                "visagismo": "Alonga o pescoço e suaviza ângulos.",
                "tipo_de_franja": "Lateral degradê",
                "penteado_indicado": "Escova modelada",
                "harmonia_refletancia_e_cor": "Valoriza pele 41.2%."
            },
            {
                "id": 5,
                "categoria": "Médio",
                "nome": "Shaggy Hair",
                "visagismo": "Volume topo e leveza pontas.",
                "tipo_de_franja": "Curtain bangs",
                "penteado_indicado": "Ativador natural",
                "harmonia_refletancia_e_cor": "Dispersão pele 41.2%."
            },
            {
                "id": 6,
                "categoria": "Médio",
                "nome": "Medium Blunt Cut",
                "visagismo": "Base reta de alta densidade.",
                "tipo_de_franja": "Sem franja/reta",
                "penteado_indicado": "Glass hair",
                "harmonia_refletancia_e_cor": "Brilho pele 41.2%."
            },
            {
                "id": 7,
                "categoria": "Longo",
                "nome": "Long Layers",
                "visagismo": "Camadas longas pós queixo.",
                "tipo_de_franja": "Longa integrada",
                "penteado_indicado": "Ondas largas",
                "harmonia_refletancia_e_cor": "Moldura pele 41.2%."
            },
            {
                "id": 8,
                "categoria": "Longo",
                "nome": "Longo Reto Despontado",
                "visagismo": "Simplicidade com toque moderno.",
                "tipo_de_franja": "Desfiada leve",
                "penteado_indicado": "Óleos reparadores",
                "harmonia_refletancia_e_cor": "Equilíbrio pele 41.2%."
            },
            {
                "id": 9,
                "categoria": "Longo",
                "nome": "Butterfly Cut",
                "visagismo": "Camadas marcadas e versáteis.",
                "tipo_de_franja": "Cortina volumosa",
                "penteado_indicado": "Max volume",
                "harmonia_refletancia_e_cor": "Destaca pele 41.2%."
            },
            {
                "id": 10,
                "categoria": "Longo",
                "nome": "Repicado Invisível",
                "visagismo": "Mantém comprimento com leveza.",
                "tipo_de_franja": "Sem franja",
                "penteado_indicado": "Semi-preso flexível",
                "harmonia_refletancia_e_cor": "Integra pele 41.2%."
            }
        ],
        "cronograma_tratamentos_intercalados": [
            {"etapa": "1. Detox", "tecnologia_e_marca": "L'Oréal - Metal Detox", "função": "Neutraliza metais pesados."},
            {"etapa": "2. pH", "tecnologia_e_marca": "Acidificação TTC", "função": "Ajusta ponto isoelétrico."},
            {"etapa": "3. Reconstrução", "tecnologia_e_marca": "L'Oréal - Absolut Repair", "função": "Repõe peptídeos no córtex."},
            {"etapa": "4. Choque", "tecnologia_e_marca": "Joico - CPR", "função": "Recupera porosidade."},
            {"etapa": "5. Regeneração", "tecnologia_e_marca": "Wella - Ultimate Repair", "função": "AHA e Ômega 9."},
            {"etapa": "6. Nutrição", "tecnologia_e_marca": "Kérastase - Chronologiste", "função": "Infusão vitamínica."},
            {"etapa": "7. Restauração", "tecnologia_e_marca": "Senscience - Inner Restore", "função": "Restaura elasticidade."},
            {"etapa": "8. Botânica", "tecnologia_e_marca": "Davines - Oi / NouNou", "função": "Proteção antioxidante."}
        ]
    },
    "gateway_monocoplano": {
        "setor": "Monocoplano Core - Biomecânica",
        "score_estabilidade_postural": 90.71,
        "score_simetria_facial": 57.26,
        "media_instabilidade_pct": 0.374,
        "leitura_sistema_parassimpatico": "Direito (Sensorial)",
        "nivel_de_fadiga_e_estresse": "Fadiga: 7.5%",
        "condicao_craniofacial": "Variação Adaptativa",
        "analise_ocular": "Dinâmico / Reativo (Alta Dinâmica Visual)"
    },
    "gateway_clinica_medica": {
        "setor": "Medicina Regenerativa",
        "biomarcadores_de_regeneracao": {
            "taxa_regeneracao_celular_diaria": "82.8%",
            "quantidade_de_agua_na_pele": "77.1%",
            "estresse_cutaneo": "6.9%",
            "oximetria_tecidual_periferica": "97.8%",
            "nivel_de_inflamacao": "Moderado (Tensão Reativa)",
            "durabilidade_estimada_toxina_botulinica": "120 dias",
            "interferencia_climatica_oxidacao_aqi": "AQI 45 (28.0°C)"
        },
        "cronograma_neuroplasticidade": {
            "dia_apice_regenerativo_e_desinflamacao": "2026-08-25",
            "tempo_estimado_para_pico_de_sinergia": "13 dias"
        },
        "protocolo_de_excelencia_pele_porcelana": {
            "objetivo": "Refinamento textural para Pele de Porcelana",
            "complementacao_toxina_e_bioestimuladores": [
                "Neurotoxina modular: 120 dias.",
                "Bioestimuladores para colágeno profundo.",
                "Complexos de luxo para matriz."
            ],
            "nivel_de_inflamacao_e_correcao": "Correção de micro-inflamação (Moderado (Tensão Reativa)).",
            "observacao_tratamentos_ultra_premium": "Ápice regenerativo: 13d | Novo nascimento: 2026-08-25 | Uso de exossomos e polinucleotídeos."
        }
    },
    "gateway_neuro_performance": {
        "setor": "Guia de Decisão e Ambiente",
        "perfil_de_decisao_e_comportamento": {
            "lado": "Direito",
            "estilo": "Criativo e Sensorial",
            "cor_indicada": "Verde / Nude",
            "oleo_fitoterapico": "Lavanda / Sândalo",
            "frequencia_musical": "528Hz (Calma)",
            "massagem": "Shiatsu Relaxante"
        },
        "tabela_guia_de_apoio": [
            {"parametro": "Paciente", "indicacao": "Paciente_salao"},
            {"parametro": "Especialista Responsável", "indicacao": "Dr. Especialista TTC"},
            {"parametro": "Estilista / Visagista", "indicacao": "Thierry Concept Global"},
            {"parametro": "Profundidade do Olhar", "indicacao": "Dinâmico / Reativo (Alta Dinâmica Visual)"},
            {"parametro": "Dominância", "indicacao": "Direito"},
            {"parametro": "Estilo de Decisão", "indicacao": "Criativo e Sensorial"},
            {"parametro": "Cromoterapia", "indicacao": "Verde / Nude"},
            {"parametro": "Óleo Fitoterápico", "indicacao": "Lavanda / Sândalo"},
            {"parametro": "Frequência Sonora", "indicacao": "528Hz (Calma)"},
            {"parametro": "Massagem Recomendada", "indicacao": "Shiatsu Relaxante"}
        ]
    },
    "desenvolvimento_tecnologico": "Thierry Concept Global"
}

with open(caminho_json, 'w', encoding='utf-8') as f:
    json.dump(dados_dossie, f, ensure_ascii=False, indent=4)

print(f"[SUCESSO] O arquivo de métricas foi gerado e salvo em: {caminho_json}")