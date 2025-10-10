const chart_scale = {
    y: {
        ticks: {
            // format: {
            //     style: 'percent'
            // }
        },
        min: 0,
        max: 100,
    },
    x: {
        ticks: {
            display: false,
            
        }
    }
}
/**
 * 
 * @param {Chart} chart 
 * @param {Array<any>} data 
 */
function addDatasets(chart, data, max_size) {
    for (let i = 0; i < data.length; i++) {
        const new_data = data[i];
        if (chart.data.datasets[i].data.length >= max_size) {
            chart.data.datasets[i].data.shift()
        }
        chart.data.datasets[i].data.push(new_data)
    }
    chart.update();
}

const usage_ctx = document.getElementById("usage_chart").getContext('2d')

const usage_chart = new Chart(usage_ctx, {
    type: "line",
    data: {
        labels: Array.from({ length: 90 }, (_, index) => index),
        datasets:[
            {
                label: "CPU usage",
                data: []
            },
            {
                label: "RAM usage",
                data: []
            }
        ]
    },
    options: {
        scales: chart_scale,
    }
})


const evtSource = new EventSource("data_stream")
evtSource.onmessage = function(event) {
    data = JSON.parse(event.data)
    addDatasets(usage_chart, [data.cpu_usage, data.ram_usage], 90)
};
evtSource.onopen = () => {
    console.log("SSE opened")
}
evtSource.onerror = function(err) {
    console.error("SSE Error:", err);
};
