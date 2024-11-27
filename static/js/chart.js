fetch('/ExchangeIISMA')
    .then(response => response.json())
    .then(data => {
        let id_element = document.getElementById('lineChart').getContext('2d');
        let line_chart = new Chart(id_element, {
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

fetch('/status-count')
    .then(response => response.json())
    .then(data => {
        let id_element = document.getElementById('pieChart_status').getContext('2d')
        let pie_chart = new Chart(id_element, {
            type: 'pie',
            data: data,
            options: {
                plugins: {
                    legend: {
                        display: true,
                        position: 'right'
                    }
                }
            }
        })
    })
    
fetch('/most-preferred-country-count')
    .then(response => response.json())
    .then(data => {
        let id_element = document.getElementById('pieChart_status2').getContext('2d')
        let pie_chart = new Chart(id_element, {
            type: 'pie',
            data: data,
            options: {
                plugins: {
                    legend: {
                        display: true,
                        position: 'right'
                    }
                }
            }
        })
    })

fetch('/status-count')
    .then(response => response.json())
    .then(data => {
        let id_element = document.getElementById('pieChart_status3').getContext('2d')
        let pie_chart = new Chart(id_element, {
            type: 'pie',
            data: data,
            options: {
                plugins: {
                    legend: {
                        display: true,
                        position: 'right'
                    }
                }
            }
        })
    })
