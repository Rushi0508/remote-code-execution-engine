import sys
import subprocess
import io

def execute_python_code(code):
    original_stdout = sys.stdout
    sys.stdout = output_capture = io.StringIO()

    try:
        exec(code)
        output = output_capture.getvalue()
        return output
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = original_stdout

def execute_java_code(code):
    try:
        with open("/tmp/Main.java", "w") as file:
            file.write(code)

        compile_result = subprocess.run(["javac", "/tmp/Main.java"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if compile_result.returncode != 0:
            return compile_result.stderr.decode("utf-8")

        run_result = subprocess.run(["java", "-classpath", "/tmp", "Main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return run_result.stdout.decode("utf-8")
    except Exception as e:
        return str(e)
    
def execute_cpp_code(code):
    try:
        with open("/tmp/temp.cpp", "w") as file:
            file.write(code)

        compile_result = subprocess.run(["g++", "/tmp/temp.cpp", "-o", "/tmp/temp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if compile_result.returncode != 0:
            return compile_result.stderr.decode("utf-8")
        
        run_result = subprocess.run(["/tmp/temp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return run_result.stdout.decode("utf-8")
    except Exception as e:
        return str(e)
    
def execute_js_code(code):
    try:
        with open("/tmp/temp.js", "w") as file:
            file.write(code)

        run_result = subprocess.run(["node", "/tmp/temp.js"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if run_result.returncode != 0:
            return run_result.stderr.decode("utf-8")

        return run_result.stdout.decode("utf-8")
    except Exception as e:
        return str(e)

def handler(event, context):
    language = event.get("language", "python")
    code = event.get("code", "")

    if language == "python":
        result =  execute_python_code(code)
    elif language == "java":
        result = execute_java_code(code)
    elif language == "cpp" or language == "c++":
        result = execute_cpp_code(code)
    elif language == "javascript":
        result = execute_js_code(code)
    else:
        result = "Language not supported " + language
    return {
        "statusCode": 200,
        "body": result
    }
        
