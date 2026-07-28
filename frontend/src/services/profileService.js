import api from "./api";

export const getProfile = async () => {

    const response = await api.get("/profile/me");

    return response.data;

};