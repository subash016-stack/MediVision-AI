import api from "./api";

export async function getDoctorDashboard() {

    const response = await api.get("/doctor/dashboard");

    return response.data;

}