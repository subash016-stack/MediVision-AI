import { useState } from "react";
import DashboardLayout from "../../layouts/DashboardLayout";
import { changePassword } from "../../services/profileService";


function ChangePassword() {

    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {

        e.preventDefault();

        if (!currentPassword || !newPassword || !confirmPassword) {
            return alert("Please fill all fields.");
        }

        if (newPassword.length < 8) {
            return alert("Password must be at least 8 characters.");
        }

        if (newPassword !== confirmPassword) {
            return alert("Passwords do not match.");
        }

        try {

            setLoading(true);

            const response = await changePassword({
                current_password: currentPassword,
                new_password: newPassword
            });

            alert(response.message);

            setCurrentPassword("");
            setNewPassword("");
            setConfirmPassword("");

        } catch (error) {

            alert(
                error.response?.data?.message ||
                "Unable to change password."
            );

        } finally {

            setLoading(false);

        }

    };

    return (

        <DashboardLayout>

            <div className="change-password-container">

                <div className="change-password-card">

                    <h2>Change Password</h2>

                    <form onSubmit={handleSubmit}>

                        <label>Current Password</label>

                        <input
                            type="password"
                            value={currentPassword}
                            onChange={(e) =>
                                setCurrentPassword(e.target.value)
                            }
                        />

                        <label>New Password</label>

                        <input
                            type="password"
                            value={newPassword}
                            onChange={(e) =>
                                setNewPassword(e.target.value)
                            }
                        />

                        <label>Confirm Password</label>

                        <input
                            type="password"
                            value={confirmPassword}
                            onChange={(e) =>
                                setConfirmPassword(e.target.value)
                            }
                        />

                        <button
                            type="submit"
                            disabled={loading}
                        >
                            {
                                loading
                                    ? "Changing..."
                                    : "Change Password"
                            }
                        </button>

                    </form>

                </div>

            </div>

        </DashboardLayout>

    );

}

export default ChangePassword;