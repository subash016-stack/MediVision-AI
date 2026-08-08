import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import DashboardLayout from "../../layouts/DashboardLayout";
import {
    getPredictionDetails,
    submitReview
} from "../../services/reviewService";

function ReviewDetails() {

    const { predictionId } = useParams();
    const navigate = useNavigate();

    const [prediction, setPrediction] = useState(null);
    const [comments, setComments] = useState("");

    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {

        loadPrediction();

    }, [predictionId]);

    const loadPrediction = async () => {

        try {

            const response =
                await getPredictionDetails(predictionId);

            setPrediction(response.data);

        } catch (error) {

            console.error(
                "Error loading prediction:",
                error
            );

            alert(
                error.response?.data?.message ||
                "Unable to load prediction details."
            );

        } finally {

            setLoading(false);

        }

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        if (!comments.trim()) {

            alert("Please enter doctor comments.");

            return;

        }

        try {

            setSubmitting(true);

            await submitReview(
                predictionId,
                comments
            );

            alert("Prediction reviewed successfully.");

            navigate("/doctor/reviews");

        } catch (error) {

            console.error(
                "Review submission error:",
                error
            );

            alert(
                error.response?.data?.message ||
                "Unable to submit review."
            );

        } finally {

            setSubmitting(false);

        }

    };

    if (loading) {

        return (

            <DashboardLayout>

                <div className="review-loading">

                    <h2>Loading prediction...</h2>

                </div>

            </DashboardLayout>

        );

    }

    if (!prediction) {

        return (

            <DashboardLayout>

                <div className="review-error">

                    <h2>
                        Prediction not found
                    </h2>

                    <button
                        onClick={() =>
                            navigate("/doctor/reviews")
                        }
                    >
                        Back to Reviews
                    </button>

                </div>

            </DashboardLayout>

        );

    }

    return (

        <DashboardLayout>

            <div className="review-details-page">

                <div className="review-details-header">

                    <div>

                        <h1>
                            Prediction Review
                        </h1>

                        <p>
                            Review the AI prediction
                            before providing your
                            medical assessment.
                        </p>

                    </div>

                    <button
                        className="back-button"
                        onClick={() =>
                            navigate("/doctor/reviews")
                        }
                    >
                        ← Back
                    </button>

                </div>


                <div className="review-details-grid">


                    {/* Patient Information */}

                    <div className="review-card">

                        <h2>
                            Patient Information
                        </h2>

                        <div className="patient-info">

                            <div>
                                <span>
                                    Name
                                </span>

                                <strong>
                                    {
                                        prediction.patient?.full_name
                                    }
                                </strong>
                            </div>


                            <div>
                                <span>
                                    Email
                                </span>

                                <strong>
                                    {
                                        prediction.patient?.email
                                    }
                                </strong>
                            </div>


                            <div>
                                <span>
                                    Phone
                                </span>

                                <strong>
                                    {
                                        prediction.patient?.phone
                                    }
                                </strong>
                            </div>

                        </div>

                    </div>


                    {/* AI Prediction */}

                    <div className="review-card">

                        <h2>
                            AI Prediction
                        </h2>

                        <div className="prediction-info">

                            <div className="prediction-disease">

                                <span>
                                    Detected Disease
                                </span>

                                <strong>
                                    {
                                        prediction.disease
                                    }
                                </strong>

                            </div>


                            <div className="prediction-confidence">

                                <span>
                                    Confidence
                                </span>

                                <strong>
                                    {
                                        prediction.confidence
                                    }%
                                </strong>

                            </div>

                        </div>

                    </div>


                    {/* X-Ray */}

                    <div className="review-card xray-card">

                        <h2>
                            X-Ray Image
                        </h2>

                        <div className="xray-container">

                            <img
                                src={`http://127.0.0.1:8000/${prediction.image_url}`}
                                alt="Patient X-Ray"
                                className="xray-image"
                            />

                        </div>

                    </div>


                    {/* Doctor Review */}

                    <div className="review-card doctor-review-card">

                        <h2>
                            Doctor's Review
                        </h2>

                        <form
                            onSubmit={handleSubmit}
                        >

                            <label>
                                Doctor Comments
                            </label>

                            <textarea
                                value={comments}
                                onChange={(e) =>
                                    setComments(
                                        e.target.value
                                    )
                                }
                                placeholder="Enter your medical assessment and comments..."
                                rows="6"
                            />

                            <div className="review-actions">

                                <button
                                    type="button"
                                    className="cancel-button"
                                    onClick={() =>
                                        navigate(
                                            "/doctor/reviews"
                                        )
                                    }
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    className="submit-review-button"
                                    disabled={submitting}
                                >

                                    {
                                        submitting
                                            ? "Submitting..."
                                            : "Submit Review"
                                    }

                                </button>

                            </div>

                        </form>

                    </div>

                </div>

            </div>

        </DashboardLayout>

    );

}

export default ReviewDetails;