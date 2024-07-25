document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("input");
    const output = document.getElementById("output");

    function update() {
        const value = input.value || input.placeholder;

        fetch("/api/get/latex", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({value})
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("HTTP error! status: ${response.status}");
                }

                return response.json()
            })
            .then(data => {
                const latex = data.latex;
                output.innerHTML = `\\(${latex}\\)`;

                MathJax.typesetPromise([output]).then(() => {
                }).catch((err) => console.error("Error rendering MathJax:", err));
            })
            .catch(error => {
                console.error("Error rendering MathJax:", error);
                console.error("Stack trace:", error.stack);
            });
    }

    input.addEventListener('input', function () {
        update();
    });

    update();
});