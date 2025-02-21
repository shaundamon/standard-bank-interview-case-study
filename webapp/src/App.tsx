import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Login } from "./pages/Login";
import { Signup } from "./pages/Signup";
import { Home } from "./pages/Home";
import { useAuthStore } from "./store/authStore";
import { Profile } from "./pages/Profile";
import { ModelSettings } from "./pages/ModelSettings";
import { AppSettings } from "./pages/AppSettings";
import { Data } from "./pages/Data";
import { useSettingsStore } from "./store/settingsStore";

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const user = useAuthStore((state) => state.user);
  return user ? <>{children}</> : <Navigate to="/login" />;
}

function App() {
  const { toggleScreenReader } = useSettingsStore();
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Toggle screen reader with Alt + S, shortcut instead of navigating to settings
      if (e.altKey && e.key === "s") {
        toggleScreenReader();
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [toggleScreenReader]);
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Home />
            </PrivateRoute>
          }
        />
        <Route
          path="/data"
          element={
            <PrivateRoute>
              <Data />
            </PrivateRoute>
          }
        />

        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          }
        />
        <Route
          path="/settings/model"
          element={
            <PrivateRoute>
              <ModelSettings />
            </PrivateRoute>
          }
        />
        <Route
          path="/settings/app"
          element={
            <PrivateRoute>
              <AppSettings />
            </PrivateRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
