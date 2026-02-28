import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import StatsPage from './pages/StatsPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <nav className="nav-bar">
        <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
          Chat
        </NavLink>
        <NavLink to="/stats" className={({ isActive }) => (isActive ? 'active' : '')}>
          Statistics
        </NavLink>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/stats" element={<StatsPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
