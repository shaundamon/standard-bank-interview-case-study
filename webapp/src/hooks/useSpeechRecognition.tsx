import "regenerator-runtime/runtime";
import { useState, useCallback } from "react";
import SpeechRecognition, {
  useSpeechRecognition as useBrowserSpeechRecognition,
} from "react-speech-recognition";
import { useSpeechSynthesis } from "./useSpeechSynthesis";

export const useSpeechRecognition = () => {
  const [isRecording, setIsRecording] = useState(false);
  const { speak } = useSpeechSynthesis();

  const { transcript, resetTranscript, browserSupportsSpeechRecognition } =
    useBrowserSpeechRecognition();

  const startRecording = useCallback(() => {
    if (!browserSupportsSpeechRecognition) {
      speak("Your browser doesn't support speech recognition");
      return;
    }
    setIsRecording(true);
    resetTranscript();
    SpeechRecognition.startListening({ continuous: true });
    // speak("Recording started"); // removed this line as it gets appended to transcript text on the input
  }, [speak, browserSupportsSpeechRecognition, resetTranscript]);

  const stopRecording = useCallback(() => {
    if (isRecording) {
      SpeechRecognition.stopListening();
      setIsRecording(false);
      speak("Recording stopped");
    }
  }, [isRecording, speak]);

  return {
    isRecording,
    transcript,
    startRecording,
    stopRecording,
    browserSupportsSpeechRecognition,
  };
};
