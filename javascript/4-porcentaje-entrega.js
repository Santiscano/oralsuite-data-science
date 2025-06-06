const data = fetch('/grafico-porcentaje-entrega')
    .then(res => res.json())
    .then(res => {
        const chartData = res.data;
        new Chart(document.getElementById("myPieChart"), {
        type: "pie",
        data: chartData,
        options: {
            plugins: {
            legend: {
                position: 'bottom'
            }
            }
        }
        });
    });
