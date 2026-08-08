import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";

import Dashboard from "./pages/Dashboard/Dashboard";
import Upload from "./pages/Upload/Upload";
import History from "./pages/History/History";
import Profile from "./pages/Profile/Profile";
import ChangePassword from "./pages/Profile/ChangePassword";

import DoctorDashboard from "./pages/Doctor/DoctorDashboard";
import ReviewQueue from "./pages/Doctor/ReviewQueue";
import ReviewDetails from "./pages/Doctor/ReviewDetails";

import ProtectedRoute from "./routes/ProtectedRoute";


function App() {

    return (

        <Routes>

            {/* =========================
                PUBLIC ROUTES
            ========================== */}

            <Route
                path="/"
                element={<Login />}
            />

            <Route
                path="/register"
                element={<Register />}
            />


            {/* =========================
                PATIENT ROUTES
            ========================== */}

            <Route
                path="/dashboard"
                element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/upload"
                element={
                    <ProtectedRoute>
                        <Upload />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/history"
                element={
                    <ProtectedRoute>
                        <History />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/profile"
                element={
                    <ProtectedRoute>
                        <Profile />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/change-password"
                element={
                    <ProtectedRoute>
                        <ChangePassword />
                    </ProtectedRoute>
                }
            />


            {/* =========================
                DOCTOR ROUTES
            ========================== */}

            <Route
                path="/doctor/dashboard"
                element={
                    <ProtectedRoute>
                        <DoctorDashboard />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/doctor/reviews"
                element={
                    <ProtectedRoute>
                        <ReviewQueue />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/doctor/reviews/:predictionId"
                element={
                    <ProtectedRoute>
                        <ReviewDetails />
                    </ProtectedRoute>
                }
            />

        </Routes>

    );

}

export default App;