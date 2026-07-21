import { createContext, useState } from "react";

export const AuthContext=createContext();

function AuthProvider({children}){

    const [token, setToken] = useState(localStorage.getItem("token"));

    const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("user"))
);

    const login = (jwt, userData) => {

    localStorage.setItem("token", jwt);

    localStorage.setItem(
        "user",
        JSON.stringify(userData)
    );

    setToken(jwt);

    setUser(userData);

};

    const logout = () => {

    localStorage.removeItem("token");

    localStorage.removeItem("user");

    setToken(null);

    setUser(null);

};

    return(

        <AuthContext.Provider
    value={{
        token,
        user,
        login,
        logout
    }}
>

            {children}

        </AuthContext.Provider>

    );

}

export default AuthProvider;