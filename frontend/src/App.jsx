import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ShoppingListPage from './pages/ShoppingListPage';
import WeekPlanPage from './pages/WeekPlanPage';
import { ROUTES } from './constants/routes';
import Navbar from './components/Navbar';

import { useAuth } from './hooks/useAuth';
import Login from './components/Login';
import RoleSelector from './components/RoleSelector';


import AuthGuard from './components/AuthGuard';
import ProtectedRoute from './components/ProtectedRoute';


function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path={ROUTES.HOME} element={<HomePage />} />

        {/* Rutas protegidas por rol */}
        <Route
          path={ROUTES.SHOPPING_LIST}
          element={
            <AuthGuard>
              <ProtectedRoute allowedRoles={['usuario']}>
                <ShoppingListPage />
              </ProtectedRoute>
            </AuthGuard>
          }
        />
        <Route
          path={ROUTES.WEEK_PLAN}
          element={
            <AuthGuard>
              <ProtectedRoute allowedRoles={['usuario', 'nutriologo']}>
                <WeekPlanPage />
              </ProtectedRoute>
            </AuthGuard>
          }
        />
        
      </Routes>
    </>
  );
}

export default App;