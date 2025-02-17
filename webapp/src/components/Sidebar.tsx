import React from 'react';
import { Settings, User, VolumeIcon, Sliders, Menu } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { useSettingsStore } from '../store/settingsStore';
import { motion, AnimatePresence } from 'framer-motion';

export const Sidebar: React.FC = () => {
  const location = useLocation();
  const { 
    isScreenReaderEnabled, 
    toggleScreenReader,
    isSidebarOpen,
    toggleSidebar 
  } = useSettingsStore();

  const menuItems = [
    { icon: User, label: 'Profile', path: '/profile' },
    { icon: Sliders, label: 'Model Settings', path: '/settings/model' },
    { icon: Settings, label: 'App Settings', path: '/settings/app' },
  ];

  return (
    <>
      <button
        onClick={toggleSidebar}
        className="fixed top-4 left-4 z-50 p-2 rounded-lg bg-white dark:bg-gray-800 shadow-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        aria-label={isSidebarOpen ? 'Close sidebar' : 'Open sidebar'}
      >
        <Menu className="w-5 h-5 text-gray-700 dark:text-gray-200" />
      </button>

      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div
            initial={{ x: -320 }}
            animate={{ x: 0 }}
            exit={{ x: -320 }}
            transition={{ type: "spring", bounce: 0, duration: 0.4 }}
            className="fixed left-0 top-0 h-screen w-64 bg-white dark:bg-gray-800 shadow-lg"
          >
            <div className="p-4 mt-14">
              <button
                onClick={toggleScreenReader}
                className="w-full flex items-center p-3 rounded-lg text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors mb-4"
                aria-label={isScreenReaderEnabled ? 'Disable screen reader' : 'Enable screen reader'}
              >
                <VolumeIcon className={`w-5 h-5 mr-3 ${isScreenReaderEnabled ? 'text-indigo-500' : ''}`} />
                <span>Screen Reader {isScreenReaderEnabled ? 'On' : 'Off'}</span>
              </button>

              <nav className="space-y-2">
                {menuItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = location.pathname === item.path;
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`flex items-center p-3 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-indigo-50 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400'
                          : 'text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'
                      }`}
                    >
                      <Icon className="w-5 h-5 mr-3" />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </nav>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};