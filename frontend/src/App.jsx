import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ShoppingListPage from './pages/ShoppingListPage';
import WeekPlanPage from './pages/WeekPlanPage';
import { ROUTES } from './constants/routes';
import Navbar from './components/Navbar';

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path={ROUTES.HOME} element={<HomePage />} />
        <Route path={ROUTES.SHOPPING_LIST} element={<ShoppingListPage />} />
        <Route path={ROUTES.WEEK_PLAN} element={<WeekPlanPage />} />
      </Routes>
    </>
  );
}

export default App;