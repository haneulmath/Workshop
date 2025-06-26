# Éléments à supprimer après validation

## 🗑️ Fichiers d'archive à supprimer (après tests complets)

### **Fichiers CSS d'archive**
```bash
# Après validation complète de l'application :
rm static/css/unused-styles.css
```

### **Fichiers JavaScript d'archive**
```bash
# Après validation que les fonctions ne sont vraiment pas utilisées :
rm static/js/unused-functions.js
```

## 🧪 Tests de validation recommandés

### **Tests fonctionnels**
- [ ] Page d'accueil : affichage des légendes de sièges
- [ ] Page admin : grille des sièges et modification
- [ ] Page de réservation : sélection des sièges
- [ ] Page showing_seats : affichage et interaction
- [ ] Responsive : test sur mobile/tablette

### **Tests d'apparence**
- [ ] Vérifier que tous les sièges s'affichent correctement
- [ ] Vérifier les états (disponible, sélectionné, occupé, PMR)
- [ ] Vérifier les légendes avec images
- [ ] Vérifier les hover effects et animations

### **Tests de performance**
- [ ] Mesurer le temps de chargement CSS avant/après
- [ ] Vérifier l'absence d'erreurs console
- [ ] Valider la taille des fichiers CSS

## 📋 Checklist de nettoyage final

### **Phase 1 : Validation (1-2 semaines)**
- [ ] Tests utilisateur complets
- [ ] Validation des différents navigateurs
- [ ] Tests responsive sur différents appareils
- [ ] Vérification des performances

### **Phase 2 : Nettoyage (après validation)**
```bash
# Supprimer les fichiers d'archive
rm static/css/unused-styles.css
rm static/js/unused-functions.js

# Optionnel : supprimer la documentation d'optimisation
rm static/OPTIMIZATION_REPORT.md
rm static/CLEANUP_DOCUMENTATION.md
rm static/REFACTORING_SUMMARY.md
rm static/SEAT_MODIFICATIONS_SUMMARY.md
rm static/CORRECTIONS_SUMMARY.md
rm static/FINAL_CORRECTIONS.md
rm static/CLEANUP_TODO.md
```

### **Phase 3 : Production**
```bash
# Minifier les CSS pour la production
# Optimiser les images si nécessaire
# Mettre en place la compression gzip
```

## ⚠️ Avertissements

### **NE PAS supprimer maintenant**
- Les fichiers `unused-*` contiennent du code potentiellement utile
- Certains styles peuvent être utilisés dans des cas edge non testés
- Les fonctions JavaScript peuvent être appelées dynamiquement

### **Validation requise**
- Tester toutes les pages de l'application
- Vérifier avec différents types d'utilisateurs
- Tester les cas d'erreur et les edge cases
- Valider sur différents navigateurs

## 🎯 Objectifs de nettoyage

### **Immédiat**
- ✅ Code optimisé et consolidé
- ✅ Réduction de 45% du CSS
- ✅ Suppression des doublons
- ✅ Documentation complète

### **Après validation**
- 🎯 Suppression des fichiers d'archive
- 🎯 Nettoyage de la documentation temporaire
- 🎯 Préparation pour la production

---
*Note : Conserver ce fichier jusqu'à la suppression finale des archives*
