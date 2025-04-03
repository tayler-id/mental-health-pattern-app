import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import { format, parseISO } from 'date-fns';
import './Charts.css';

const ActivityChart = ({ data }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);
  
  useEffect(() => {
    if (!data || data.length === 0) return;
    
    // Destroy existing chart if it exists
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }
    
    // Group activities by type
    const activityTypes = {};
    data.forEach(entry => {
      const type = entry.activity_type || 'Other';
      if (!activityTypes[type]) {
        activityTypes[type] = 0;
      }
      activityTypes[type]++;
    });
    
    // Prepare data for chart
    const labels = Object.keys(activityTypes);
    const counts = Object.values(activityTypes);
    
    // Generate colors for each activity type
    const colors = labels.map((_, index) => {
      const hue = (index * 137) % 360; // Golden angle approximation for good distribution
      return `hsl(${hue}, 70%, 60%)`;
    });
    
    // Create the chart
    chartInstance.current = new Chart(chartRef.current, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: counts,
          backgroundColor: colors,
          borderColor: 'white',
          borderWidth: 2,
          hoverOffset: 10
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              boxWidth: 12,
              padding: 15,
              font: {
                size: 11
              }
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.raw || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = Math.round((value / total) * 100);
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        },
        cutout: '70%',
        animation: {
          animateScale: true,
          animateRotate: true
        }
      }
    });
    
    // Cleanup function
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [data]);
  
  if (!data || data.length === 0) {
    return (
      <div className="chart-empty">
        <p>No activity data available</p>
      </div>
    );
  }
  
  return (
    <div className="chart-wrapper">
      <canvas ref={chartRef} />
    </div>
  );
};

export default ActivityChart;
