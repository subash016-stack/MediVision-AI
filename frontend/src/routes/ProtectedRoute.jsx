import { Navigate, useLocation } from "react-router-dom";

function ProtectedRoute({ children }) {

    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    const location = useLocation();

    // User is not logged in
    if (!token) {
        return <Navigate to="/" replace />;
    }

    // Doctor-only routes
    if (
        location.pathname.startsWith("/doctor") &&
        role !== "doctor"
    ) {
        return <Navigate to="/dashboard" replace />;
    }

    // Patient-only routes
    if (
        (
            location.pathname.startsWith("/dashboard") ||
            location.pathname.startsWith("/upload") ||
            location.pathname.startsWith("/history") ||
            location.pathname.startsWith("/profile") ||
            location.pathname.startsWith("/change-password")
        ) &&
        role !== "patient"
    ) {
        return <Navigate to="/doctor/dashboard" replace />;
    }

    return children;
}

export default ProtectedRoute;