import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Navbar() {

    const { logout } = useContext(AuthContext);

    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/");
    };

    return (
        <div className="navbar">
            <h3>Patient Dashboard</h3>

            <button onClick={handleLogout}>
                Logout
            </button>
        </div>
    );
}

export default Navbar;