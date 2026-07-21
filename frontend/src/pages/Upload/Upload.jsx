import { useState } from "react";
import DashboardLayout from "../../layouts/DashboardLayout";
import {
    uploadXray,
    predictDisease
} from "../../services/uploadService";

function Upload() {

    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleFile = (e) => {

        const selected = e.target.files[0];

        if (!selected) return;

        setFile(selected);

        setPreview(URL.createObjectURL(selected));

        setResult(null);

    };

    const handleUpload = async () => {

        if (!file) {

            alert("Select an X-ray image.");

            return;

        }

        try {

            setLoading(true);

            const upload = await uploadXray(file);

            console.log(upload);

            const imageId = upload.data.image_id;

            const prediction = await predictDisease(imageId);

            console.log(prediction);

            setResult(prediction.data);

        }

        catch (err) {

            console.error(err);

            alert("Prediction failed.");

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <DashboardLayout>

            <div className="upload-container">

                <h1>Upload Chest X-ray</h1>

                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFile}
                />

                {preview && (

                    <img
                        src={preview}
                        alt="preview"
                        className="preview"
                    />

                )}

                <br />

                <button onClick={handleUpload}>

                    Upload & Predict

                </button>

                {loading &&

                    <h3>Running AI Prediction...</h3>

                }

                {result && (

                    <div className="result-card">

                        <h2>

                            Disease

                        </h2>

                        <h3>

                            {result.disease}

                        </h3>

                        <p>

                            Confidence

                        </p>

                        <h2>

                            {result.confidence.toFixed(2)}%

                        </h2>

                    </div>

                )}

            </div>

        </DashboardLayout>

    );

}

export default Upload;