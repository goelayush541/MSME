document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();
    
    // Initialize image gallery functionality
    initImageGallery();
    
    // Form validation
    initFormValidation();
    
    // Auto-dismiss alerts
    initAutoDismissAlerts();
    
    // Modal form handling
    initModalForms();
    
    // Tab functionality
    initTabs();
});

function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initImageGallery() {
    document.querySelectorAll('.img-thumbnail').forEach(function(thumb) {
        thumb.addEventListener('click', function() {
            const mainImg = this.closest('.card').querySelector('.card-img-top');
            if (mainImg) {
                mainImg.src = this.src;
            }
        });
    });
}

function initFormValidation() {
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
        });
    });
}

function initAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

function initModalForms() {
    // Clear modal form when hidden
    document.querySelectorAll('.modal').forEach(function(modal) {
        modal.addEventListener('hidden.bs.modal', function () {
            const form = this.querySelector('form');
            if (form) {
                form.reset();
                form.querySelectorAll('.is-invalid').forEach(function(el) {
                    el.classList.remove('is-invalid');
                });
            }
        });
    });
}

function initTabs() {
    // Activate first tab if none is active
    document.querySelectorAll('.nav-tabs').forEach(function(tabGroup) {
        if (!tabGroup.querySelector('.nav-link.active')) {
            const firstTab = tabGroup.querySelector('.nav-link');
            if (firstTab) {
                firstTab.classList.add('active');
                const tabContent = document.querySelector(firstTab.getAttribute('data-bs-target'));
                if (tabContent) {
                    tabContent.classList.add('show', 'active');
                }
            }
        }
    });
}