import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface SettingsState {
  isScreenReaderEnabled: boolean;
  modelTemperature: number;
  isSidebarOpen: boolean;
  toggleScreenReader: () => void;
  setModelTemperature: (temp: number) => void;
  toggleSidebar: () => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      isScreenReaderEnabled: false,
      modelTemperature: 0.7,
      isSidebarOpen: true,
      toggleScreenReader: () =>
        set((state) => ({ isScreenReaderEnabled: !state.isScreenReaderEnabled })),
      setModelTemperature: (temp) => set({ modelTemperature: temp }),
      toggleSidebar: () =>
        set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
    }),
    {
      name: 'settings-storage',
    }
  )
);