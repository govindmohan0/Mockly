import { useAVToggle, useHMSActions } from "@100mslive/react-sdk";
import { MdMic, MdMicOff, MdVideocam, MdVideocamOff, MdCallEnd, MdSettings } from "react-icons/md";

const Footer = () => {
  const { isLocalAudioEnabled, toggleAudio, isLocalVideoEnabled, toggleVideo } = useAVToggle();
  const hmsActions = useHMSActions();

  const handleEndCall = async () => {
    await hmsActions.leave();
  };

  return (
    <div className=" w-full flex justify-center gap-6 px-4 bg-gray-900">
      <button onClick={toggleAudio} className="p-3 bg-gray-700 rounded-full hover:bg-gray-600">
        {isLocalAudioEnabled ? <MdMic size={24} /> : <MdMicOff size={24} />}
      </button>

      <button onClick={toggleVideo} className="p-3 bg-gray-700 rounded-full hover:bg-gray-600">
        {isLocalVideoEnabled ? <MdVideocam size={24} /> : <MdVideocamOff size={24} />}
      </button>

      <button onClick={handleEndCall} className="p-3 bg-red-600 !important rounded-full hover:bg-red-700">
  <MdCallEnd size={24} />
</button>

      {/* <button className="p-3 bg-gray-700 rounded-full hover:bg-gray-600">
        <MdSettings size={24} />
      </button> */}
    </div>
  );
};

export default Footer;
