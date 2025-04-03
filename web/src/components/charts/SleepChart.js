import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import { format, parseISO } from 'date-fns';
import './Charts.css';

const SleepChart = ({ data }) => {
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
    const sleepDurations = sortedData.map(entry => entry.duration_hours);
    const sleepQualities = sortedData.map(entry => entry.quality_rating);
    
    // Create the chart
    chartInstance.current = new Chart(chartRef.current, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Sleep Duration (hours)',
            data: sleepDurations,
            backgroundColor: 'rgba(139, 92, 246, 0.7)',
            borderColor: 'rgba(139, 92, 246, 1)',
            borderWidth: 1,
            borderRadius: 4,
            barPercentage: 0.6,
            categoryPercentage: 0.7
          },
          {
            label: 'Sleep Quality (1-10)',
            data: sleepQualities,
            backgroundColor: 'rgba(16, 185, 129, 0.7)',
            borderColor: 'rgba(16, 185, 129, 1)',
            borderWidth: 1,
            borderRadius: 4,
            barPercentage: 0.6,
            categoryPercentage: 0.7
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 12,
              padding: 15,
              font: {
                size: 11
              }
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              afterLabel: function(context) {
                const index = context.dataIndex;
                const entry = sortedData[index];
                
                if (entry.notes) {
                  return `Notes: ${entry.notes}`;
                }
                
                return '';
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 10,
            grid: {
              color: 'rgba(0, 0, 0, 0.05)'
            },
            ticks: {
              stepSize: 2
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
        <p>No sleep data available</p>
      </div>
    );
  }
  
  return (
    <div className="chart-wrapper">
      <canvas ref={chartRef} />
    </div>
  );
};

export default SleepChart;
