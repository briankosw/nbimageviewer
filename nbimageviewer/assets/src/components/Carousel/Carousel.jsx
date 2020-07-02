import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import _Carousel from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';

class Carousel extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: 0,
      slidesPerPage: 1,
    };
    this.socket = new WebSocket(window.addr);
  }

  componentDidMount() {
    this.socket.addEventListener('open', () => {
      this.socket.send('js_client');
    });
    this.socket.addEventListener('message', (payload) => {
      const data = JSON.parse(payload.data)['message'];
      this.setState(data);
    });
  }

  render() {
    return (
      <_Carousel arrows dots slidesPerPage={this.state.slidesPerPage}>
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
