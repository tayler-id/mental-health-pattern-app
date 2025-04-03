import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faHome,
  faPlusCircle,
  faChartLine,
  faSearch,
  faLightbulb,
  faCog,
  faHistory,
  faBrain
} from '@fortawesome/free-solid-svg-icons';

// Import styles
import './App.css';
import './styles/theme.css';

// Import components
import Dashboard from './components/Dashboard';
import MoodEntryForm from './components/MoodEntryForm';
import MoodHistory from './components/MoodHistory';
import ActivityEntryForm from './components/ActivityEntryForm';
import SleepEntryForm from './components/SleepEntryForm';
import AnalysisPanel from './components/AnalysisPanel';
import VisualizationsPanel from './components/VisualizationsPanel';
import InsightsPanel from './components/InsightsPanel';
import SettingsPanel from './components/SettingsPanel';
import Header from './components/Header';
import Footer from './components/Footer';

// Import context
import { AppProvider } from './context/AppContext';

// Section component with animations
const Section = ({ title, children }) => {
  return (
    <motion.div
      className="section"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <h2 className="section-title">{title}</h2>
      <div className="section-content">
        {children}
      </div>
    </motion.div>
  );
};

// Navigation item component
const NavItem = ({ to, icon, label }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <li className={isActive ? 'active' : ''}>
      <Link to={to}>
        <FontAwesomeIcon icon={icon} />
        <span>{label}</span>
        {isActive && (
          <motion.div
            className="nav-indicator"
            layoutId="nav-indicator"
            transition={{ type: 'spring', duration: 0.5 }}
          />
        )}
      </Link>
    </li>
  );
};

function AppContent() {
  const location = useLocation();

  return (
    <div className="app-container">
      <Header />

      <div className="app-content">
        <aside className="sidebar">
          <div className="sidebar-header">
            <h3>Mental Health Pattern Assistant</h3>
          </div>
          <nav>
            <ul>
              <NavItem to="/" icon={faHome} label="Dashboard" />
              <NavItem to="/data-entry" icon={faPlusCircle} label="Data Entry" />
              <NavItem to="/view-data" icon={faHistory} label="View Data" />
              <NavItem to="/analysis" icon={faBrain} label="Analysis" />
              <NavItem to="/visualizations" icon={faChartLine} label="Visualizations" />
              <NavItem to="/insights" icon={faLightbulb} label="Insights" />
              <NavItem to="/settings" icon={faCog} label="Settings" />
            </ul>
          </nav>
        </aside>

        <main className="main-content">
          <AnimatePresence mode="wait">
            <Routes location={location} key={location.pathname}>
              <Route path="/" element={
                <Section title="Dashboard">
                  <Dashboard />
                </Section>
              } />

              <Route path="/data-entry" element={
                <Section title="Data Entry">
                  <div className="entry-forms">
                    <MoodEntryForm />
                    <ActivityEntryForm />
                    <SleepEntryForm />
                  </div>
                </Section>
              } />

              <Route path="/view-data" element={
                <Section title="View Data">
                  <MoodHistory />
                </Section>
              } />

              <Route path="/analysis" element={
                <Section title="Analysis">
                  <AnalysisPanel />
                </Section>
              } />

              <Route path="/visualizations" element={
                <Section title="Visualizations">
                  <VisualizationsPanel />
                </Section>
              } />

              <Route path="/insights" element={
                <Section title="Insights">
                  <InsightsPanel />
                </Section>
              } />

              <Route path="/settings" element={
                <Section title="Settings">
                  <SettingsPanel />
                </Section>
              } />
            </Routes>
          </AnimatePresence>
        </main>
      </div>

      <Footer />
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <Router>
        <AppContent />
      </Router>
    </AppProvider>
  );
}

export default App;
