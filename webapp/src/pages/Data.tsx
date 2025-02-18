import React, { useState, useEffect } from "react";
import { Database, Download, FolderOpen } from "lucide-react";
import { datasetApi } from "../lib/api";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";
import { Layout } from "../components/Layout";


export const Data: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<{
    exists: boolean;
    image_count: number;
    data_path: string;
  } | null>(null);
  const { speak } = useSpeechSynthesis();

  const checkStatus = async () => {
    try {
      const status = await datasetApi.getDatasetStatus();
      setStatus(status);
      setError(null);
      speak(
        `Dataset status: ${
          status.exists
            ? "Downloaded with " + status.image_count + " images"
            : "Not downloaded"
        }`
      );
    } catch (error) {
      setError("Failed to check dataset status");
      speak("Failed to check dataset status");
      console.error("Error checking dataset status:", error);
    }
  };

  const handleDownload = async () => {
    setLoading(true);
    setError(null);
    speak("Starting dataset download");
    try {
      const eventSource = await datasetApi.downloadDataset();

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.error) {
          setError(data.error);
          speak("Download failed: " + data.error);
          eventSource.close();
          setLoading(false);
        } else if (data.status === "completed") {
          eventSource.close();
          checkStatus();
          speak("Dataset download completed successfully");
          setLoading(false);
        }
      };

      eventSource.onerror = () => {
        setError("Download failed");
        speak("Download failed");
        eventSource.close();
        setLoading(false);
      };
    } catch (error) {
      setError("Failed to start download");
      speak("Failed to start download");
      console.error("Error downloading dataset:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

 return (
   <Layout title="Dataset Management">
     <div
       className="max-w-6xl mx-auto"
       role="main"
       aria-label="Dataset Management Page"
     >
       <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
         <div className="flex items-center mb-6" role="banner">
           <Database
             className="h-8 w-8 text-indigo-600 dark:text-indigo-400 mr-3"
             aria-hidden="true"
           />
           <h1
             className="text-2xl font-bold text-gray-900 dark:text-white"
             tabIndex={0}
           >
             Dataset Management
           </h1>
         </div>

         {error && (
           <div
             className="mb-4 p-4 bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-400 rounded-lg"
             role="alert"
             aria-live="polite"
           >
             {error}
           </div>
         )}

         <div className="space-y-6">
           <div
             className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
             role="region"
             aria-label="Dataset Location"
           >
             <div className="flex items-center space-x-2">
               <FolderOpen
                 className="h-5 w-5 text-gray-600 dark:text-gray-300"
                 aria-hidden="true"
               />
               <span
                 className="text-sm text-gray-600 dark:text-gray-300"
                 tabIndex={0}
                 aria-label={`Dataset location: ${
                   status?.data_path || "No dataset location"
                 }`}
               >
                 {status?.data_path || "No dataset location"}
               </span>
             </div>
           </div>

           <div
             className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4"
             role="region"
             aria-label="Dataset Status"
           >
             <div className="flex justify-between mb-2">
               <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                 Status
               </span>
               <span
                 className="text-sm text-gray-600 dark:text-gray-400"
                 aria-live="polite"
               >
                 {status?.exists ? "Downloaded" : "Not Downloaded"}
               </span>
             </div>
             {status?.exists && (
               <div className="flex justify-between">
                 <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                   Images
                 </span>
                 <span
                   className="text-sm text-gray-600 dark:text-gray-400"
                   aria-live="polite"
                 >
                   {status.image_count} images available
                 </span>
               </div>
             )}
           </div>

           <button
             onClick={handleDownload}
             disabled={loading}
             className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
             aria-busy={loading}
             aria-label={
               loading
                 ? "Downloading dataset"
                 : status?.exists
                 ? "Refresh Dataset"
                 : "Download Dataset"
             }
           >
             {loading ? (
               <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
             ) : (
               <>
                 <Download className="h-5 w-5 mr-2" />
                 {status?.exists ? "Refresh Dataset" : "Download Dataset"}
               </>
             )}
           </button>
         </div>
       </div>
     </div>
   </Layout>
 );
};
