const ChatMessage = ({ message, isBot }) => {
    return (
      <div className={`flex ${isBot ? 'justify-start' : 'justify-end'}`}>
        <div className={`p-2 m-2 ${isBot ? 'bg-gray-200' : 'bg-blue-500 text-white'} rounded-lg`}>
          <p>{message}</p>
        </div>
      </div>
    );
  };
  
  export default ChatMessage;
  