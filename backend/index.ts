import { Context, APIGatewayProxyResult, APIGatewayEvent } from "aws-lambda";
import { execSync } from "child_process";
import * as fs from "fs";

const execute_python_code = (code: string) => {
  try {
    // Create a temporary file with the Python code
    const tempFile = `/tmp/python_code_${Date.now()}.py`;
    fs.writeFileSync(tempFile, code);

    // Execute the Python code directly
    const output = execSync(`python ${tempFile}`).toString();

    // Clean up the temporary file
    fs.unlinkSync(tempFile);

    return output.trim();
  } catch (error) {
    console.error("Error executing Python code:", error);
    return `Error: ${error.message}`;
  }
};

const execute_javascript_code = (code: string) => {
  try {
    const tempFile = `/tmp/javascript_code_${Date.now()}.js`;
    fs.writeFileSync(tempFile, code);
    const output = execSync(`node ${tempFile}`).toString();
    fs.unlinkSync(tempFile);
    return output.trim();
  } catch (error) {
    console.error("Error executing JavaScript code:", error);
    return `Error: ${error.message}`;
  }
};

const execute_java_code = (code: string) => {
  try {
    const tempFile = `/tmp/java_code_${Date.now()}.java`;
    fs.writeFileSync(tempFile, code);
    const output = execSync(
      `javac ${tempFile} && java ${tempFile.replace(".java", "")}`
    ).toString();
    fs.unlinkSync(tempFile);
    return output.trim();
  } catch (error) {
    console.error("Error executing Java code:", error);
    return `Error: ${error.message}`;
  }
};

const execute_cpp_code = (code: string) => {
  try {
    const tempFile = `/tmp/cpp_code_${Date.now()}.cpp`;
    fs.writeFileSync(tempFile, code);
    const output = execSync(`g++ ${tempFile} && ./a.out`).toString();
    fs.unlinkSync(tempFile);
    return output.trim();
  } catch (error) {
    console.error("Error executing C++ code:", error);
    return `Error: ${error.message}`;
  }
};

export const handler = async (
  event: APIGatewayEvent,
  context: Context
): Promise<APIGatewayProxyResult> => {
  let { language, code }: any = event;
  let result = "";
  if (language == "python") {
    result = execute_python_code(code?.toString() ?? "");
  } else if (language == "javascript") {
    result = execute_javascript_code(code?.toString() ?? "");
  } else if (language == "java") {
    result = execute_java_code(code?.toString() ?? "");
  } else if (language == "c++" || language == "cpp") {
    result = execute_cpp_code(code?.toString() ?? "");
  } else {
    result = "Language not supported + " + language;
  }
  return {
    statusCode: 200,
    body: result,
  };
};
