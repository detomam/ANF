import './App.css';
import React, { useState } from "react";
import SendIcon from "./send.svg";
import Logo from './logo.png';

export default function MyApp() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');

  // send a message to the bot
  const sendQuery = async (query) => {
    //make a new message to display for user
    let updatedMessages = [...messages, {message: query, isUser: 1}];
    
    // TODO: Get BOT response then send new message in chat
        // for now just echo back original message
        try {
          const response = await fetch("http://127.0.0.1:8000/process-query", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify({ query }),
          });

          if (!response.ok) {
              throw new Error("Failed to fetch response from server");
          }

          const data = await response.json();
          // Add the bot's response to the chat
          updatedMessages = [...updatedMessages, { message: data.response, isUser: 0 }];
          setMessages(updatedMessages);
      } catch (error) {
          console.error("Error:", error);
          updatedMessages = [...updatedMessages, { message: "Error fetching response", isUser: 0 }];
          setMessages(updatedMessages);
      }

      // Clear the input box
      setQuery("");
      document.getElementById("inputBox").value = "";
  };
  
  return (
    <div className="app">
    <h1 className="MyApp white">
      Ask ALISSAA
      <img className="logo" src={Logo} alt="Logo" />
    </h1>
      <div className="messaging bg-white">
        {messages?.length > 0 ? (
          <div className="container">
            {messages.map((message, index) => (
              <div
                className="message-container"
                key={index}
              >
                <div className={`message ${message.isUser ? 'user bg-orange' : 'bot bg-black'}`}>
                  {message.message}
                </div>
                <div className={`message-actions ${message.isUser ? 'user' : 'bot'}`}>
                  <div className={`username ${message.isUser ? 'user orange' : 'bot black'}`}>
                    {message.isUser ? 'You' : 'Alissaa'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty">No messages yet.</div>
        )}
      </div>
      <div className="input">
        <div className="textarea-container">
        <textarea
          className="textarea white bg-gray"
          id="inputBox"
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && query.trim().length !== 0) {
              e.preventDefault(); // Prevent a new line from being added
              sendQuery(query);
            }
          }}
          placeholder="Write something..">
        </textarea>
          <img
            className="send"
            src={SendIcon}
            alt="send"
            onClick={() => (query.length !== 0) ? sendQuery(query) : null}
          />
        </div>
      </div>
    </div>
  );
}
