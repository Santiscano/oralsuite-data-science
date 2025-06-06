const data = fetch('/grafico-tiempo-entrega')
    .then(res => res.json())
    .then(res => {
        const chartData = res.data;
        new Chart(document.getElementById("myChart"), {
            type: "bar",
            data: chartData,
            options: {
                scales: {
                y: {
                    title: {
                    display: true,
                    text: 'Días de entrega promedio'
                    }
                },
                x: {
                    title: {
                    display: true,
                    text: 'Clase de trabajo'
                    }
                }
                }
            }
        });
    });
