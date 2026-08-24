async function start() {
    const pc = new RTCPeerConnection({
        iceServers: []
    });

    pc.ontrack = event => {
        document.getElementById("video").srcObject =
            event.streams[0];
    };

    pc.onconnectionstatechange = () => {
        console.log(
            "Connection:",
            pc.connectionState
        );
    };

    pc.addTransceiver(
        "video",
        {
            direction: "recvonly"
        }
    );

    await pc.setLocalDescription(
        await pc.createOffer()
    );

    const response = await fetch(
        "/offer",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sdp: pc.localDescription.sdp,
                type: pc.localDescription.type
            })
        }
    );

    const answer = await response.json();

    await pc.setRemoteDescription(answer);
}

start();