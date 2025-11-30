import React, { useEffect, useRef } from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement
} from 'chart.js';
import { Radar, Doughnut, Bar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement
);

const SkillChart = ({ coveredSkills, missingSkills, coveragePercentage }) => {
  const chartRef = useRef(null);

  // Categorize skills for radar chart
  const categorizeSkills = (skills) => {
    const categories = {
      'Programming': [],
      'Web Development': [],
      'Data & Analytics': [],
      'Tools & Frameworks': [],
      'Fundamentals': [],
      'Other': []
    };

    const categoryKeywords = {
      'Programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin', 'swift'],
      'Web Development': ['html', 'css', 'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring'],
      'Data & Analytics': ['sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'machine learning', 'data science', 'statistics', 'pandas', 'numpy'],
      'Tools & Frameworks': ['git', 'docker', 'kubernetes', 'aws', 'azure', 'jenkins', 'webpack', 'babel', 'linux'],
      'Fundamentals': ['data structures', 'algorithms', 'object oriented programming', 'system design', 'software engineering', 'computer networks', 'operating systems']
    };

    skills.forEach(skill => {
      const skillLower = skill.toLowerCase();
      let categorized = false;

      for (const [category, keywords] of Object.entries(categoryKeywords)) {
        if (keywords.some(keyword => skillLower.includes(keyword))) {
          categories[category].push(skill);
          categorized = true;
          break;
        }
      }

      if (!categorized) {
        categories['Other'].push(skill);
      }
    });

    return categories;
  };

  const coveredCategories = categorizeSkills(coveredSkills);
  const missingCategories = categorizeSkills(missingSkills);
  const allCategories = Object.keys(coveredCategories);

  // Prepare radar chart data
  const radarData = {
    labels: allCategories,
    datasets: [
      {
        label: 'Skills Covered',
        data: allCategories.map(category => coveredCategories[category].length),
        backgroundColor: 'rgba(34, 197, 94, 0.2)',
        borderColor: 'rgba(34, 197, 94, 1)',
        pointBackgroundColor: 'rgba(34, 197, 94, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(34, 197, 94, 1)',
      },
      {
        label: 'Skills Missing',
        data: allCategories.map(category => missingCategories[category].length),
        backgroundColor: 'rgba(251, 191, 36, 0.2)',
        borderColor: 'rgba(251, 191, 36, 1)',
        pointBackgroundColor: 'rgba(251, 191, 36, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(251, 191, 36, 1)',
      },
    ],
  };

  // Doughnut chart for overall coverage
  const doughnutData = {
    labels: ['Covered Skills', 'Missing Skills'],
    datasets: [
      {
        data: [coveredSkills.length, missingSkills.length],
        backgroundColor: ['#22c55e', '#fbbf24'],
        borderColor: ['#16a34a', '#f59e0b'],
        borderWidth: 2,
      },
    ],
  };

  // Bar chart for category comparison
  const barData = {
    labels: allCategories,
    datasets: [
      {
        label: 'Covered',
        data: allCategories.map(category => coveredCategories[category].length),
        backgroundColor: '#22c55e',
      },
      {
        label: 'Missing',
        data: allCategories.map(category => missingCategories[category].length),
        backgroundColor: '#fbbf24',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        cornerRadius: 8,
        displayColors: true,
      },
    },
  };

  const radarOptions = {
    ...chartOptions,
    scales: {
      r: {
        angleLines: {
          display: true,
        },
        suggestedMin: 0,
        suggestedMax: Math.max(
          ...allCategories.map(cat => 
            coveredCategories[cat].length + missingCategories[cat].length
          )
        ) + 2,
        ticks: {
          stepSize: 1,
        },
      },
    },
    plugins: {
      ...chartOptions.plugins,
      tooltip: {
        ...chartOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            const category = context.label;
            const dataset = context.dataset.label;
            const value = context.parsed.r;
            
            if (dataset === 'Skills Covered' && value > 0) {
              const skills = coveredCategories[category].join(', ');
              return `${dataset}: ${value} (${skills})`;
            } else if (dataset === 'Skills Missing' && value > 0) {
              const skills = missingCategories[category].join(', ');
              return `${dataset}: ${value} (${skills})`;
            }
            return `${dataset}: ${value}`;
          }
        }
      }
    }
  };

  const doughnutOptions = {
    ...chartOptions,
    cutout: '60%',
    plugins: {
      ...chartOptions.plugins,
      legend: {
        position: 'bottom',
      },
    },
  };

  const barOptions = {
    ...chartOptions,
    plugins: {
      ...chartOptions.plugins,
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className="space-y-8">
      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4 text-center">
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-green-600">{coveredSkills.length}</div>
          <div className="text-sm text-green-800">Skills Covered</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-yellow-600">{missingSkills.length}</div>
          <div className="text-sm text-yellow-800">Skills Missing</div>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">{coveragePercentage.toFixed(1)}%</div>
          <div className="text-sm text-blue-800">Coverage</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Radar Chart */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h4 className="text-lg font-semibold text-gray-900 mb-4 text-center">
            Skills by Category (Radar View)
          </h4>
          <div className="chart-container h-80">
            <Radar ref={chartRef} data={radarData} options={radarOptions} />
          </div>
        </div>

        {/* Doughnut Chart */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h4 className="text-lg font-semibold text-gray-900 mb-4 text-center">
            Overall Coverage
          </h4>
          <div className="chart-container h-80">
            <Doughnut data={doughnutData} options={doughnutOptions} />
          </div>
        </div>
      </div>

      {/* Bar Chart - Full Width */}
      <div className="bg-gray-50 p-6 rounded-lg">
        <h4 className="text-lg font-semibold text-gray-900 mb-4 text-center">
          Category Breakdown
        </h4>
        <div className="chart-container h-64">
          <Bar data={barData} options={barOptions} />
        </div>
      </div>

      {/* Category Details */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {allCategories.map(category => {
          const covered = coveredCategories[category];
          const missing = missingCategories[category];
          const total = covered.length + missing.length;
          
          if (total === 0) return null;

          return (
            <div key={category} className="bg-white border border-gray-200 rounded-lg p-4">
              <h5 className="font-medium text-gray-900 mb-2">{category}</h5>
              <div className="space-y-1 text-sm">
                {covered.length > 0 && (
                  <div className="text-green-700">
                    ✅ {covered.length} covered: {covered.join(', ')}
                  </div>
                )}
                {missing.length > 0 && (
                  <div className="text-yellow-700">
                    ⚠️ {missing.length} missing: {missing.join(', ')}
                  </div>
                )}
              </div>
              <div className="mt-2">
                <div className="bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{ width: `${(covered.length / total) * 100}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {((covered.length / total) * 100).toFixed(0)}% coverage
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SkillChart;
