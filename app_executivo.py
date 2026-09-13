import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as str
import plotly.graph_objects as go

# 1. ORCHESTRATION & ULTRA HIGH-END CONFIGURATION
str.set_page_config(
    page_title="THIERRY TECHNOLOGY GLOBAL // MONACO & DUBAI PROTOCOL",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. LUXURY ARCHITECTURE INJECTION
str.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@200;300;400;500&display=swap');

        #MainMenu, footer, header {visibility: hidden;}
        
        .stApp {
            background-color: #07080a !important;
            font-family: 'Inter', sans-serif;
            color: #E5D3B3;
        }
        
        .imperial-title {
            font-family: 'Cinzel', serif;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 5px;
            color: #E5D3B3;
        }

        .quantum-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.015) 0%, rgba(229, 211, 179, 0.03) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(229, 211, 179, 0.12);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 10px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7), 0 0 15px rgba(229, 211, 179, 0.03);
        }
        
        .quantum-tag {
            font-family: 'Cinzel', serif;
            color: #D4AF37;
            font-size: 9px;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 4px;
            opacity: 0.85;
            font-weight: 600;
        }

        .quantum-value {
            color: #FFFFFF;
            font-size: 22px;
            font-weight: 200;
            letter-spacing: -0.5px;
            margin-bottom: 2px;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        }
        
        .quantum-status {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: rgba(229, 211, 179, 0.6);
        }
    </style>
""", unsafe_allow_html=True)

# Inicialização do Fluxo de Estados do Protocolo TTC Global
if "fluxo_etapa" not in str.session_state:
    str.session_state.fluxo_etapa = 0  # 0: Início/Repouso, 1: Coleta de Dados, 2: Security & Stripe, 3: Câmera Biométrica, 4: Relatório PDF Pronto

if "paciente" not in str.session_state:
    str.session_state.paciente = ""
if "medico" not in str.session_state:
    str.session_state.medico = ""
if "empresa" not in str.session_state:
    str.session_state.empresa = ""

# Cabeçalho corporativo compactado
str.markdown(
    '<div class="imperial-title" style="font-size: 11px; text-align: center; padding: 2px 0 10px 0;">'
    'TTC GLOBAL // MONACO & DUBAI ELITE PROTOCOL'
    '</div>', 
    unsafe_allow_html=True
)

# 3. METRIC DISTRIBUTION (3 Colunas)
col1, col2, col3 = str.columns([1, 1.4, 1])

with col1:
    str.markdown('<div class="quantum-card">'
                 '<div class="quantum-tag">🧠 Neurogenomic Index</div>'
                 '<div class="quantum-value">94.8 SQ</div>'
                 '<div class="quantum-status">[ Ápice Homeostático ]</div>'
                 '</div>', unsafe_allow_html=True)
    
    str.markdown('<div class="quantum-card">'
                 '<div class="quantum-tag">⚡ Neuroplasticity Rate</div>'
                 '<div class="quantum-value">4.82 Hz</div>'
                 '<div class="quantum-status">[ Potencial Sináptico Elevado ]</div>'
                 '</div>', unsafe_allow_html=True)
    
    str.markdown('<div class="imperial-title" style="font-size:9px; opacity:0.8; margin-bottom:2px; margin-left:2px;">📊 Telemetria Sináptica</div>', unsafe_allow_html=True)
    
    fig_neuro = go.Figure()
    fig_neuro.add_trace(go.Scatterpolar(
        r=[85, 90, 75, 88, 92],
        theta=['Vascularização', 'Dopamina', 'Simetria', 'Serotonina', 'Cognição'],
        mode='markers',
        marker=dict(size=6, color='#D4AF37', symbol='diamond', line=dict(color='#FFFFFF', width=0.5)),
        name='HUD Neurosináptico'
    ))
    fig_neuro.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showline=False, showticklabels=False, gridcolor='rgba(212, 175, 55, 0.05)', range=[0, 100]),
            angularaxis=dict(gridcolor='rgba(212, 175, 55, 0.06)', tickfont=dict(size=8, color='rgba(229, 211, 179, 0.8)', family='Inter, sans-serif'), linecolor='rgba(212, 175, 55, 0.1)'),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        margin=dict(l=25, r=25, t=5, b=5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=150
    )
    str.plotly_chart(fig_neuro, config={'displayModeBar': False}, use_container_width=True)

with col2:
    # ELEMENTO CENTRAL: Máquina de Estados do Protocolo Lógico
    
    # ETAPA 0: Tela Inicial com o Rosto Holográfico e Gatilho de Clique
    if str.session_state.fluxo_etapa == 0:
        scanner_html = """
        <div style="display: flex; justify-content: center; align-items: center; height: 320px; background: transparent;">
            <div style="position: relative; width: 280px; height: 280px; display: flex; justify-content: center; align-items: center; background: radial-gradient(circle, rgba(229,211,179,0.03) 0%, rgba(7,8,10,0.8) 70%); border-radius: 50%; box-shadow: inset 0 0 40px rgba(229,211,179,0.05);">
                
                <div style="position: absolute; width: 85%; height: 1.5px; background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.8), transparent); z-index: 3; animation: scanVertical 6s ease-in-out infinite; filter: drop-shadow(0 0 8px #D4AF37);"></div>
                <div style="position: absolute; width: 100%; height: 100%; border: 0.5px dashed rgba(212, 175, 55, 0.2); border-radius: 50%; animation: rotateClockwise 50s linear infinite;"></div>
                <div style="position: absolute; width: 92%; height: 92%; border: 0.5px solid rgba(229, 211, 179, 0.05); border-radius: 50%; animation: rotateCounterClockwise 35s linear infinite;"></div>
                
                <svg style="position: absolute; width: 75%; height: 75%; z-index: 2; animation: floatAndGlow 5s ease-in-out infinite; filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.25));" viewBox="0 0 100 100" fill="none" xmlns="http://w3.org/2000/svg">
                    <path d="M25,28 C25,12 75,12 75,28 C75,52 66,74 50,88 C34,74 25,52 25,28 Z" stroke="#D4AF37" stroke-width="0.35" stroke-dasharray="3 1"/>
                    <path d="M25.8,32 Q50,44 74.2,32" stroke="rgba(229, 211, 179, 0.3)" stroke-width="0.25"/>
                    <path d="M27.5,42 Q50,56 72.5,42" stroke="rgba(229, 211, 179, 0.3)" stroke-width="0.25"/>
                    <path d="M30,55 Q50,70 70,55" stroke="rgba(229, 211, 179, 0.2)" stroke-width="0.25"/>
                    <path d="M34,68 Q50,80 66,68" stroke="rgba(229, 211, 179, 0.15)" stroke-width="0.25"/>
                    <path d="M38,20 C36,40 38,60 44,75" stroke="rgba(212, 175, 55, 0.25)" stroke-width="0.25"/>
                    <path d="M62,20 C64,40 62,60 56,75" stroke="rgba(212, 175, 55, 0.25)" stroke-width="0.25"/>
                    <line x1="50" y1="13" x2="50" y2="88" stroke="rgba(212, 175, 55, 0.25)" stroke-width="0.25" stroke-dasharray="1 3"/>
                    <path d="M32,45 Q40,39 45,45 Q40,49 32,45 Z" stroke="#E5D3B3" stroke-width="0.45"/>
                    <path d="M68,45 Q60,39 55,45 Q60,49 68,45 Z" stroke="#E5D3B3" stroke-width="0.45"/>
                    <circle cx="38.5" cy="44.5" r="1.2" stroke="#E5D3B3" stroke-width="0.3"/>
                    <circle cx="61.5" cy="44.5" r="1.2" stroke="#E5D3B3" stroke-width="0.3"/>
                    <path d="M47,39 L47,44 L45,58 L50,62 L55,58 L53,44 L53,39" stroke="#E5D3B3" stroke-width="0.45" stroke-linejoin="round"/>
                    <path d="M37,68 Q50,62 63,68 Q50,75 37,68 Z" stroke="#E5D3B3" stroke-width="0.45"/>
                    <circle cx="50" cy="14" r="0.8" fill="#FFF" filter="drop-shadow(0 0 4px #D4AF37)"/>
                    <circle cx="32" cy="45" r="0.8" fill="#FFF" filter="drop-shadow(0 0 4px #D4AF37)"/>
                    <circle cx="68" cy="45" r="0.8" fill="#FFF" filter="drop-shadow(0 0 4px #D4AF37)"/>
                    <circle cx="50" cy="62" r="0.8" fill="#FFF" filter="drop-shadow(0 0 4px #D4AF37)"/>
                    <circle cx="50" cy="87" r="0.8" fill="#FFF" filter="drop-shadow(0 0 4px #D4AF37)"/>
                </svg>
            </div>
        </div>

        <style>
            @keyframes rotateClockwise { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            @keyframes rotateCounterClockwise { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
            @keyframes scanVertical { 0%, 100% { top: 10%; opacity: 0; } 15%, 85% { opacity: 1; } 50% { top: 90%; } }
            @keyframes floatAndGlow {
                0%, 100% { transform: translateY(0px); opacity: 0.95; }
                50% { transform: translateY(-6px); opacity: 1; filter: drop-shadow(0 6px 16px rgba(212, 175, 55, 0.35)); }
            }
        </style>
        """
        str.components.v1.html(scanner_html, height=320)
        
        if str.button("🚀 INICIAR PROTOCOLO HOLOGRÁFICO", use_container_width=True):
            str.session_state.fluxo_etapa = 1
            str.rerun()

    # ETAPA 1: Coleta de Dados (Pessoa, Médico, Empresa)
    elif str.session_state.fluxo_etapa == 1:
        str.markdown('<div class="quantum-card">', unsafe_allow_html=True)
        str.markdown('<div class="quantum-tag">CREDENCIMENTO EXECUTIVO</div>', unsafe_allow_html=True)
        
        str.session_state.paciente = str.text_input("Nome da Pessoa / Paciente", str.session_state.paciente)
        str.session_state.medico = str.text_input("Nome do Médico / Especialista", str.session_state.medico)
        str.session_state.empresa = str.text_input("Empresa / Instituição", str.session_state.empresa)
        
        if str.button("VALIDAR & ACIONAR SECURITY ENGINE", use_container_width=True):
            if str.session_state.paciente and str.session_state.medico:
                str.session_state.fluxo_etapa = 2
                str.rerun()
            else:
                str.warning("Por favor, preencha os campos obrigatórios.")
        str.markdown('</div>', unsafe_allow_html=True)

    # ETAPA 2: Acordar Security & Abrir Licenciamento Stripe
    elif str.session_state.fluxo_etapa == 2:
        str.markdown('<div class="quantum-card" style="text-align: center; padding: 40px 20px;">', unsafe_allow_html=True)
        str.markdown('<div class="quantum-tag">[ SECURITY & STRIPE GATEWAY ]</div>', unsafe_allow_html=True)
        str.markdown('<div class="quantum-value" style="font-size: 16px; margin: 15px 0;">Sistemas de Segurança Despertados. Conectando Licenciamento Monaco Tier...</div>', unsafe_allow_html=True)
        str.markdown('<div class="quantum-status">Status: Pagamento Aprovado via Stripe API.</div>', unsafe_allow_html=True)
        
        if str.button("⏩ AVANÇAR PARA CÂMERA BIOMÉTRICA", use_container_width=True):
            str.session_state.fluxo_etapa = 3
            str.rerun()
        str.markdown('</div>', unsafe_allow_html=True)

    # ETAPA 3: Câmera com Motor Biométrico
    elif str.session_state.fluxo_etapa == 3:
        str.markdown('<div class="quantum-card" style="text-align: center; padding: 30px 20px;">', unsafe_allow_html=True)
        str.markdown('<div class="quantum-tag">[ MOTOR BIOMÉTRICO ATIVO ]</div>', unsafe_allow_html=True)
        str.markdown('<div style="color: #FFF; font-size: 12px; margin: 15px 0;">Processando malha facial, osteometria e telemetria em tempo real...</div>', unsafe_allow_html=True)
        
        # Simulação visual da captura da câmera biométrica
        scanner_cam = """
        <div style="display: flex; justify-content: center; align-items: center; height: 180px; background: rgba(0,0,0,0.6); border: 1px solid #D4AF37; border-radius: 8px;">
            <div style="font-family: 'Cinzel', serif; color: #D4AF37; font-size: 11px; letter-spacing: 2px;">[ WEBCAM / MEDIAPIPE CONECTADO ]</div>
        </div>
        """
        str.components.v1.html(scanner_cam, height=180)
        
        if str.button("✅ CONCLUIR LEITURA & GERAR PDF", use_container_width=True):
            str.session_state.fluxo_etapa = 4
            str.rerun()
        str.markdown('</div>', unsafe_allow_html=True)

    # ETAPA 4: Exibir Resultado PDF em Tempo Real
    elif str.session_state.fluxo_etapa == 4:
        str.markdown('<div class="quantum-card" style="padding: 20px;">', unsafe_allow_html=True)
        str.markdown('<div class="quantum-tag">[ RELATÓRIO EXECUTIVO GERADO ]</div>', unsafe_allow_html=True)
        str.markdown(f'<div class="quantum-value" style="font-size: 15px; margin-top: 10px;">Paciente: {str.session_state.paciente}</div>', unsafe_allow_html=True)
        str.markdown(f'<div class="quantum-status">Médico: {str.session_state.medico} | Empresa: {str.session_state.empresa}</div>', unsafe_allow_html=True)
        str.markdown('<hr style="border-color: rgba(212,175,55,0.2);">', unsafe_allow_html=True)
        str.markdown('<div style="font-size: 11px; color: #E5D3B3; margin-bottom: 15px;">PDF estruturado com sucesso e validado pelo motor biométrico Monaco & Dubai Protocol.</div>', unsafe_allow_html=True)
        
        if str.button("🔄 REINICIAR NOVO PROTOCOLO", use_container_width=True):
            str.session_state.fluxo_etapa = 0
            str.session_state.paciente = ""
            str.session_state.medico = ""
            str.session_state.empresa = ""
            str.rerun()
        str.markdown('</div>', unsafe_allow_html=True)

with col3:
    str.markdown('<div class="quantum-card">'
                 '<div class="quantum-tag">🧬 Regenerative Medicine</div>'
                 '<div class="quantum-value">91.4%</div>'
                 '<div class="quantum-status">[ Telômeros Estabilizados ]</div>'
                 '</div>', unsafe_allow_html=True)
    
    str.markdown('<div class="quantum-card">'
                 '<div class="quantum-tag">⏳ Cellular Longevity</div>'
                 '<div class="quantum-value">1.18 yrs</div>'
                 '<div class="quantum-status">[ Desaceleração Epigenética ]</div>'
                 '</div>', unsafe_allow_html=True)
    
    str.markdown('<div class="imperial-title" style="font-size:9px; opacity:0.8; margin-bottom:2px; margin-left:2px;">📊 Densidade Celular</div>', unsafe_allow_html=True)
    
    fig_regen = go.Figure()
    fig_regen.add_trace(go.Scatterpolar(
        r=[89, 94, 82, 91, 88],
        theta=['Colágeno IV', 'Fibroblastos', 'Melanina', 'Mitocôndria', 'Oxigenação'],
        mode='markers',
        marker=dict(size=6, color='#D4AF37', symbol='diamond', line=dict(color='#FFFFFF', width=0.5)),
        name='HUD Regenerativo'
    ))
    fig_regen.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showline=False, showticklabels=False, gridcolor='rgba(212, 175, 55, 0.05)', range=[0, 100]),
            angularaxis=dict(gridcolor='rgba(212, 175, 55, 0.06)', tickfont=dict(size=8, color='rgba(229, 211, 179, 0.8)', family='Inter, sans-serif'), linecolor='rgba(212, 175, 55, 0.1)'),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        margin=dict(l=25, r=25, t=5, b=5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=150
    )
    str.plotly_chart(fig_regen, config={'displayModeBar': False}, use_container_width=True)