import { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getToken, setToken, removeToken } from '../utils/auth'; // Utility functions to handle tokens

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // On component mount, check if a token exists in local storage
  useEffect(() => {
    const token = getToken();
    if (token) {
      // If token exists, set user and navigate to homepage
      setUser({ token });
      navigate('/home');
    }
  }, [navigate]);

  // Login function
  const login = (token) => {
    setToken(token); // Save token to local storage
    setUser({ token });
    navigate('/home'); // Redirect to homepage
  };

  // Logout function
  const logout = () => {
    removeToken(); // Remove token from local storage
    setUser(null); // Clear user state
    navigate('/login'); // Redirect to login page
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to access auth state
export const useAuth = () => useContext(AuthContext);
