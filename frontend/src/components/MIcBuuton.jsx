export default function MicButton({ listening, toggle }) {
  return (
    <button
      onClick={toggle}
      className={`px-6 py-3 rounded-xl text-white font-bold 
        ${listening ? "bg-red-600" : "bg-green-600"}`
      }
    >
      {listening ? "Stop Listening" : "Start Listening"}
    </button>
  );
}
