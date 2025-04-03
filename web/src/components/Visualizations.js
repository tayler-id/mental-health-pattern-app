import React from 'react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { motion } from 'framer-motion';
import { 
  moodData, 
  emotionData, 
  activityCorrelation, 
  weekdayMoodData 
} from '../data/sampleData';

const Visualizations = ({ onBack, audioManager }) => {
  // Color constants
  const MOOD_COLOR = 'var(--primary)';
  const ACTIVITY_COLOR = 'var(--accent)';
  const SLEEP_COLOR = 'var(--secondary)';
  const CORRELATION_POSITIVE_COLOR = 'var(--secondary)';
  const CORRELATION_NEGATIVE_COLOR = 'var(--tertiary)';
  
  // Emotion pie chart colors
  const EMOTION_COLORS = [
    'var(--primary)',
    'var(--secondary)',
    'var(--accent)',
    'var(--info)',
    'var(--neutral-500)',
    'var(--warning)',
    'var(--error)',
    'var(--neutral-700)'
  ];
  
  // Play button click sound
  const handleBackClick = () => {
    audioManager.playSound('click');
    onBack();
  };
  
  // Card animation variants
  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: {
        duration: 0.5,
        ease: "easeOut"
      }
    }
  };
  
  // Format correlation values for tooltip
  const formatCorrelation = (value) => {
    return `${(value * 100).toFixed(0)}%`;
  };
  
  // Calculate color based on correlation value
  const getCorrelationColor = (value) => {
    return value >= 0 ? CORRELATION_POSITIVE_COLOR : CORRELATION_NEGATIVE_COLOR;
  };
  
  return (
    <div className="visualizations-container animate-fade-in">
      <h2 className="text-center mb-4">Data Visualizations</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Mood Timeline Chart */}
        <motion.div 
          className="chart-container"
          variants={cardVariants}
          initial="hidden"
          animate="visible"
        >
          <div className="chart-header">
            <h3 className="chart-title">Mood Timeline</h3>
            <div className="chart-legend">
              <div className="legend-item">
                <div className="legend-color" style={{ backgroundColor: MOOD_COLOR }}></div>
                <span>Mood</span>
              </div>
              <div className="legend-item">
                <div className="legend-color" style={{ backgroundColor: ACTIVITY_COLOR }}></div>
                <span>Activities</span>
              </div>
              <div className="legend-item">
                <div className="legend-color" style={{ backgroundColor: SLEEP_COLOR }}></div>
                <span>Sleep</span>
              </div>
            </div>
          </div>
          
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={moodData}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="var(--neutral-200)" />
              <XAxis dataKey="date" tick={{ fill: 'var(--neutral-700)' }} />
              <YAxis domain={[0, 10]} tick={{ fill: 'var(--neutral-700)' }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'var(--neutral-50)', 
                  borderColor: 'var(--neutral-200)',
                  borderRadius: '0.375rem'
                }} 
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="mood" 
                stroke={MOOD_COLOR} 
                strokeWidth={3}
                activeDot={{ r: 6 }}
              />
              <Line 
                type="monotone" 
                dataKey="activities" 
                stroke={ACTIVITY_COLOR} 
                strokeWidth={2}
              />
              <Line 
                type="monotone" 
                dataKey="sleep" 
                stroke={SLEEP_COLOR} 
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
        
        {/* Emotion Distribution */}
        <motion.div 
          className="chart-container"
          variants={cardVariants}
          initial="hidden"
          animate="visible"
          transition={{ delay: 0.1 }}
        >
          <div className="chart-header">
            <h3 className="chart-title">Emotion Distribution</h3>
          </div>
          
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={emotionData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={2}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {emotionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={EMOTION_COLORS[index % EMOTION_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value) => [`${value} entries`, 'Count']}
                contentStyle={{ 
                  backgroundColor: 'var(--neutral-50)', 
                  borderColor: 'var(--neutral-200)',
                  borderRadius: '0.375rem'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
        
        {/* Activity Correlation */}
        <motion.div 
          className="chart-container"
          variants={cardVariants}
          initial="hidden"
          animate="visible"
          transition={{ delay: 0.2 }}
        >
          <div className="chart-header">
            <h3 className="chart-title">Activity-Mood Correlation</h3>
          </div>
          
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={activityCorrelation}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 60, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="var(--neutral-200)" />
              <XAxis 
                type="number" 
                domain={[-1, 1]} 
                tick={{ fill: 'var(--neutral-700)' }}
                tickFormatter={formatCorrelation}
              />
              <YAxis 
                dataKey="name" 
                type="category" 
                tick={{ fill: 'var(--neutral-700)' }} 
              />
              <Tooltip 
                formatter={(value) => [formatCorrelation(value), 'Correlation']}
                contentStyle={{ 
                  backgroundColor: 'var(--neutral-50)', 
                  borderColor: 'var(--neutral-200)',
                  borderRadius: '0.375rem'
                }}
              />
              <Bar 
                dataKey="correlation" 
                radius={[0, 4, 4, 0]}
              >
                {activityCorrelation.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getCorrelationColor(entry.correlation)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
        
        {/* Weekly Mood Pattern */}
        <motion.div 
          className="chart-container"
          variants={cardVariants}
          initial="hidden"
          animate="visible"
          transition={{ delay: 0.3 }}
        >
          <div className="chart-header">
            <h3 className="chart-title">Weekly Mood Pattern</h3>
          </div>
          
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={weekdayMoodData}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="var(--neutral-200)" />
              <XAxis dataKey="day" tick={{ fill: 'var(--neutral-700)' }} />
              <YAxis domain={[0, 10]} tick={{ fill: 'var(--neutral-700)' }} />
              <Tooltip 
                formatter={(value) => [`${value.toFixed(1)} / 10`, 'Average Mood']}
                contentStyle={{ 
                  backgroundColor: 'var(--neutral-50)', 
                  borderColor: 'var(--neutral-200)',
                  borderRadius: '0.375rem'
                }}
              />
              <Bar 
                dataKey="mood" 
                fill={MOOD_COLOR} 
                radius={[4, 4, 0, 0]}
                barSize={40}
              />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>
      
      <div className="flex justify-center mt-6">
        <button 
          className="btn btn-primary"
          onClick={handleBackClick}
        >
          Back to Menu
        </button>
      </div>
    </div>
  );
};

export default Visualizations;
