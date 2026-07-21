import { useEffect, useState } from "react";
import DashboardLayout from "../../layouts/DashboardLayout";
import { getDashboardStats } from "../../services/dashboardService";

function Dashboard() {

    const [stats, setStats] = useState(null);

    useEffect(() => {

        const loadStats = async () => {

            try {

                const response = await getDashboardStats();

                setStats(response.data);

            } catch (error) {

                console.error(error);

            }

        };

        loadStats();

    }, []);

    if (!stats) {

        return (
            <DashboardLayout>
                <h2>Loading Dashboard...</h2>
            </DashboardLayout>
        );

    }

    return (

        <DashboardLayout>

            <h1>Welcome to MediVision AI</h1>

            <div className="dashboard-cards">

                <div className="card">
                    <h3>Total Uploads</h3>
                    <p>{stats.total_uploads}</p>
                </div>

                <div className="card">
                    <h3>Total Predictions</h3>
                    <p>{stats.total_predictions}</p>
                </div>

                <div className="card">
                    <h3>Last Disease</h3>
                    <p>{stats.last_prediction}</p>
                </div>

                <div className="card">
                    <h3>Avg Confidence</h3>
                    <p>{stats.average_confidence}%</p>
                </div>

            </div>

        </DashboardLayout>

    );

}

export default Dashboard;