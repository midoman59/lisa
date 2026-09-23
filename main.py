#!/usr/bin/env python3
"""
Agent Lisa Demo - Point d'entrée principal
Démonstrateur d'agent IA pour LS V3.8.0
"""

import sys
import os

# Ajouter src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent.agent_data import DataAgent

def main():
    """Lance l'agent Lisa en mode interactif"""
    print("\n" + "=" * 70)
    print("  🏦 AGENT LISA DEMO - LS V3.8.0")
    print("  Loan Servicing Intelligent Agent")
    print("=" * 70)

    try:
        # Initialiser l'agent
        print("\n📦 Initialisation de l'Agent...")
        agent = DataAgent()
        print("✓ Agent initialisé avec succès\n")

        # Lancer en mode conversation
        agent.chat()

    except KeyboardInterrupt:
        print("\n\n👋 Arrêt de l'agent. Au revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
