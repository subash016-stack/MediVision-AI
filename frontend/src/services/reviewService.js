import api from "./api";


/*
    Get all pending predictions
*/

export async function getPendingReviews() {

    const response =
        await api.get("/review/pending");

    return response.data;

}


/*
    Get details of one prediction
*/

export async function getPredictionDetails(
    predictionId
) {

    const response =
        await api.get(
            `/review/${predictionId}`
        );

    return response.data;

}


/*
    Submit doctor's review
*/

export async function submitReview(
    predictionId,
    doctorComments
) {

    const response =
        await api.put(
            `/review/${predictionId}`,
            {
                doctor_comments: doctorComments
            }
        );

    return response.data;

}