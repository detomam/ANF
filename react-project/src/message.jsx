import React from 'react';

const Message = ({ text, index, isUser }) => {
    const className = isUser === 1 ? "message user bg-orange" : "message bot bg-gray";

    return (
      <div key={index} className={className}>
        {"\n" + text}
      </div>
    );
  }
  

export default Message;