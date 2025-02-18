import React from "react";
import { Sliders, Thermometer } from "lucide-react";
import { useSettingsStore } from "../store/settingsStore";
import { Layout } from "../components/Layout";
import { toast } from "react-hot-toast";


export const ModelSettings: React.FC = () => {
  const { modelTemperature, setModelTemperature } = useSettingsStore();
  const [tempValue, setTempValue] = React.useState(modelTemperature);
  const [isSaving, setIsSaving] = React.useState(false);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Only update if value has changed
      if (tempValue !== modelTemperature) {
        setModelTemperature(tempValue);
        toast.success("Temperature settings saved successfully!");
      }
    } catch (error) {
      console.error(error);
      toast.error("Failed to save temperature settings");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Layout title="Model Settings">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="flex items-center space-x-4 mb-6">
            <Sliders className="w-12 h-12 text-indigo-600 dark:text-indigo-400" />
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Model Settings
            </h1>
          </div>

          <div className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Thermometer className="w-5 h-5 text-gray-500 dark:text-gray-400" />
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Model Temperature
                  </label>
                </div>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {tempValue.toFixed(1)}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={tempValue}
                onChange={(e) => setTempValue(parseFloat(e.target.value))}
                className="w-fulla"
              />
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Adjust the creativity level of the model. Higher values make the
                output more diverse but potentially less focused.
              </p>
              <button
                onClick={handleSave}
                disabled={isSaving || tempValue === modelTemperature}
                className={`mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2 ${
                  (isSaving || tempValue === modelTemperature) ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {/* <Sliders className="w-4 h-4" /> */}
                {isSaving ? 'Saving...' : 'Save'}
              </button>
            </div>

          </div>
        </div>
      </div>
    </Layout>
  );
};
