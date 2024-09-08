"use client";

import { Editor } from "@monaco-editor/react";
import axios from "axios";
import { useState } from "react";

export default function Home() {
  const [language, setLanguage] = useState("javascript");
  const [code, setCode] = useState<string | undefined>("");
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [time, setTime] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleRun = async () => {
    setOutput("");
    setTime("");

    try {
      setIsLoading(true);
      const startTime = Date.now();
      const { data } = await axios.post("https://wx5xrkoq2e.execute-api.us-east-1.amazonaws.com/default/execute-code", {
        language,
        code,
      });
      const endTime = Date.now();
      const executionTime = endTime - startTime;
      setOutput(data.body);
      setTime(executionTime.toString());
    } catch (err) {
      console.log(err);
    }
    finally {
      setIsLoading(false);
    }
  };


  return (
    <div className="flex flex-col h-screen w-full">
      <h1 className="text-3xl font-bold text-center py-4">Code Editor</h1>
      <div className="flex flex-row flex-1 overflow-hidden">
        <div className="w-[60%] h-full mx-2 flex flex-col">
          <div className="mb-2 flex justify-between items-center">
            <select
              className="w-1/3 p-2 border border-gray-300 rounded"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="c++">C++</option>
              <option value="javascript">JavaScript</option>
              <option value="python">Python</option>
              <option value="java">Java</option>
            </select>
            <div>
              <button disabled={isLoading} onClick={() => handleRun()} className="bg-blue-500 text-white px-4 py-2 rounded mr-2 hover:bg-blue-600">
                {isLoading ? "Running..." : "Run"}
              </button>
              <button className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Submit</button>
            </div>
          </div>
          <Editor
            value={code}
            onChange={(value) => setCode(value)}
            theme="vs-dark"
            className="flex-1"
            language={language == 'c++' ? 'cpp' : language}
            defaultValue="// Write your code here"
          />
        </div>
        <div className="w-[40%] flex flex-col px-4 py-1 overflow-hidden">
          <div className="flex-1 flex flex-col overflow-hidden">
            <div className="mb-4 flex-1 min-h-0">
              <h2 className="text-xl font-semibold mb-2">Input</h2>
              <textarea value={input} onChange={(e) => setInput(e.target.value)} className="w-full h-[calc(100%-2rem)] p-2 border border-gray-300 rounded resize-none" placeholder="Enter input here"></textarea>
            </div>
            <div className="flex-1 min-h-0">
              <h2 className="text-xl font-semibold flex items-center mb-2">Output
                {time && <span className="text-sm text-gray-500 ml-2">({(parseFloat(time) / 1000).toFixed(2)}s)</span>}
              </h2>
              <div className="w-full h-[calc(100%-2rem)] p-2 border border-gray-300 rounded bg-gray-100 overflow-auto">
                {output}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
