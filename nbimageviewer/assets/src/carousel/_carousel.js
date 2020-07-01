import React, { Component } from 'react';
import { w3cwebclient as W3CWebSocket } from 'webclient';

export default class App extends Component {
  client = new W3CWebSocket('ws://localhost:' + window.port);

  componentWillMount() {
    this.client.onopen = () => {
      console.log('WebSocket client connected.');
      client.message('js_client');
    };
    this.client.onmessage = (message) => {
      console.log(message);
    };
    this.client.onclose = () => {
      console.log('WebSocket client disconnected.');
    };
  }
}
