import React, { Component } from 'react';
import './Gallery.css';

class Gallery extends Component {
  socket = new WebSocket('ws://localhost:' + window.port);

  componentDidMount() {
    this.socket.onopen = () => {
      console.log('WebSocket client connected');
      this.socket.send('js_client');
    };
  }
}
