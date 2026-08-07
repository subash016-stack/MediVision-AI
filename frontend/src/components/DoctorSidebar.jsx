import { Link } from "react-router-dom";

function DoctorSidebar() {
    return (
        <aside className="sidebar">
            <h2>MediVision AI</h2>

            <Link to="/doctor/dashboard">Dashboard</Link>
            <Link to="/doctor/patients">Patients</Link>
            <Link to="/doctor/reviews">AI Reviews</Link>
            <Link to="/profile">Profile</Link>
        </aside>
    );
}

export default DoctorSidebar;