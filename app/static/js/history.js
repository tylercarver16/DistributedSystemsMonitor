document.addEventListener('DOMContentLoaded', function () {
    const raw = document.getElementById('history-data');
    if (!raw) return;
    const allLogs = JSON.parse(raw.textContent);

    for (const machine in allLogs) {
        const logs = allLogs[machine];
        const labels = logs.map(l => new Date(l.timestamp).toLocaleTimeString());

        function render(idPrefix, label, values, color, maxY = null) {
            const canvas = document.getElementById(`${idPrefix}_${machine}`);
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: label,
                        data: values,
                        borderColor: color,
                        fill: false,
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: maxY
                        }
                    }
                }
            });
        }

        render('cpuHistory', 'CPU %', logs.map(l => l.cpu_usage), '#36A2EB', 100);
        render('memoryHistory', 'Memory Used', logs.map(l => l.memory_usage), '#FF6384');
        render('diskHistory', 'Disk Used', logs.map(l => l.disk_usage), '#4BC0C0');
        render('networkHistory', 'Network In', logs.map(l => l.network_usage), '#9966FF');
    }
});
