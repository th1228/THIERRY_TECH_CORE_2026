import math
import sys

# Ajuste para garantir que o terminal aceite emojis e caracteres especiais
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class LuxuryPorts:
    """
    Base de dados oficial da THIERRY Technology Concept Global.
    """

    def __init__(self):
        self.active_hubs = {
            "monaco": {
                "name": "Port Hercule, Monaco 🇲🇨",
                "coords": (43.7345, 7.4253),
                "tier": "Standard Mônaco | High Performance"
            },
            "usa": {
                "name": "Manhattan Hub, USA 🇺🇸",
                "coords": (40.7128, -74.0060),
                "tier": "Premium Tech"
            },
            "dubai": {
                "name": "Dubai Marina, UAE 🇦🇪",
                "coords": (25.0819, 55.1367),
                "tier": "Ultra-Luxury Hub"
            },
            "switzerland": {
                "name": "Zurich Hub, Switzerland 🇨🇭",
                "coords": (47.3769, 8.5417),
                "tier": "Precision Science"
            },
            "france": {
                "name": "Paris Hub, France 🇫🇷",
                "coords": (48.8566, 2.3522),
                "tier": "Luxury Aesthetics"
            },
            "japan": {
                "name": "Tokyo Hub, Japan 🇯🇵",
                "coords": (35.6895, 139.6917),
                "tier": "Advanced Robotics"
            },
            "germany": {
                "name": "Berlin Hub, Germany 🇩🇪",
                "coords": (52.5200, 13.4050),
                "tier": "Engineering Excellence"
            },
            "brazil": {
                "name": "São Luís Tech Base, Brazil 🇧🇷",
                "coords": (-2.5307, -44.3068),
                "tier": "Development Headquarters"
            }
        }

    def list_all_hubs(self):
        return [data["name"] for data in self.active_hubs.values()]

if __name__ == "__main__":
    ttc_ports = LuxuryPorts()
    print("--- TTC GLOBAL: LISTA DE DESTINOS ---")
    hubs = ttc_ports.list_all_hubs()
    for hub in hubs:
        # Usamos o .encode().decode() como segurança extra para o terminal
        print(f"Ativo: {hub}")