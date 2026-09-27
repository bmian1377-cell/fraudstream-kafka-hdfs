from flask import Flask, jsonify
from flask_cors import CORS
from hdfs import InsecureClient

app = Flask(__name__)
CORS(app)

HDFS_URL = "http://localhost:9870"
HDFS_USER = "bilawal"
ANALYSIS_PATH = "/fraudstream/analysis-output/part-00000"

client = InsecureClient(HDFS_URL, user=HDFS_USER)

def parse_analysis_output():
    with client.read(ANALYSIS_PATH, encoding="utf-8") as reader:
        content = reader.read()

    result = {}
    for line in content.strip().split("\n"):
        parts = line.strip().split("\t")
        label = "fraud" if parts[0].lower() == "fraud" else "normal"

        stats = {}
        for kv in parts[1:]:
            key, value = kv.split("=")
            stats[key] = float(value)

        result[label] = {
            "count": int(stats["count"]),
            "total_amount": round(stats["total_amount"], 2),
            "avg_amount": round(stats["avg_amount"], 2),
        }
    return result
        
    
    

@app.route("/api/fraud-stats", methods=["GET"])
def fraud_stats():
    try:
        data = parse_analysis_output()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
