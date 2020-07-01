// var ws = new WebSocket("ws://localhost:" + window.port);
//
// ws.addEventListener("open", () => {
//     ws.send("js_client");
//     var primary = new Splide("#primary", {
//         autoWidth: true,
//         arrows: "slider",
//         pagination: false,
//     });
//     var secondary = new Splide("#secondary", {
//         pagination: false,
//         gap: 5,
//         fixedWidth: 100,
//         fixedHeight: 100,
//         cover: true,
//         isNavigation: true,
//         focus: "center",
//         arrows: false,
//         speed: 200
//     }).mount();
//     primary.sync(secondary).mount();
// });
//
// ws.addEventListener("message", (payload) => {
//     const data = JSON.parse(payload.data)["data"];
//     for (const [i, img] of Object.entries(data)) {
//         const item = document.createElement("div");
//         item.className = "carousel-item";
//         if (i == 0) {
//             item.className += " active";
//         }
//         const image = document.createElement("img");
//         image.src = "data:image/jpeg;base64," + img;
//         image.className = "d-block w-100";
//         item.appendChild(image);
//         document.getElementsByClassName("carousel-inner")[0].appendChild(item);
//     }
// });
import React from 'react';
import Carousel, { Dots } from '@brainhubeu/react-carousel';

export default class MyCarousel extends React.Component {
  constructor() {
    super();
    this.state = {
      value: 0,
      slides: [
        <img src={imageOne} />,
        <img src={imageTwo} />,
        <img src={imageThree} />,
      ],
      thumbnails: [
        <img src={thumbnailOne} />,
        <img src={thumbnailTwo} />,
        <img src={thumbnailThree} />,
      ],
    };
    this.onchange = this.onchange.bind(this);
  }

  onchange(value) {
    this.setState({ value });
  }

  render() {
    return (
      <div>
        <Carousel
          value={this.state.value}
          slides={this.state.sldes}
          onChange={this.onchange}
        />
        <Dots
          number={this.state.thumbnails.length}
          thumbnails={this.state.thumbnails}
          value={this.state.value}
          onChange={this.onchange}
          number={this.state.slides.length}
        />
      </div>
    );
  }
}
