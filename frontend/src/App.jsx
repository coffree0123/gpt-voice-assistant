import { Layout, theme, Input } from 'antd';
import React, { useState, useRef } from 'react';
import AudioRecorder from './Record';

const { Header, Content, Footer, Sider } = Layout;

const { Search } = Input;
function App() {
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  const [inputValue, setInputValue] = useState("")

  const [messages, setMessages] = useState([
    {
      "message": "Hi, I am a ai assistant. How can I help?",
      "type": "apiMessage"
    },
  ]);
  const messageListRef = useRef(null);

  const onSearch = (value, event) => {
    setInputValue("");
    setMessages((prevMessages) => [...prevMessages, { "message": value, "type": "userMessage" }])
    fetch("/api/text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "text": value
      })
    }).then(
      res => res.json()
    ).then(
      json => setMessages((prevMessages) => [...prevMessages, { "message": json.response, "type": "apiMessage" }])
    )
  }

  return (

    <Layout>
      <Content
        style={{
          margin: '24px 20% 0',
          overflow: "auto",
          height: "100%",
          background: colorBgContainer,
        }}
      >
        <div ref={messageListRef} style={{
          // padding: "0",
          minHeight: 360,
          height: "100%",
          background: colorBgContainer,
        }}>
          {messages.map((message, index) => {
            switch (message.type) {
              case "apiMessage":
                return (

                  // The latest message sent by the user will be animated while waiting for a response
                  <div key={index} style={{ padding: "20px" }}>
                    <div>
                      {/* Messages are being rendered in Markdown format */}
                      <div style={{ color: "black", whiteSpace: "pre-line" }}>{message.message}</div>
                    </div>
                  </div>
                )
              case "userMessage":
                return (

                  // The latest message sent by the user will be animated while waiting for a response
                  <div key={index} style={{ padding: "20px", whiteSpace: "pre-line", textAlign: "right", background: "gray", width: "100%", color: "white" }}>
                    <div>
                      {/* Messages are being rendered in Markdown format */}
                      <div>{message.message}</div>
                    </div>
                  </div>
                )
              default:
                break;
            }

          })}
        </div>
      </Content>
      <Footer
        style={{
          textAlign: 'center',
          margin: '0 20% 0',
          padding: "2% 0"
        }}
      >
        {/* <AudioRecorder></AudioRecorder> */}
        <Search placeholder="input search text"
          allowClear
          enterButton="Search" size="large" onSearch={onSearch}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        ></Search>
      </Footer>
    </Layout>
  );
}

export default App
