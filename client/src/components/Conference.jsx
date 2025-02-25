import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import Peer from "./Peer";
import Footer from "./Footer";

const Conference = () => {
  const peers = useHMSStore(selectPeers);

  return (
    <div className="fixed inset-0 flex flex-col bg-black text-white">
      
      {/* Video Container */}
      <div className="flex-grow relative flex items-center justify-center">
        {/* Main Video */}
        {peers.length > 0 && (
          <div className="w-full h-full flex items-center justify-center">
            <Peer key={peers[0].id} peer={peers[0]} isMain={true} />
          </div>
        )}

        {/* Mini Video for Other Participants */}
        {peers.length > 1 && (
          <div className="absolute bottom-5 right-5 w-40 h-24 bg-gray-900 rounded-lg overflow-hidden shadow-lg">
            <Peer key={peers[1].id} peer={peers[1]} isMini={true} />
          </div>
        )}
      </div>

      {/* Footer Controls */}
      <Footer />
      
    </div>
  );
};

export default Conference;
