// Dark Mode Toggle
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

// Simulated Real-time Data Updates
function updateStats() {
    document.getElementById("usersCount").innerText = Math.floor(Math.random() * 5000) + " Users";
    document.getElementById("sessionsCount").innerText = Math.floor(Math.random() * 1000) + " Active";
    document.getElementById("conversionRate").innerText = (Math.random() * 10 + 5).toFixed(2) + "%";
}

// Update stats every 3 seconds
setInterval(updateStats, 3000);
updateStats();

// Traffic Chart
const ctx = document.getElementById('trafficChart').getContext('2d');
const trafficChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Website Traffic',
            data: [1200, 1900, 3000, 2500, 3200, 4000],
            borderColor: '#ff4500',
            backgroundColor: 'rgba(255, 69, 0, 0.2)',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Simulated Real-time Chart Updates
function updateChart() {
    let newData = Math.floor(Math.random() * 5000);
    if (trafficChart.data.datasets[0].data.length > 10) {
        trafficChart.data.datasets[0].data.shift();
    }
    trafficChart.data.datasets[0].data.push(newData);
    trafficChart.update();
}

// Update chart every 5 seconds
setInterval(updateChart, 5000);
