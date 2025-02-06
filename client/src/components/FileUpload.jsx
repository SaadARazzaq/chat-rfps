

// import { useState } from "react";
// import { Upload, Loader2 } from "lucide-react"; // Import Loader2 for the spinner
// import { Button } from "@/components/ui/button";
// import { Card, CardContent } from "@/components/ui/card";
// import { toast, ToastContainer } from "react-toastify";
// import "react-toastify/dist/ReactToastify.css";

// export function FileUpload() {
//   const [dragActive, setDragActive] = useState(false);
//   const [files, setFiles] = useState([]);
//   const [isLoading, setIsLoading] = useState(false); // Loading state

//   // Allowed file types
//   const allowedTypes = [
//     "application/pdf",
//     "application/msword", // .doc
//     "application/vnd.openxmlformats-officedocument.wordprocessingml.document", // .docx
//   ];
//   const maxSize = 200 * 1024 * 1024; // 200MB

//   const handleDrag = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
//     else if (e.type === "dragleave") setDragActive(false);
//   };

//   const handleDrop = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     setDragActive(false);

//     const droppedFiles = Array.from(e.dataTransfer.files);
//     const validFiles = droppedFiles.filter(
//       (file) => allowedTypes.includes(file.type) && file.size <= maxSize
//     );
//     const invalidFiles = droppedFiles.filter(
//       (file) => !allowedTypes.includes(file.type) || file.size > maxSize
//     );

//     if (invalidFiles.length > 0) {
//       toast.error(
//         `Some files were not accepted. Only PDF, DOC, and DOCX files up to 200MB are allowed.`
//       );
//     }

//     setFiles((prevFiles) => [...prevFiles, ...validFiles]);
//   };

//   const handleFileInput = (e) => {
//     if (e.target.files) {
//       const selectedFiles = Array.from(e.target.files);
//       const validFiles = selectedFiles.filter(
//         (file) => allowedTypes.includes(file.type) && file.size <= maxSize
//       );
//       const invalidFiles = selectedFiles.filter(
//         (file) => !allowedTypes.includes(file.type) || file.size > maxSize
//       );

//       if (invalidFiles.length > 0) {
//         toast.error(
//           `Some files were not accepted. Only PDF, DOC, and DOCX files up to 200MB are allowed.`
//         );
//       }

//       setFiles((prevFiles) => [...prevFiles, ...validFiles]);
//     }
//   };

//   const handleSubmit = async () => {
//     if (files.length === 0) return;

//     setIsLoading(true); // Start loading
//     const formData = new FormData();
//     files.forEach((file) => formData.append("files", file));

//     try {
//       const response = await fetch("http://localhost:8000/upload", {
//         method: "POST",
//         body: formData,
//       });
//       const data = await response.json();
//       toast.success(data.message);
//     } catch (error) {
//       console.error("Error uploading files:", error);
//       toast.error("Error uploading files. Please try again.");
//     } finally {
//       setIsLoading(false); // Stop loading
//     }
//   };

//   return (
//     <div className="w-[40vw] max-w-md">
//       <ToastContainer />
//       <Card className="border-2 border-dashed">
//         <CardContent className="p-4">
//           <div
//             className={`flex flex-col items-center justify-center space-y-4 p-4 text-center ${
//               dragActive ? "bg-muted/50" : ""
//             }`}
//             onDragEnter={handleDrag}
//             onDragLeave={handleDrag}
//             onDragOver={handleDrag}
//             onDrop={handleDrop}
//           >
//             <Upload className="h-8 w-8 text-muted-foreground" />
//             <div className="space-y-2">
//               <p className="text-sm font-medium">Drag & drop files here</p>
//               <p className="text-xs text-muted-foreground">PDF, DOC, DOCX (Max: 200MB)</p>
//             </div>
//             <div className="flex gap-2">
//               <Button variant="outline" onClick={() => document.getElementById("file-input").click()}>
//                 Browse files
//               </Button>
//               <Button
//                 variant="default"
//                 disabled={files.length === 0 || isLoading} // Disable button when loading
//                 onClick={handleSubmit}
//               >
//                 {isLoading ? (
//                   <Loader2 className="h-4 w-4 animate-spin" /> // Show spinner when loading
//                 ) : (
//                   "Submit & Process"
//                 )}
//               </Button>
//             </div>
//             <input
//               id="file-input"
//               type="file"
//               className="hidden"
//               accept=".pdf,.doc,.docx"
//               multiple
//               onChange={handleFileInput}
//             />
//           </div>
//           {files.length > 0 && (
//             <div className="mt-4 space-y-2">
//               <p className="text-sm font-medium">Selected files:</p>
//               {files.map((file, index) => (
//                 <p key={index} className="text-xs text-muted-foreground">
//                   {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
//                 </p>
//               ))}
//             </div>
//           )}
//         </CardContent>
//       </Card>
//     </div>
//   );
// }


// ---------------------------------------------------------------------------------------

//                                     WITH

// Frontend (FileUpload component):

// Add a "Reset Documents" button to clear all uploaded files.

// Add a selection box (cross) next to each document to delete individual files.

// Ensure the state persists across reloads by fetching the document list from the backend.


import { useState, useEffect } from "react";
import { Upload, Loader2, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export function FileUpload() {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch files from the backend on component mount (page load or refresh)
  useEffect(() => {
    fetchUploadedFiles();
  }, []);

  const fetchUploadedFiles = async () => {
    try {
      const response = await fetch("http://localhost:8000/upload");
      const data = await response.json();
      setFiles(data.files || []); // Update the state with the fetched files
    } catch (error) {
      console.error("Error fetching uploaded files:", error);
      toast.error("Failed to fetch uploaded files.");
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
    else if (e.type === "dragleave") setDragActive(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    await handleFileUpload(droppedFiles);
  };

  const handleFileInput = async (e) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      await handleFileUpload(selectedFiles);
    }
  };

  const handleFileUpload = async (files) => {
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      toast.success(data.message);

      // Update the state with the new files from the backend
      setFiles(data.files);
    } catch (error) {
      console.error("Error uploading files:", error);
      toast.error("Error uploading files. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      const response = await fetch("http://localhost:8000/reset", {
        method: "POST",
      });
      const data = await response.json();
      toast.success(data.message);

      // Clear the local state
      setFiles([]);
    } catch (error) {
      console.error("Error resetting files:", error);
      toast.error("Error resetting files. Please try again.");
    }
  };

  const handleDelete = async (filename) => {
    try {
      const response = await fetch(`http://localhost:8000/delete/${filename}`, {
        method: "POST",
      });
      const data = await response.json();
      toast.success(data.message);

      // Update the local state with the remaining files
      setFiles(data.files);
    } catch (error) {
      console.error("Error deleting file:", error);
      toast.error("Error deleting file. Please try again.");
    }
  };

  return (
    <div className="w-[40vw] max-w-md">
      <ToastContainer />
      <Card className="border-2 border-dashed">
        <CardContent className="p-4">
          <div
            className={`flex flex-col items-center justify-center space-y-4 p-4 text-center ${
              dragActive ? "bg-muted/50" : ""
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <Upload className="h-8 w-8 text-muted-foreground" />
            <div className="space-y-2">
              <p className="text-sm font-medium">Drag & drop files here</p>
              <p className="text-xs text-muted-foreground">PDF, DOC, DOCX (Max: 200MB)</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => document.getElementById("file-input").click()}>
                Browse files
              </Button>
              <Button
                variant="default"
                disabled={files.length === 0 || isLoading}
                onClick={handleReset}
              >
                {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Reset Documents"}
              </Button>
            </div>
            <input
              id="file-input"
              type="file"
              className="hidden"
              accept=".pdf,.doc,.docx"
              multiple
              onChange={handleFileInput}
            />
          </div>
          {files.length > 0 && (
            <div className="mt-4 space-y-2">
              <p className="text-sm font-medium">Selected files:</p>
              {files.map((file, index) => (
                <div key={index} className="flex items-center justify-between">
                  <p className="text-xs text-muted-foreground">
                    {file.filename} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                  </p>
                  <Trash2
                    className="h-4 w-4 text-red-500 cursor-pointer"
                    onClick={() => handleDelete(file.filename)}
                  />
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}