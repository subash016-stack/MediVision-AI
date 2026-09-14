import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../../layouts/DashboardLayout";
import {
    getPredictionHistory,
    deletePrediction
} from "../../services/historyService";

function History() {

    const navigate = useNavigate();
    const [history, setHistory] = useState([]);
    const [filteredHistory, setFilteredHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");

    const loadHistory = async () => {

        try {

            const response = await getPredictionHistory();

            setHistory(response.data || []);
            setFilteredHistory(response.data || []);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }

    };

    useEffect(() => {

        loadHistory();

    }, []);

    useEffect(() => {

        const filtered = history.filter(item =>
            item.disease.toLowerCase().includes(search.toLowerCase()) ||
            (item.doctor_status && item.doctor_status.toLowerCase().includes(search.toLowerCase()))
        );

        setFilteredHistory(filtered);

    }, [search, history]);

    const handleDelete = async (predictionId) => {

        const confirmDelete = window.confirm(
            "Delete this prediction?"
        );

        if (!confirmDelete) return;

        try {

            await deletePrediction(predictionId);

            loadHistory();

        } catch (error) {

            console.error(error);

        }

    };

    return (

        <DashboardLayout>

            <h1>Prediction History</h1>

            <input
                type="text"
                placeholder="Search Disease or Status..."
                value={search}
                onChange={(e) =>
                    setSearch(e.target.value)
                }
                className="search-box"
            />

            {loading ? (

                <h3>Loading...</h3>

            ) : filteredHistory.length === 0 ? (

                <h3>No Predictions Found</h3>

            ) : (

                <table className="history-table">

                    <thead>

                        <tr>

                            <th>Image</th>
                            <th>Disease</th>
                            <th>Confidence</th>
                            <th>Doctor Status</th>
                            <th>Date</th>
                            <th>Action</th>

                        </tr>

                    </thead>

                    <tbody>

                        {filteredHistory.map((item) => (

                            <tr key={item.prediction_id}>

                                <td>

                                    <img
                                        src={`http://127.0.0.1:8000/${item.image_url}`}
                                        alt="X-Ray"
                                        className="history-image"
                                    />

                                </td>

                                <td>
                                    <strong>{item.disease}</strong>
                                </td>

                                <td>{item.confidence}%</td>

                                <td>
                                    <span className={`status-badge ${item.doctor_status === 'Reviewed' ? 'status-reviewed' : 'status-pending'}`}>
                                        {item.doctor_status || "Pending"}
                                    </span>
                                </td>

                                <td>
                                    {new Date(
                                        item.created_at
                                    ).toLocaleDateString()}
                                </td>

                                <td>

                                    <div style={{ display: "flex", gap: "8px", justifyContent: "center" }}>
                                        <button
                                            className="review-button"
                                            style={{ padding: "6px 12px", fontSize: "0.85rem" }}
                                            onClick={() => navigate(`/report/${item.prediction_id}`)}
                                        >
                                            View Report
                                        </button>

                                        <button
                                            className="delete-btn"
                                            onClick={() =>
                                                handleDelete(
                                                    item.prediction_id
                                                )
                                            }
                                        >
                                            Delete
                                        </button>
                                    </div>

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            )}

        </DashboardLayout>

    );

}

export default History; 