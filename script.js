async function searchFAQ() {
    const query = document.getElementById('query-input').value;
    if (!query) {
        alert("Please enter a question.");
        return;
    }

    const response = await fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
    });

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    if (response.ok) {
        const faq = await response.json();
        resultDiv.innerHTML = `
            <h5>Question:</h5>
            <p>${faq.question}</p>
            <h5>Answer:</h5>
            <p>${faq.answer}</p>
        `;
    } else {
        const error = await response.json();
        resultDiv.innerHTML = `<p class="text-danger">${error.error}</p>`;
    }
}
