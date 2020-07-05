import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import _Gallery from 'react-photo-gallery';
import './Gallery.css';

class Gallery extends Component {
  constructor(props) {
    super(props);
    this.state = {
      photos: [],
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
      } else if (msg_key === 'data') {
        const photos = Object.values(message[msg_key]).map((image) => {
          const photo = 'data:image/jpeg;base64,' + image;
          return { src: photo };
        });
        this.setState({ photos: photos });
      }
    });
  }

  render() {
    return <_Gallery photos={this.state.photos} />;
  }
}

ReactDOM.render(<Gallery />, document.getElementById(window.id));
