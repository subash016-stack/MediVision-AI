import { useEffect, useState } from "react";
import DashboardLayout from "../../layouts/DashboardLayout";
import {
    getProfile,
    updateProfile
} from "../../services/profileService";

function Profile() {

    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    const [fullName, setFullName] = useState("");
    const [phone, setPhone] = useState("");
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        loadProfile();
    }, []);

    const loadProfile = async () => {

        try {

            setLoading(true);

            const response = await getProfile();

            setProfile(response.data);

            setFullName(response.data.full_name);
            setPhone(response.data.phone);

        } catch (error) {

            console.error(error);

            alert("Failed to load profile.");

        } finally {

            setLoading(false);

        }

    };

    const handleSave = async () => {

        try {

            setSaving(true);

            await updateProfile({
                full_name: fullName,
                phone: phone
            });

            alert("Profile updated successfully!");

            await loadProfile();

        } catch (error) {

            console.error(error);

            alert("Failed to update profile.");

        } finally {

            setSaving(false);

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

                    <input
                        className="profile-input profile-name"
                        type="text"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                    />

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

                            <input
                                className="profile-input"
                                type="text"
                                value={phone}
                                onChange={(e) => setPhone(e.target.value)}
                            />
                        </div>

                        <div className="info-row">
                            <strong>Joined</strong>
                            <span>
                                {new Date(profile.created_at).toLocaleDateString()}
                            </span>
                        </div>

                    </div>

                    <button
                        className="save-btn"
                        onClick={handleSave}
                        disabled={saving}
                    >
                        {saving ? "Saving..." : "Save Changes"}
                    </button>

                </div>

            </div>

        </DashboardLayout>

    );

}

export default Profile;