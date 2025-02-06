import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import ChatbotPage from './pages/ChatbotPage';
import RegisterPage from './pages/RegisterPage';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute'; // Import PrivateRoute

function App() {
  return (
    <Router>
      <AuthProvider> {/* AuthProvider should be inside the Router */}
        <Navbar /> {/* Add Navbar here */}
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Private routes that require authentication */}
          <Route element={<PrivateRoute />}>
            <Route path="/home" element={<HomePage />} />
            <Route path="/chatbot" element={<ChatbotPage />} />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
