import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import DashboardLayout from "../../layouts/DashboardLayout";

import {
    getPendingReviews
} from "../../services/reviewService";


function ReviewQueue() {

    const navigate = useNavigate();

    const [reviews, setReviews] = useState([]);

    const [loading, setLoading] = useState(true);


    useEffect(() => {

        loadReviews();

    }, []);


    const loadReviews = async () => {

        try {

            const response = await getPendingReviews();

            setReviews(response.data || []);

        } catch (error) {

            console.error(
                "Error loading pending reviews:",
                error
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

                {/* =========================
                    PAGE HEADER
                ========================== */}

                <div className="review-queue-header">

                    <div className="review-title-section">

                        <h1>
                            Pending Reviews
                        </h1>

                        <p>
                            Review AI predictions submitted
                            by patients.
                        </p>

                    </div>


                    {/* Pending Count */}

                    <div className="pending-count">

                        <strong>
                            {reviews.length}
                        </strong>

                        <span>
                            Pending
                        </span>

                    </div>

                </div>


                {/* =========================
                    NO REVIEWS
                ========================== */}

                {reviews.length === 0 ? (

                    <div className="no-reviews">

                        <h2>
                            No Pending Reviews
                        </h2>

                        <p>
                            There are currently no
                            predictions waiting for review.
                        </p>

                    </div>

                ) : (


                    /* =========================
                       REVIEWS TABLE
                    ========================== */

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

                                {reviews.map((item) => (

                                    <tr
                                        key={
                                            item.prediction_id
                                        }
                                    >

                                        {/* Patient */}

                                        <td>

                                            <div className="patient-cell">

                                                <strong>
                                                    {
                                                        item.patient_name
                                                    }
                                                </strong>

                                                <span>
                                                    {
                                                        item.patient_email
                                                    }
                                                </span>

                                            </div>

                                        </td>


                                        {/* Disease */}

                                        <td>

                                            <strong>
                                                {
                                                    item.disease
                                                }
                                            </strong>

                                        </td>


                                        {/* Confidence */}

                                        <td>

                                            <strong>
                                                {
                                                    item.confidence
                                                }%
                                            </strong>

                                        </td>


                                        {/* Status */}

                                        <td>

                                            <span className="status-pending">

                                                Pending

                                            </span>

                                        </td>


                                        {/* Action */}

                                        <td>

                                            <button
                                                className="review-button"
                                                onClick={() =>
                                                    navigate(
                                                        `/doctor/reviews/${item.prediction_id}`
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