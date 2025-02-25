import { selectPeers, useHMSStore, useHMSActions } from "@100mslive/react-sdk";
import Peer from "./Peer";

const Conference = () => {
  const peers = useHMSStore(selectPeers);
  const hmsActions = useHMSActions();

  const handleEndCall = async () => {
    await hmsActions.leave();
  };

  return (
    <div className="flex flex-col items-center p-4 bg-gray-100 min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Conference</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full max-w-5xl">
        {peers.map((peer) => (
          <Peer key={peer.id} peer={peer} className="p-4 bg-white shadow rounded-lg" />
        ))}
      </div>
      <button 
        onClick={handleEndCall} 
        className="mt-6 px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-all">
        End Call
      </button>
    </div>
  );
};

export default Conference;
