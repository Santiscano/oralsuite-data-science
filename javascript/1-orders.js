const data = fetch('/grafico-ordenes')
    .then(res => res.json())
    .then(chartData => {
        new Chart(document.getElementById("myChart"), {
        type: "bar",
        data: chartData,
        });
    });
