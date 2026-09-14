import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import DashboardLayout from "../../layouts/DashboardLayout";

import { getPendingReviews } from "../../services/reviewService";


function ReviewQueue() {

    const navigate = useNavigate();

    const [reviews, setReviews] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    useEffect(() => {

        loadReviews();

    }, []);


    const loadReviews = async () => {

        try {

            setLoading(true);

            setError("");

            const response =
                await getPendingReviews();

            setReviews(response.data || []);

        } catch (error) {

            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Failed to load pending reviews."
            );

        } finally {

            setLoading(false);

        }

    };


    if (loading) {

        return (

            <DashboardLayout>

                <div className="review-loading">

                    <h2>
                        Loading reviews...
                    </h2>

                </div>

            </DashboardLayout>

        );

    }


    return (

        <DashboardLayout>

            <div className="review-queue-page">


                {/* Header */}

                <div className="review-queue-header">

                    <div>

                        <h1>
                            Pending Reviews
                        </h1>

                        <p>
                            Review AI predictions submitted by patients.
                        </p>

                    </div>


                    <div className="pending-count">

                        <strong>
                            {reviews.length}
                        </strong>

                        <span>
                            Pending
                        </span>

                    </div>

                </div>


                {/* Error */}

                {error && (

                    <div className="review-error-message">

                        {error}

                    </div>

                )}


                {/* No Reviews */}

                {reviews.length === 0 ? (

                    <div className="no-reviews">

                        <h2>
                            No Pending Reviews
                        </h2>

                        <p>
                            There are currently no predictions
                            waiting for review.
                        </p>

                    </div>

                ) : (

                    <div className="reviews-table-container">

                        <table className="reviews-table">

                            <thead>

                                <tr>

                                    <th>
                                        Patient
                                    </th>

                                    <th>
                                        Disease
                                    </th>

                                    <th>
                                        Confidence
                                    </th>

                                    <th>
                                        Status
                                    </th>

                                    <th>
                                        Action
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {reviews.map((review) => (

                                    <tr
                                        key={review.prediction_id}
                                    >

                                        <td>

                                            <div className="patient-cell">

                                                <strong>
                                                    {review.patient_name}
                                                </strong>

                                                <span>
                                                    {review.patient_email}
                                                </span>

                                            </div>

                                        </td>


                                        <td>

                                            <strong>
                                                {review.disease}
                                            </strong>

                                        </td>


                                        <td>

                                            <strong>
                                                {review.confidence}%
                                            </strong>

                                        </td>


                                        <td>

                                            <span className="status-badge">

                                                {review.doctor_status ||
                                                    "Pending"}

                                            </span>

                                        </td>


                                        <td>

                                            <button
                                                className="review-button"
                                                onClick={() =>
                                                    navigate(
                                                        `/doctor/reviews/${review.prediction_id}`
                                                    )
                                                }
                                            >
                                                Review
                                            </button>

                                        </td>

                                    </tr>

                                ))}

                            </tbody>

                        </table>

                    </div>

                )}

            </div>

        </DashboardLayout>

    );

}


export default ReviewQueue;