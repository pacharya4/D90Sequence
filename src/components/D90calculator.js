import React, { useState, useRef } from 'react';

function D90Calculator() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [d90Value, setD90Value] = useState('');
  const [showDropZone, setShowDropZone] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setFileName(droppedFile.name);
      setShowDropZone(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleFileSelect = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setFileName(selected.name);
      setShowDropZone(false);
    }
  };

  const handleCalculateD90 = async () => {
    if (!file) {
      alert('Please upload a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/uploadfile/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const result = await response.json();
      setD90Value(result.D90.toFixed(2));
    } catch (error) {
      console.error('Error calculating D90:', error);
      alert('Something went wrong');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white px-4">
      

      {/* Upload File Button */}
      <button
        onClick={() => {
          setShowDropZone(true);
          fileInputRef.current.click(); // Optional: open file dialog immediately
        }}
        className="mb-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-lg"
      >
        Upload File
      </button>

      {/* Hidden File Input */}
      <input
        type="file"
        ref={fileInputRef}
        accept=".txt"
        style={{ display: 'none' }}
        onChange={handleFileSelect}
      />

      {/* Drop Zone shown conditionally */}
      {showDropZone && (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className="w-full max-w-md border-4 border-dashed border-gray-500 rounded-lg p-8 text-center text-gray-400 cursor-pointer hover:border-white transition mb-4"
          onClick={() => fileInputRef.current.click()}
        >
          Drag and drop your .txt file here, or click to browse
        </div>
      )}

      {/* Show selected file */}
      {fileName && <p className="text-white mb-4">📄 Selected File: {fileName}</p>}

      {/* Calculate Button */}
      <button
        onClick={handleCalculateD90}
        className="mt-2 px-6 py-2 bg-green-600 hover:bg-green-700 rounded text-white text-lg"
      >
        Calculate D90
      </button>

      {/* D90 Output */}
      {d90Value && (
        <div className="mt-6 text-2xl">
          <strong>D90 Value:</strong> {d90Value}
        </div>
      )}
    </div>
  );
}

export default D90Calculator;
