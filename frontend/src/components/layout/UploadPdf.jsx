import { useState } from "react";
import "./UploadPdf.css";
import { useAuth } from "../../context/AuthContext";
import { uploadPdf } from "../../services/pdfServices";
import { toast } from "react-toastify";
import {ClipLoader} from "react-spinners";
const UploadPdf = ({ onClose }) => {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const  [isLoading, setIsLoading] = useState(false);
  const { setPdfName, setPdfId} = useAuth();
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
    } else {
      alert("Please select a PDF file");
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
    } else {
      toast.error("Please drop a PDF file");
    }
  };

  const handleSubmit = async(e) => {
    e.preventDefault();
    if (file) {
      console.log("File ready for upload:", file.name);
      setIsLoading(true);
      const response = await uploadPdf(file);
      setIsLoading(false);
      if(response.error) {
        toast.error("Some error occured while uploading the pdf");
        return;
      }
      setPdfName(response.filename);
      setPdfId(response.pdf_id);
      toast.success("Pdf file uploaded successfully");
      onClose();
    } else {
      toast.error("Please select a PDF file first");
    }
  };

  return (
    <div className="upload-modal-overlay">
      <div className="upload-modal">
        <button className="close-btn" onClick={onClose}>
          &times;
        </button>
        <h2>Upload PDF</h2>
        <form 
          onSubmit={handleSubmit}
          className={`dropzone ${isDragging ? "dragging" : ""}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="upload-area">
            {file ? (
              <p>Selected file: {file.name}</p>
            ) : (
              <>
                <p>Drag & drop your PDF here or</p>
                <label htmlFor="pdf-upload" className="file-input-label">
                  Browse Files
                </label>
                <input
                  id="pdf-upload"
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileChange}
                  className="file-input"
                />
              </>
            )}
          </div>
          <button type="submit" className="upload-btn" disabled={isLoading}>
            {isLoading ? <ClipLoader/> : "Upload pdf"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default UploadPdf;