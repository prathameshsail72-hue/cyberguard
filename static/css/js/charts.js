document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('securityChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk URLs', 'Medium Risk URLs', 'High Risk Phishing'],
            datasets: [{
                data: [65, 20, 15],
                backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                title: { display: true, text: 'Scan History Overview' }
            }
        }
    });
});