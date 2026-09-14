import api from "./api";


export async function getPendingReviews() {
    const response = await api.get("/review/pending");
    return response.data;
}


export async function getPredictionForReview(predictionId) {
    const response = await api.get(`/review/${predictionId}`);
    return response.data;
}

export const getPredictionDetails = getPredictionForReview;


export async function submitReview(predictionId, reviewData) {
    const payload = typeof reviewData === "string" 
        ? { doctor_comments: reviewData }
        : reviewData;

    const response = await api.put(
        `/review/${predictionId}`,
        payload
    );

    return response.data;
}