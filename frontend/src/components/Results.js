import React from 'react';
import { CheckCircle, AlertTriangle, ExternalLink, TrendingUp, Award } from 'lucide-react';
import SkillChart from './SkillChart';

const Results = ({ analysis, onNewAnalysis }) => {
  if (!analysis) return null;

  const {
    university,
    field,
    covered_skills,
    missing_skills,
    skill_coverage_percentage,
    recommendations
  } = analysis;

  const coverageColor = skill_coverage_percentage >= 75 
    ? 'text-green-600' 
    : skill_coverage_percentage >= 50 
    ? 'text-yellow-600' 
    : 'text-red-600';

  const coverageColorBg = skill_coverage_percentage >= 75 
    ? 'bg-green-100' 
    : skill_coverage_percentage >= 50 
    ? 'bg-yellow-100' 
    : 'bg-red-100';

  return (
    <div className="fade-in max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <div className="text-center">
          <div className={`inline-flex items-center justify-center w-20 h-20 ${coverageColorBg} rounded-full mb-4`}>
            <Award className={`w-10 h-10 ${coverageColor}`} />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Skill Gap Analysis Results
          </h2>
          <p className="text-gray-600 mb-4">
            {university} • {field}
          </p>
          <div className="flex items-center justify-center space-x-4">
            <div className={`px-4 py-2 ${coverageColorBg} rounded-full`}>
              <span className={`text-2xl font-bold ${coverageColor}`}>
                {skill_coverage_percentage.toFixed(1)}%
              </span>
              <span className="text-sm text-gray-600 ml-2">Coverage</span>
            </div>
          </div>
        </div>
      </div>

      {/* Skills Overview Grid */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Covered Skills */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center mb-6">
            <CheckCircle className="w-6 h-6 text-green-600 mr-3" />
            <h3 className="text-xl font-bold text-gray-900">
              Skills You Already Have
            </h3>
            <span className="ml-auto bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              {covered_skills.length} skills
            </span>
          </div>
          
          {covered_skills.length > 0 ? (
            <div className="space-y-3 max-h-80 overflow-y-auto custom-scrollbar">
              {covered_skills.map((skill, index) => (
                <div
                  key={index}
                  className="skill-badge covered flex items-center justify-between"
                >
                  <span>{skill}</span>
                  <CheckCircle className="w-4 h-4 text-green-600" />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <TrendingUp className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p>No matching skills found in your syllabus</p>
            </div>
          )}
        </div>

        {/* Missing Skills */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center mb-6">
            <AlertTriangle className="w-6 h-6 text-yellow-600 mr-3" />
            <h3 className="text-xl font-bold text-gray-900">
              Skills You Need to Learn
            </h3>
            <span className="ml-auto bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
              {missing_skills.length} skills
            </span>
          </div>
          
          {missing_skills.length > 0 ? (
            <div className="space-y-3 max-h-80 overflow-y-auto custom-scrollbar">
              {missing_skills.map((skill, index) => (
                <div
                  key={index}
                  className="skill-badge missing flex items-center justify-between"
                >
                  <span>{skill}</span>
                  <AlertTriangle className="w-4 h-4 text-yellow-600" />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <CheckCircle className="w-12 h-12 text-green-300 mx-auto mb-4" />
              <p>Excellent! No skill gaps identified</p>
            </div>
          )}
        </div>
      </div>

      {/* Skill Coverage Chart */}
      {(covered_skills.length > 0 || missing_skills.length > 0) && (
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-6 text-center">
            Skill Coverage Visualization
          </h3>
          <SkillChart 
            coveredSkills={covered_skills}
            missingSkills={missing_skills}
            coveragePercentage={skill_coverage_percentage}
          />
        </div>
      )}

      {/* Learning Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex items-center mb-6">
            <ExternalLink className="w-6 h-6 text-blue-600 mr-3" />
            <h3 className="text-xl font-bold text-gray-900">
              Recommended Learning Paths
            </h3>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className="skill-card border border-gray-200 rounded-lg p-6 hover:border-blue-300"
              >
                <div className="flex items-start justify-between mb-3">
                  <h4 className="font-semibold text-gray-900 line-clamp-2">
                    {rec.title}
                  </h4>
                  <ExternalLink className="w-4 h-4 text-gray-400 flex-shrink-0 ml-2" />
                </div>
                
                <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                  {rec.description}
                </p>
                
                <div className="flex items-center justify-between">
                  <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                    {rec.platform}
                  </span>
                  
                  <a
                    href={rec.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Learn More →
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={onNewAnalysis}
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105"
        >
          Analyze Another Syllabus
        </button>
        
        <button
          onClick={() => window.print()}
          className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
        >
          Print Results
        </button>
      </div>

      {/* Coverage Insights */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-8">
        <h3 className="text-lg font-bold text-gray-900 mb-4">
          📊 Analysis Insights
        </h3>
        
        <div className="grid md:grid-cols-3 gap-6 text-center">
          <div>
            <div className="text-2xl font-bold text-green-600">
              {covered_skills.length}
            </div>
            <div className="text-sm text-gray-600">Skills Covered</div>
          </div>
          
          <div>
            <div className="text-2xl font-bold text-yellow-600">
              {missing_skills.length}
            </div>
            <div className="text-sm text-gray-600">Skills to Learn</div>
          </div>
          
          <div>
            <div className={`text-2xl font-bold ${coverageColor}`}>
              {skill_coverage_percentage.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">Industry Readiness</div>
          </div>
        </div>
        
        <div className="mt-6 text-center">
          <p className="text-gray-700">
            {skill_coverage_percentage >= 75 
              ? "Excellent! You're well-prepared for the industry. Focus on the remaining skills to become a top candidate."
              : skill_coverage_percentage >= 50 
              ? "Good foundation! Work on the missing skills to boost your industry readiness."
              : "Great start! Focus on building the core skills to increase your market competitiveness."
            }
          </p>
        </div>
      </div>
    </div>
  );
};

export default Results;
