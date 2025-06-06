const data = fetch('/grafico-clases-por-clinica')
    .then(res => res.json())
    .then(res => {
        const chartData = res.data;
        new Chart(document.getElementById("clasesClinicasChart"), {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            scales: {
            x: {
                stacked: true,  // Cambia a false para barras agrupadas
                title: {
                display: true,
                text: 'Clínica'
                }
            },
            y: {
                stacked: true,
                beginAtZero: true,
                title: {
                display: true,
                text: 'Número de órdenes'
                }
            }
            },
            plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Distribución de las 5 mayores clases de trabajo por las 5 clínicas principales'
            }
            }
        }
        });
    });
