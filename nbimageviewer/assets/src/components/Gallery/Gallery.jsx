import React, { useState, useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';
import _Gallery from 'react-photo-gallery';
import './Gallery.css';

function Gallery() {
  const [photos, setPhotos] = useState([]);
  const socket = useRef(new WebSocket(window.addr));

  useEffect(() => {
    socket.current.onopen = () =>
      socket.current.send(JSON.stringify({ js_client: null }));
    socket.current.onclose = () => console.log('WebSocket closed.');

    return () => {
      socket.current.close();
    };
  }, []);

  useEffect(() => {
    if (!socket.current) return;

    socket.current.onmessage = (payload) => {
      const message = JSON.parse(payload.data);
      const msg_key = Object.keys(message)[0];
      if (msg_key === 'data') {
        const photos = Object.values(message[msg_key]).map((image) => {
          const photo = 'data:image/jpeg;base64,' + image;
          return { src: photo };
        });
        setPhotos(photos);
      }
    };
  }, [photos]);

  return <_Gallery photos={photos} />;
}

ReactDOM.render(<Gallery />, document.getElementById(window.id));
