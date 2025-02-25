import React from 'react'
import { HMSRoomProvider } from "@100mslive/react-sdk";
import Videocall from './Videocall';
const Videocallon = () => {
  return (
    <>
      <React.StrictMode>
    <HMSRoomProvider>
      <Videocall />
    </HMSRoomProvider>
  </React.StrictMode>
    </>
  )
}

export default Videocallon