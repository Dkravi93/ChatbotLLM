import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PrivateRoute = () => {
  const { user } = useAuth();
  console.log("yyyy",user);
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />; // If logged in, allow access to the child route
};

export default PrivateRoute;
