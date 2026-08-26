const ws = new WebSocket(`ws://${window.location.host}/ws/control`);

ws.onopen = () => {
    console.log("Control WebSocket connected")
};

ws.onlcose = () => {
    console.log("Control WebSocket disconnected")
};

ws.onerror = () => {
    console.error("WebSocket error:", error);
}

function sendControl(command) {
    if (ws.readyState !== WebSocket.OPEN) {
        console.warn("WebSocket is not connected");
        return;
    }

    ws.send(JSON.stringify({
        type: "control",
        command: command
    }));
}

document.getElementById("forward").onclick = () => {
    sendControl("forward");
};

document.getElementById("backward").onclick = () => {
    sendControl("backward");
};

document.getElementById("left").onclick = () => {
    sendControl("left");
};

document.getElementById("right").onclick = () => {
    sendControl("right");
};

document.getElementById("stop").onclick = () => {
    sendControl("stop");
};

/**
 * 
 */
const keys = new Set();

window.addEventListener("keydown", (event) => { 
    const key = event.key.toLowerCase();
    if (["w", "a", "s", "d"].includes(key)) {
        event.preventDefault();
        keys.add(key);
        sendKeys();
    }
})

window.addEventListener("keyup", (event) => {
    const key = event.key.toLowerCase();
    if (["w", "a", "s", "d"].includes(key)) {
        event.preventDefault();
        keys.delete(key);
       // sendKeys();
    }
})

function sendKeys() { 
    let ctrl = {
        x: 0.0,
        y: 0.0
    }
    if(keys.has("w")) ctrl.y = 1
    if(keys.has("s")) ctrl.y = -1
    if(keys.has("a")) ctrl.x = -1
    if(keys.has("d")) ctrl.x = 1
 =
    sendControl({
        type: 'control',
        x: ctrl.x,
        y: ctrl.y
    })
    // console.log(
    //     keys
    // )
    // console.log(
    //     JSON.stringify({
    //         keys: [...keys]
    //     })
    // )
    // ws.send(JSON.stringify({
    //     keys: [...keys]aw
    // }));
}