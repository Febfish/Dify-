from flask import Flask, request, Response, jsonify
import os
import json
import sys

app = Flask(__name__)

# Markdown 文件路径，从环境变量读取，默认值为相对路径
DOCS_PATH = os.getenv("DOCS_PATH", "./md_files")
os.makedirs(DOCS_PATH, exist_ok=True)

# 初始化场景映射
def load_scene_map():
    scene_map = {}
    if os.path.exists(DOCS_PATH):
        for fname in os.listdir(DOCS_PATH):
            if fname.endswith(".md"):
                scene_name = os.path.splitext(fname)[0]
                scene_map[scene_name] = fname
    return scene_map

scene_map = load_scene_map()

def find_contains_match(scene_name):
    """包含匹配场景名称"""
    for key in scene_map.keys():
        if key in scene_name or scene_name in key:
            return key
    return None

@app.route("/get_doc", methods=["POST"])
def get_doc():
    global scene_map
    data = request.json
    scene = data.get("scene", "").strip()

    if not scene:
        return Response(json.dumps({"error": "缺少 scene 参数"}, ensure_ascii=False),
                        mimetype="application/json", status=400)

    # 重新加载场景映射以应对新文件
    scene_map = load_scene_map()

    matched_scene = None

    if scene in scene_map:
        matched_scene = scene
        filename = scene_map[scene]
    else:
        best_match = find_contains_match(scene)
        if best_match:
            matched_scene = best_match
            filename = scene_map[best_match]
        else:
            candidate_file = f"{scene}.md"
            candidate_path = os.path.join(DOCS_PATH, candidate_file)
            if os.path.exists(candidate_path):
                scene_map[scene] = candidate_file
                matched_scene = scene
                filename = candidate_file
            else:
                return Response(json.dumps({
                    "error": f"未找到与场景 {scene} 匹配的资料",
                    "available_scenes": list(scene_map.keys())
                }, ensure_ascii=False), mimetype="application/json", status=404)

    filepath = os.path.join(DOCS_PATH, filename)
    if not os.path.exists(filepath):
        return Response(json.dumps({"error": f"文件 {filename} 不存在"}, ensure_ascii=False),
                        mimetype="application/json", status=404)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    result = {
        "input_scene": scene,
        "matched_scene": matched_scene,
        "content": content
    }

    return Response(json.dumps(result, ensure_ascii=False),
                    mimetype="application/json", status=200)

if __name__ == '__main__':
    # 确保在生产环境中使用环境变量而不是硬编码的端口
    port = int(os.getenv("PORT", 7000))
    app.run(host='0.0.0.0', port=port, debug=True)