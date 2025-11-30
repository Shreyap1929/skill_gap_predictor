import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, AlertCircle } from 'lucide-react';

const FileUpload = ({ onFileUpload, isLoading, university, setUniversity, field, setField }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [textContent, setTextContent] = useState('');
  const [uploadMode, setUploadMode] = useState('file'); 
  const [errors, setErrors] = useState({});

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      setErrors({ file: 'Please upload only PDF files' });
      return;
    }

    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      setErrors({});
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const removeFile = () => {
    setUploadedFile(null);
    setErrors({});
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!university.trim()) {
      newErrors.university = 'University name is required';
    }
    
    if (!field.trim()) {
      newErrors.field = 'Field of study is required';
    }
    
    if (uploadMode === 'file' && !uploadedFile) {
      newErrors.file = 'Please upload a PDF file';
    }
    
    if (uploadMode === 'text' && !textContent.trim()) {
      newErrors.text = 'Please enter syllabus content';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const formData = new FormData();
    formData.append('university', university);
    formData.append('field', field);
    
    if (uploadMode === 'file' && uploadedFile) {
      formData.append('file', uploadedFile);
    } else if (uploadMode === 'text' && textContent) {
      formData.append('text_content', textContent);
    }
    
    onFileUpload(formData);
  };

  const availableFields = [
    'Engineering',
    'Computer Science',
    'Information Technology',
    'Electronics',
    'Artificial Intelligence and Data Science',
    'Artificial Intelligence and Machine Learning'
  ];

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-4">
          <Upload className="w-8 h-8 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Upload Your University Syllabus
        </h2>
        <p className="text-gray-600">
          Analyze your curriculum and discover skill gaps for your career
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* University Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            University Name *
          </label>
          <input
            type="text"
            value={university}
            onChange={(e) => setUniversity(e.target.value)}
            placeholder="e.g., Mumbai University"
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.university ? 'border-red-500' : 'border-gray-300'
            }`}
          />
          {errors.university && (
            <p className="mt-1 text-sm text-red-600 flex items-center">
              <AlertCircle className="w-4 h-4 mr-1" />
              {errors.university}
            </p>
          )}
        </div>

        {/* Field Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Field of Study *
          </label>
          <select
            value={field}
            onChange={(e) => setField(e.target.value)}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.field ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            <option value="">Select your field of study</option>
            {availableFields.map(fieldOption => (
              <option key={fieldOption} value={fieldOption}>
                {fieldOption}
              </option>
            ))}
          </select>
          {errors.field && (
            <p className="mt-1 text-sm text-red-600 flex items-center">
              <AlertCircle className="w-4 h-4 mr-1" />
              {errors.field}
            </p>
          )}
        </div>

        {/* Upload Mode Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            How would you like to provide your syllabus?
          </label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                value="file"
                checked={uploadMode === 'file'}
                onChange={(e) => {
                  setUploadMode(e.target.value);
                  setTextContent('');
                  setErrors({});
                }}
                className="mr-2 text-blue-600"
              />
              <span className="text-sm text-gray-700">Upload PDF File</span>
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                value="text"
                checked={uploadMode === 'text'}
                onChange={(e) => {
                  setUploadMode(e.target.value);
                  setUploadedFile(null);
                  setErrors({});
                }}
                className="mr-2 text-blue-600"
              />
              <span className="text-sm text-gray-700">Paste Text Content</span>
            </label>
          </div>
        </div>

        {/* File Upload Section */}
        {uploadMode === 'file' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Syllabus Document *
            </label>
            {!uploadedFile ? (
              <div
                {...getRootProps()}
                className={`upload-dropzone p-8 text-center cursor-pointer rounded-lg transition-colors ${
                  isDragActive ? 'dragover' : ''
                } ${errors.file ? 'border-red-500' : 'border-gray-300'}`}
              >
                <input {...getInputProps()} />
                <FileText className="mx-auto w-12 h-12 text-gray-400 mb-4" />
                {isDragActive ? (
                  <p className="text-blue-600 font-medium">
                    Drop the PDF file here...
                  </p>
                ) : (
                  <>
                    <p className="text-gray-600 font-medium mb-2">
                      Drag and drop your PDF file here, or{' '}
                      <span className="text-blue-600">browse</span>
                    </p>
                    <p className="text-sm text-gray-500">
                      PDF files up to 10MB are supported
                    </p>
                  </>
                )}
              </div>
            ) : (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <FileText className="w-8 h-8 text-red-600 mr-3" />
                    <div>
                      <p className="font-medium text-gray-900">{uploadedFile.name}</p>
                      <p className="text-sm text-gray-500">
                        {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={removeFile}
                    className="text-gray-400 hover:text-red-600 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>
            )}
            {errors.file && (
              <p className="mt-2 text-sm text-red-600 flex items-center">
                <AlertCircle className="w-4 h-4 mr-1" />
                {errors.file}
              </p>
            )}
          </div>
        )}

        {/* Text Input Section */}
        {uploadMode === 'text' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Syllabus Content *
            </label>
            <textarea
              value={textContent}
              onChange={(e) => setTextContent(e.target.value)}
              placeholder="Paste your syllabus content here..."
              rows={8}
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
                errors.text ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.text && (
              <p className="mt-2 text-sm text-red-600 flex items-center">
                <AlertCircle className="w-4 h-4 mr-1" />
                {errors.text}
              </p>
            )}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-4 px-6 rounded-lg font-medium transition-all duration-200 ${
            isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-105'
          } text-white`}
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="spinner w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-3"></div>
              Analyzing Your Syllabus...
            </div>
          ) : (
            'Analyze Skill Gaps'
          )}
        </button>
      </form>
    </div>
  );
};

export default FileUpload;
