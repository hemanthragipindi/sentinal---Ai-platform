import { Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { useAuthStore } from '../store/auth';
import Dashboard from '../pages/Dashboard';
import Conversations from '../pages/Conversations';
import Memory from '../pages/Memory';
import Retrieval from '../pages/Retrieval';
import Security from '../pages/Security';
import Storage from '../pages/Storage';
import Reports from '../pages/Reports';
import Settings from '../pages/Settings';
import Profile from '../pages/Profile';
import Login from '../pages/Login';
import Register from '../pages/Register';

function PrivateRoute({ children }) {
  const { isAuthenticated, access_token } = useAuthStore();
  if (!isAuthenticated && !access_token) return <Navigate to="/login" replace />;
  return children;
}

function GuestRoute({ children }) {
  const { isAuthenticated } = useAuthStore();
  if (isAuthenticated) return <Navigate to="/" replace />;
  return children;
}

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<GuestRoute><Login /></GuestRoute>} />
      <Route path="/register" element={<GuestRoute><Register /></GuestRoute>} />
      <Route element={<PrivateRoute><AppLayout /></PrivateRoute>}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/conversations" element={<Conversations />} />
        <Route path="/memory" element={<Memory />} />
        <Route path="/retrieval" element={<Retrieval />} />
        <Route path="/security" element={<Security />} />
        <Route path="/storage" element={<Storage />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/profile" element={<Profile />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
