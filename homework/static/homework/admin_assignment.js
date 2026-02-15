// static/homework/admin_assignment.js

(function() {
    function init() {
        const templateSelect = document.getElementById('id_source_template');
        if (!templateSelect) {
            console.warn('Assignment template select element not found: id_source_template');
            return;
        }

        console.log('Assignment template script initialized. Listening on #id_source_template');
        
        templateSelect.addEventListener('change', function() {
            const templateId = this.value;
            console.log('Template selected:', templateId);
            
            if (!templateId) return;

            fetch(`/homework/template-json/${templateId}/`)
                .then(response => {
                    console.log('Fetch response status:', response.status);
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(data => {
                    console.log('Template data received:', data);
                    if (data.error) {
                        console.error(data.error);
                        return;
                    }
                    
                    // Fields to populate
                    const titleField = document.getElementById('id_title');
                    const descField = document.getElementById('id_description');
                    const starterCodeField = document.getElementById('id_starter_code'); 
                    
                    if (titleField) {
                        titleField.value = data.title;
                        console.log('Updated title');
                    }
                    if (descField) {
                         descField.value = data.description;
                         console.log('Updated description');
                    }
                    if (starterCodeField) {
                        starterCodeField.value = data.starter_code;
                        console.log('Updated starter code');
                    }

                })
                .catch(err => console.error('Error fetching template:', err));
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
