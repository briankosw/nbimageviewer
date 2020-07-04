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
      slides: [],
      slidesPerPage: 1,
      slidesPerScroll: 1,
    };
    this.onChange = this.onChange.bind(this);
    this.socket = new WebSocket(window.addr);
    this.socket.addEventListener('open', () => {
      this.socket.send(JSON.stringify({ js_client: null }));
    });
    this.socket.addEventListener('message', (payload) => {
      const message = JSON.parse(payload.data);
      const msg_key = Object.keys(message)[0];
      if (msg_key === 'attrs') {
        this.setState(message[msg_key]);
      } else if (msg_key === 'data') {
        const images = Object.values(message[msg_key]).map((image) => {
          const image_str = 'data:image/jpeg;base64,' + image;
          return <img src={image_str} />;
        });
        this.setState({ slides: images });
      }
    });
  }

  onChange(value) {
    this.setState({ value });
    // I think communicate the state back to Python for lazy-loading.
  }

  render() {
    return (
      <_Carousel
        value={this.state.value}
        slides={this.state.slides}
        onChange={this.onChange}
        slidesPerPage={this.state.slidesPerPage}
        slidesPerScroll={this.state.slidesPerScroll}
        arrows
      ></_Carousel>
    );
  }
}

ReactDOM.render(<Carousel />, document.getElementById(window.id));
