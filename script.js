document.addEventListener('DOMContentLoaded', () => {
    const cvForm = document.getElementById('cv-form');
    const rewriteButton = document.getElementById('rewrite-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    const errorMessageDiv = document.getElementById('error-message');
    const resultContainer = document.getElementById('result-container');
    const rewrittenCvPre = document.getElementById('rewritten-cv');
    const copyButton = document.getElementById('copy-button');
    const downloadButton = document.getElementById('download-button');

    cvForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        // Clear previous results and errors
        resultContainer.style.display = 'none';
        errorMessageDiv.style.display = 'none';
        errorMessageDiv.textContent = '';
        rewrittenCvPre.textContent = ''; // Clear previous text
        loadingIndicator.style.display = 'block';
        rewriteButton.disabled = true;
        rewriteButton.textContent = 'Rewriting...';

        // Collect form data
        const formData = new FormData(cvForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        try {
            // Send data to backend API
            const response = await fetch('/rewrite', { // Relative path to backend endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                // Try to get error message from backend response body
                let errorMsg = `HTTP error! Status: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.error || JSON.stringify(errorData);
                } catch (e) {
                    // If response is not JSON or empty
                    errorMsg = `HTTP error! Status: ${response.status}. Could not parse error response.`;
                }
                 throw new Error(errorMsg);
            }

            const result = await response.json();

            // Display the result
            rewrittenCvPre.textContent = result.rewritten_cv;
            resultContainer.style.display = 'block'; // Show the result container

        } catch (error) {
            console.error('Error during rewrite:', error);
            errorMessageDiv.textContent = `Error: ${error.message}`;
            errorMessageDiv.style.display = 'block';
        } finally {
            // Hide loading indicator and re-enable button
            loadingIndicator.style.display = 'none';
            rewriteButton.disabled = false;
            rewriteButton.textContent = 'Rewrite CV';
        }
    });

    // --- Result Actions ---

    // Copy Button
    copyButton.addEventListener('click', () => {
        const textToCopy = rewrittenCvPre.textContent;
        navigator.clipboard.writeText(textToCopy).then(() => {
            // Success feedback
            copyButton.textContent = 'Copied!';
            setTimeout(() => {
                copyButton.textContent = 'Copy to Clipboard';
            }, 2000); // Reset button text after 2 seconds
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            alert('Failed to copy text. Please try manually.'); // Fallback message
        });
    });

    // Download Button
    downloadButton.addEventListener('click', () => {
        const textToDownload = rewrittenCvPre.textContent;
        const blob = new Blob([textToDownload], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');

        a.href = url;
        // Suggest a filename (user can change it)
        const companyName = document.getElementById('company').value || 'company';
        a.download = `rewritten_cv_${companyName.replace(/\s+/g, '_')}.txt`;

        // Programmatically click the link to trigger the download
        document.body.appendChild(a); // Append link to body (needed for Firefox)
        a.click();

        // Clean up: remove the link and revoke the object URL
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});