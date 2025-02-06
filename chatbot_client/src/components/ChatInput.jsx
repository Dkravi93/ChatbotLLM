const ChatInput = ({ query, setQuery, handleSend }) => {
    return (
      <div className="flex">
        <input
          type="text"
          className="flex-1 border p-2 rounded-l-md"
          placeholder="Enter your query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={handleSend}
          className="bg-blue-500 text-white px-4 py-2 rounded-r-md"
        >
          Send
        </button>
      </div>
    );
  };
  
  export default ChatInput;
  