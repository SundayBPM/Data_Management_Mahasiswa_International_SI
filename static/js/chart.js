fetch('/ExchangeIISMA')
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById('lineChart').getContext('2d');
        var line_chart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Testing'
                    }
                }
            }
        })
    })

function makePieChart(labels, data, id, title) {
    const get_id = document.getElementById(id);
    new Chart(get_id, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{

            }]
        }
    })
}
