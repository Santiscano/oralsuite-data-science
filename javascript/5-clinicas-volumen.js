const data = fetch('/grafico-clinicas-volumen')
    .then(res => res.json())
    .then(res => {
        const chartData = res.data;
        new Chart(document.getElementById("myLineChart"), {
        type: "line",
        data: chartData,
        options: {
            responsive: true,
            scales: {
            x: {
                title: {
                display: true,
                text: "Clínica"
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
