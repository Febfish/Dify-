from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import uuid
from docx import Document
import sys

app = Flask(__name__)

# 文件保存目录
SAVE_DIR = os.getenv("SAVE_DIR", "./files")
os.makedirs(SAVE_DIR, exist_ok=True)

# reference.docx 模板路径
REFERENCE_DOCX = os.getenv("REFERENCE_DOCX", "./reference.docx")
if not os.path.exists(REFERENCE_DOCX):
    print(f"错误: 模板文件 {REFERENCE_DOCX} 不存在！请确保文件已放置在正确位置。", file=sys.stderr)
    exit(1)

# 提供下载接口
@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(SAVE_DIR, filename)

# Markdown 转 Word 接口
@app.route("/convert", methods=["POST"])
def convert_md_to_docx():
    try:
        if request.is_json:
            md_content = request.json.get("markdown", "")
        else:
            md_content = request.data.decode("utf-8")

        if not md_content.strip():
            return jsonify({"error": "No markdown content provided"}), 400

        file_id = str(uuid.uuid4())
        md_path = os.path.join(SAVE_DIR, f"{file_id}.md")
        docx_path = os.path.join(SAVE_DIR, f"{file_id}.docx")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        subprocess.run([
            "pandoc", md_path, "-o", docx_path,
            "--reference-doc", REFERENCE_DOCX,
            "--standalone"
        ], check=True)

        doc = Document(docx_path)
        for table in doc.tables:
            table.style = "Table Grid"
        doc.save(docx_path)

        return jsonify({"message": "Conversion successful", "file_url": f"/files/{os.path.basename(docx_path)}"})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Pandoc conversion failed: {e.stderr.decode('utf-8')}"}), 500
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)