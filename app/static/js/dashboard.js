document.addEventListener('DOMContentLoaded', function () {
    const raw = document.getElementById('live-metrics');
    if (!raw) return console.warn("Missing metrics JSON block.");
    const allData = JSON.parse(raw.textContent);

    for (const machine in allData) {
        const data = allData[machine];
        if (data.error) {
            console.warn(`Error fetching data for ${machine}:`, data.error);
            continue;
        }

        const labels = data.cpu.timestamps.map(t => new Date(t * 1000).toLocaleTimeString());

        function render(idSuffix, label, values, color, max = null) {
            const ctx = document.getElementById(`${idSuffix}_${machine}`)?.getContext('2d');
            if (!ctx) return;
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
                        y: { beginAtZero: true, max: max }
                    }
                }
            });
        }

        render('cpuChart', 'CPU %', data.cpu.values, '#36A2EB', 100);
        render('memoryChart', 'Memory Used', data.memory.values, '#FF6384');
        render('diskChart', 'Disk Used', data.disk.values, '#4BC0C0');
        render('networkChart', 'Network In', data.network.values, '#9966FF');
    }
});
