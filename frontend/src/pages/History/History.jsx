import { useEffect, useState } from "react";
import DashboardLayout from "../../layouts/DashboardLayout";
import {
    getPredictionHistory,
    deletePrediction
} from "../../services/historyService";

function History() {

    const [history, setHistory] = useState([]);
    const [filteredHistory, setFilteredHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");

    const loadHistory = async () => {

        try {

            const response = await getPredictionHistory();

            setHistory(response.data);
            setFilteredHistory(response.data);

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
            item.disease.toLowerCase().includes(search.toLowerCase())
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
                placeholder="Search Disease..."
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

                                <td>{item.disease}</td>

                                <td>{item.confidence}%</td>

                                <td>
                                    {new Date(
                                        item.created_at
                                    ).toLocaleString()}
                                </td>

                                <td>

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