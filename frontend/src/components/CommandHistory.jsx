export default function CommandHistory({ list }) {
  return (
    <div className="p-4 bg-gray-700 rounded-xl h-48 overflow-y-auto text-white">
      <h2 className="text-lg font-semibold mb-2">History</h2>
      <ul>
        {list.map((cmd, i) => (
          <li key={i} className="border-b border-gray-500 py-1">
            {cmd}
          </li>
        ))}
      </ul>
    </div>
  );
}
