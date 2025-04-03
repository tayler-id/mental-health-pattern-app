import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import { format, parseISO, subDays } from 'date-fns';
import './Charts.css';

const MoodChart = ({ data }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);
  
  useEffect(() => {
    if (!data || data.length === 0) return;
    
    // Destroy existing chart if it exists
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }
    
    // Sort data by timestamp
    const sortedData = [...data].sort((a, b) => {
      return new Date(a.timestamp) - new Date(b.timestamp);
    });
    
    // Prepare data for chart
    const labels = sortedData.map(entry => format(parseISO(entry.timestamp), 'MMM d'));
    const moodLevels = sortedData.map(entry => entry.mood_level);
    
    // Get the canvas context
    const ctx = chartRef.current.getContext('2d');
    
    // Create gradient for the line
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(99, 102, 241, 0.5)');
    gradient.addColorStop(1, 'rgba(99, 102, 241, 0.1)');
    
    // Create the chart
    chartInstance.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Mood Level',
          data: moodLevels,
          borderColor: 'rgba(99, 102, 241, 1)',
          backgroundColor: gradient,
          borderWidth: 2,
          tension: 0.3,
          fill: true,
          pointBackgroundColor: 'rgba(99, 102, 241, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              afterLabel: function(context) {
                const index = context.dataIndex;
                const entry = sortedData[index];
                let result = '';
                
                if (entry.emotions && entry.emotions.length > 0) {
                  result += `Emotions: ${entry.emotions.join(', ')}`;
                }
                
                if (entry.notes) {
                  if (result) result += '\n';
                  result += `Notes: ${entry.notes}`;
                }
                
                return result;
              }
            }
          }
        },
        scales: {
          y: {
            min: 0,
            max: 10,
            grid: {
              color: 'rgba(0, 0, 0, 0.05)'
            },
            ticks: {
              stepSize: 1,
              callback: function(value) {
                if (value === 0) return '';
                if (value === 10) return 'Excellent';
                if (value === 5) return 'Okay';
                if (value === 1) return 'Poor';
                return value;
              }
            }
          },
          x: {
            grid: {
              display: false
            }
          }
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
        <p>No mood data available</p>
      </div>
    );
  }
  
  return (
    <div className="chart-wrapper">
      <canvas ref={chartRef} />
    </div>
  );
};

export default MoodChart;
