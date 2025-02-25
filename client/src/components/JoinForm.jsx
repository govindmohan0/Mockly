import { useHMSActions } from "@100mslive/react-sdk";
import { useState } from "react";

const JoinForm = () => {
  const hmsActions = useHMSActions();
  const [userName, setUserName] = useState("");
  const roomCode = "xyp-adpt-pxc"; // Hardcoded room code

  const handleInputChange = (e) => {
    setUserName(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const authToken = await hmsActions.getAuthTokenByRoomCode({ roomCode });
      await hmsActions.join({ userName, authToken });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen ">
      <form onSubmit={handleSubmit} className="flex flex-col items-center bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-4">Join Room</h2>
        <div className="mb-4">
          <input
            required
            id="name"
            type="text"
            name="name"
            value={userName}
            onChange={handleInputChange}
            placeholder="Your Name"
            className="p-2 border border-gray-300 rounded"
          />
        </div>
        <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Join</button>
      </form>
    </div>
  );
};

export default JoinForm;
