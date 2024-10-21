async function searchFAQ() {
    const query = document.getElementById('query-input').value.trim();
    const resultDiv = document.getElementById("result");
    const submitButton = document.querySelector('button[type="submit"]');

    // Clear previous results
    resultDiv.innerHTML = "";

    if (!query) {
        alert("Please enter a question.");
        return;
    }

    try {
        // Disable submit button to prevent multiple submissions
        submitButton.disabled = true;
        resultDiv.innerHTML = "<p>Searching...</p>";  // Show loading indicator

        const response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query }),
        });

        if (response.ok) {
            const faq = await response.json();
            resultDiv.innerHTML = `
                <h5>Question:</h5>
                <p>${escapeHTML(faq.question)}</p>
                <h5>Answer:</h5>
                <p>${escapeHTML(faq.answer)}</p>
            `;
        } else {
            const error = await response.json();
            resultDiv.innerHTML = `<p class="text-danger">${escapeHTML(error.error)}</p>`;
        }
    } catch (err) {
        console.error("Error:", err);
        resultDiv.innerHTML = `<p class="text-danger">An unexpected error occurred. Please try again.</p>`;
    } finally {
        // Re-enable submit button
        submitButton.disabled = false;
    }
}

// Utility function to escape HTML characters
function escapeHTML(str) {
    const div = document.createElement('div');
    div.innerText = str;
    return div.innerHTML;
}
