var ws = new WebSocket("ws://localhost:" + window.port);

ws.addEventListener("open", () => {
    ws.send("js_client");
});

ws.addEventListener("message", (payload) => {
    const data = JSON.parse(payload.data)["data"];
    console.log("Received payload: " + data);
    const image = document.createElement("img");
    image.src = "data:image/jpeg;base64," + data;
    document.getElementById("root").appendChild(image);
});

