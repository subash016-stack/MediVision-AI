import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "../../layouts/DashboardLayout";
import { getPredictionDetails } from "../../services/historyService";

function MedicalReport() {
    const { predictionId } = useParams();
    const navigate = useNavigate();

    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [viewMode, setViewMode] = useState("original"); // "original" or "gradcam"

    useEffect(() => {
        loadReport();
    }, [predictionId]);

    const loadReport = async () => {
        try {
            setLoading(true);
            setError("");
            const response = await getPredictionDetails(predictionId);
            setReport(response.data);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.message || "Failed to load medical report.");
        } finally {
            setLoading(false);
        }
    };

    const handlePrint = () => {
        window.print();
    };

    if (loading) {
        return (
            <DashboardLayout>
                <div className="review-loading">
                    <h2>Generating Medical Report...</h2>
                </div>
            </DashboardLayout>
        );
    }

    if (error || !report) {
        return (
            <DashboardLayout>
                <div className="review-error">
                    <h2>Unable to Load Report</h2>
                    <p>{error || "Record not found."}</p>
                    <button onClick={() => navigate(-1)}>← Go Back</button>
                </div>
            </DashboardLayout>
        );
    }

    const isReviewed = report.doctor_status === "Reviewed";

    return (
        <DashboardLayout>
            <div className="medical-report-page">
                {/* Actions Bar (Hidden on print) */}
                <div className="report-actions-bar no-print">
                    <button className="back-button" onClick={() => navigate(-1)}>
                        ← Back
                    </button>
                    <div style={{ display: "flex", gap: "12px" }}>
                        <button className="review-button" onClick={handlePrint}>
                            🖨️ Print / Save as PDF
                        </button>
                    </div>
                </div>

                {/* Printable Document Container */}
                <div className="report-paper">
                    {/* Header */}
                    <div className="report-header">
                        <div className="report-brand">
                            <h1>MEDIVISION-AI</h1>
                            <span>AI-Assisted Diagnostic Analysis Platform</span>
                        </div>
                        <div className="report-meta-badge">
                            <span className="report-id">REPORT ID: {report.prediction_id}</span>
                            <span className={`status-badge ${isReviewed ? 'status-reviewed' : 'status-pending'}`}>
                                {isReviewed ? "CLINICALLY REVIEWED" : "PENDING DOCTOR REVIEW"}
                            </span>
                        </div>
                    </div>

                    <hr className="report-divider" />

                    {/* Patient & Exam Metadata */}
                    <div className="report-section">
                        <h3 className="section-title">PATIENT & CLINICAL EXAMINATION</h3>
                        <div className="report-grid">
                            <div className="report-info-box">
                                <label>Patient Name</label>
                                <strong>{report.patient?.full_name || "Patient Record"}</strong>
                            </div>
                            <div className="report-info-box">
                                <label>Patient ID</label>
                                <strong>{report.user_id}</strong>
                            </div>
                            <div className="report-info-box">
                                <label>Contact Email</label>
                                <strong>{report.patient?.email || "N/A"}</strong>
                            </div>
                            <div className="report-info-box">
                                <label>Examination Date</label>
                                <strong>{new Date(report.created_at).toLocaleString()}</strong>
                            </div>
                        </div>
                    </div>

                    {/* Imaging & AI Findings */}
                    <div className="report-section">
                        <h3 className="section-title">CHEST RADIOGRAPH & AI ANALYSIS</h3>
                        <div className="imaging-grid">
                            <div className="imaging-visual">
                                <div className="image-tabs no-print">
                                    <button 
                                        className={`tab-btn ${viewMode === 'original' ? 'active' : ''}`}
                                        onClick={() => setViewMode('original')}
                                    >
                                        Original X-Ray
                                    </button>
                                    {report.heatmap_url && (
                                        <button 
                                            className={`tab-btn ${viewMode === 'gradcam' ? 'active' : ''}`}
                                            onClick={() => setViewMode('gradcam')}
                                        >
                                            Grad-CAM Heatmap
                                        </button>
                                    )}
                                </div>
                                <div className="image-display-frame">
                                    <img 
                                        src={`http://127.0.0.1:8000/${viewMode === 'gradcam' && report.heatmap_url ? report.heatmap_url : report.image_url}`} 
                                        alt="Chest Radiograph" 
                                        className="radiograph-img"
                                    />
                                    <span className="caption-text">
                                        {viewMode === 'gradcam' && report.heatmap_url ? "Grad-CAM Class Activation Heatmap" : "Original Posterior-Anterior Chest Radiograph"}
                                    </span>
                                </div>
                            </div>

                            <div className="ai-summary-card">
                                <h4>AI Model Classification (EfficientNetB0)</h4>
                                <div className="finding-row">
                                    <span>Primary Detected Pattern:</span>
                                    <strong className="finding-disease">{report.disease}</strong>
                                </div>
                                <div className="finding-row">
                                    <span>Model Confidence:</span>
                                    <strong className="finding-confidence">{report.confidence}%</strong>
                                </div>
                                <p className="finding-note">
                                    Grad-CAM localization highlights regions of interest contributing most heavily to the predicted classification.
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Doctor's Clinical Review Section */}
                    <div className="report-section">
                        <h3 className="section-title">PHYSICIAN CLINICAL ASSESSMENT</h3>
                        <div className="doctor-assessment-box">
                            {isReviewed ? (
                                <>
                                    <div className="review-meta-row">
                                        <div>
                                            <label>Reviewing Physician:</label>
                                            <strong>Dr. {report.doctor_name || report.reviewed_by || "Assigned Physician"}</strong>
                                        </div>
                                        <div>
                                            <label>Review Timestamp:</label>
                                            <strong>{new Date(report.reviewed_at).toLocaleString()}</strong>
                                        </div>
                                    </div>
                                    <div className="doctor-notes">
                                        <label>Medical Comments & Observations:</label>
                                        <p>{report.doctor_comments}</p>
                                    </div>
                                </>
                            ) : (
                                <div className="pending-review-notice">
                                    <p>⚠️ This prediction is currently in the physician review queue. Final clinical validation will be appended upon review completion.</p>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Disclaimer & Footer */}
                    <div className="report-footer">
                        <p className="disclaimer-text">
                            <strong>CONFIDENTIAL MEDICAL DOCUMENTATION:</strong> MediVision-AI is an assistive diagnostic decision-support system. AI predictions are supplementary findings and must be interpreted in conjunction with complete clinical history by authorized medical personnel.
                        </p>
                        <div className="signature-area">
                            <div className="sig-line">
                                <span>Physician Signature / Verification:</span>
                                <strong>{isReviewed ? (report.doctor_name || "Verified by Doctor") : "Pending Signature"}</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}

export default MedicalReport;
