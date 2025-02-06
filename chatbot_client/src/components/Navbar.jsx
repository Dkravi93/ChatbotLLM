import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-blue-500 p-4">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <Link to="/home" className="text-white text-2xl font-semibold">
          Chatbot
        </Link>
        <div className="space-x-4">
          {!user ? (
            <>
              <Link to="/login" className="text-white">Login</Link>
              <Link to="/register" className="text-white">Register</Link>
            </>
          ) : (
            <>
              <Link to="/chatbot" className="text-white">Chatbot</Link>
              <button
                onClick={logout}
                className="text-white bg-red-500 px-4 py-2 rounded"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
