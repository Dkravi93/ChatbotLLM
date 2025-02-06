import { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getToken, setToken, removeToken } from '../utils/auth';
import { fetchUserData } from '../utils/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const token = getToken();
    if (token) {
      // Fetch user data from API if token is available
      fetchUserData(token)
        .then((userData) => {
          console.log("IIIIIIII", userData);
          
          setUser({ ...userData, token }); // Store both token and user data
        })
        .catch((error) => {
          console.error("Failed to fetch user data:", error);
          removeToken(); // Remove invalid token if fetching fails
        });
    }
  }, [navigate]);

  // Login function
  const login = (token) => {
    setToken(token);
    // Fetch user data after login and store it along with token
    fetchUserData(token)
      .then((userData) => {
        console.log("IIIIIIIItt", userData);
        setUser({ ...userData, token });
        navigate('/home');
      })
      .catch((error) => {
        console.error("Failed to fetch user data:", error);
        // Handle error appropriately (show error message or redirect)
      });
  };

  // Logout function
  const logout = () => {
    removeToken();
    setUser(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to access auth state
export const useAuth = () => useContext(AuthContext);
