import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const HomePage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login'); // Redirect to login page after logout
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-3xl text-center">Welcome to the Chatbot</h2>
      <p className="text-center text-lg mt-2">Hello, {user ? 'User' : 'Guest'}!</p>
      <div className="flex justify-center mt-4">
        <button
          onClick={() => navigate('/chatbot')}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Go to Chatbot
        </button>
      </div>
      <div className="flex justify-center mt-4">
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default HomePage;
