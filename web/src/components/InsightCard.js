import React from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faLightbulb,
  faChartLine,
  faRunning,
  faBed,
  faCalendarAlt,
  faExclamationTriangle
} from '@fortawesome/free-solid-svg-icons';
import './InsightCard.css';

const InsightCard = ({ insight, delay = 0 }) => {
  // Get icon based on insight type
  const getInsightIcon = () => {
    const type = insight.type?.toLowerCase() || '';
    
    if (type.includes('mood')) return faChartLine;
    if (type.includes('activity')) return faRunning;
    if (type.includes('sleep')) return faBed;
    if (type.includes('pattern')) return faCalendarAlt;
    if (type.includes('warning')) return faExclamationTriangle;
    
    return faLightbulb; // Default icon
  };
  
  // Get class based on insight type
  const getInsightClass = () => {
    const type = insight.type?.toLowerCase() || '';
    
    if (type.includes('warning')) return 'warning';
    if (type.includes('positive')) return 'positive';
    if (type.includes('negative')) return 'negative';
    
    return 'neutral'; // Default class
  };
  
  return (
    <motion.div
      className={`insight-card ${getInsightClass()}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: 0.7 + delay }}
    >
      <div className="insight-icon">
        <FontAwesomeIcon icon={getInsightIcon()} />
      </div>
      <div className="insight-content">
        <h4 className="insight-title">{insight.title || 'Insight'}</h4>
        <p className="insight-description">{insight.description || insight.message || 'No description available.'}</p>
        {insight.recommendation && (
          <p className="insight-recommendation">
            <strong>Recommendation:</strong> {insight.recommendation}
          </p>
        )}
      </div>
    </motion.div>
  );
};

export default InsightCard;
