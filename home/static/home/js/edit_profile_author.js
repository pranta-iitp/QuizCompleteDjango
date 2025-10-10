document.addEventListener('DOMContentLoaded', function() {
    const saveBtn = document.getElementById('saveProfileBtn');
    
    if (saveBtn) {
        saveBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const formData = {
                user_id: document.getElementById('userId')?.value || '',
                author_id: document.getElementById('authorId')?.value || '',
                author_name: document.getElementById('author_name').value,
                author_subject_a: document.getElementById('author_subject_a').value,
                author_subject_b: document.getElementById('author_subject_b').value,
                author_subject_c: document.getElementById('author_subject_c').value,
                author_subject_d: document.getElementById('author_subject_d').value
            };
            
            const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
            
            fetch('/update_author_profile/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => Promise.reject(err));
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                
                // Remove focus
                if (document.activeElement) {
                    document.activeElement.blur();
                }
                
                // Close edit profile modal
                const editModalElement = document.getElementById('editProfileModal');
                const editModal = bootstrap.Modal.getInstance(editModalElement);
                if (editModal) {
                    editModal.hide();
                }
                
                // ✅ Show success modal after brief delay
                setTimeout(() => {
                    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
                    successModal.show();
                }, 300);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating profile: ' + (error.error || 'Please try again.'));
            });
        });
    }
});