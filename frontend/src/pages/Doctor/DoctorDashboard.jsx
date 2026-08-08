import { useEffect, useState, useContext } from "react";

import DashboardLayout from "../../layouts/DashboardLayout";

import { AuthContext } from "../../context/AuthContext";

import { getDoctorDashboard } from "../../services/doctorService";

function DoctorDashboard() {

    const { user } = useContext(AuthContext);

    const [dashboard, setDashboard] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    useEffect(() => {

        loadDashboard();

    }, []);

    const loadDashboard = async () => {

        try {

            console.log("Loading doctor dashboard...");

            const response = await getDoctorDashboard();

            console.log("Doctor dashboard response:", response);

            if (response.success) {

                setDashboard(response.data);

            } else {

                setError(
                    response.message || "Unable to load dashboard."
                );

            }

        } catch (error) {

            console.error(
                "Doctor dashboard error:",
                error
            );

            setError(
                error.response?.data?.message ||
                "Unable to load doctor dashboard."
            );

        } finally {

            setLoading(false);

        }

    };

    if (loading) {

        return (

            <DashboardLayout>

                <div className="doctor-dashboard">

                    <h2>
                        Loading Dashboard...
                    </h2>

                </div>

            </DashboardLayout>

        );

    }

    if (error) {

        return (

            <DashboardLayout>

                <div className="doctor-dashboard">

                    <h2>
                        Unable to load dashboard
                    </h2>

                    <p>
                        {error}
                    </p>

                </div>

            </DashboardLayout>

        );

    }

    return (

        <DashboardLayout>

            <div className="doctor-dashboard">

                <div className="doctor-header">

                    <h1>
                        Welcome, Dr. {user?.full_name}
                    </h1>

                    <p>
                        Here is an overview of today's review activities.
                    </p>

                </div>


                <div className="doctor-stats">


                    <div className="stat-card">

                        <h3>
                            Total Patients
                        </h3>

                        <h2>
                            {dashboard?.stats?.total_patients ?? 0}
                        </h2>

                    </div>


                    <div className="stat-card">

                        <h3>
                            Total Predictions
                        </h3>

                        <h2>
                            {dashboard?.stats?.total_predictions ?? 0}
                        </h2>

                    </div>


                    <div className="stat-card">

                        <h3>
                            Pending Reviews
                        </h3>

                        <h2>
                            {dashboard?.stats?.pending_reviews ?? 0}
                        </h2>

                    </div>


                    <div className="stat-card">

                        <h3>
                            Completed Reviews
                        </h3>

                        <h2>
                            {dashboard?.stats?.completed_reviews ?? 0}
                        </h2>

                    </div>


                </div>

            </div>

        </DashboardLayout>

    );

}

export default DoctorDashboard;