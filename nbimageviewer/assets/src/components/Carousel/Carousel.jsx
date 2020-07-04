import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import _Carousel from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';
import './Carousel.css';

class Carousel extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: 0,
      slidesPerPage: 1,
    };
    this.socket = new WebSocket(window.addr);
    this.socket.addEventListener('open', () => {
      this.socket.send(JSON.stringify({ js_client: null }));
    });
    this.socket.addEventListener('message', (payload) => {
      const message = JSON.parse(payload.data);
      const msg_key = Object.keys(message)[0];
      if (msg_key === 'attrs') {
        this.setState(message[msg_key]);
      }
    });
  }

  render() {
    return (
      <_Carousel
        arrows
        dots
        slidesPerPage={this.state.slidesPerPage}
        slidesPerScroll={this.state.slidesPerScroll}
      >
        <img src="https://picsum.photos/300?random=1" />
        <img src="https://picsum.photos/200?random=2" />
        <img src="https://picsum.photos/200?random=3" />
        <img src="https://picsum.photos/200?random=4" />
        <img src="https://picsum.photos/200?random=5" />
      </_Carousel>
    );
  }
}

ReactDOM.render(<Carousel />, document.getElementById(window.id));
