import {
    selectIsConnectedToRoom,
    useHMSActions,
    useHMSStore,
  } from "@100mslive/react-sdk";
  import "./videocall.css";
  
  import { useEffect } from "react";
import Conference from "../Conference";
import Footer from "../Footer";
import JoinForm from "../JoinForm";
 
  
  function Videocall() {
    const isConnected = useHMSStore(selectIsConnectedToRoom);
    const hmsActions = useHMSActions();
  
    useEffect(() => {
      window.onunload = () => {
        if (isConnected) {
          hmsActions.leave();
        }
      };
    }, [hmsActions, isConnected]);
  
    return (
      <div className="App mt-40">
        {isConnected ? (
          <>
            <Conference />
            <Footer />
          </>
        ) : (
          <div className="ml-182 mb-186"><JoinForm/></div>
        )}
      </div>
    );
  }
  
  export default Videocall;
  