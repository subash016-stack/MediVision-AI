import api from "./api";

// Get all predictions
export const getPredictionHistory = async () => {

    const response = await api.get("/prediction/history");

    return response.data;

};

// Delete prediction
export const deletePrediction = async (predictionId) => {

    const response = await api.delete(
        `/prediction/${predictionId}`
    );

    return response.data;

};

// Get single prediction details
export const getPredictionDetails = async (predictionId) => {

    const response = await api.get(
        `/prediction/details/${predictionId}`
    );

    return response.data;

};