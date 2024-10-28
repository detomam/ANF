import './App.css';
import React, { useState, useEffect } from "react";
import SendIcon from "./send.svg";

import Message from "./message";

export default function MyApp() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');

  // send a message to the bot
  const sendQuery = (query) => {
    //make a new message to display for user
    let updatedMessages = [...messages, {message: query, isUser: 1}];
    
    // TODO: Get BOT response then send new message in chat
        // for now just echo back original message
    updatedMessages = [...updatedMessages, {message: "Response to " + query, isUser: 0}];
    
    //update messages
    setMessages(updatedMessages);

    //clear the input box
    document.getElementById("inputBox").value = "";
  }
  
  return (
    <div class="app">
      <h1 class="MyApp white">Alissaa</h1>
      <div class="messaging bg-white">
        {messages?.length > 0 ? (
          <div className="container">
            {messages.map((message, index) => (
              <Message text={message.message} index={index} isUser={message.isUser}></Message>
            ))}
          </div>
        ) : (
          <div className="empty">
            <p>No messages yet.</p>
          </div>
        )}
      </div>
      <div class="input">
        <div className="textarea-container">
          <textarea
              class="textarea white bg-gray"
              id="inputBox"
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Write something..">
          </textarea>
          <img
              class="send"
              src={SendIcon}
              alt="send"
              onClick={() => (query.length !== 0) ? sendQuery(query) : null}
          />
        </div>
      </div>
    </div>
  );
}