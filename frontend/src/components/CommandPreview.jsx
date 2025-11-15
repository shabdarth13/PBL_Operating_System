export default function CommandPreview({ command }) {
  return (
    <div className="p-4 bg-gray-900 text-green-400 rounded-xl h-24 overflow-y-auto">
      <h2 className="text-lg font-semibold mb-1">Mapped Command</h2>
      <code>{command || "No command yet"}</code>
    </div>
  );
}
