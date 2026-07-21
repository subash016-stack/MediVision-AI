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