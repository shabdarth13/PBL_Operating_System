export default function SpeechBox({ text }) {
  return (
    <div className="p-4 bg-gray-800 text-white rounded-xl h-32 overflow-y-auto">
      <h2 className="text-lg font-semibold mb-2">Recognized Speech</h2>
      <p>{text || "Waiting for input..."}</p>
    </div>
  );
}
