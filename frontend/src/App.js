import React, { useState } from 'react';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import Loading from './components/Loading';
import Results from './components/Results';
import Error from './components/Error';
import { GraduationCap, Github, Twitter, Mail } from 'lucide-react';

axios.defaults.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
axios.defaults.timeout = 120000;

function App() {
  const [currentState, setCurrentState] = useState('upload');
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);
  const [university, setUniversity] = useState('');
  const [field, setField] = useState('');

  const handleFileUpload = async (formData) => {
    setCurrentState('loading');
    setError(null);

    try {
      const response = await axios.post('/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setAnalysis(response.data);
      setCurrentState('results');
    } catch (err) {
      console.error('Analysis error:', err);
      
      let errorMessage = 'Failed to analyze your syllabus. Please try again.';
      
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      setCurrentState('error');
    }
  };

  const handleRetry = () => {
    setCurrentState('upload');
    setError(null);
  };

  const handleNewAnalysis = () => {
    setCurrentState('upload');
    setAnalysis(null);
    setError(null);
    setUniversity('');
    setField('');
  };

  const renderContent = () => {
    switch (currentState) {
      case 'loading':
        return <Loading />;
      
      case 'results':
        return <Results analysis={analysis} onNewAnalysis={handleNewAnalysis} />;
      
      case 'error':
        return (
          <Error 
            error={error} 
            onRetry={handleRetry} 
            onHome={handleNewAnalysis}
          />
        );
      
      default:
        return (
          <>
            <section className="container mx-auto px-4 py-16">
              <div className="text-center mb-16">
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                  Bridge the Gap Between
                  <br />
                  <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    Education & Industry
                  </span>
                </h1>
                <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
                  Upload your university syllabus and discover exactly which skills you need 
                  to master for your dream career. Our system analyzes your curriculum against 
                  real industry requirements.
                </p>
                
                <div className="grid md:grid-cols-3 gap-8 mt-16 max-w-4xl mx-auto">
                  <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 shadow-lg">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                      <GraduationCap className="w-6 h-6 text-blue-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Smart Analysis</h3>
                    <p className="text-gray-600 text-sm">
                      Automated extraction of skills from your university syllabus
                    </p>
                  </div>
                  
                  <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 shadow-lg">
                    <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                      <GraduationCap className="w-6 h-6 text-purple-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Industry Match</h3>
                    <p className="text-gray-600 text-sm">
                      Compare against real-world job requirements and industry standards
                    </p>
                  </div>
                  
                  <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 shadow-lg">
                    <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                      <GraduationCap className="w-6 h-6 text-green-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Learning Path</h3>
                    <p className="text-gray-600 text-sm">
                      Get personalized recommendations for courses and resources
                    </p>
                  </div>
                </div>
              </div>

              <FileUpload
                onFileUpload={handleFileUpload}
                isLoading={currentState === 'loading'}
                university={university}
                setUniversity={setUniversity}
                field={field}
                setField={setField}
              />
            </section>
          </>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {currentState === 'upload' && (
        <header className="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <GraduationCap className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">
                    Skill Gap Predictor
                  </h1>
                  <p className="text-sm text-gray-600">
                    Career Readiness Analysis Platform
                  </p>
                </div>
              </div>
              
              <nav className="hidden md:flex items-center space-x-6">
                <span className="text-gray-600 hover:text-gray-900 transition-colors cursor-pointer">
                  Features
                </span>
                <span className="text-gray-600 hover:text-gray-900 transition-colors cursor-pointer">
                  How It Works
                </span>
                <span className="text-gray-600 hover:text-gray-900 transition-colors cursor-pointer">
                  About
                </span>
              </nav>
            </div>
          </div>
        </header>
      )}

      <main className="flex-1">
        {renderContent()}
      </main>

      {currentState === 'upload' && (
        <footer className="bg-gray-900 text-white py-12 mt-16">
          <div className="container mx-auto px-4">
            <div className="grid md:grid-cols-4 gap-8">
              <div className="col-span-2">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                    <GraduationCap className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-xl font-bold">Skill Gap Predictor</span>
                </div>
                <p className="text-gray-400 mb-6">
                  Empowering students with data-driven career readiness insights. 
                  Bridge the gap between education and industry requirements.
                </p>
                <div className="flex space-x-4">
                  <span className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                    <Github className="w-5 h-5" />
                  </span>
                  <span className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                    <Twitter className="w-5 h-5" />
                  </span>
                  <span className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                    <Mail className="w-5 h-5" />
                  </span>
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold mb-4">Features</h4>
                <ul className="space-y-2 text-gray-400">
                  <li>PDF Analysis</li>
                  <li>Skill Extraction</li>
                  <li>Industry Comparison</li>
                  <li>Learning Recommendations</li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold mb-4">Supported Fields</h4>
                <ul className="space-y-2 text-gray-400">
                  <li>Computer Science</li>
                  <li>Engineering</li>
                  <li>Information Technology</li>
                  <li>Electronics</li>
                  <li>Data Science</li>
                  <li>Machine Learning</li>
                </ul>
              </div>
            </div>
            
            <div className="border-t border-gray-800 pt-8 mt-8 text-center text-gray-400">
              <p>&copy; Skill Gap Predictor.</p>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
}

export default App;