document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');
    const statusText = document.getElementById('status');
    const imageInput = document.getElementById('image_query');
    const textInput = document.getElementById('text_query');

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault(); 
        const formData = new FormData(searchForm);          
        resultsContainer.innerHTML = '';
        statusText.textContent = 'Searching...';

        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                body: formData, 
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            if (data.results && data.results.length > 0) {
                statusText.textContent = `Found ${data.results.length} matching images:`;
                data.results.forEach(filename => {
                    const imgElement = document.createElement('img');
                    
                    imgElement.src = `/static/images/${filename}`; 
                    imgElement.alt = filename;
                    imgElement.style.width = '100%';
                    resultsContainer.appendChild(imgElement);
                });
            } else {
                statusText.textContent = 'No results found.';
            }

        } catch (error) {
            console.error('Error during search:', error);
            statusText.textContent = 'An error occurred. Please try again.';
        }

        
        imageInput.value = '';
        textInput.value = '';
    });
});