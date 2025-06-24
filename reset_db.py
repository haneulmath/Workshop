#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import modele

if __name__ == "__main__":
    print("🔄 Réinitialisation forcée de la base de données...")
    if modele.force_reset_database():
        print("✅ Base de données réinitialisée avec succès!")
    else:
        print("❌ Erreur lors de la réinitialisation")
