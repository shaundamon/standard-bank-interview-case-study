import React from "react";
import { Settings, Volume2, PanelLeftClose } from "lucide-react";
import { useSettingsStore } from "../store/settingsStore";
import { Layout } from "../components/Layout";


export const AppSettings: React.FC = () => {
  const {
    isScreenReaderEnabled,
    toggleScreenReader,
    isSidebarOpen,
    toggleSidebar,
  } = useSettingsStore();

  return (
    <Layout title="App Settings">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="flex items-center space-x-4 mb-6">
            <Settings className="w-12 h-12 text-indigo-600 dark:text-indigo-400" />
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              App Settings
            </h1>
          </div>

          <div className="space-y-6">
            <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div className="flex items-center space-x-3">
                <Volume2 className="w-6 h-6 text-gray-500 dark:text-gray-400" />
                <div>
                  <h3 className="font-medium text-gray-900 dark:text-white">
                    Screen Reader
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Enable voice feedback for search results
                  </p>
                </div>
              </div>
              <button
                onClick={toggleScreenReader}
                className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                  isScreenReaderEnabled
                    ? "bg-indigo-600"
                    : "bg-gray-200 dark:bg-gray-600"
                }`}
              >
                <span className="sr-only">Toggle screen reader</span>
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                    isScreenReaderEnabled ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div className="flex items-center space-x-3">
                <PanelLeftClose className="w-6 h-6 text-gray-500 dark:text-gray-400" />
                <div>
                  <h3 className="font-medium text-gray-900 dark:text-white">
                    Sidebar Default
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Keep sidebar open by default
                  </p>
                </div>
              </div>
              <button
                onClick={toggleSidebar}
                className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                  isSidebarOpen
                    ? "bg-indigo-600"
                    : "bg-gray-200 dark:bg-gray-600"
                }`}
              >
                <span className="sr-only">Toggle sidebar default</span>
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                    isSidebarOpen ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};
