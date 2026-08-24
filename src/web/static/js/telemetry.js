const ws = new WebSocket(`ws://${window.location.host}/ws/telemetry`);

ws.onopen = () => {
    console.log("Control WebSocket connected")

};

ws.onlcose = () => {
    console.log("Control WebSocket disconnected")
};

ws.onerror = () => {
    console.error("WebSocket error:", error);
}

ws.onmessage = (event) => {
    const telemetry = JSON.parse(event.data);

    console.log("Speed:", telemetry.speed);
    console.log("Battery:", telemetry.battery);
    console.log("Voltage:", telemetry.voltage);
};

// ws.onmessage = (event) => {
//     const data = JSON.parse(event.data);

//     document.querySelector("#speed").textContent = data.speed;
//     document.querySelector("#battery").textContent = `${data.battery}%`;
//     document.querySelector("#voltage").textContent = `${data.voltage}V`;
// };