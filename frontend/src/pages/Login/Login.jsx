import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login as loginAPI } from "../../services/authService";
import { AuthContext } from "../../context/AuthContext";

function Login() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const navigate = useNavigate();

    const { login } = useContext(AuthContext);

    const handleLogin = async () => {

    try {
        console.log("Email:", JSON.stringify(email));
        console.log("Password:", JSON.stringify(password));
        const response = await loginAPI({
            email,
            password
        });

        console.log("Response:", response);

        login(
            response.data.access_token,
            response.data.user
        );

        console.log("Token saved:",
            localStorage.getItem("token")
        );

        navigate("/dashboard");

    } catch (error) {

        console.error(error);

    }

}

    return (

        <div className="login-page">

            <div className="login-card">

                <h1>MediVision AI</h1>

                <p>Chest X-ray Disease Detection</p>

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e)=>setEmail(e.target.value)}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e)=>setPassword(e.target.value)}
                />

                <button onClick={handleLogin}>
                    Login
                </button>

                <p className="register-text">

                    Don't have an account?

                    <Link to="/register">

                        Register

                    </Link>

                </p>

            </div>

        </div>

    );

}

export default Login;