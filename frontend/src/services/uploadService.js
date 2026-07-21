import api from "./api";

export const uploadXray = async (file) => {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/upload/xray",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }
    );

    return response.data;
};

export const predictDisease = async (imageId) => {

    const response = await api.post(
        `/prediction/${imageId}`
    );

    return response.data;
};