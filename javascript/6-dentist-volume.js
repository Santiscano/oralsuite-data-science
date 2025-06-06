const data = fetch('/grafico-odontologos-volumen')
    .then(res => res.json())
    .then(res => {
        const chartData = res.data;
        new Chart(document.getElementById("odontologosChart"), {
        type: "line",
        data: chartData,
        options: {
            responsive: true,
            scales: {
            x: {
                title: {
                display: true,
                text: "Odontólogo"
                }
            },
            y: {
                title: {
                display: true,
                text: "Número de órdenes"
                },
                beginAtZero: true
            }
            }
        }
        });
    });
