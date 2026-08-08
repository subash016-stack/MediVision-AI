import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

function Sidebar() {

    const { user } = useContext(AuthContext);

    return (

        <div className="sidebar">

            <h1>MediVision AI</h1>

            <ul>

                {/* PATIENT */}

                {user?.role === "patient" && (
                    <>

                        <li>
                            <Link to="/dashboard">
                                Dashboard
                            </Link>
                        </li>

                        <li>
                            <Link to="/upload">
                                Upload
                            </Link>
                        </li>

                        <li>
                            <Link to="/history">
                                History
                            </Link>
                        </li>

                        <li>
                            <Link to="/profile">
                                Profile
                            </Link>
                        </li>

                    </>
                )}


                {/* DOCTOR */}

                {user?.role === "doctor" && (
                    <>

                        <li>
                            <Link to="/doctor/dashboard">
                                Dashboard
                            </Link>
                        </li>

                        <li>
                            <Link to="/doctor/reviews">
                                Pending Reviews
                            </Link>
                        </li>

                        <li>
                            <Link to="/profile">
                                Profile
                            </Link>
                        </li>

                    </>
                )}

            </ul>

        </div>

    );

}

export default Sidebar;