import React, { useState, useEffect } from "react";
import axios from 'axios';
import { Button } from 'antd';

const AudioRecorder = () => {
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [chunks, setChunks] = useState([]);

  useEffect(() => {
    // Request permissions to record audio
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const newMediaRecorder = new MediaRecorder(stream);
        setMediaRecorder(newMediaRecorder);

        newMediaRecorder.ondataavailable = e => {
          setChunks((oldChunks) => [...oldChunks, e.data]);
        };

        newMediaRecorder.onstop = () => {
          const blob = new Blob(chunks, {'type' : 'audio/ogg; codecs=opus'});
          const formData = new FormData();
          formData.append('file', blob);

          axios.post('/api/audio', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(response => {
            console.log(response);
          })
          .catch(error => {
            console.log(error);
          });

          setChunks([]);
        };
      });
  }, []);

  const startRecording = () => {
    if (mediaRecorder) {
      setRecording(true);
      mediaRecorder.start();
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      setRecording(false);
      mediaRecorder.stop();
    }
  };

  return (
    <div>
      <Button onClick={startRecording} disabled={recording}>Start Recording</Button>
      <Button onClick={stopRecording} disabled={!recording}>Stop Recording</Button>
    </div>
  );
};

export default AudioRecorder;
