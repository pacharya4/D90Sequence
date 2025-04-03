import React from 'react';

// Use forwardRef to handle refs correctly
const FileUploader = React.forwardRef(({ onFileSelect }, ref) => {
  return (
    <input
      type="file"
      onChange={(event) => onFileSelect(event.target.files[0])}
      style={{ display: 'none' }} // Keep this hidden
      ref={ref} // Attach the ref here
    />
  );
});

export default FileUploader;
