// Helper to populate the Quiz Subject select element for the current author
function populateQuizSubjects() {
    const authorId = document.getElementById('authorId').value;
    const quizSubjectSelect = document.getElementById('quizSubject');
    const subjectError = document.getElementById('subjectError');
    const createQuizBtn = document.getElementById('quizCreateSubmitButton')
    // Clear previous options
    quizSubjectSelect.innerHTML = '';
    if (!authorId) return; // No author ID

    fetch(`/author_subjects_api/?author_id=${encodeURIComponent(authorId)}`)
        .then(response => response.json())
        .then(data => {
            const subjects = data.subjects || [];
            console.log('subjects',subjects);
            if (subjects.length === 0) {
                quizSubjectSelect.innerHTML = '<option value="">No subjects configured</option>';
                subjectError.innerHTML = 'No subjects configured for this author. Consider updating your profile.';
                if (createQuizBtn) {
                    createQuizBtn.classList.add('disabled');
                    createQuizBtn.setAttribute('title', 'You must have at least one subject to create a quiz');
                    createQuizBtn.style.pointerEvents = 'none'; // Prevent click
                }
            } else {
                quizSubjectSelect.innerHTML = '<option value="">Select a subject</option>';
                subjects.forEach(subject => {
                    const option = document.createElement('option');
                    option.value = subject;
                    option.textContent = subject;
                    quizSubjectSelect.appendChild(option);
                });
            }
        })
        .catch(() => {
            quizSubjectSelect.innerHTML = '<option value="">Error loading subjects</option>';
        });
}

// When 'Create New Quiz' is clicked, prepare the subject dropdown
document.addEventListener('DOMContentLoaded', function() {
    const createQuizBtn = document.querySelector('a[data-bs-target="#createQuizModal"]');
    if (createQuizBtn) {
        createQuizBtn.addEventListener('click', populateQuizSubjects);
    }
    // Optional: also repopulate if modal is shown via other means
    const quizModal = document.getElementById('createQuizModal');
    if (quizModal) {
        quizModal.addEventListener('show.bs.modal', populateQuizSubjects);
    }
});
