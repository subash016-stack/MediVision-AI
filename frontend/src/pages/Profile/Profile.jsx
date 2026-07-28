import { useEffect, useState } from "react";
import DashboardLayout from "../../layouts/DashboardLayout";
import { getProfile } from "../../services/profileService";

function Profile() {

    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        loadProfile();

    }, []);

    const loadProfile = async () => {

        try {

            const response = await getProfile();

            setProfile(response.data);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }

    };

    if (loading) {

        return (

            <DashboardLayout>

                <h2>Loading Profile...</h2>

            </DashboardLayout>

        );

    }

    return (

        <DashboardLayout>

            <div className="profile-container">

                <div className="profile-card">

                    <div className="profile-avatar">

                        👤

                    </div>

                    <h2>{profile.full_name}</h2>

                    <p>{profile.role.toUpperCase()}</p>

                    <div className="profile-info">

                        <div className="info-row">
                            <strong>User ID</strong>
                            <span>{profile.user_id}</span>
                        </div>

                        <div className="info-row">
                            <strong>Email</strong>
                            <span>{profile.email}</span>
                        </div>

                        <div className="info-row">
                            <strong>Phone</strong>
                            <span>{profile.phone}</span>
                        </div>

                        <div className="info-row">
                            <strong>Joined</strong>
                            <span>
                                {new Date(profile.created_at).toLocaleDateString()}
                            </span>
                        </div>

                    </div>

                </div>

            </div>

        </DashboardLayout>

    );

}

export default Profile;