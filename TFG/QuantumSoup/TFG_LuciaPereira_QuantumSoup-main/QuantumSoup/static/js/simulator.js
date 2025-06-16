// Inicializar CodeMirror
const editor = CodeMirror.fromTextArea(document.getElementById("quantum-code"), {
    lineNumbers: true,
    lineWrapping: true,
});
  

// Variable global para guardar la instancia del gráfico
let ResultChart = null;

// Función para manejar la simulación
document.getElementById("execute-btn").addEventListener("click", function () {
    // Limpia gráfico anterior si existe
    if (ResultChart) {
        ResultChart.destroy();
        ResultChart = null;
    }

    // Obtener el codigo del editor
    const quantumCode = editor.getValue();

    // Enviar el codigo al servidor usando fetch
    fetch('api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: quantumCode }),
    })
        .then(async (response) => {
            const data = await response.json();  
        
            if (!response.ok || data.error) {
                const errorMessage = data.error || 'Error desconocido en el servidor.';
                showError(errorMessage);
                throw new Error(errorMessage);  
            }
        
            renderResultTable(data.result);
            renderHistogram(data.result);
            document.getElementById("result-section").scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        })
        .catch((error) => {
            console.error("Error:", error);
            if (!document.getElementById("error-message").innerText) {
                showError(errorMessage);
            }
        });
});

// Mostrar el circuito como imagen en un pop-up
document.getElementById("view-circuit-btn").addEventListener("click", function () {
    const quantumCode = editor.getValue();

    fetch('api/draw/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: quantumCode }),
    })
        .then(async (response) => {
            const data = await response.json();  
        
            if (!response.ok || data.error) {
                const errorMessage = data.error || 'Error desconocido en el servidor.';
                showError(errorMessage);
                throw new Error(errorMessage);  
            }
        
            // Mostrar la imagen del circuito usando la respuesta base64
            const image = new Image();
            image.src = "data:image/png;base64," + data.circuit_image;
        
            // Mostrar el pop-up con la imagen
            const modal = document.getElementById("circuit-modal");
            const circuitImage = document.getElementById("circuit-image");
            circuitImage.src = image.src; // Asignar la imagen al src del img en el modal
        
            // Mostrar el modal
            modal.style.display = "block";
        })
        .catch((error) => {
            console.error("Error:", error);
            if (!document.getElementById("error-message").innerText) {
                showError(errorMessage);
            }
        });
});

// Cerrar el modal cuando el usuario haga clic en la "X"
document.getElementById("close-btn").addEventListener("click", function() {
    const modal = document.getElementById("circuit-modal");
    modal.style.display = "none"; // Cierra el modal
});

function renderHistogram(resultData) {
    const labels = Object.keys(resultData);
    const values = Object.values(resultData);

    const ctx = document.getElementById('graphic-result').getContext('2d');

    ResultChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Conteo por estado',
                data: values,
                backgroundColor: '#9e0c39',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: '#333',
                    titleFont: { family: 'Sofia Sans Condensed', size: 16 },
                    bodyFont: { family: 'Sofia Sans Condensed', size: 16 },
                    padding: 10,
                    cornerRadius: 6
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                            family: 'Sofia Sans Condensed',
                            size: 15
                        },
                        color: '#222'
                    },
                    title: {
                        display: true,
                        text: 'Frecuencia',
                        font: {
                            family: 'Sofia Sans Condensed',
                            size: 18,
                            weight: 'bold'
                        },
                        color: '#222'
                    },
                    grid: {
                        color: '#eee'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            family: 'Sofia Sans Condensed',
                            size: 15
                        },
                        color: '#222'
                    },
                    title: {
                        display: true,
                        text: 'Estados',
                        font: {
                            family: 'Sofia Sans Condensed',
                            size: 18,
                            weight: 'bold'
                        },
                        color: '#222'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function renderResultTable(counts) {
    const totalShots = Object.values(counts).reduce((sum, val) => sum + val, 0);

    let tableHTML = `
        <div class="scroll-table">
            <table class="result-table">
                <thead>
                    <tr>
                        <th>Estado</th>
                        <th>Porcentaje</th>
                    </tr>
                </thead>
                <tbody>
    `;

    for (const [state, count] of Object.entries(counts)) {
        const percentage = ((count / totalShots) * 100).toFixed(2);
        tableHTML += `
                <tr>
                    <td>${state}</td>
                    <td>${percentage}%</td>
                </tr>
        `;
    }

    tableHTML += `
                </tbody>
            </table>
        </div>
    `;

    document.getElementById("result-table-container").innerHTML = tableHTML;
}

function showError(message) {
    document.getElementById("error-message").innerText = message;
    document.getElementById("error-modal").style.display = "flex";
}

// Cerrar el modal cuando el usuario haga clic en la "X"
document.getElementById("close-error-btn").addEventListener("click", function() {
    document.getElementById("error-modal").style.display = "none";
});



// Inicializa CodeMirror
// const editor = CodeMirror.fromTextArea(document.getElementById("quantum-code"), {
//     lineNumbers: true,
//     mode: "text/x-python",
//     theme: "default",
//     matchBrackets: true,
//     autoCloseBrackets: true
//   });
  
//   // Maneja el clic del botón para enviar el código al backend
//   document.getElementById("simulate-btn").addEventListener("click", () => {
//     const quantumCode = editor.getValue();
  
//     fetch('api/', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ code: quantumCode }),
//     })
//       .then(response => {
//         if (!response.ok) {
//           throw new Error('Error en la respuesta de la API');
//         }
//         return response.json();
//       })
//       .then(data => {
//         const resultBox = document.getElementById("result");
//         if (data.error) {
//           resultBox.innerText = "Error: " + data.error;
//         } else {
//           resultBox.innerText = "Resultado: " + JSON.stringify(data.result, null, 2);
//         }
//       })
//       .catch(error => {
//         console.error("Error:", error);
//         document.getElementById("result").innerText = "Error: " + error.message;
//       });
//   });

