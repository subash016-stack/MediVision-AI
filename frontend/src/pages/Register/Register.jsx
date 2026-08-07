import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../../services/authService";

function Register() {

    const navigate = useNavigate();

    const [formData, setFormData] = useState({

        full_name: "",
        email: "",
        phone: "",
        password: "",
        role: "patient"

    });

    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {

        setFormData({

            ...formData,

            [e.target.name]: e.target.value

        });

    };

    const handleRegister = async () => {

        try {

            setLoading(true);

            const response = await register(formData);

            alert(response.message);

            navigate("/");

        } catch (error) {

            console.error(error);

            alert(
                error.response?.data?.message ||
                "Registration Failed"
            );

        } finally {

            setLoading(false);

        }

    };

    return (

        <div className="register-page">

            <div className="register-card">

                <h1>Create Account</h1>

                <p>MediVision AI</p>

                <input
                    name="full_name"
                    placeholder="Full Name"
                    value={formData.full_name}
                    onChange={handleChange}
                />

                <input
                    name="email"
                    type="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                />

                <input
                    name="phone"
                    placeholder="Phone Number"
                    value={formData.phone}
                    onChange={handleChange}
                />

                <input
                    name="password"
                    type="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                />

                <select
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                >

                    <option value="patient">
                        Patient
                    </option>

                    <option value="doctor">
                        Doctor
                    </option>

                </select>

                <button
                    onClick={handleRegister}
                    disabled={loading}
                >

                    {

                        loading

                            ? "Registering..."

                            : "Register"

                    }

                </button>

                <p className="register-text">

                    Already have an account?

                    <Link to="/">

                        Login

                    </Link>

                </p>

            </div>

        </div>

    );

}

export default Register;