var ws = new WebSocket("ws://localhost:" + window.port);

ws.addEventListener("open", () => {
    ws.send("js_client");
    var primary = new Splide("#primary", {
        autoWidth: true,
        arrows: "slider",
        pagination: false,
    });
    var secondary = new Splide("#secondary", {
        pagination: false,
        gap: 5,
        fixedWidth: 100,
        fixedHeight: 100,
        cover: true,
        isNavigation: true,
        focus: "center",
        arrows: false,
        speed: 200
    }).mount();
    primary.sync(secondary).mount();
});

ws.addEventListener("message", (payload) => {
    const data = JSON.parse(payload.data)["data"];
    for (const [i, img] of Object.entries(data)) {
        const item = document.createElement("div");
        item.className = "carousel-item";
        if (i == 0) {
            item.className += " active";
        }
        const image = document.createElement("img");
        image.src = "data:image/jpeg;base64," + img;
        image.className = "d-block w-100";
        item.appendChild(image);
        document.getElementsByClassName("carousel-inner")[0].appendChild(item);
    }
});

