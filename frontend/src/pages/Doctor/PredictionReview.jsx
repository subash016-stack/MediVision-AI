import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import DashboardLayout from "../../layouts/DashboardLayout";

import {
    getPredictionDetails,
    submitReview
} from "../../services/reviewService";


function PredictionReview() {

    const { predictionId } = useParams();

    const navigate = useNavigate();

    const [prediction, setPrediction] = useState(null);

    const [comments, setComments] = useState("");

    const [loading, setLoading] = useState(true);

    const [submitting, setSubmitting] = useState(false);

    const [error, setError] = useState("");

    const [viewMode, setViewMode] = useState("original");


    useEffect(() => {

        loadPrediction();

    }, [predictionId]);


    const loadPrediction = async () => {

        try {

            setLoading(true);

            setError("");

            const response =
                await getPredictionDetails(predictionId);

            setPrediction(response.data);

        } catch (error) {

            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Failed to load prediction details."
            );

        } finally {

            setLoading(false);

        }

    };


    const handleSubmit = async (event) => {

        event.preventDefault();

        if (!comments.trim()) {

            alert("Please enter your medical assessment.");

            return;

        }


        try {

            setSubmitting(true);

            await submitReview(
                predictionId,
                {
                    doctor_comments: comments
                }
            );

            alert("Review submitted successfully.");

            navigate("/doctor/reviews");

        } catch (error) {

            console.error(error);

            alert(
                error.response?.data?.detail ||
                "Failed to submit review."
            );

        } finally {

            setSubmitting(false);

        }

    };


    if (loading) {

        return (

            <DashboardLayout>

                <div className="review-loading">

                    <h2>
                        Loading prediction...
                    </h2>

                </div>

            </DashboardLayout>

        );

    }


    if (error) {

        return (

            <DashboardLayout>

                <div className="review-error">

                    <h2>
                        Unable to load prediction
                    </h2>

                    <p>
                        {error}
                    </p>

                    <button
                        onClick={() =>
                            navigate("/doctor/reviews")
                        }
                    >
                        ← Back to Reviews
                    </button>

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
                        ← Back to Reviews
                    </button>

                </div>

            </DashboardLayout>

        );

    }


    return (

        <DashboardLayout>

            <div className="prediction-review-page">


                {/* ================================= */}
                {/* PAGE HEADER */}
                {/* ================================= */}

                <div className="prediction-review-header">

                    <div>

                        <h1>
                            Prediction Review
                        </h1>

                        <p>
                            Review the AI prediction before providing
                            your medical assessment.
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


                {/* ================================= */}
                {/* PATIENT + AI INFORMATION */}
                {/* ================================= */}

                <div className="review-info-grid">


                    {/* Patient Information */}

                    <div className="review-card">

                        <h2>
                            Patient Information
                        </h2>


                        <div className="patient-info">

                            <div className="info-item">

                                <span>
                                    Name
                                </span>

                                <strong>
                                    {prediction.patient?.full_name}
                                </strong>

                            </div>


                            <div className="info-item">

                                <span>
                                    Email
                                </span>

                                <strong>
                                    {prediction.patient?.email}
                                </strong>

                            </div>


                            <div className="info-item">

                                <span>
                                    Phone
                                </span>

                                <strong>
                                    {prediction.patient?.phone}
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

                            <div className="prediction-item">

                                <span>
                                    Detected Disease
                                </span>

                                <strong className="disease-name">
                                    {prediction.disease}
                                </strong>

                            </div>


                            <div className="prediction-item">

                                <span>
                                    Confidence
                                </span>

                                <strong className="confidence-value">
                                    {prediction.confidence}%
                                </strong>

                            </div>

                        </div>

                    </div>

                </div>


                {/* ================================= */}
                {/* IMAGE + DOCTOR REVIEW */}
                {/* ================================= */}

                <div className="review-main-grid">


                    {/* X-RAY IMAGE */}

                    <div className="review-card xray-card">

                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
                            <h2 style={{ margin: 0 }}>
                                X-Ray Image
                            </h2>

                            {prediction.heatmap_url && (
                                <div className="image-tabs" style={{ margin: 0 }}>
                                    <button 
                                        type="button"
                                        className={`tab-btn ${viewMode === 'original' ? 'active' : ''}`}
                                        onClick={() => setViewMode('original')}
                                    >
                                        Original
                                    </button>
                                    <button 
                                        type="button"
                                        className={`tab-btn ${viewMode === 'gradcam' ? 'active' : ''}`}
                                        onClick={() => setViewMode('gradcam')}
                                    >
                                        Grad-CAM Heatmap
                                    </button>
                                </div>
                            )}
                        </div>


                        <div className="xray-container">

                            <img
                                src={`http://127.0.0.1:8000/${viewMode === 'gradcam' && prediction.heatmap_url ? prediction.heatmap_url : prediction.image_url}`}
                                alt="Patient X-Ray"
                                className="xray-image"
                            />

                        </div>

                    </div>


                    {/* DOCTOR REVIEW */}

                    <div className="review-card doctor-review-card">

                        <h2>
                            Doctor's Review
                        </h2>


                        <form
                            onSubmit={handleSubmit}
                            className="review-form"
                        >

                            <label htmlFor="doctor-comments">

                                Doctor Comments

                            </label>


                            <textarea
                                id="doctor-comments"
                                value={comments}
                                onChange={(event) =>
                                    setComments(event.target.value)
                                }
                                placeholder="Enter your medical assessment and comments..."
                                rows="8"
                            />


                            <div className="review-actions">

                                <button
                                    type="button"
                                    className="cancel-button"
                                    onClick={() =>
                                        navigate("/doctor/reviews")
                                    }
                                >
                                    Cancel
                                </button>


                                <button
                                    type="submit"
                                    className="submit-review-button"
                                    disabled={submitting}
                                >

                                    {submitting
                                        ? "Submitting..."
                                        : "Submit Review"}

                                </button>

                            </div>

                        </form>

                    </div>

                </div>

            </div>

        </DashboardLayout>

    );

}


export default PredictionReview;