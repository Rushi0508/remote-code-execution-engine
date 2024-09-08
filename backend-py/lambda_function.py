import sys
import subprocess
import io
import os
import hashlib
import time
import shutil

MAX_CACHE_SIZE_MB = 512  # Maximum cache size in MB
MAX_CACHE_AGE_SECONDS = 3600  # Maximum age of cache entries in seconds

def cleanup_cache():
    cache_dir = "/tmp"
    current_time = time.time()
    total_size = 0
    entries = []

    for entry in os.scandir(cache_dir):
        if entry.name.startswith(("java_", "cpp_")):
            entry_size = get_dir_size(entry.path)
            entry_age = current_time - entry.stat().st_mtime
            entries.append((entry.path, entry_size, entry_age))
            total_size += entry_size

    # Sort entries by age (oldest first)
    entries.sort(key=lambda x: x[2], reverse=True)

    # Remove old entries
    for entry_path, entry_size, entry_age in entries:
        if entry_age > MAX_CACHE_AGE_SECONDS:
            shutil.rmtree(entry_path)
            total_size -= entry_size
        elif total_size > MAX_CACHE_SIZE_MB * 1024 * 1024:
            shutil.rmtree(entry_path)
            total_size -= entry_size
        else:
            break

def get_dir_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

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
        cleanup_cache()
        code_hash = hashlib.md5(code.encode()).hexdigest()
        class_name = f"JavaCode{code_hash[:8]}"
        temp_dir = f"/tmp/java_{code_hash}"
        temp_file = f"{temp_dir}/{class_name}.java"
        class_file = f"{temp_dir}/{class_name}.class"

        if not os.path.exists(class_file):
            os.makedirs(temp_dir, exist_ok=True)
            modified_code = code.replace("public class Main", f"public class {class_name}")
            with open(temp_file, "w") as file:
                file.write(modified_code)
            compile_result = subprocess.run(["javac", temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if compile_result.returncode != 0:
                return compile_result.stderr.decode("utf-8")

        run_result = subprocess.run(["java", "-classpath", temp_dir, class_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return run_result.stdout.decode("utf-8")
    except Exception as e:
        return str(e)

def execute_cpp_code(code):
    try:
        cleanup_cache()
        code_hash = hashlib.md5(code.encode()).hexdigest()
        temp_dir = f"/tmp/cpp_{code_hash}"
        temp_file = f"{temp_dir}/code.cpp"
        exec_file = f"{temp_dir}/a.out"

        if not os.path.exists(exec_file):
            os.makedirs(temp_dir, exist_ok=True)
            with open(temp_file, "w") as file:
                file.write(code)
            compile_result = subprocess.run(["g++", temp_file, "-o", exec_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if compile_result.returncode != 0:
                return compile_result.stderr.decode("utf-8")

        run_result = subprocess.run([exec_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

