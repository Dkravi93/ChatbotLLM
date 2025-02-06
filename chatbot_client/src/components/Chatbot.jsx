import { useState } from 'react';
import { sendQuery } from '../utils/api';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import LoadingSpinner from './LoadingSpinner';

const Chatbot = () => {
  const [query, setQuery] = useState('');
  const [chat, setChat] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (query.trim() === '') return;

    setIsLoading(true);

    const newMessage = { query, response: '...' }; // Initial bot response is a placeholder
    setChat([...chat, newMessage]);

    try {
      const data = await sendQuery(query);
      setChat([...chat, { query, response: data.response }]);
    } catch (error) {
      console.error('Error fetching response:', error);
      setChat([...chat, { query, response: "Sorry, I couldn't process your request." }]);
    } finally {
      setIsLoading(false);
      setQuery('');
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <div className="mb-4 space-y-4 max-h-[400px] overflow-y-auto">
        {chat.map((msg, idx) => (
          <ChatMessage key={idx} message={msg.response} isBot={idx % 2 !== 0} />
        ))}
        {isLoading && <LoadingSpinner />}
      </div>
      <ChatInput query={query} setQuery={setQuery} handleSend={handleSend} />
    </div>
  );
};

export default Chatbot;
