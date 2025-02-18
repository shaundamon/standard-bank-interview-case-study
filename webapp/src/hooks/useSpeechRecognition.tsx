import { useState } from "react";
import { useSpeechSynthesis } from "./useSpeechSynthesis";

export const useSpeechRecognition = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(
    null
  );
  const { speak } = useSpeechSynthesis();

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);

      recorder.onstart = () => {
        setIsRecording(true);
        speak("Recording started");
      };

      recorder.onstop = () => {
        setIsRecording(false);
        speak("Processing your voice query");
      };

      recorder.start();
      setMediaRecorder(recorder);
    } catch (err) {
      console.error("Error starting recording:", err);
      speak("Could not access microphone. Please check your permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach((track) => track.stop());
    }
  };

  return {
    isRecording,
    startRecording,
    stopRecording,
  };
};
