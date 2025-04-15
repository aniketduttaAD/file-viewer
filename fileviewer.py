from flask import Flask, request, send_file, render_template_string, Response
import os

app = Flask(__name__)

FILE_PATH = "data.txt"
ABSOLUTE_FILE_PATH = os.path.join(os.getcwd(), FILE_PATH)

# Ensure data.txt exists
if not os.path.exists(ABSOLUTE_FILE_PATH):
    with open(ABSOLUTE_FILE_PATH, 'w') as f:
        f.write("Hello, world!\n")

@app.route("/view")
def view_file():
    with open(ABSOLUTE_FILE_PATH, 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/plain')

@app.route("/edit", methods=["GET", "POST"])
def edit_file():
    message = ""
    if request.method == "POST":
        content = request.form.get("content", "")
        with open(ABSOLUTE_FILE_PATH, 'w') as f:
            f.write(content)
        message = "File updated successfully!"

    with open(ABSOLUTE_FILE_PATH, 'r') as f:
        content = f.read()

    return render_template_string('''
        <h2>Edit File</h2>
        <form method="post">
            <textarea name="content" 
                      style="width: 100%; height: 300px; max-height: 600px; resize: vertical; overflow: auto;" 
                      rows="20">{{ content }}</textarea><br>
            <input type="submit" value="Update">
        </form>
        <p style="color: green;">{{ message }}</p>
    ''', content=content, message=message)

@app.route("/download")
def download_file():
    return send_file(ABSOLUTE_FILE_PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
