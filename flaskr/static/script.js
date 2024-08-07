const BASE_URL = "/api/get/";

// Get the input and output elements
const INPUT = document.getElementById("input-equation");
const OUTPUT = document.getElementById("output-equation");

let initialConditions = null;

document.addEventListener("DOMContentLoaded", function () {
    function update() {
        getAsLatex();
    }

    if (!INPUT.value) {
        INPUT.addEventListener("input", update);
    }

    update();
});


document.getElementById("clear")
    .addEventListener("click", () => {
        document.getElementById("solve").classList.add("hidden")
        document.getElementById("solve-title").innerHTML = "";
        document.getElementById("step-by-step").innerHTML = ""

        INPUT.value = "";

        if (initialConditions !== null) {
            initialConditions = null;
        }

        document.getElementById("initial-conditions").value = "y(0) = 0";
        getAsLatex();
    });

document.getElementById("form-equation-input")
    .addEventListener("submit", (event) => {
        event.preventDefault();

        document.getElementById("solve-title").innerHTML = "Solución paso a paso";
        document.getElementById("solve").classList.remove("hidden")

        fetch(BASE_URL + "solve_ode", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body:
                JSON.stringify({
                    value: INPUT.value || INPUT.placeholder,
                    method: document.getElementById("options").value,
                    initial_conditions: initialConditions || ""
                })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const container = document.getElementById("step-by-step");
                container.innerHTML = "";

                let ul = document.createElement("ul");
                ul.className = "list-group";

                function add(li, id, text) {
                    const span = document.createElement("span");

                    span.className = id;
                    span.innerHTML = text;

                    li.appendChild(span);
                }

                for (const [title, l] of Object.values(data.steps)) {
                    const li = document.createElement("li");

                    add(li, "title", title);
                    add(li, "latex", `\\(${l}\\)`);

                    ul.appendChild(li);
                }

                container.appendChild(ul);

                MathJax.typesetPromise([ul])
                    .then(() => console.info("MathJax typeset successfully"))
                    .catch((err) => console.error("Error rendering MathJax:", err));

                // Remove the initial conditions
                if (initialConditions !== null) {
                    initialConditions = null
                }

                document.getElementById("initial-conditions").value = "y(0) = 0";
            });
    });


function getAsLatex() {
    fetch(BASE_URL + "latex_format", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            value: INPUT.value || INPUT.placeholder,
            initial_conditions: initialConditions || ""
        })
    })
        .then(response => {
            return response.json()
        })
        .then(data => {
            OUTPUT.innerHTML = `\\(${data.latex}\\)`;
            MathJax.typesetPromise([OUTPUT])
                .then(() => console.info("[Display Equation] MathJax typeset successfully"))
                .catch((err) => console.error("Error rendering MathJax:", err));
        })
}

const modal = document.getElementById("myModal");
const btn = document.getElementById("openModalBtn");
const span = document.getElementsByClassName("close")[0];

btn.onclick = function () {
    modal.style.display = "block";

    // Rellenar el campo con la información guardada, si existe
    if (initialConditions != null) {
        document.getElementById('initial-conditions').value = initialConditions;
    } else {
        document.getElementById('initial-conditions').value = "";
    }
}

span.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

document.getElementById('initialConditionsForm').onsubmit = function (event) {
    event.preventDefault();

    initialConditions = document.getElementById('initial-conditions').value;
    modal.style.display = "none";

    document.getElementById('initial-conditions').innerHTML = "";

    getAsLatex();
}