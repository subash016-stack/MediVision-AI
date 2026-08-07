import DoctorSidebar from "../components/DoctorSidebar";
import Navbar from "../components/Navbar";

function DoctorLayout({ children }) {
    return (
        <div className="dashboard-layout">

            <DoctorSidebar />

            <div className="main-content">

                <Navbar title="Doctor Dashboard" />

                {children}

            </div>

        </div>
    );
}

export default DoctorLayout;