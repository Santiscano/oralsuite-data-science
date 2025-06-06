const data = fetch('/grafico-clases-trabajo')
    .then(res => res.json())
    .then(res => {
        const chartData = res.data;
        new Chart(document.getElementById("myChart"), {
        type: "bar",
        data: chartData,
        options: {
            indexAxis: 'y', // Esto hace que sea horizontal
        }
        });
    });
