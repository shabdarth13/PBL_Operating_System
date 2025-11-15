export default function TerminalOutput({ output }) {
  return (
    <div className="p-4 bg-black text-gray-300 rounded-xl h-48 font-mono overflow-y-auto">
      <h2 className="text-lg font-semibold mb-2 text-white">Output</h2>
      <pre>{output}</pre>
    </div>
  );
}
