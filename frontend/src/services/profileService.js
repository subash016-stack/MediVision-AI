import api from "./api";

export const getProfile = async () => {

    const response = await api.get("/profile/me");

    return response.data;

};
export const updateProfile = async (data) => {

    const response = await api.put(
        "/profile/update",
        data
    );

    return response.data;
};
export const changePassword = async (data) => {

    const response = await api.put(
        "/profile/change-password",
        data
    );

    return response.data;
};