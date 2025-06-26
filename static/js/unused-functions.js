// Fonctions JavaScript non utilisées - Archive
// Ces fonctions ont été identifiées comme non utilisées dans l'application actuelle
// Elles sont archivées ici pour référence future

// Fonction utilitaire pour formater les prix - non utilisée dans les templates
function formatPrice(cents) {
    return (cents / 100).toFixed(2) + '€';
}

// Fonction utilitaire pour formater les dates - non utilisée dans les templates
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleDateString('fr-FR');
}

// Fonction utilitaire pour formater les heures - non utilisée dans les templates
function formatTime(time) {
    if (typeof time === 'string') {
        return time.substring(0, 5); // Garder seulement HH:MM
    }
    return time;
}

// Fonction pour afficher les messages d'alerte - non utilisée dans les templates
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insérer l'alerte au début du conteneur principal
    const container = document.querySelector('.container, .container-fluid');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    // Auto-supprimer l'alerte après 5 secondes
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Fonction pour gérer les confirmations de suppression - non utilisée dans les templates
function confirmDelete(message = 'Êtes-vous sûr de vouloir supprimer cet élément ?') {
    return confirm(message);
}

// Fonction pour valider les formulaires - non utilisée dans les templates
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Fonction pour gérer les requêtes AJAX - non utilisée dans les templates
async function makeAjaxRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erreur AJAX:', error);
        showAlert('Une erreur est survenue lors de la communication avec le serveur.', 'danger');
        throw error;
    }
}

// Fonctions d'initialisation non utilisées
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate="true"]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showAlert('Veuillez remplir tous les champs requis.', 'warning');
            }
        });
    });
}

function initializeModalFocus() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = this.querySelector('input, select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });
}
