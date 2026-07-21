import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

function DashboardLayout({ children }) {
    return (
        <div className="container">
            <Sidebar />

            <div className="content">
                <Navbar />

                <main className="main-content">
                    {children}
                </main>
            </div>
        </div>
    );
}

export default DashboardLayout;