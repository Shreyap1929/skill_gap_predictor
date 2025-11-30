import React from 'react';
import { Brain, FileText, Search, TrendingUp } from 'lucide-react';

const Loading = () => {
  const steps = [
    {
      icon: FileText,
      title: 'Extracting Text',
      description: 'Reading your PDF document...',
    },
    {
      icon: Brain,
      title: 'Processing Content',
      description: 'Identifying skills and technologies...',
    },
    {
      icon: Search,
      title: 'Comparing Skills',
      description: 'Matching with industry requirements...',
    },
    {
      icon: TrendingUp,
      title: 'Generating Report',
      description: 'Creating your personalized analysis...',
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-8">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
        <div className="mb-8">
          <div className="relative mx-auto w-20 h-20 mb-6">
            <div className="absolute inset-0 border-4 border-blue-200 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-blue-600 rounded-full animate-spin border-t-transparent"></div>
            <Brain className="absolute inset-0 w-8 h-8 text-blue-600 m-auto animate-pulse" />
          </div>
          
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Analyzing Your Syllabus
          </h2>
          <p className="text-gray-600">
            Processing your document and identifying skill gaps...
          </p>
        </div>

        <div className="space-y-4">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div
                key={index}
                className={`flex items-center p-3 rounded-lg transition-all duration-500 ${
                  index <= 1 ? 'bg-blue-50 border-l-4 border-blue-500' : 'bg-gray-50'
                }`}
                style={{
                  animationDelay: `${index * 0.5}s`,
                }}
              >
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                  index <= 1 ? 'bg-blue-500' : 'bg-gray-300'
                }`}>
                  <Icon className={`w-4 h-4 ${index <= 1 ? 'text-white' : 'text-gray-500'}`} />
                </div>
                <div className="text-left">
                  <div className={`font-medium ${index <= 1 ? 'text-blue-900' : 'text-gray-700'}`}>
                    {step.title}
                  </div>
                  <div className={`text-sm ${index <= 1 ? 'text-blue-700' : 'text-gray-500'}`}>
                    {step.description}
                  </div>
                </div>
                {index <= 1 && (
                  <div className="ml-auto">
                    <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-6">
          <div className="bg-gray-200 rounded-full h-2 mb-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full progress-bar animate-pulse"
              style={{ width: '45%' }}
            ></div>
          </div>
          <p className="text-sm text-gray-500">
            This may take a few moments depending on document size...
          </p>
        </div>

        <div className="mt-8 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
          <div className="text-sm text-gray-700">
            <strong>💡 Did you know?</strong>
            <br />
            The average job posting requires 5-10 different technical skills. 
            Our system analyzes over 1000+ industry skill requirements to give you 
            the most accurate gap analysis!
          </div>
        </div>
      </div>
    </div>
  );
};

export default Loading;