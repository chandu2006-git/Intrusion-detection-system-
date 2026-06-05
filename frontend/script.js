// ================================
// IDS DASHBOARD
// ================================

let trafficChart;
let alertChart;

// ================================
// INIT
// ================================

window.onload = () => {

    initializeCharts();

    fetchData();

    setInterval(fetchData, 2000);
};

// ================================
// CHARTS
// ================================

function initializeCharts() {

    const trafficCtx =
        document.getElementById("trafficChart");

    const alertCtx =
        document.getElementById("alertChart");

    trafficChart = new Chart(trafficCtx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Packets/sec",
                data: [],
                borderColor: "#38bdf8",
                backgroundColor: "rgba(56,189,248,0.2)",
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    alertChart = new Chart(alertCtx, {
        type: "bar",
        data: {
            labels: [],
            datasets: [{
                label: "Alerts",
                data: [],
                backgroundColor: "#ef4444"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// ================================
// FETCH API
// ================================

async function fetchData() {

    try {

        const response =
            await fetch("http://127.0.0.1:5000/status");

        const data =
            await response.json();

        updateDashboard(data);

    }

    catch(error) {

        console.error(
            "API Error:",
            error
        );
    }
}

// ================================
// UPDATE DASHBOARD
// ================================

function updateDashboard(data) {

    const activeFlows =
        data.active_flows || 0;

    const alerts =
        data.alerts || [];

    const latest =
        alerts.length > 0
        ? alerts[alerts.length - 1]
        : null;

    // =====================
    // TOP COUNTS
    // =====================

    document.getElementById(
        "activeFlows"
    ).textContent = activeFlows;

    document.getElementById(
        "pps"
    ).textContent = activeFlows * 10;

    document.getElementById(
        "bps"
    ).textContent = activeFlows * 50;

    document.getElementById(
        "alertCount"
    ).textContent = alerts.length;

    const currentStatus =
        document.getElementById(
            "currentStatus"
        );

    currentStatus.textContent =
        latest
        ? latest.final
        : "Normal";

    currentStatus.style.color =
        latest && latest.final !== "Normal"
        ? "#ef4444"
        : "#22c55e";

    // =====================
    // LIVE FEED
    // =====================

    updateFeed(alerts);

    // =====================
    // TABLE
    // =====================

    updateTable(alerts);

    // =====================
    // CHARTS
    // =====================

    updateCharts(
        activeFlows * 10,
        alerts.length
    );
}

// ================================
// LIVE FEED
// ================================

function updateFeed(alerts) {

    const feed =
        document.getElementById(
            "detectionFeed"
        );

    if (!alerts.length) {

        feed.innerHTML =
            `<div class="feed-item normal">
                Waiting for detections...
             </div>`;

        return;
    }

    feed.innerHTML =
        alerts
        .slice(-15)
        .reverse()
        .map(alert => {

            const attack =
                alert.final !== "Normal";

            return `
                <div class="feed-item ${attack ? 'attack' : 'normal'}">

                    [${alert.time}]
                    ${alert.final}

                    <br>

                    ${alert.flow
                        ? alert.flow[0]
                        : "Unknown Source"}

                </div>
            `;
        })
        .join("");
}

// ================================
// TABLE
// ================================

function updateTable(alerts) {

    const table =
        document.getElementById(
            "flowTable"
        );

    table.innerHTML = "";

    alerts
    .slice(-15)
    .reverse()
    .forEach(alert => {

        const row =
            document.createElement("tr");

        let protocol = "-";

        if(alert.flow){

            protocol =
                alert.flow[4] == 6
                ? "TCP"
                : alert.flow[4] == 17
                ? "UDP"
                : alert.flow[4] == 1
                ? "ICMP"
                : alert.flow[4];
        }

        row.innerHTML = `

            <td>${alert.time}</td>

            <td>
                ${
                    alert.flow
                    ? alert.flow[0]
                    : "-"
                }
            </td>

            <td>
                ${
                    alert.flow
                    ? alert.flow[1]
                    : "-"
                }
            </td>

            <td>${protocol}</td>

            <td class="${
                alert.final === "Normal"
                ? "normal"
                : "attack"
            }">

                ${alert.final}

            </td>
        `;

        table.appendChild(row);
    });
}

// ================================
// CHARTS
// ================================

function updateCharts(pps, alerts) {

    const time =
        new Date()
        .toLocaleTimeString();

    // =====================
    // TRAFFIC CHART
    // =====================

    trafficChart.data.labels.push(time);

    trafficChart.data.datasets[0]
        .data.push(pps);

    if (
        trafficChart.data.labels.length > 20
    ) {

        trafficChart.data.labels.shift();

        trafficChart.data.datasets[0]
            .data.shift();
    }

    trafficChart.update();

    // =====================
    // ALERT CHART
    // =====================

    alertChart.data.labels.push(time);

    alertChart.data.datasets[0]
        .data.push(alerts);

    if (
        alertChart.data.labels.length > 20
    ) {

        alertChart.data.labels.shift();

        alertChart.data.datasets[0]
            .data.shift();
    }

    alertChart.update();
}