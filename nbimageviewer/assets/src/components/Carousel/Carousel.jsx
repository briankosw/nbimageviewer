import React, { useState, useRef, useEffect, useCallback } from 'react';
import ReactDOM from 'react-dom';
import _Carousel, { Dots } from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';
import './Carousel.css';

function Carousel() {
  const [value, setValue] = useState(0);
  const [slides, setSlides] = useState([]);
  const [slidesPerPage, setSlidesPerPage] = useState(1);
  const [slidesPerScroll, setSlidesPerScroll] = useState(1);
  const socket = useRef(new WebSocket(window.addr));

  const onChange = useCallback((value) => {
    setValue(value);
  });

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
      if (msg_key === 'attrs') {
        for (const [attr, val] of Object.entries(message[msg_key])) {
          switch (attr) {
            case 'slidesPerPage':
              setSlidesPerPage(val);
              break;
            case 'slidesPerScroll':
              setSlidesPerScroll(val);
              break;
          }
        }
      } else if (msg_key === 'data') {
        const images = Object.values(message[msg_key]).map((image) => {
          const image_str = 'data:image/jpeg;base64,' + image;
          return <img src={image_str} />;
        });
        setSlides(images);
      }
    };
  }, [slides, slidesPerPage, slidesPerScroll]);

  return (
    <React.Fragment>
      <_Carousel
        value={value}
        slides={slides}
        onChange={onChange}
        slidesPerPage={slidesPerPage}
        slidesPerScroll={slidesPerScroll}
        arrows
      />
      <Dots number={20} thumbnails={slides} value={value} onChange={onChange} />
    </React.Fragment>
  );
}

ReactDOM.render(<Carousel />, document.getElementById(window.id));
