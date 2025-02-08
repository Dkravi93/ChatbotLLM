import { useState, useRef, useEffect } from "react";
import { sendQuery } from "../utils/api";
import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import LoadingSpinner from "./LoadingSpinner";
import { useAuth } from "../context/AuthContext";

const Chatbot = () => {
  const { user } = useAuth();
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  // ✅ Scroll to bottom whenever chat updates
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const handleSend = async () => {
    if (!query.trim()) return;

    setIsLoading(true);

    const newMessage = { query, response: "..." };
    setChat((prevChat) => [...prevChat, newMessage]);
    console.log("UUSHSHSN", user, query, newMessage);
    
    try {
      const data = await sendQuery({ token: user?.token, query: query });
      setChat([...chat, { query, response: data.response }]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setChat([
        ...chat,
        { query, response: "Sorry, I couldn't process your request." },
      ]);
    } finally {
      setIsLoading(false);
      setQuery(""); // Reset input field
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <div className="mb-4 space-y-4 max-h-[400px] overflow-y-auto scrollbar-thin">
        {chat.map((msg, idx) => (
          <ChatMessage key={idx} message={msg.response} isBot={idx % 2 !== 0} />
        ))}
        {isLoading && <LoadingSpinner />}
        <div ref={chatEndRef} /> {/* Auto-scroll target */}
      </div>
      <ChatInput query={query} setQuery={setQuery} handleSend={handleSend} />
    </div>
  );
};

export default Chatbot;
