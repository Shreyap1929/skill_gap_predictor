import React from 'react';
import { AlertCircle, RefreshCw, Home } from 'lucide-react';

const Error = ({ error, onRetry, onHome }) => {
  const getErrorMessage = (error) => {
    if (typeof error === 'string') return error;
    if (error?.message) return error.message;
    if (error?.detail) return error.detail;
    return 'An unexpected error occurred while analyzing your syllabus.';
  };

  const getErrorSuggestions = (error) => {
    const errorMessage = getErrorMessage(error).toLowerCase();
    
    if (errorMessage.includes('pdf')) {
      return [
        'Ensure your file is a valid PDF document',
        'Try a different PDF file or reduce file size',
        'Check if the PDF contains extractable text (not just images)'
      ];
    }
    
    if (errorMessage.includes('api') || errorMessage.includes('key')) {
      return [
        'Check your internet connection',
        'The service might be temporarily unavailable',
        'Try again in a few minutes'
      ];
    }
    
    if (errorMessage.includes('text') || errorMessage.includes('content')) {
      return [
        'Ensure your syllabus contains readable text',
        'Try uploading a different document',
        'Use the text input option instead of file upload'
      ];
    }
    
    return [
      'Check your internet connection',
      'Try refreshing the page',
      'Contact support if the problem persists'
    ];
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-red-50 to-orange-50 p-8">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
        <div className="mx-auto w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-6">
          <AlertCircle className="w-8 h-8 text-red-600" />
        </div>

        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Analysis Failed
        </h2>
        
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800 text-sm">
            {getErrorMessage(error)}
          </p>
        </div>

        <div className="text-left mb-8">
          <h3 className="font-semibold text-gray-900 mb-3">
            💡 Try these solutions:
          </h3>
          <ul className="space-y-2">
            {getErrorSuggestions(error).map((suggestion, index) => (
              <li key={index} className="flex items-start text-sm text-gray-700">
                <span className="flex-shrink-0 w-2 h-2 bg-gray-400 rounded-full mt-2 mr-3"></span>
                {suggestion}
              </li>
            ))}
          </ul>
        </div>

        <div className="space-y-3">
          {onRetry && (
            <button
              onClick={onRetry}
              className="w-full flex items-center justify-center px-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Try Again
            </button>
          )}
          
          <button
            onClick={onHome}
            className="w-full flex items-center justify-center px-4 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
          >
            <Home className="w-4 h-4 mr-2" />
            Start Over
          </button>
        </div>

        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-2">
            Still having trouble?
          </h4>
          <p className="text-sm text-gray-600 mb-3">
            Our analysis works best with:
          </p>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• PDF files with clear, readable text</li>
            <li>• University syllabi in English</li>
            <li>• Files smaller than 10MB</li>
            <li>• Documents with structured course content</li>
          </ul>
        </div>

        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-800">
            <strong>Alternative:</strong> You can also paste your syllabus text 
            directly instead of uploading a PDF file.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Error;