import { useRoomContext } from "@livekit/components-react";
import { useEffect, useState } from "react";
import { Slides } from "./Slides";

export default function SlidesRPCHandler() {
  const room = useRoomContext();
  const participant = room.localParticipant;
  const [slides, setSlides] = useState(
    "<section><h1>Create A Presentation</h1></section>"
  );

  useEffect(() => {
    if (!participant) return;
    console.log("Registering RPC method: navigate_to_slides");

    // something wrong with types but it works!
    participant.registerRpcMethod("navigate_to_slides", async (data: any) => {
      console.log(
        `Received greeting from ${data.callerIdentity}: ${data.payload}`
      );
      try {
        const payload = JSON.parse(data.payload);
        setSlides(payload?.slides);
      } catch (e) {
        return "Invalid JSON";
      }
      return `Hello, ${data.callerIdentity}!`;
    });
  }, []);

  return <Slides slides={slides} />;
}
