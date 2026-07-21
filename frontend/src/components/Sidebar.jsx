import { Link } from "react-router-dom";

function Sidebar() {
    return (
        <div className="sidebar">
            <h2>MediVision AI</h2>

            <ul>
                <li><Link to="/dashboard">Dashboard</Link></li>
                <li><Link to="/upload">Upload</Link></li>
                <li><Link to="/history">History</Link></li>
                <li><Link to="/profile">Profile</Link></li>
            </ul>
        </div>
    );
}

export default Sidebar;